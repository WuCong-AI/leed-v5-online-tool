"""Deterministic drawing/specification review engine."""

from __future__ import annotations

import re

from ..models import ReviewFinding


def _contains(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def review_design_text(
    text: str,
    rating_version: str = "LEED v5",
    project_type: str = "BD+C: New Construction",
    location: str = "",
) -> list[ReviewFinding]:
    """Review notes with transparent keyword and omission rules.

    This is intentionally deterministic so teams can audit why a finding fired.
    It is a simulation layer, not an LLM or a compliance determination.
    """

    clean = " ".join(text.split())
    if not clean:
        return []
    findings: list[ReviewFinding] = []
    is_v5 = rating_version == "LEED v5"
    iaq_criterion = "EQp2 Fundamental Air Quality" if is_v5 else "EQp Minimum Indoor Air Quality Performance"
    low_emitting_criterion = "MRc3 Low-Emitting Materials" if is_v5 else "EQc Low-Emitting Materials"
    energy_criterion = "EAc3 Enhanced Energy Efficiency" if is_v5 else "EAc Optimize Energy Performance"
    metering_criterion = "EAp4 Energy Metering and Reporting" if is_v5 else "EAc Advanced Energy Metering"

    if _contains(clean, (r"fresh air monitoring.{0,35}not specified", r"outdoor air.{0,35}(not|no) (monitor|sensor)", r"ventilation.{0,25}(not specified|tbd|unknown)")):
        findings.append(ReviewFinding(
            iaq_criterion, "High", "Outdoor-air verification is missing",
            "The notes explicitly omit or defer ventilation/fresh-air monitoring.",
            "MECHANICAL: Add outdoor-airflow measurement at each applicable air-handling system; show sensor location, accessible test point, alarm setpoints, trend requirements, and BAS sequence. Coordinate the ventilation schedule with design occupancy and filtration.",
        ))
    elif _contains(clean, (r"outdoor air", r"fresh air", r"ventilation")) and not _contains(clean, (r"monitor", r"sensor", r"airflow station", r"trend")):
        findings.append(ReviewFinding(
            iaq_criterion, "Medium", "Ventilation is mentioned but verification is not",
            "Outdoor air appears in the notes without monitoring, controls, or commissioning language.",
            "MECHANICAL CONTROLS: Identify the outdoor-air measurement method and add minimum-flow alarms, BAS trend points, balancing tolerances, and functional test references.",
        ))

    if _contains(clean, (r"r[- ]?134a", r"r[- ]?410a", r"high[- ]gwp", r"gwp\s*[=:]?\s*(1[0-9]{3,}|[2-9][0-9]{3,})")):
        findings.append(ReviewFinding(
            "EAc6 Enhanced Refrigerant Management", "High", "High-GWP refrigerant requires an alternatives study",
            "A refrigerant associated with material lifecycle climate impact is identified.",
            "MECHANICAL SCHEDULE: Add refrigerant type, charge (kg), equipment life, leak-detection provisions, and calculated lifecycle refrigerant impact. Issue an alternatives analysis for lower-GWP equipment and record the selected option.",
        ))

    combustion = _contains(clean, (r"natural gas", r"gas[- ]fired", r"diesel", r"fuel oil", r"combustion boiler"))
    if combustion:
        findings.append(ReviewFinding(
            "IPp3 Carbon Assessment / EAc1 Electrification" if is_v5 else "EAp Minimum Energy Performance", "High", "Onsite combustion requires rating-system-specific energy review",
            "Fossil-fuel combustion equipment is included in the design description.",
            "MEP BASIS OF DESIGN: Complete an all-electric alternative and hourly emissions comparison. Replace combustion heating with electric heat-pump systems where feasible; if retained, state the exceptional load, annual fuel use, emissions, and transition plan.",
        ))

    if _contains(clean, (r"paint", r"adhesive", r"sealant", r"flooring", r"insulation", r"furniture")) and not _contains(clean, (r"voc", r"emission certificate", r"cdph", r"low[- ]emitting")):
        findings.append(ReviewFinding(
            low_emitting_criterion, "Medium", "Interior product emissions criteria are absent",
            "Interior finish/product language appears without VOC content or emissions requirements.",
            "SPECIFICATIONS 01 81 13 / PRODUCT SECTIONS: Add product-category VOC content and general emissions evaluation requirements, compliant test standards, submittal certificates, wet-applied product log, and contractor tracking responsibilities.",
        ))

    if _contains(clean, (r"concrete", r"steel", r"structure", r"façade", r"facade")) and not _contains(clean, (r"lca", r"embodied carbon", r"kg\s*co2e", r"epd")):
        findings.append(ReviewFinding(
            "MRp2 Quantify and Assess Embodied Carbon", "Medium", "No embodied-carbon basis is stated",
            "Carbon-intensive assemblies are described without quantities, EPDs, or an LCA baseline.",
            "STRUCTURAL/ARCHITECTURAL: Add material quantities and product-specific EPD submittals; identify the whole-building LCA baseline, scope, service life, and kgCO₂e/m² target on the sustainability drawing index and in Division 01.",
        ))

    if _contains(clean, (r"variable[- ]speed", r"heat recovery", r"high[- ]efficiency", r"energy model", r"demand control")):
        findings.append(ReviewFinding(
            energy_criterion, "Positive", "Efficiency strategy is visible",
            "The notes include an efficiency or control measure that should be captured in the energy model.",
            "ENERGY COORDINATION: Preserve this measure in the basis of design, equipment schedules, controls sequences, and energy-model input log; add acceptance criteria so procurement substitutions do not erode modeled performance.",
            status="Opportunity",
        ))

    if not _contains(clean, (r"meter", r"submeter", r"trend", r"measurement")):
        findings.append(ReviewFinding(
            metering_criterion, "Medium", "Metering scope cannot be verified",
            "No energy metering, data interval, or reporting pathway is present in the submitted notes.",
            "ELECTRICAL/CONTROLS: Add the whole-building and source meter schedule, data interval, communications protocol, BAS trend points, data retention, and owner reporting responsibility.",
        ))

    occupancy_labels = r"(?:fte(?:s)?|peak occupancy|occupants?|building users?|population)"
    occupancy_matches = re.findall(
        occupancy_labels + r"[^\d]{0,35}(\d{2,5}(?:,\d{3})*)",
        clean,
        re.IGNORECASE,
    ) + re.findall(
        r"(\d{2,5}(?:,\d{3})*)\s*" + occupancy_labels,
        clean,
        re.IGNORECASE,
    )
    occupancy_values = {int(value.replace(",", "")) for value in occupancy_matches}
    if len(occupancy_values) >= 2 and max(occupancy_values) > min(occupancy_values) * 1.1:
        findings.append(ReviewFinding(
            "PI Project Information / cross-credit occupancy", "High", "Occupancy values are inconsistent across evidence",
            f"Detected materially different occupancy values: {', '.join(str(value) for value in sorted(occupancy_values))}.",
            "ALL DISCIPLINES: Issue one approved occupancy matrix listing FTE, visitors/transients, peak occupants, schedules, and zone populations. Reconcile the same values in Project Information, water, ventilation, thermal comfort, energy, and daylight documentation.",
        ))

    area_values = {
        float(value.replace(",", ""))
        for value in re.findall(
            r"(?:gross floor area|project area|total surface area of (?:flooring|walls?|ceilings?|insulation))[^\d]{0,40}(\d[\d,]*(?:\.\d+)?)\s*(?:m2|m²|square meters?)",
            clean,
            re.IGNORECASE,
        )
    }
    if len(area_values) >= 2 and max(area_values) > min(area_values) * 1.35:
        findings.append(ReviewFinding(
            "PI Project Information / material quantities", "High", "Area totals do not reconcile",
            f"Detected area values ranging from {min(area_values):,.1f} to {max(area_values):,.1f} m².",
            "ARCHITECT/CONTRACTOR: Reconcile registered GFA, certifying area, regularly occupied area, and product-category surface areas. Add an area reconciliation table with drawing references and explain legitimate differences such as multilayer assemblies.",
        ))

    if _contains(clean, (r"vrf indoor coils?",)) and _contains(clean, (r"fan coil", r"fcu")):
        findings.append(ReviewFinding(
            "Energy model / mechanical drawing coordination", "High", "HVAC system types conflict",
            "The evidence references VRF indoor coils as well as fan-coil units, a mismatch observed in calibrated GBCI review comments.",
            "MECHANICAL/ENERGY MODEL: Create a tag-by-tag reconciliation of every proposed HVAC system, including system type, airflow, fan power, capacity, efficiency, controls, and modeled object. Update the model or drawings so the final inputs match the issued design.",
        ))

    if "low-emitting" in clean.lower() and "#value!" in clean.lower():
        findings.append(ReviewFinding(
            low_emitting_criterion, "High", "Low-emitting calculator contains formula errors",
            "A #VALUE! result was found in low-emitting material evidence.",
            "ARCHITECT/CONTRACTOR: Correct calculator errors, enter every installed product in each attempted category, and reconcile product totals against finish schedules, MR product logs, quantities, purchase dates, and qualifying emissions/VOC certificates.",
        ))
    if re.search(r"\bgreenguard\b(?!\s+gold)", clean, re.IGNORECASE):
        findings.append(ReviewFinding(
            low_emitting_criterion, "High", "Certificate tier may not qualify",
            "A GREENGUARD reference was detected without confirmation of GREENGUARD Gold or another accepted emissions pathway.",
            "SUBMITTALS: Verify the exact certification program, test standard, test date, modeling scenario, accreditation, and product purchase date. Replace nonqualifying certificates and update the calculator before claiming the product.",
        ))

    city_candidates = ("beijing", "shanghai", "shenzhen", "guangzhou", "chengdu", "hong kong")
    project_city = next((city for city in city_candidates if city in location.lower()), "")
    weather_match = re.search(r"weather file.{0,80}\b(" + "|".join(city_candidates) + r")\b", clean, re.IGNORECASE)
    if project_city and weather_match and weather_match.group(1).lower() != project_city:
        findings.append(ReviewFinding(
            "EQc Daylight / simulation inputs", "High", "Simulation weather file uses the wrong city",
            f"Project location indicates {project_city.title()}, but the evidence references a {weather_match.group(1).title()} weather file.",
            "DAYLIGHT/ENERGY MODEL: Replace the weather file with the project-location file, rerun simulations, and update reports, geometry plots, thresholds, and narratives. Record file name and source in the model QA log.",
        ))

    if "leed certification review report" in clean.lower():
        denied = sorted(set(re.findall(r"([A-Z][A-Za-z &\-]+?)\s+(?:Denied|Withdrawn)(?:\s*:\s*\d+)?", clean)))
        if denied:
            findings.append(ReviewFinding(
                "Official GBCI review history", "High", "Denied or withdrawn items detected in the uploaded review report",
                "Official status history includes: " + ", ".join(item.strip() for item in denied[:8]) + ".",
                "LEED ADMIN: Treat the official review status as controlling. Map every reviewer comment to a response, revised file, responsible party, and closure check; do not award automated points solely from keyword presence.",
            ))

    return findings
