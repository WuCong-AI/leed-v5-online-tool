"""Pre-submission narrative risk assessment."""

from __future__ import annotations

import re

from ..models import Credit, RiskAssessment

EVIDENCE_TERMS: dict[str, tuple[str, ...]] = {
    "IP": ("charrette", "stakeholder", "date", "decision", "action"),
    "LT": ("map", "distance", "calculation", "route", "plan"),
    "SS": ("site", "area", "drawing", "calculation", "species"),
    "WE": ("baseline", "fixture", "flow", "calculation", "meter"),
    "EA": ("baseline", "model", "energy", "carbon", "schedule"),
    "MR": ("quantity", "epd", "product", "calculation", "invoice"),
    "EQ": ("drawing", "schedule", "test", "occupancy", "standard"),
    "IN": ("measurable", "baseline", "outcome", "team", "evidence"),
    "PP": ("priority", "location", "requirement", "form", "evidence"),
}


def assess_submission_risk(credit: Credit, narrative: str) -> RiskAssessment:
    clean = " ".join(narrative.split())
    lower = clean.lower()
    flags: list[str] = []
    actions: list[str] = []
    strengths: list[str] = []
    score = 0

    terms = EVIDENCE_TERMS.get(credit.code[:2], ("calculation", "drawing", "evidence", "requirement"))
    matched = [term for term in terms if term in lower]
    coverage = round(100 * len(matched) / len(terms))

    if len(clean) < 180:
        score += 3
        flags.append("Narrative is too short to establish approach, calculations, and document cross-references.")
        actions.append("Expand the narrative into: requirement/path, project approach, calculation result, and exact uploaded evidence.")
    else:
        strengths.append("Narrative length is sufficient for a structured compliance explanation.")

    if coverage < 40:
        score += 3
        flags.append(f"Only {coverage}% of expected evidence concepts are visible for this credit family.")
        actions.append("Name the governing baseline, calculation method, drawing/spec references, and responsible verifier.")
    elif coverage < 70:
        score += 1
        flags.append(f"Evidence coverage is partial ({coverage}%); reviewer traceability may be weak.")
        actions.append("Add missing evidence concepts: " + ", ".join(term for term in terms if term not in matched) + ".")
    else:
        strengths.append(f"Evidence vocabulary coverage is strong ({coverage}%).")

    if not re.search(r"\b\d+(?:\.\d+)?\s*(?:%|kwh|mwh|kg|tco2e|kgco2e|m2|m²|gpm|lpm|ppm|points?)(?=\s|[.,;:)]|$)", lower):
        score += 2
        flags.append("No unit-bearing performance result is stated.")
        actions.append("State the final design result with units, baseline value, percentage improvement, and calculation file name.")
    else:
        strengths.append("A quantitative, unit-bearing performance result is included.")

    future_terms = re.findall(r"\b(?:will|tbd|to be confirmed|anticipated|expected|intend to|pending)\b", lower)
    if future_terms:
        score += 2
        flags.append("Future-tense or unresolved commitments appear in a final-submission narrative.")
        actions.append("Replace future commitments with completed actions and final as-built/submittal evidence, or clearly identify a permitted deferred submittal.")

    if not re.search(r"\b(?:drawing|sheet|specification|section|appendix|report|model|schedule|upload|attachment)\b", lower):
        score += 2
        flags.append("The narrative does not cross-reference an uploaded document, sheet, schedule, or report.")
        actions.append("Add exact file names, drawing numbers, specification sections, and report page/table references.")
    else:
        strengths.append("The narrative includes at least one document cross-reference.")

    if not re.search(r"\b(?:architect|engineer|contractor|owner|consultant|commissioning|modeler|verified|prepared by)\b", lower):
        score += 1
        flags.append("No accountable author or verifier is identified.")
        actions.append(f"Identify the accountable party; the planning owner for this credit is {credit.responsible_party}.")

    if credit.platinum_gate and "platinum" not in lower:
        score += 1
        flags.append("This credit supports a LEED v5 Platinum gate, but the narrative does not reconcile the applicable mandatory threshold.")
        actions.append("Add a short Platinum-gate statement citing the applicable threshold and the final achieved value.")

    level = "High" if score >= 7 else "Medium" if score >= 4 else "Low"
    if not flags:
        actions.append("Perform a final filename, value, and cross-reference reconciliation before upload.")
    return RiskAssessment(
        level=level, score=score, evidence_coverage=coverage,
        strengths=tuple(strengths), flags=tuple(flags), corrective_actions=tuple(dict.fromkeys(actions)),
    )
