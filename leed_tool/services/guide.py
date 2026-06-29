"""Customized LEED v5 design guide generation."""

from __future__ import annotations

from datetime import date
from html import escape

from ..data import CERTIFICATION_THRESHOLDS, credits_for, prerequisites_for
from ..models import Credit, ProjectProfile

TARGET_CREDIT_CODES = {
    "Certified": ("IPc1", "LTc3", "WEc1", "EAc1", "EAc5", "MRc3", "EQc1", "INc2"),
    "Silver": ("IPc1", "LTc3", "LTc4", "WEc1", "WEc2", "EAc1", "EAc5", "MRc1", "MRc3", "EQc1", "EQc2", "INc2"),
    "Gold": ("IPc1", "LTc3", "LTc4", "LTc5", "SSc3", "WEc1", "WEc2", "EAc1", "EAc2", "EAc4", "EAc5", "EAc6", "MRc2", "MRc3", "EQc1", "EQc2", "EQc5", "INc2"),
    "Platinum": ("IPc1", "LTc3", "LTc4", "LTc5", "SSc1", "SSc3", "SSc4", "WEc1", "WEc2", "WEc3", "EAc1", "EAc2", "EAc3", "EAc4", "EAc5", "EAc6", "MRc1", "MRc2", "MRc3", "MRc4", "EQc1", "EQc2", "EQc4", "EQc5", "EQc6", "INc2", "PPc1"),
}


def strategic_credits(profile: ProjectProfile) -> tuple[Credit, ...]:
    allowed = set(TARGET_CREDIT_CODES[profile.target_level])
    return tuple(c for c in credits_for(profile.project_type) if c.code in allowed)


def _platinum_note(profile: ProjectProfile) -> str:
    if profile.target_level != "Platinum":
        return "Build a 5–8 point buffer above the target before design freeze."
    return (
        "Platinum is not points-only under LEED v5. Confirm the registered rating "
        "system's mandatory electrification, energy efficiency, renewable energy, "
        "and embodied-carbon reduction thresholds."
    )


def build_guide_markdown(profile: ProjectProfile) -> str:
    """Generate a portable Markdown report for download."""

    prerequisites = prerequisites_for(profile.project_type)
    credits = strategic_credits(profile)
    threshold = CERTIFICATION_THRESHOLDS[profile.target_level]
    target_with_buffer = min(110, threshold + (8 if profile.target_level in {"Gold", "Platinum"} else 5))
    lines = [
        f"# LEED v5 Design Guide — {profile.name}",
        "",
        f"**Project:** {profile.name}  ",
        f"**Location:** {profile.location}  ",
        f"**Gross floor area:** {profile.gross_floor_area_m2:,.0f} m²  ",
        f"**Rating system:** {profile.project_type}  ",
        f"**Target:** {profile.target_level} ({threshold}+ points; planning target {target_with_buffer})  ",
        f"**Generated:** {date.today().isoformat()}",
        "",
        "> Planning aid only. Reconcile requirements with the current USGBC rating system, Arc forms, and addenda effective on the project's registration date.",
        "",
        "## Mandatory prerequisites",
        "",
    ]
    for prereq in prerequisites:
        lines.extend(
            [
                f"### {prereq.code} — {prereq.name}",
                f"- Category: {prereq.category}",
                f"- Impact: {prereq.pillar}",
                f"- Design action: {prereq.summary}",
                "",
            ]
        )
    lines.extend(["## Strategic credit pathway", ""])
    for credit in credits:
        lines.extend(
            [
                f"### {credit.code} — {credit.name} ({credit.points} pts)",
                f"- Category: {credit.category}",
                f"- Primary impact: {credit.pillar}",
                f"- Strategy: {credit.strategy}",
                f"- Evidence owner: {credit.responsible_party}",
                "",
            ]
        )
    lines.extend(
        [
            "## Delivery controls",
            "",
            "1. Confirm rating-system selection and registration-date addenda.",
            "2. Assign one accountable owner and one evidence due date per attempted credit.",
            "3. Lock carbon, resilience, water, and human-impact baselines before schematic design concludes.",
            "4. Reconcile design drawings, specifications, calculations, and contractor submittals at every stage gate.",
            f"5. {_platinum_note(profile)}",
            "",
        ]
    )
    return "\n".join(lines)


