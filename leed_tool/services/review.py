"""Deterministic drawing/specification review engine."""

from __future__ import annotations

import re

from ..models import ReviewFinding


def _contains(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def review_design_text(text: str) -> list[ReviewFinding]:
    """Review notes with transparent keyword and omission rules.

    This is intentionally deterministic so teams can audit why a finding fired.
    It is a simulation layer, not an LLM or a compliance determination.
    """

    clean = " ".join(text.split())
    if not clean:
        return []
    findings: list[ReviewFinding] = []

    if _contains(clean, (r"fresh air monitoring.{0,35}not specified", r"outdoor air.{0,35}(not|no) (monitor|sensor)", r"ventilation.{0,25}(not specified|tbd|unknown)")):
        findings.append(ReviewFinding(
            "EQp2 Fundamental Air Quality", "High", "Outdoor-air verification is missing",
            "The notes explicitly omit or defer ventilation/fresh-air monitoring.",
            "MECHANICAL: Add outdoor-airflow measurement at each applicable air-handling system; show sensor location, accessible test point, alarm setpoints, trend requirements, and BAS sequence. Coordinate the ventilation schedule with design occupancy and filtration.",
        ))
    elif _contains(clean, (r"outdoor air", r"fresh air", r"ventilation")) and not _contains(clean, (r"monitor", r"sensor", r"airflow station", r"trend")):
        findings.append(ReviewFinding(
            "EQp2 Fundamental Air Quality", "Medium", "Ventilation is mentioned but verification is not",
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
            "IPp3 Carbon Assessment / EAc2 Operational Carbon", "High", "Onsite combustion conflicts with a near-zero-carbon pathway",
            "Fossil-fuel combustion equipment is included in the design description.",
            "MEP BASIS OF DESIGN: Complete an all-electric alternative and hourly emissions comparison. Replace combustion heating with electric heat-pump systems where feasible; if retained, state the exceptional load, annual fuel use, emissions, and transition plan.",
        ))

    if _contains(clean, (r"paint", r"adhesive", r"sealant", r"flooring", r"insulation", r"furniture")) and not _contains(clean, (r"voc", r"emission certificate", r"cdph", r"low[- ]emitting")):
        findings.append(ReviewFinding(
            "MRc3 Low-Emitting Materials", "Medium", "Interior product emissions criteria are absent",
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
            "EAc1 Enhanced Energy Efficiency", "Positive", "Efficiency strategy is visible",
            "The notes include an efficiency or control measure that should be captured in the energy model.",
            "ENERGY COORDINATION: Preserve this measure in the basis of design, equipment schedules, controls sequences, and energy-model input log; add acceptance criteria so procurement substitutions do not erode modeled performance.",
            status="Opportunity",
        ))

    if not _contains(clean, (r"meter", r"submeter", r"trend", r"measurement")):
        findings.append(ReviewFinding(
            "EAp4 Energy Metering and Reporting", "Medium", "Metering scope cannot be verified",
            "No energy metering, data interval, or reporting pathway is present in the submitted notes.",
            "ELECTRICAL/CONTROLS: Add the whole-building and source meter schedule, data interval, communications protocol, BAS trend points, data retention, and owner reporting responsibility.",
        ))

    return findings

