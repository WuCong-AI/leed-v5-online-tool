"""Downloadable audit bundle for automated package analysis."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict
from html import escape
from io import BytesIO, StringIO
from zipfile import ZIP_DEFLATED, ZipFile

from ..models import CertificationResult, ReviewFinding, RiskAssessment
from .auto_assessment import EvidenceAssessment
from .ingestion import DocumentRecord


def _csv_bytes(rows: list[dict[str, object]]) -> bytes:
    if not rows:
        return b""
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


def build_summary_html(
    project_name: str,
    documents: list[DocumentRecord],
    credit_evidence: list[EvidenceAssessment],
    prerequisites: list[EvidenceAssessment],
    findings: list[ReviewFinding],
    projection: CertificationResult,
    rating_version: str = "LEED v5",
) -> str:
    credit_rows = "".join(
        f"<tr><td>{escape(item.code)}</td><td>{escape(item.name)}</td><td>{escape(item.status)}</td><td>{item.confidence}%</td><td>{escape(', '.join(item.sources) or 'No evidence source')}</td></tr>"
        for item in credit_evidence
    )
    prereq_rows = "".join(
        f"<tr><td>{escape(item.code)}</td><td>{escape(item.name)}</td><td>{escape(item.status)}</td><td>{escape(', '.join(item.matched_terms) or 'No evidence found')}</td></tr>"
        for item in prerequisites
    )
    finding_rows = "".join(
        f"<article><strong>{escape(f.severity)} · {escape(f.criterion)}</strong><h3>{escape(f.title)}</h3><p>{escape(f.evidence)}</p><p><b>Drawing comment:</b> {escape(f.drawing_comment)}</p></article>"
        for f in findings
    ) or "<p>No deterministic text-rule findings were triggered.</p>"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{escape(rating_version)} Automated Review</title>
<style>body{{font:15px/1.5 Inter,Arial,sans-serif;color:#19332c;margin:0;background:#f4f7f3}}main{{max-width:1150px;margin:auto;padding:36px}}header{{background:#173d34;color:white;padding:30px;border-radius:16px}}.metrics{{display:flex;gap:12px;flex-wrap:wrap}}.metric,article{{background:white;border:1px solid #dfe8e2;border-radius:12px;padding:15px;margin:10px 0}}.metric{{min-width:180px}}table{{width:100%;border-collapse:collapse;background:white}}th,td{{padding:9px;border-bottom:1px solid #e4ebe7;text-align:left;vertical-align:top}}th{{background:#eaf2ed}}small{{color:#66756f}}</style></head>
<body><main><header><small>{escape(rating_version)} · UPLOAD-FIRST AUTOMATED REVIEW</small><h1>{escape(project_name)}</h1><p>Planning evidence screen; not a certification decision.</p></header>
<div class="metrics"><div class="metric"><small>Files processed</small><h2>{len(documents)}</h2></div><div class="metric"><small>Committed points</small><h2>{projection.yes_points}</h2></div><div class="metric"><small>Potential points</small><h2>+{projection.maybe_points}</h2></div><div class="metric"><small>Pipeline</small><h2>{escape(projection.level)} · {projection.projected_points}</h2></div></div>
<h2>Prerequisite evidence screen</h2><table><tr><th>Code</th><th>Prerequisite</th><th>Signal</th><th>Matched evidence</th></tr>{prereq_rows}</table>
<h2>Automated credit scorecard</h2><table><tr><th>Code</th><th>Credit</th><th>Status</th><th>Confidence</th><th>Source files</th></tr>{credit_rows}</table>
<h2>Drawing/specification findings</h2>{finding_rows}
<p><small>Verify against the live USGBC rating system, Arc forms, and addenda effective on the project registration date. Scanned and raster drawings require OCR or human visual review.</small></p></main></body></html>"""


def build_result_bundle(
    project_name: str,
    documents: list[DocumentRecord],
    credit_evidence: list[EvidenceAssessment],
    prerequisites: list[EvidenceAssessment],
    findings: list[ReviewFinding],
    checklist_rows: list[dict[str, str]],
    projection: CertificationResult,
    risk_results: dict[str, RiskAssessment] | None = None,
    rating_version: str = "LEED v5",
    total_available: int = 110,
) -> bytes:
    """Return a ZIP with report, manifest, scorecard, checklist, and findings."""

    manifest = [
        {
            "File Name": d.name, "Type": d.kind, "Size Bytes": d.size_bytes,
            "Pages": d.page_count, "Extraction Status": d.extraction_status,
            "SHA-256": d.sha256, "Warnings": " | ".join(d.warnings),
        }
        for d in documents
    ]
    credit_rows = [
        {
            "Code": e.code, "Credit": e.name, "Assessment": e.status,
            "Confidence": e.confidence, "Matched Terms": " | ".join(e.matched_terms),
            "Source Files": " | ".join(e.sources), "Evidence Snippet": e.evidence_snippet,
        }
        for e in credit_evidence
    ]
    prereq_rows = [
        {
            "Code": e.code, "Prerequisite": e.name, "Assessment": e.status,
            "Confidence": e.confidence, "Matched Terms": " | ".join(e.matched_terms),
            "Source Files": " | ".join(e.sources),
        }
        for e in prerequisites
    ]
    finding_rows = [asdict(f) for f in findings]
    risk_rows = [
        {
            "Credit Code": code, "Risk Level": result.level, "Risk Score": result.score,
            "Evidence Coverage": result.evidence_coverage,
            "Flags": " | ".join(result.flags),
            "Corrective Actions": " | ".join(result.corrective_actions),
        }
        for code, result in (risk_results or {}).items()
    ]
    summary = {
        "project_name": project_name,
        "files_processed": len(documents),
        "yes_points": projection.yes_points,
        "maybe_points": projection.maybe_points,
        "pipeline_points": projection.projected_points,
        "projected_level": projection.level,
        "rating_version": rating_version,
        "total_available": total_available,
        "limitations": [
            "Automated evidence signals are not LEED compliance determinations.",
            "Raster/scanned drawings require OCR or human visual review.",
            "Use the rating system and addenda effective on the registration date.",
        ],
    }
    html = build_summary_html(project_name, documents, credit_evidence, prerequisites, findings, projection, rating_version)
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("00_executive_summary.json", json.dumps(summary, indent=2, ensure_ascii=False))
        archive.writestr("01_leed_auto_report.html", html.encode("utf-8"))
        archive.writestr("02_file_manifest.csv", _csv_bytes(manifest))
        archive.writestr("03_prerequisite_evidence.csv", _csv_bytes(prereq_rows))
        archive.writestr("04_automated_scorecard.csv", _csv_bytes(credit_rows))
        archive.writestr("05_drawing_review_findings.csv", _csv_bytes(finding_rows))
        archive.writestr("06_documentation_checklist.csv", _csv_bytes(checklist_rows))
        archive.writestr("07_submission_risk_register.csv", _csv_bytes(risk_rows))
    return output.getvalue()
