"""Evidence-to-credit mapping for one-click uploaded package analysis."""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..data import CREDITS, PREREQUISITES
from .ingestion import DocumentRecord


@dataclass(frozen=True, slots=True)
class EvidenceAssessment:
    code: str
    name: str
    status: str
    confidence: int
    matched_terms: tuple[str, ...]
    sources: tuple[str, ...]
    evidence_snippet: str


CREDIT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "IPc1": ("integrative design", "charrette", "stakeholder workshop", "leed goal", "basis of design"),
    "LTc1": ("previously developed", "sensitive land", "wetland", "floodplain", "habitat survey"),
    "LTc2": ("community engagement", "social equity", "affordable housing", "equitable development", "community benefit"),
    "LTc3": ("transit", "diverse uses", "walk score", "density", "walking distance"),
    "LTc4": ("transportation demand", "bicycle storage", "mode share", "shower facilities", "carpool"),
    "LTc5": ("electric vehicle", "ev charging", "evse", "ev ready", "load management"),
    "SSc1": ("native planting", "adapted vegetation", "habitat restoration", "soil restoration", "biodiversity"),
    "SSc2": ("open space", "biophilic", "outdoor amenity", "vegetated area", "human nature"),
    "SSc3": ("rainwater", "stormwater", "infiltration", "retention", "runoff"),
    "SSc4": ("resilient site", "flood protection", "climate hazard", "drought", "extreme heat"),
    "SSc5": ("heat island", "sri", "reflectance", "photometric", "light trespass"),
    "WEc1": ("water use", "low flow", "fixture schedule", "irrigation", "water reduction"),
    "WEc2": ("water meter", "submeter", "water monitoring", "leak detection", "meter schedule"),
    "WEc3": ("reclaimed water", "rainwater reuse", "cooling tower", "cycles of concentration", "alternative water"),
    "EAc1": ("energy model", "energy efficiency", "ashrae 90.1", "energy cost", "site energy"),
    "EAc2": ("operational carbon", "greenhouse gas", "electrification", "kgco2e", "hourly emissions"),
    "EAc3": ("demand response", "load shifting", "battery storage", "grid interactive", "peak demand"),
    "EAc4": ("renewable energy", "photovoltaic", "solar pv", "power purchase agreement", "green-e"),
    "EAc5": ("commissioning plan", "commissioning authority", "functional testing", "cx issues log", "design review"),
    "EAc6": ("refrigerant", "gwp", "leak detection", "refrigerant charge", "low-gwp"),
    "MRc1": ("material reuse", "building reuse", "salvaged", "existing structure", "retained structure"),
    "MRc2": ("whole building lca", "embodied carbon reduction", "life cycle assessment", "kgco2e/m2", "lca baseline"),
    "MRc3": ("low-emitting", "voc", "cdph", "emissions certificate", "wet-applied"),
    "MRc4": ("environmental product declaration", "epd", "ingredient disclosure", "responsible sourcing", "procurement tracker"),
    "EQc1": ("outdoor air", "merv", "filtration", "ventilation", "airflow monitoring"),
    "EQc2": ("thermal comfort", "occupant control", "views", "adaptable", "comfort survey"),
    "EQc3": ("accessibility", "inclusive design", "universal design", "sensory", "accessible route"),
    "EQc4": ("passive survivability", "resilient space", "critical load", "shelter in place", "outage"),
    "EQc5": ("air quality testing", "iaq testing", "continuous monitoring", "pm2.5", "co2 sensor"),
    "EQc6": ("daylight simulation", "sda", "ase", "lighting quality", "glare"),
    "EQc7": ("acoustic", "reverberation", "sound isolation", "background noise", "speech privacy"),
    "INc1": ("innovation", "exemplary performance", "pilot credit", "measurable outcome", "innovative strategy"),
    "INc2": ("leed ap", "accredited professional", "leed professional"),
    "PPc1": ("project priority", "regional priority", "priority credit", "regional environmental"),
}

