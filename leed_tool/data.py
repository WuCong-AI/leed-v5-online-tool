"""Curated LEED v5 planning dataset.

The scorecard is a representative 110-point consultant planning model. It is
deliberately compact enough for interactive pre-assessment and is not a copy of
USGBC/GBCI proprietary forms. Teams must reconcile it with the rating system,
credit library, Arc forms, and addenda applicable on the registration date.
"""

from __future__ import annotations

from .models import Credit, Prerequisite

PROJECT_TYPES = (
    "BD+C: New Construction",
    "BD+C: Core & Shell",
    "ID+C: Commercial Interiors",
)

TARGET_LEVELS = ("Certified", "Silver", "Gold", "Platinum")

PILLAR_COLORS = {
    "Decarbonization": "#D59A45",
    "Quality of Life": "#59A89C",
    "Ecological Conservation": "#7FAF5B",
}

CERTIFICATION_THRESHOLDS = {
    "Certified": 40,
    "Silver": 50,
    "Gold": 60,
    "Platinum": 80,
}


PREREQUISITES: tuple[Prerequisite, ...] = (
    Prerequisite("IPp1", "Integrative Process", "Climate Resilience Assessment", "Quality of Life", summary="Identify acute and chronic climate hazards, vulnerable systems, and adaptation priorities."),
    Prerequisite("IPp2", "Integrative Process", "Human Impact Assessment", "Quality of Life", summary="Assess equity, accessibility, health, and community impacts early enough to change design."),
    Prerequisite("IPp3", "Integrative Process", "Carbon Assessment", "Decarbonization", summary="Establish operational, embodied, refrigerant, and transportation carbon baselines."),
    Prerequisite("IPp4", "Integrative Process", "Tenant Guidelines", "Decarbonization", applicability=("BD+C: Core & Shell",), summary="Issue enforceable tenant design and construction guidance aligned with project goals."),
    Prerequisite("SSp1", "Sustainable Sites", "Minimize Site Disturbance", "Ecological Conservation", applicability=("BD+C",), summary="Protect special-status vegetation and limit disturbance within the project boundary."),
    Prerequisite("WEp1", "Water Efficiency", "Water Metering and Reporting", "Ecological Conservation", summary="Provide whole-project metering and a pathway for ongoing water-performance reporting."),
    Prerequisite("WEp2", "Water Efficiency", "Minimum Water Efficiency", "Ecological Conservation", summary="Document baseline and design-case indoor, outdoor, and process water demand."),
    Prerequisite("EAp1", "Energy & Atmosphere", "Minimum Energy Performance", "Decarbonization", summary="Demonstrate minimum energy efficiency and associated greenhouse-gas performance."),
    Prerequisite("EAp2", "Energy & Atmosphere", "Fundamental Refrigerant Management", "Decarbonization", summary="Inventory refrigerants and avoid prohibited ozone-depleting substances."),
    Prerequisite("EAp3", "Energy & Atmosphere", "Fundamental Commissioning", "Decarbonization", summary="Define owner requirements, basis of design, commissioning scope, and issue resolution."),
    Prerequisite("EAp4", "Energy & Atmosphere", "Energy Metering and Reporting", "Decarbonization", summary="Meter energy sources and establish ongoing performance reporting."),
    Prerequisite("MRp1", "Materials & Resources", "Planning for Zero Waste Operations", "Ecological Conservation", summary="Plan storage, collection, diversion, and measurement for operational waste streams."),
    Prerequisite("MRp2", "Materials & Resources", "Quantify and Assess Embodied Carbon", "Decarbonization", summary="Quantify upfront embodied carbon and identify high-priority reduction opportunities."),
    Prerequisite("EQp1", "Indoor Environmental Quality", "Construction Management", "Quality of Life", summary="Control construction-phase moisture, particulates, emissions, and contamination."),
    Prerequisite("EQp2", "Indoor Environmental Quality", "Fundamental Air Quality", "Quality of Life", summary="Document ventilation, filtration, source control, and system integration."),
    Prerequisite("EQp3", "Indoor Environmental Quality", "No Smoking", "Quality of Life", summary="Prohibit tobacco smoke and emissions in and around the project."),
)


