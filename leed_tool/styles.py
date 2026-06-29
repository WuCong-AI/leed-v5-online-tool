"""Visual system for the Streamlit interface."""

from __future__ import annotations

import streamlit as st


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root {
          --forest-950:#102e28; --forest-800:#194b3e; --forest-650:#26705b;
          --mint-100:#e9f3ee; --paper:#f7f8f4; --ink:#19332c; --muted:#64736d;
          --amber:#d79a43; --coral:#d46f5c; --line:#dfe8e2;
        }
        .stApp { background: linear-gradient(180deg,#f7f8f4 0,#f3f6f2 100%); color:var(--ink); }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stSidebar"] { background:#f0f5f1; border-right:1px solid var(--line); }
        [data-testid="stSidebar"] .stMarkdown h3 { color:var(--forest-950); }
        .block-container { max-width:1400px; padding-top:2.3rem; padding-bottom:4rem; }
        h1,h2,h3 { letter-spacing:-.025em; }
        h1 { color:var(--forest-950); }
        .hero {
          background:radial-gradient(circle at 86% 5%,#3b806b 0,transparent 33%),
                     linear-gradient(120deg,#12352d,#1c5948);
          color:white; padding:34px 38px; border-radius:22px; margin-bottom:18px;
          box-shadow:0 18px 45px rgba(18,53,45,.13); position:relative; overflow:hidden;
        }
        .hero:after { content:""; position:absolute; right:-48px; bottom:-75px; width:230px; height:230px;
          border:1px solid rgba(255,255,255,.17); border-radius:50%; box-shadow:0 0 0 28px rgba(255,255,255,.035),0 0 0 58px rgba(255,255,255,.025); }
        .hero-kicker { color:#a6d9c4; font-size:.73rem; font-weight:750; letter-spacing:.16em; text-transform:uppercase; }
        .hero h1 { color:white; font-size:2.45rem; margin:.35rem 0 .5rem; max-width:800px; }
        .hero p { color:#d6e9e1; max-width:760px; font-size:1.02rem; margin:0; }
        .pill-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:20px; }
        .impact-pill { border:1px solid rgba(255,255,255,.23); background:rgba(255,255,255,.08); padding:7px 11px; border-radius:999px; font-size:.78rem; }
        .module-head { margin:.8rem 0 1.25rem; }
        .module-head .kicker { color:var(--forest-650); font-size:.72rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
        .module-head h2 { margin:.25rem 0; font-size:1.75rem; }
        .module-head p { color:var(--muted); margin:.25rem 0; max-width:850px; }
        .surface { background:white; border:1px solid var(--line); border-radius:16px; padding:18px 20px; margin-bottom:14px; box-shadow:0 7px 24px rgba(25,75,62,.045); }
        .metric-card { background:white; border:1px solid var(--line); border-radius:15px; padding:16px 18px; min-height:102px; box-shadow:0 7px 24px rgba(25,75,62,.04); }
        .metric-label { color:var(--muted); font-size:.73rem; font-weight:750; letter-spacing:.08em; text-transform:uppercase; }
        .metric-value { color:var(--forest-950); font-size:1.72rem; line-height:1.2; font-weight:760; margin-top:7px; }
        .metric-note { color:var(--muted); font-size:.76rem; margin-top:4px; }
        .finding { background:white; border:1px solid var(--line); border-left:5px solid var(--amber); border-radius:12px; padding:14px 17px; margin-bottom:10px; }
        .finding.high { border-left-color:var(--coral); } .finding.positive { border-left-color:#4e9b78; }
        .finding-top { display:flex; justify-content:space-between; gap:12px; align-items:center; }
        .finding h4 { margin:0; font-size:1rem; } .finding p { color:#536a62; margin:.55rem 0 0; }
        .severity { font-size:.7rem; font-weight:800; padding:4px 8px; border-radius:999px; background:#f7ecdb; color:#81551f; }
        .high .severity { background:#fae8e4; color:#973f30; } .positive .severity { background:#e6f3ec; color:#266b50; }
        .drawing-comment { background:#eef5f1; border:1px solid #d6e6dc; border-radius:12px; padding:14px 16px; margin-bottom:10px; }
        .drawing-comment strong { color:var(--forest-800); }
        .risk-panel { padding:20px 22px; border-radius:16px; color:white; margin-bottom:14px; }
        .risk-low { background:linear-gradient(120deg,#24664f,#36836a); }
        .risk-medium { background:linear-gradient(120deg,#a76b22,#cf9346); }
        .risk-high { background:linear-gradient(120deg,#913f34,#c15f50); }
        .risk-panel small { opacity:.82; letter-spacing:.1em; text-transform:uppercase; }
        .risk-panel h3 { color:white; margin:.35rem 0 0; font-size:1.7rem; }
        .empty { text-align:center; background:white; border:1px dashed #cbd9d1; border-radius:16px; padding:38px; color:var(--muted); }
        .source-note { font-size:.78rem; color:var(--muted); border-top:1px solid var(--line); margin-top:22px; padding-top:14px; }
        [data-baseweb="tab-list"] { gap:7px; }
        [data-baseweb="tab"] { height:50px; padding:0 15px; background:white; border:1px solid var(--line); border-radius:12px 12px 0 0; }
        [aria-selected="true"][data-baseweb="tab"] { background:var(--mint-100); color:var(--forest-800); }
        .stButton > button, .stDownloadButton > button { border-radius:10px; border-color:#b8cec2; font-weight:650; }
        .stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] { background:var(--forest-800); border-color:var(--forest-800); }
        [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
        @media (max-width:760px) { .hero{padding:26px 24px}.hero h1{font-size:2rem}.block-container{padding-left:1rem;padding-right:1rem} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def module_header(number: int, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="module-head">
          <div class="kicker">Module {number:02d}</div>
          <h2>{title}</h2><p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )

