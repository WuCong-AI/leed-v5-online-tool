"""Parse final GBCI review reports and LEED scorecards supplied by the user."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .ingestion import DocumentRecord


@dataclass(frozen=True, slots=True)
class OfficialResult:
    project_name: str
    project_id: str
    rating_system: str
    certification_level: str
    awarded_points: int
    total_points: int
    source_file: str


def infer_rule_pack(result: OfficialResult) -> tuple[str, str] | None:
    """Map official report naming to the application's version/system selectors."""

    label = result.rating_system.lower().replace("core and shell", "core & shell")
    if "v4.1" in label:
        version = "LEED v4.1"
    elif "v4" in label or "(4" in label:
        version = "LEED v4"
    elif "v5" in label:
        version = "LEED v5"
    else:
        return None

    if "id+c" in label or "commercial interiors" in label:
        project_type = "ID+C: Commercial Interiors"
    elif "core & shell" in label:
        project_type = "BD+C: Core & Shell"
    elif "o+m" in label or "existing buildings" in label:
        project_type = "O+M: Existing Buildings"
    elif "bd+c" in label:
        project_type = "BD+C: New Construction"
    else:
        return None
    return version, project_type


def detect_official_result(documents: list[DocumentRecord]) -> OfficialResult | None:
    for document in documents:
        text = document.text.replace("ﬁ", "fi").replace("ﬀ", "ff")
        lower = text.lower()
        if "leed certification review report" in lower:
            project_id = re.search(r"Project ID\s*(\d+)", text, re.IGNORECASE)
            rating = re.search(r"Rating system\s*&\s*version\s*([^\n]+)", text, re.IGNORECASE)
            level = re.search(r"Project certification date\s*[^\n]+\s*(Certified|Silver|Gold|Platinum)\s+Certified", text, re.IGNORECASE)
            points = re.search(r"Awarded:\s*(\d+)\s*of\s*(\d+)\s*points", text, re.IGNORECASE)
            name = re.search(r"\n([^\n]+)\nProject ID\s*\n?\d+", text, re.IGNORECASE)
            if points:
                return OfficialResult(
                    project_name=" ".join(name.group(1).split()) if name else "LEED project",
                    project_id=project_id.group(1) if project_id else "",
                    rating_system=rating.group(1).strip() if rating else "",
                    certification_level=level.group(1).title() if level else "",
                    awarded_points=int(points.group(1)),
                    total_points=int(points.group(2)),
                    source_file=document.name,
                )
        if "awarded" in lower and "total" in lower and "leed bd+c" in lower:
            points = re.search(r"TOTAL(?:TOTAL)?\s*(\d{1,3})\s*/\s*(100|110|111)", text, re.IGNORECASE)
            rating = re.search(r"(LEED\s+(?:BD\+C|ID\+C|O\+M)[^\n]+?\(v?4(?:\.1)?\))", text, re.IGNORECASE)
            level = re.search(r"\b(CERTIFIED|SILVER|GOLD|PLATINUM)\s*,?\s*AWARDED", text, re.IGNORECASE)
            project_id = re.search(r"\b(\d{10})\b", text)
            name = re.search(r"\d{10},[^\n]*\n([^\n]+)", text)
            if points:
                return OfficialResult(
                    project_name=name.group(1).strip() if name else "LEED project",
                    project_id=project_id.group(1) if project_id else "",
                    rating_system=rating.group(1).strip() if rating else "",
                    certification_level=level.group(1).title() if level else "",
                    awarded_points=int(points.group(1)),
                    total_points=int(points.group(2)),
                    source_file=document.name,
                )
    return None