CREDITS: tuple[Credit, ...] = (
    Credit("IPc1", "Integrative Process", "Integrative Design Process", 1, "Quality of Life", "Charrette agenda and minutes; LEED goals; cross-discipline action log", "LEED Consultant / Architect", strategy="Run a pre-design charrette linking carbon, health, water, and habitat decisions."),
    Credit("LTc1", "Location & Transportation", "Sensitive Land Protection", 1, "Ecological Conservation", "Site survey; sensitive land map; civil narrative", "Civil Engineer / Ecologist", strategy="Prefer previously developed land and avoid sensitive resources."),
    Credit("LTc2", "Location & Transportation", "Equitable Development", 2, "Quality of Life", "Community context assessment; engagement record; commitments matrix", "Owner / Social Impact Lead", strategy="Convert community priorities into measurable project commitments."),
    Credit("LTc3", "Location & Transportation", "Compact and Connected Development", 6, "Decarbonization", "Density and diverse-use calculations; transit maps; walking routes", "Architect / Transport Planner", strategy="Leverage density, daily services, walking, and high-quality transit."),
    Credit("LTc4", "Location & Transportation", "Transportation Demand Management", 4, "Decarbonization", "TDM plan; mode-share forecast; bicycle plans; tenant communications", "Transport Planner / Owner", strategy="Reduce single-occupancy vehicle trips through infrastructure and programs."),
    Credit("LTc5", "Location & Transportation", "Electric Vehicles", 3, "Decarbonization", "Parking plan; EVSE schedule; electrical load calculations", "Electrical Engineer", strategy="Provide accessible charging and EV-ready capacity with load management."),
    Credit("SSc1", "Sustainable Sites", "Enhanced Ecological Site Performance", 2, "Ecological Conservation", "Habitat assessment; planting plan; native/adapted species schedule", "Landscape Architect / Ecologist", strategy="Restore habitat, soils, and ecological function beyond the prerequisite."),
    Credit("SSc2", "Sustainable Sites", "Open Space and Human-Nature Connection", 2, "Quality of Life", "Open-space plan; area calculations; biophilic design narrative", "Landscape Architect", strategy="Make vegetated outdoor space accessible and restorative for occupants."),
    Credit("SSc3", "Sustainable Sites", "Rainwater Management", 3, "Ecological Conservation", "Hydrologic model; civil drawings; green-infrastructure calculations", "Civil Engineer / Landscape Architect", strategy="Manage runoff through infiltration, evapotranspiration, reuse, and safe conveyance."),
    Credit("SSc4", "Sustainable Sites", "Enhanced Resilient Site Design", 2, "Quality of Life", "Hazard maps; resilience narrative; civil and landscape details", "Civil Engineer / Resilience Lead", strategy="Design site systems for projected heat, flood, drought, and storm conditions."),
    Credit("SSc5", "Sustainable Sites", "Heat Island and Light Pollution Reduction", 1, "Quality of Life", "Roof/site reflectance plan; lighting photometrics; fixture schedule", "Architect / Electrical Engineer", strategy="Reduce thermal stress and protect nocturnal habitat and neighboring communities."),
    Credit("WEc1", "Water Efficiency", "Enhanced Water Efficiency", 7, "Ecological Conservation", "Water balance; fixture schedule; irrigation and process calculations", "Plumbing Engineer / Landscape Architect", strategy="Reduce potable demand across indoor, outdoor, and process uses."),
    Credit("WEc2", "Water Efficiency", "Enhanced Water Metering", 2, "Ecological Conservation", "Meter schedule; riser diagram; controls points list", "Plumbing Engineer / Controls Contractor", strategy="Submeter significant end uses and trend data for leak and performance management."),
    Credit("WEc3", "Water Efficiency", "Water Reuse and Cooling Systems", 2, "Ecological Conservation", "Alternative-water study; cooling tower cycles calculation; water quality plan", "Plumbing / Mechanical Engineer", strategy="Match nonpotable sources to demands and optimize cooling-system water use."),
    Credit("EAc1", "Energy & Atmosphere", "Enhanced Energy Efficiency", 16, "Decarbonization", "Whole-building energy model; model inputs; efficiency measures narrative", "Energy Modeler / MEP Engineer", strategy="Prioritize passive load reduction, efficient systems, controls, and measured outcomes.", platinum_gate=True),
    Credit("EAc2", "Energy & Atmosphere", "Operational Carbon Performance", 5, "Decarbonization", "GHG calculations; hourly emissions analysis; electrification plan", "Energy Modeler / Electrical Engineer", strategy="Eliminate onsite combustion and reduce grid-related operational emissions.", platinum_gate=True),
    Credit("EAc3", "Energy & Atmosphere", "Grid-Interactive and Flexible Building", 2, "Decarbonization", "Load profiles; controls sequence; demand-response or storage narrative", "Electrical Engineer / Controls Contractor", strategy="Shape and shift loads to support a lower-carbon, resilient grid."),
    Credit("EAc4", "Energy & Atmosphere", "Renewable Energy", 4, "Decarbonization", "Renewable feasibility study; system design or procurement contract", "Owner / Electrical Engineer", strategy="Supply project demand with high-quality renewable energy.", platinum_gate=True),
    Credit("EAc5", "Energy & Atmosphere", "Enhanced Commissioning", 3, "Decarbonization", "Cx plan; design reviews; functional test scripts; issues log", "Commissioning Authority", strategy="Extend commissioning through design, envelope, monitoring, and operations."),
    Credit("EAc6", "Energy & Atmosphere", "Enhanced Refrigerant Management", 3, "Decarbonization", "Refrigerant inventory; GWP calculations; leak detection specification", "Mechanical Engineer", strategy="Select low-GWP refrigerants and limit lifecycle leakage."),
    Credit("MRc1", "Materials & Resources", "Building and Material Reuse", 4, "Decarbonization", "Existing conditions survey; reuse schedule; area/quantity calculations", "Architect / Contractor", strategy="Retain structures and components to avoid new-material carbon."),
    Credit("MRc2", "Materials & Resources", "Embodied Carbon Reduction", 4, "Decarbonization", "Whole-building LCA; baseline comparison; product quantities", "LCA Consultant / Structural Engineer", strategy="Reduce whole-building embodied carbon through structure, envelope, and procurement.", platinum_gate=True),
    Credit("MRc3", "Materials & Resources", "Low-Emitting Materials", 3, "Quality of Life", "Product VOC/emissions certificates; tracking log; cost or area calculations", "Architect / Contractor", strategy="Specify and verify low-emitting interior products and wet-applied materials."),
    Credit("MRc4", "Materials & Resources", "Building Product Selection and Procurement", 2, "Ecological Conservation", "EPDs; ingredient disclosures; procurement tracker; invoices", "Architect / Contractor", strategy="Reward transparent, optimized, responsibly sourced products."),
    Credit("EQc1", "Indoor Environmental Quality", "Enhanced Air Quality", 3, "Quality of Life", "Ventilation calculations; filtration schedule; air-quality controls sequence", "Mechanical Engineer", strategy="Exceed fundamental ventilation, filtration, and pollutant source control."),
    Credit("EQc2", "Indoor Environmental Quality", "Occupant Experience", 4, "Quality of Life", "Thermal comfort analysis; controls plan; views/daylight documentation", "Architect / MEP Engineer", strategy="Provide adaptable, comfortable spaces with effective occupant control."),
    Credit("EQc3", "Indoor Environmental Quality", "Accessibility and Inclusion", 2, "Quality of Life", "Accessibility audit; inclusive design drawings; user journey narrative", "Architect / Accessibility Consultant", strategy="Go beyond minimum code to support diverse physical and sensory needs."),
    Credit("EQc4", "Indoor Environmental Quality", "Resilient Spaces", 2, "Quality of Life", "Passive survivability analysis; critical space plans; outage scenarios", "Architect / Resilience Lead", strategy="Maintain safe, habitable conditions during disruptive events."),
    Credit("EQc5", "Indoor Environmental Quality", "Air Quality Testing and Monitoring", 2, "Quality of Life", "Flush-out/testing report; monitor plan; sensor schedule and locations", "IAQ Consultant / Mechanical Engineer", strategy="Verify post-construction air quality and continuously monitor priority pollutants."),
    Credit("EQc6", "Indoor Environmental Quality", "Daylight and Lighting Quality", 2, "Quality of Life", "Daylight simulation; lighting calculations; reflected ceiling plans", "Lighting Designer / Architect", strategy="Deliver useful daylight and high-quality electric lighting without glare."),
    Credit("EQc7", "Indoor Environmental Quality", "Acoustic Performance", 1, "Quality of Life", "Acoustic criteria; calculations; partition and equipment details", "Acoustic Consultant", strategy="Control background noise, isolation, reverberation, and speech privacy."),
    Credit("INc1", "Innovation", "Innovation", 5, "Quality of Life", "Innovation proposal; measurable performance evidence; team narrative", "LEED Consultant / Discipline Lead", strategy="Pursue verified outcomes not already rewarded by the rating system."),
    Credit("INc2", "Innovation", "LEED Accredited Professional", 1, "Quality of Life", "LEED AP credential and project role confirmation", "LEED Consultant", strategy="Engage a LEED AP with the appropriate specialty."),
    Credit("PPc1", "Regional / Project Priority", "Project Priority Strategies", 4, "Ecological Conservation", "Priority credit forms and location/context evidence", "LEED Consultant / Discipline Lead", strategy="Select priority credits published for the project's geography and context."),
)


def project_family(project_type: str) -> str:
    """Return the broad rating-system family for applicability checks."""

    return "ID+C" if project_type.startswith("ID+C") else "BD+C"


def is_applicable(applicability: tuple[str, ...], project_type: str) -> bool:
    """Match exact project types first, then broad BD+C/ID+C families."""

    return project_type in applicability or project_family(project_type) in applicability


def credits_for(project_type: str) -> tuple[Credit, ...]:
    return tuple(c for c in CREDITS if is_applicable(c.applicability, project_type))


def prerequisites_for(project_type: str) -> tuple[Prerequisite, ...]:
    return tuple(p for p in PREREQUISITES if is_applicable(p.applicability, project_type))
