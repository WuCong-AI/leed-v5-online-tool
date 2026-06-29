"""LEED v5 Certification & Automation Tool — Streamlit entry point."""

from __future__ import annotations

from html import escape
from io import StringIO
from pathlib import Path
import re

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from leed_tool.data import (
    CERTIFICATION_THRESHOLDS,
    CREDITS,
    PROJECT_TYPES,
    TARGET_LEVELS,
    credits_for,
)
from leed_tool.models import ProjectProfile
from leed_tool.services.assessment import calculate_certification, category_scores, score_assessment
from leed_tool.services.auto_assessment import assess_credit_evidence, assess_prerequisite_evidence
from leed_tool.services.checklist import build_checklist
from leed_tool.services.export import build_result_bundle, build_summary_html
from leed_tool.services.guide import build_guide_html, build_guide_markdown, strategic_credits
from leed_tool.services.ingestion import MAX_ARCHIVE_BYTES, MAX_FILE_BYTES, extract_many
from leed_tool.services.review import review_design_text
from leed_tool.services.risk import assess_submission_risk
from leed_tool.styles import inject_css, metric_card, module_header

st.set_page_config(
    page_title="LEED v5 Automation Tool",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()


def init_state() -> None:
    defaults = {
        "assessment_statuses": {credit.code: "No" for credit in CREDITS},
        "checklist_records": {},
        "review_findings": [],
        "risk_results": {},
        "upload_analysis": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar() -> ProjectProfile:
    with st.sidebar:
        st.markdown("### Optional project settings")
        st.caption("Upload-first analysis works without editing these fields. Use them to customize the consultant modules and design guide.")
        project_name = st.text_input("Project name", value="Harbor Commons")
        gross_area = st.number_input(
            "Gross floor area (m²)", min_value=1.0, max_value=10_000_000.0,
            value=18500.0, step=100.0, format="%.0f",
        )
        location = st.text_input("Location", value="Shanghai, China")
        project_type = st.selectbox("Project type", PROJECT_TYPES)
        target_level = st.selectbox("Target certification", TARGET_LEVELS, index=2)
        st.divider()
        st.markdown("**Framework lens**")
        st.caption("◉ Decarbonization")
        st.caption("◉ Quality of life")
        st.caption("◉ Ecological conservation & restoration")
        st.divider()
        st.caption("Planning model · 110 available points")
        st.caption("Certification bands: 40 / 50 / 60 / 80")
    return ProjectProfile(
        name=project_name.strip() or "Untitled Project",
        gross_floor_area_m2=float(gross_area),
        location=location.strip() or "Location not set",
        project_type=project_type,
        target_level=target_level,
    )


def render_hero(profile: ProjectProfile) -> None:
    st.markdown(
        f"""
        <section class="hero">
          <div class="hero-kicker">Upload once · evidence to decision</div>
          <h1>LEED v5 Online Review Workspace</h1>
          <p>Upload drawings, specifications, schedules, and calculations once. The workspace extracts evidence and produces the scorecard, design comments, document checklist, and submission risks automatically.</p>
          <div class="pill-row"><span class="impact-pill">Decarbonization</span><span class="impact-pill">Quality of life</span><span class="impact-pill">Ecological conservation</span></div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _infer_project_name(uploaded_names: list[str]) -> str:
    if not uploaded_names:
        return "Uploaded LEED Project"
    stem = Path(uploaded_names[0]).stem
    stem = re.sub(r"(?i)[-_ ]?(drawing|drawings|spec|specification|leed|set|package|report|calculation|calc|rev)[-_ ]?[a-z0-9.]*$", "", stem).strip(" _-")
    return stem or Path(uploaded_names[0]).stem or "Uploaded LEED Project"


def render_upload_workspace(profile: ProjectProfile) -> None:
    module_header(0, "Upload & Auto-Analyze", "Upload the complete design package. Files stay in memory for this session; the automated evidence screen populates every downstream module and prepares one audit-ready download bundle.")
    left, right = st.columns([1.35, .65], gap="large")
    with left:
        uploaded = st.file_uploader(
            "Project files and drawings",
            type=["pdf", "docx", "xlsx", "xlsm", "csv", "txt", "md", "png", "jpg", "jpeg", "tif", "tiff", "dxf", "ifc", "dwg", "zip"],
            accept_multiple_files=True,
            help=(
                f"Up to 20 uploads per run, {MAX_FILE_BYTES // (1024 * 1024)} MB per document, "
                f"or {MAX_ARCHIVE_BYTES // (1024 * 1024)} MB per ZIP. ZIP contents are inspected in memory; "
                "nested and password-protected archives are skipped."
            ),
        )
        action_left, action_right = st.columns([1.35, 1])
        with action_left:
            analyze = st.button("Analyze uploaded package", type="primary", use_container_width=True, disabled=not uploaded)
        with action_right:
            demo = st.button("Try demo package", use_container_width=True)
    with right:
        st.markdown(
            '<div class="surface"><strong>Private by default</strong><br><span style="color:#64736d">Local, in-memory parsing. No project content is sent to an external AI service.</span><hr style="border:none;border-top:1px solid #dfe8e2"><strong>Best inputs</strong><br><span style="color:#64736d">Searchable PDF, DOCX specifications, XLSX/XLSM calculations, IFC/DXF exports, or one ZIP project package.</span></div>',
            unsafe_allow_html=True,
        )

    if analyze or demo:
        limited_uploads = list(uploaded[:20]) if uploaded else []
        overflow_error = [] if len(uploaded or []) <= 20 else [f"Only the first 20 of {len(uploaded)} uploaded files were processed."]
        if demo:
            payloads = [
                ("Harbor-Commons-Energy-Model.txt", b"Energy model and energy efficiency assessment against ASHRAE 90.1 show 28% energy cost improvement. Operational carbon is 42 kgCO2e/m2 using an all-electric heat pump design and hourly emissions analysis. Renewable energy includes solar PV for 35% of demand. Commissioning plan by the commissioning authority includes design review, functional testing, and a Cx issues log. R-1234ze low-GWP refrigerant charge and leak detection are scheduled. Energy metering and reporting with 15-minute trend data are specified.", "text/plain"),
                ("Harbor-Commons-Site-Water.txt", b"The landscape plan provides native planting, biodiversity habitat restoration and soil restoration. Rainwater and stormwater runoff are managed by infiltration and retention. The fixture schedule and water baseline calculation show 35% water reduction using low flow fixtures. Water meters, submeters, leak detection and water monitoring are shown on P-601. Climate hazard, flood risk, drought, extreme heat and adaptation measures are documented in the climate resilience assessment.", "text/plain"),
                ("Harbor-Commons-Specifications.txt", b"Fundamental air quality includes ventilation, outdoor air, MERV 13 filtration and airflow monitoring. Low-emitting VOC products require CDPH emissions certificates for paint, adhesive, sealant, flooring and wet-applied products. Product procurement requires environmental product declarations, EPD tracking and ingredient disclosure. Daylight simulation reports sDA and glare results. Accessibility, inclusive design and accessible route drawings are included. No smoking and construction IAQ pollution controls are specified.", "text/plain"),
            ]
            overflow_error = []
        else:
            payloads = [(item.name, item.getvalue(), item.type or "") for item in limited_uploads]
        with st.spinner("Extracting project evidence and running LEED v5 checks…"):
            documents, errors = extract_many(payloads)
            errors = overflow_error + errors
            credit_evidence = assess_credit_evidence(documents)
            prerequisite_evidence = assess_prerequisite_evidence(documents)
            statuses = {item.code: item.status for item in credit_evidence}
            combined_text = "\n".join(f"[{doc.name}]\n{doc.text}" for doc in documents)[:400_000]
            findings = review_design_text(combined_text)
            yes_points, maybe_points = score_assessment(CREDITS, statuses)
            projection = calculate_certification(yes_points, maybe_points)
            checklist_rows = build_checklist(CREDITS, statuses)
            risk_results = {
                item.code: assess_submission_risk(
                    next(c for c in CREDITS if c.code == item.code),
                    f"Evidence extracted from {', '.join(item.sources)}. {item.evidence_snippet}",
                )
                for item in credit_evidence if item.status in {"Yes", "Maybe"}
            }
            project_name = _infer_project_name([doc.name for doc in documents])
            bundle = build_result_bundle(
                project_name, documents, credit_evidence, prerequisite_evidence,
                findings, checklist_rows, projection, risk_results,
            )
            st.session_state.assessment_statuses = statuses
            st.session_state.review_findings = findings
            st.session_state.risk_results = risk_results
            st.session_state.checklist_records = {}
            st.session_state.pop("scorecard_editor", None)
            st.session_state.pop("checklist_editor", None)
            st.session_state.pop("checklist_signature", None)
            st.session_state.upload_analysis = {
                "project_name": project_name, "documents": documents, "errors": errors,
                "credit_evidence": credit_evidence, "prerequisites": prerequisite_evidence,
                "findings": findings, "projection": projection, "checklist": checklist_rows,
                "bundle": bundle, "risks": risk_results,
            }

    analysis = st.session_state.upload_analysis
    if not analysis:
        st.markdown('<div class="empty">Upload the project package to generate all LEED v5 outputs in one run.<br><small>Nothing is stored by the application after the session ends.</small></div>', unsafe_allow_html=True)
        return

    documents = analysis["documents"]
    projection = analysis["projection"]
    all_warnings = [f"{doc.name}: {warning}" for doc in documents for warning in doc.warnings] + analysis["errors"]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Files processed", str(len(documents)), f"{sum(doc.page_count for doc in documents)} PDF pages")
    with c2:
        metric_card("Extracted evidence", f"{sum(len(doc.text) for doc in documents):,}", "Searchable characters")
    with c3:
        metric_card("Pipeline score", f"{projection.projected_points}/110", f"{projection.yes_points} committed + {projection.maybe_points} potential")
    with c4:
        metric_card("Projected level", projection.level, "Subject to prerequisites and v5 gates")
    st.progress(projection.projected_points / 110, text=f"Automated evidence projection · {projection.projected_points} / 110")
    if all_warnings:
        with st.expander(f"Extraction notes · {len(all_warnings)}", expanded=True):
            for warning in all_warnings:
                st.warning(warning)

    summary_tab, prereq_tab, score_tab, findings_tab, risks_tab = st.tabs(["Package summary", "Prerequisite screen", "Automated scorecard", "Drawing/spec findings", "Submission risks"])
    with summary_tab:
        manifest = pd.DataFrame([
            {"File": d.name, "Type": d.kind, "Size (MB)": round(d.size_bytes / 1_048_576, 2), "Pages": d.page_count, "Extraction": d.extraction_status, "Characters": len(d.text)}
            for d in documents
        ])
        st.dataframe(manifest, hide_index=True, use_container_width=True)
        st.caption("SHA-256 fingerprints and detailed extraction notes are included in the downloadable file manifest.")
    with prereq_tab:
        prereq_df = pd.DataFrame([
            {"Code": e.code, "Prerequisite": e.name, "Evidence Signal": e.status, "Confidence": f"{e.confidence}%", "Matched Terms": ", ".join(e.matched_terms), "Sources": ", ".join(e.sources)}
            for e in analysis["prerequisites"]
        ])
        st.dataframe(prereq_df, hide_index=True, use_container_width=True, height=510)
        st.caption("‘No’ means no evidence was found in the uploaded package—not confirmed noncompliance.")
    with score_tab:
        evidence_df = pd.DataFrame([
            {"Code": e.code, "Credit": e.name, "Assessment": e.status, "Confidence": f"{e.confidence}%", "Matched Evidence": ", ".join(e.matched_terms), "Source Files": ", ".join(e.sources)}
            for e in analysis["credit_evidence"]
        ])
        st.dataframe(evidence_df, hide_index=True, use_container_width=True, height=560)
    with findings_tab:
        if analysis["findings"]:
            for finding in analysis["findings"]:
                severity = "error" if finding.severity == "High" else "success" if finding.severity == "Positive" else "warning"
                getattr(st, severity)(f"{finding.severity} · {finding.criterion} — {finding.title}\n\n{finding.drawing_comment}")
        else:
            st.info("No deterministic text-rule findings were triggered. This does not replace drawing-by-drawing human review.")
    with risks_tab:
        if analysis["risks"]:
            risk_df = pd.DataFrame([
                {"Credit": code, "Risk": result.level, "Score": result.score, "Evidence Coverage": f"{result.evidence_coverage}%", "Primary Flag": result.flags[0] if result.flags else "No material automated flag", "First Corrective Action": result.corrective_actions[0]}
                for code, result in analysis["risks"].items()
            ])
            st.dataframe(risk_df, hide_index=True, use_container_width=True, height=520)
        else:
            st.info("No attempted credits were inferred, so the submission risk register is empty.")

    report_html = build_summary_html(
        analysis["project_name"], documents, analysis["credit_evidence"],
        analysis["prerequisites"], analysis["findings"], projection,
    )
    d1, d2, _ = st.columns([1.2, 1, 1.5])
    with d1:
        st.download_button("Download complete result bundle (.zip)", analysis["bundle"], file_name=f"{analysis['project_name'].lower().replace(' ', '-')}-leed-v5-results.zip", mime="application/zip", type="primary", use_container_width=True)
    with d2:
        st.download_button("Download executive report (.html)", report_html, file_name=f"{analysis['project_name'].lower().replace(' ', '-')}-leed-v5-report.html", mime="text/html", use_container_width=True)


def render_guide(profile: ProjectProfile) -> None:
    module_header(1, "Design Guide Generator", "A project-specific briefing that turns the certification target into prerequisites, design priorities, evidence owners, and delivery controls.")
    guide_html = build_guide_html(profile)
    guide_md = build_guide_markdown(profile)
    strategy = strategic_credits(profile)
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Target threshold", f"{CERTIFICATION_THRESHOLDS[profile.target_level]}+ pts", profile.target_level)
    with c2:
        metric_card("Strategic pathway", f"{sum(c.points for c in strategy)} pts", f"{len(strategy)} priority credits")
    with c3:
        buffer = 8 if profile.target_level in {"Gold", "Platinum"} else 5
        metric_card("Recommended buffer", f"+{buffer} pts", "Above minimum target")
    st.write("")
    components.html(guide_html, height=780, scrolling=True)
    d1, d2, _ = st.columns([1, 1, 2])
    with d1:
        st.download_button("Download HTML report", guide_html, file_name=f"{profile.name.lower().replace(' ', '-')}-leed-v5-guide.html", mime="text/html", type="primary", use_container_width=True)
    with d2:
        st.download_button("Download Markdown", guide_md, file_name=f"{profile.name.lower().replace(' ', '-')}-leed-v5-guide.md", mime="text/markdown", use_container_width=True)


def render_scorecard(profile: ProjectProfile) -> None:
    module_header(2, "Interactive Pre-assessment", "Mark each planning credit Yes, Maybe, or No. The forecast treats Yes as committed and Yes + Maybe as the potential certification pipeline.")
    credits = credits_for(profile.project_type)
    statuses = st.session_state.assessment_statuses
    scorecard = pd.DataFrame([
        {
            "Code": c.code, "Category": c.category, "Credit": c.name,
            "Impact Area": c.pillar, "Max Points": c.points,
            "Assessment": statuses.get(c.code, "No"),
        }
        for c in credits
    ])
    edited = st.data_editor(
        scorecard,
        column_config={
            "Assessment": st.column_config.SelectboxColumn("Assessment", options=["Yes", "Maybe", "No"], required=True),
            "Max Points": st.column_config.NumberColumn("Max Points", format="%d pts"),
        },
        disabled=["Code", "Category", "Credit", "Impact Area", "Max Points"],
        hide_index=True, use_container_width=True, height=530,
        key="scorecard_editor",
    )
    for row in edited.to_dict("records"):
        statuses[row["Code"]] = row["Assessment"]
    yes_points, maybe_points = score_assessment(credits, statuses)
    projection = calculate_certification(yes_points, maybe_points)

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Committed", f"{yes_points} pts", "Credits marked Yes")
    with m2:
        metric_card("Potential", f"+{maybe_points} pts", "Credits marked Maybe")
    with m3:
        metric_card("Projected level", projection.level, f"{projection.projected_points} pipeline points")
    with m4:
        if projection.next_level:
            metric_card("Next threshold", f"{projection.points_to_next} pts", f"To reach {projection.next_level}")
        else:
            metric_card("Top threshold", "Reached", "Confirm Platinum gates")
    st.progress(projection.projected_points / 110, text=f"Pipeline score · {projection.projected_points} / 110")
    if projection.level == "Platinum":
        st.warning("LEED v5 Platinum has additional mandatory energy efficiency, electrification/carbon, renewable energy, and embodied-carbon requirements. An 80-point projection alone is not sufficient.")

    with st.expander("Category pipeline", expanded=False):
        category_df = pd.DataFrame(category_scores(credits, statuses)).set_index("Category")
        st.bar_chart(category_df[["Yes", "Maybe"]], color=["#26705b", "#d79a43"], horizontal=True)
        st.caption("This is a consultant planning scorecard—not an official Arc scorecard or compliance determination.")


def render_design_review() -> None:
    module_header(3, "AI-Driven Drawing & Specification Review", "Paste notes or specification text. The transparent rules engine flags omissions and carbon, health, and materials risks, then writes drafting-team instructions.")
    sample = "HVAC system uses a variable-speed centrifugal chiller with R-134a refrigerant; fresh air monitoring is not specified in the current mechanical plan. Interior paints and adhesives are included."
    review_text = st.text_area("Design notes or drawing/specification excerpt", value=sample, height=180, help="No project data leaves the app. The current engine uses local deterministic keyword and omission rules.")
    if st.button("Run design review", type="primary", use_container_width=False):
        st.session_state.review_findings = review_design_text(review_text)
    findings = st.session_state.review_findings
    if not findings:
        st.markdown('<div class="empty">Run the review to generate traceable findings and drafting comments.</div>', unsafe_allow_html=True)
        return
    left, right = st.columns([1, 1.15], gap="large")
    with left:
        st.subheader("Review Findings")
        for finding in findings:
            css = "high" if finding.severity == "High" else "positive" if finding.severity == "Positive" else ""
            st.markdown(
                f'<div class="finding {css}"><div class="finding-top"><h4>{escape(finding.title)}</h4><span class="severity">{escape(finding.severity)}</span></div><p><strong>{escape(finding.criterion)}</strong><br>{escape(finding.evidence)}</p></div>',
                unsafe_allow_html=True,
            )
    with right:
        st.subheader("Specific Drawing Modification Comments")
        for index, finding in enumerate(findings, start=1):
            st.markdown(f'<div class="drawing-comment"><strong>Comment {index} · {escape(finding.criterion)}</strong><br>{escape(finding.drawing_comment)}</div>', unsafe_allow_html=True)
    st.caption("Simulated review only. Confirm every finding against the registered rating system and current addenda before issuing it to the design team.")


def render_checklist(profile: ProjectProfile) -> None:
    module_header(4, "Dynamic Documentation Checklist", "The list is generated only from credits marked Yes or Maybe in Module 2. Deliverables, owners, and workflow status remain editable.")
    credits = credits_for(profile.project_type)
    statuses = st.session_state.assessment_statuses
    selected_signature = tuple((c.code, statuses.get(c.code, "No")) for c in credits if statuses.get(c.code, "No") in {"Yes", "Maybe"})
    if st.session_state.get("checklist_signature") != selected_signature:
        st.session_state.checklist_signature = selected_signature
        st.session_state.pop("checklist_editor", None)
    rows = build_checklist(credits, statuses, st.session_state.checklist_records)
    if not rows:
        st.markdown('<div class="empty">No active documentation items yet.<br>Mark credits Yes or Maybe in Module 2 and this checklist will populate automatically.</div>', unsafe_allow_html=True)
        return
    checklist_df = pd.DataFrame(rows)
    edited = st.data_editor(
        checklist_df,
        column_config={
            "Assessment": st.column_config.SelectboxColumn("Assessment", options=["Yes", "Maybe"], disabled=True),
            "Status": st.column_config.SelectboxColumn("Status", options=["Not Started", "In Progress", "Complete"], required=True),
            "Required Deliverables": st.column_config.TextColumn("Required Deliverables", width="large"),
            "Responsible Party": st.column_config.TextColumn("Responsible Party", width="medium"),
        },
        disabled=["Credit Code", "Credit Name", "Assessment"],
        hide_index=True, use_container_width=True, height=min(590, 74 + len(rows) * 35),
        key="checklist_editor",
    )
    for row in edited.to_dict("records"):
        st.session_state.checklist_records[row["Credit Code"]] = {
            "Required Deliverables": row["Required Deliverables"],
            "Responsible Party": row["Responsible Party"],
            "Status": row["Status"],
        }
    complete = int((edited["Status"] == "Complete").sum())
    in_progress = int((edited["Status"] == "In Progress").sum())
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Active credits", str(len(edited)), "Yes + Maybe")
    with c2:
        metric_card("In progress", str(in_progress), "Evidence under development")
    with c3:
        metric_card("Complete", f"{complete}/{len(edited)}", "Ready for QA review")
    csv_buffer = StringIO()
    edited.to_csv(csv_buffer, index=False)
    st.download_button("Download checklist CSV", csv_buffer.getvalue(), file_name=f"{profile.name.lower().replace(' ', '-')}-documentation-checklist.csv", mime="text/csv")


def render_risk_review(profile: ProjectProfile) -> None:
    module_header(5, "Final Submission Reviewer & Risk Assessment", "Stress-test a final narrative for evidence coverage, quantified outcomes, document traceability, unresolved commitments, and Platinum-gate exposure.")
    credits = credits_for(profile.project_type)
    credit_by_label = {f"{c.code} · {c.name} ({c.points} pts)": c for c in credits}
    credit_labels = list(credit_by_label)
    first_auto_reviewed = next(iter(st.session_state.risk_results), None)
    default_index = next(
        (index for index, label in enumerate(credit_labels) if credit_by_label[label].code == first_auto_reviewed),
        0,
    )
    selected_label = st.selectbox("LEED v5 credit", credit_labels, index=default_index)
    selected = credit_by_label[selected_label]
    narrative = st.text_area("Final submission narrative or calculation summary", height=230, placeholder="Describe the selected compliance path, baseline, final quantified result, calculation method, responsible professional, and exact uploaded file/sheet/specification references…")
    if st.button("Assess submission risk", type="primary"):
        st.session_state.risk_results[selected.code] = assess_submission_risk(selected, narrative)
    result = st.session_state.risk_results.get(selected.code)
    if result is None:
        st.markdown('<div class="empty">Choose a credit, paste the final narrative, and run the reviewer.</div>', unsafe_allow_html=True)
        return
    risk_class = f"risk-{result.level.lower()}"
    st.markdown(f'<div class="risk-panel {risk_class}"><small>Audit risk level</small><h3>{result.level} · risk score {result.score}</h3><div>Evidence concept coverage: {result.evidence_coverage}%</div></div>', unsafe_allow_html=True)
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader("Review flags")
        if result.flags:
            for flag in result.flags:
                st.warning(flag)
        else:
            st.success("No material automated flags detected.")
        if result.strengths:
            with st.expander("What is already working", expanded=False):
                for strength in result.strengths:
                    st.write(f"• {strength}")
    with right:
        st.subheader("Corrective Action Plan")
        for number, action in enumerate(result.corrective_actions, start=1):
            st.markdown(f"**{number}.** {action}")
    st.info("Before formal submittal, perform a human cross-check between every narrative value and the final uploaded calculation, drawing, schedule, and specification reference.")


init_state()
project = render_sidebar()
render_hero(project)

tab_upload, tab_guide, tab_scorecard, tab_review, tab_docs, tab_risk = st.tabs([
    "00 · Upload & auto-analyze", "01 · Design guide", "02 · Pre-assessment", "03 · Design review",
    "04 · Documentation", "05 · Submission risk",
])
with tab_upload:
    render_upload_workspace(project)
with tab_guide:
    render_guide(project)
with tab_scorecard:
    render_scorecard(project)
with tab_review:
    render_design_review()
with tab_docs:
    render_checklist(project)
with tab_risk:
    render_risk_review(project)

st.markdown(
    '<div class="source-note"><strong>Framework note.</strong> This planning aid reflects LEED v5\'s three impact areas and standard 40/50/60/80 certification bands. Always use the live <a href="https://www.usgbc.org/leed/v5" target="_blank">USGBC LEED v5 rating system, credit library, scorecards, and addenda</a> governing the project registration date. LEED® is a registered trademark of the U.S. Green Building Council; this tool is independent and not endorsed by USGBC or GBCI.</div>',
    unsafe_allow_html=True,
)