PREREQUISITE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "IPp1": ("climate resilience", "climate hazard", "flood risk", "extreme heat", "adaptation"),
    "IPp2": ("human impact", "social equity", "health assessment", "community", "accessibility"),
    "IPp3": ("carbon assessment", "operational carbon", "embodied carbon", "refrigerant", "transportation carbon"),
    "IPp4": ("tenant guidelines", "tenant design", "green lease"),
    "SSp1": ("minimize site disturbance", "special-status vegetation", "limits of disturbance", "tree protection"),
    "WEp1": ("water metering", "water meter", "water reporting"),
    "WEp2": ("minimum water efficiency", "fixture schedule", "water baseline"),
    "EAp1": ("minimum energy performance", "energy model", "ashrae 90.1"),
    "EAp2": ("fundamental refrigerant", "refrigerant inventory", "ozone depletion"),
    "EAp3": ("fundamental commissioning", "commissioning plan", "owner's project requirements", "basis of design"),
    "EAp4": ("energy metering", "energy meter", "energy reporting"),
    "MRp1": ("zero waste", "operational waste", "waste storage", "recycling collection"),
    "MRp2": ("quantify embodied carbon", "whole building lca", "embodied carbon", "kgco2e"),
    "EQp1": ("construction iaq", "moisture control", "construction pollution", "smacna"),
    "EQp2": ("fundamental air quality", "ventilation", "outdoor air", "filtration"),
    "EQp3": ("no smoking", "smoking prohibited", "tobacco smoke"),
}


def _find_snippet(text: str, term: str, width: int = 260) -> str:
    index = text.lower().find(term.lower())
    if index < 0:
        return ""
    start = max(0, index - 70)
    end = min(len(text), index + len(term) + width - 70)
    return " ".join(text[start:end].split())


def _map_one(code: str, name: str, keywords: tuple[str, ...], documents: list[DocumentRecord]) -> EvidenceAssessment:
    matches: list[str] = []
    sources: list[str] = []
    snippet = ""
    searchable_documents = [doc for doc in documents if doc.text]
    for term in keywords:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        term_sources = [doc for doc in searchable_documents if pattern.search(doc.text)]
        if term_sources:
            matches.append(term)
            sources.extend(doc.name for doc in term_sources)
            if not snippet:
                snippet = _find_snippet(term_sources[0].text, term)
    distinct = len(matches)
    has_quantified_evidence = any(
        re.search(r"\b\d+(?:\.\d+)?\s*(?:%|kwh|mwh|kg|tco2e|kgco2e|m2|m²|gpm|lpm|ppm)(?=\s|[.,;:)]|$)", doc.text, re.IGNORECASE)
        for doc in searchable_documents if doc.name in sources
    )
    if distinct >= 3 and (has_quantified_evidence or len(set(sources)) >= 2):
        status = "Yes"
        confidence = min(95, 58 + distinct * 7 + (8 if has_quantified_evidence else 0))
    elif distinct >= 1:
        status = "Maybe"
        confidence = min(79, 34 + distinct * 12 + (6 if has_quantified_evidence else 0))
    else:
        status = "No"
        confidence = 20
    return EvidenceAssessment(code, name, status, confidence, tuple(matches), tuple(dict.fromkeys(sources)), snippet)


def assess_credit_evidence(documents: list[DocumentRecord]) -> list[EvidenceAssessment]:
    return [_map_one(c.code, c.name, CREDIT_KEYWORDS.get(c.code, (c.name.lower(),)), documents) for c in CREDITS]


def assess_prerequisite_evidence(documents: list[DocumentRecord]) -> list[EvidenceAssessment]:
    return [_map_one(p.code, p.name, PREREQUISITE_KEYWORDS.get(p.code, (p.name.lower(),)), documents) for p in PREREQUISITES]