def build_guide_html(profile: ProjectProfile) -> str:
    """Generate a styled, self-contained HTML guide for display/download."""

    prerequisites = prerequisites_for(profile.project_type)
    credits = strategic_credits(profile)
    threshold = CERTIFICATION_THRESHOLDS[profile.target_level]
    target_with_buffer = min(110, threshold + (8 if profile.target_level in {"Gold", "Platinum"} else 5))
    prereq_cards = "".join(
        f"""
        <article class="item">
          <div><span class="code">{escape(p.code)}</span><span class="pill">{escape(p.pillar)}</span></div>
          <h3>{escape(p.name)}</h3><p>{escape(p.summary)}</p>
          <small>{escape(p.category)}</small>
        </article>"""
        for p in prerequisites
    )
    credit_rows = "".join(
        f"""
        <tr><td><strong>{escape(c.code)}</strong><br>{escape(c.name)}</td>
        <td>{c.points}</td><td>{escape(c.pillar)}</td>
        <td>{escape(c.strategy)}</td><td>{escape(c.responsible_party)}</td></tr>"""
        for c in credits
    )
    platinum = ""
    if profile.target_level == "Platinum":
        platinum = f'<div class="callout"><strong>Platinum gate:</strong> {escape(_platinum_note(profile))}</div>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LEED v5 Design Guide — {escape(profile.name)}</title>
<style>
body{{font-family:Inter,Arial,sans-serif;color:#18312a;background:#f4f7f3;margin:0;line-height:1.5}}
.page{{max-width:1100px;margin:auto;padding:40px 24px}} header{{padding:36px;border-radius:18px;background:#173d34;color:white}}
h1{{font-size:34px;margin:8px 0}} h2{{margin-top:34px}} .eyebrow{{letter-spacing:.14em;text-transform:uppercase;color:#a8d6c1;font-size:12px}}
.meta{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:24px}} .meta div{{background:#ffffff14;border:1px solid #ffffff22;padding:12px;border-radius:10px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}} .item{{background:white;padding:18px;border-radius:12px;border:1px solid #dce7df}}
.item h3{{margin:10px 0 5px}} .item p{{color:#49625a}} .code{{font-weight:700;color:#27735f}} .pill{{float:right;background:#edf5ef;padding:4px 8px;border-radius:20px;font-size:11px}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}} th,td{{padding:12px;border-bottom:1px solid #e7ece8;text-align:left;vertical-align:top}} th{{background:#eaf2ed}}
.callout{{border-left:5px solid #d69a43;background:#fff7e9;padding:16px;margin:22px 0}} .note{{color:#5e716b;font-size:13px}} @media(max-width:760px){{.meta,.grid{{grid-template-columns:1fr}}}}
</style></head><body><main class="page">
<header><div class="eyebrow">LEED v5 design guide</div><h1>{escape(profile.name)}</h1>
<p>{escape(profile.location)} · {escape(profile.project_type)}</p>
<div class="meta"><div><small>Gross floor area</small><br><strong>{profile.gross_floor_area_m2:,.0f} m²</strong></div><div><small>Certification target</small><br><strong>{escape(profile.target_level)} · {threshold}+ pts</strong></div><div><small>Planning target</small><br><strong>{target_with_buffer} pts</strong></div></div></header>
<p class="note">Generated {date.today().isoformat()}. Consultant planning aid only; verify current USGBC/GBCI requirements and project-specific addenda.</p>
{platinum}<h2>Mandatory prerequisites</h2><div class="grid">{prereq_cards}</div>
<h2>Strategic credit pathway</h2><table><thead><tr><th>Credit</th><th>Pts</th><th>Impact</th><th>Design strategy</th><th>Evidence owner</th></tr></thead><tbody>{credit_rows}</tbody></table>
<h2>Delivery controls</h2><ol><li>Confirm rating-system selection and registration-date addenda.</li><li>Assign accountable owners and evidence due dates.</li><li>Freeze carbon, resilience, water, and human-impact baselines before schematic design closes.</li><li>Reconcile drawings, specifications, calculations, and submittals at each stage gate.</li><li>{escape(_platinum_note(profile))}</li></ol>
</main></body></html>"""

