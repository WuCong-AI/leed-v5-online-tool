# LEED v4 / v4.1 / v5 Certification & Automation Tool

A deploy-ready, upload-first Streamlit consultant workspace. Upload the project package once and it connects evidence extraction, a version/system-specific pre-assessment, deterministic drawing review, documentation collection, and final-submission risk control.

## Upload-first online workflow

The default `00 · Upload & auto-analyze` tab accepts up to 20 project files per run (30 MB each): searchable PDF, DOCX, XLSX, CSV, TXT/Markdown, PNG/JPEG/TIFF, IFC, DXF, and DWG.

One click produces:

- File inventory with SHA-256 fingerprints and extraction diagnostics
- Prerequisite evidence screen
- Switchable LEED v4, v4.1, and v5 rule packs for BD+C, ID+C, and O+M
- Automated Yes/Maybe/No scorecards with version-specific totals, confidence, and source files
- Official GBCI review report/scorecard detection; Awarded/Denied statuses override keyword signals
- Reviewer-calibrated cross-checks for occupancy, area, HVAC model/drawing, weather file, low-emitting product, and formula consistency
- Exact drawing/specification modification comments
- Scorecard-driven documentation checklist
- Submission risk register and corrective actions
- A downloadable ZIP containing HTML, JSON, and CSV deliverables

Parsing is local and in memory. Project content is not sent to an external AI service. Searchable PDF is strongly preferred: raster images are validated and inventoried, but they are explicitly marked for OCR/visual review. Native DWG files are inventoried and should be exported to searchable PDF, IFC, or DXF for automated content review.

## Run locally

Python 3.10 or later is required.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL printed by Streamlit (normally `http://localhost:8501`).

## Architecture

```text
leed-v5-automation-tool/
├── app.py                         # Streamlit composition and shared session state
├── Dockerfile                     # Non-root production container and health check
├── leed_tool/
│   ├── data.py                    # Prerequisites, 110-point planning scorecard, deliverables
│   ├── models.py                  # Typed immutable domain models
│   ├── styles.py                  # Responsive visual system and reusable UI components
│   └── services/
│       ├── assessment.py          # Yes/Maybe scoring and certification forecast
│       ├── auto_assessment.py     # Uploaded evidence to prerequisite/credit signals
│       ├── checklist.py           # Scorecard-driven evidence checklist
│       ├── export.py              # HTML/JSON/CSV ZIP result bundle
│       ├── guide.py               # Markdown and standalone HTML guide generation
│       ├── ingestion.py           # Safe in-memory PDF/DOCX/XLSX/image/CAD extraction
│       ├── review.py              # Auditable drawing/spec keyword and omission rules
│       └── risk.py                # Narrative completeness and clarification-risk scoring
├── tests/test_services.py         # Domain regression tests
├── .streamlit/config.toml         # Theme and safe local defaults
└── requirements.txt
```

The UI is intentionally thin. Business rules are pure Python functions in `leed_tool/services`, making them testable and ready to expose through an API or replace with a database/LLM-backed implementation later.

## The five connected modules

1. **Design Guide Generator** — project profile, prerequisites, target-level strategy, embedded HTML preview, and HTML/Markdown downloads.
2. **Interactive Pre-assessment** — Yes/Maybe/No data editor, committed and potential points, certification projection, and category pipeline.
3. **Drawing & Specification Review** — transparent deterministic checks for ventilation monitoring, refrigerants, electrification, low-emitting materials, embodied carbon, efficiency, and metering.
4. **Documentation Checklist** — automatically includes only attempted Yes/Maybe credits; deliverables, owners, and status are editable and downloadable as CSV.
5. **Final Submission Reviewer** — evaluates evidence coverage, numeric results, file/sheet references, finality, accountable parties, and LEED v5 Platinum-gate exposure.

The upload pipeline automatically populates all five consultant modules through shared Streamlit session state, so users can accept the automated outputs or refine them manually.

Supported uploads include searchable PDF, DOCX, XLSX/XLSM, CSV, TXT/Markdown, raster drawings, IFC/DXF/DWG, and ZIP project packages up to 500 MB. ZIP files are inspected only in memory with limits on member count, expanded size, individual file size, and compression ratio. One nested ZIP level is inspected, password-protected archives are skipped, and XLSM macros are never executed. Rapid mode prioritizes review reports, clarifications, calculators, narratives, and key evidence while inventorying large scanned drawings; Deep drawing scan performs page-level extraction.

## Deploy online

### Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app with `app.py` as the entry point.
3. Deploy. The platform installs `requirements.txt` automatically.

### Any Docker host

```powershell
docker build -t leed-v5-online .
docker run --rm -p 8501:8501 leed-v5-online
```

For real client documents, use a private deployment with TLS, authentication, regional data controls, malware scanning at the gateway, encrypted logs/storage, retention rules, and a signed data-processing agreement. The application itself intentionally does not persist uploads.

## Framework basis and limitations

The data model supports LEED v4, v4.1, and v5 family-specific scorecards and the standard 40/50/60/80 certification bands. LEED v5 additionally reflects decarbonization, quality of life, and ecological conservation/restoration impact areas and flags its additional Platinum performance requirements.

This is an independent consultant planning and QA aid, not an official USGBC/GBCI scorecard, Arc form, certification decision, or substitute for the licensed reference guide. Credit names, point groupings, and deliverables are a compact representative planning model. Before using any output for a real application, reconcile it with:

- [USGBC LEED v5 hub](https://www.usgbc.org/leed/v5)
- [USGBC LEED v4.1 hub](https://www.usgbc.org/leed/v41)
- [USGBC LEED v4 hub](https://www.usgbc.org/leed/v4)
- [Official commercial certification guide](https://www.usgbc.org/tools/leed-certification/commercial)
- The registered project's live Arc forms and rating-system selection
- The online credit library and all addenda effective on the registration date

LEED® is a registered trademark of the U.S. Green Building Council. This project is not endorsed by USGBC or GBCI.

## Tests

```powershell
python -m pytest -q
```
