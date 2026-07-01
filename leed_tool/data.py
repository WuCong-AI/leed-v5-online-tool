"""Curated multi-version LEED planning datasets.

The rule packs are consultant planning models calibrated to official scorecard
structures and supplied GBCI review examples. Teams must still reconcile them
with the live rating system, credit library, Arc forms, and registration-date addenda.
"""

from __future__ import annotations

from .models import Credit, Prerequisite

RATING_VERSIONS = ("LEED v4", "LEED v4.1", "LEED v5")

PROJECT_TYPES = (
    "BD+C: New Construction",
    "BD+C: Core & Shell",
    "ID+C: Commercial Interiors",
    "O+M: Existing Buildings",
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


_CATEGORY_META = {
    "Integrative Process": ("Quality of Life", "LEED Consultant / Owner"),
    "Location & Transportation": ("Decarbonization", "Transport Planner / Architect"),
    "Sustainable Sites": ("Ecological Conservation", "Civil Engineer / Landscape Architect"),
    "Water Efficiency": ("Ecological Conservation", "Plumbing Engineer / Landscape Architect"),
    "Energy & Atmosphere": ("Decarbonization", "Energy Modeler / MEP Engineer"),
    "Materials & Resources": ("Decarbonization", "Architect / Contractor"),
    "Indoor Environmental Quality": ("Quality of Life", "Architect / MEP Engineer"),
    "Innovation": ("Quality of Life", "LEED Consultant"),
    "Regional / Project Priority": ("Ecological Conservation", "LEED Consultant"),
}


def _credit(code: str, category: str, name: str, points: int) -> Credit:
    pillar, owner = _CATEGORY_META[category]
    return Credit(
        code, category, name, points, pillar,
        f"Applicable calculator/form; narrative; drawings or schedules; source records for {name}",
        owner,
        strategy=f"Document the selected compliance path and reconcile every reported value for {name}.",
    )


def _prereq(code: str, category: str, name: str) -> Prerequisite:
    pillar, _ = _CATEGORY_META[category]
    return Prerequisite(
        code, category, name, pillar,
        summary=f"Demonstrate the mandatory {name} requirement using the selected version's form, calculations, and coordinated design/operations evidence.",
    )


V4_BDC_CREDITS = tuple(_credit(*row) for row in (
    ("IPc1", "Integrative Process", "Integrative Process", 1),
    ("LTc1", "Location & Transportation", "Sensitive Land Protection", 2),
    ("LTc2", "Location & Transportation", "High Priority Site", 3),
    ("LTc3", "Location & Transportation", "Surrounding Density and Diverse Uses", 6),
    ("LTc4", "Location & Transportation", "Access to Quality Transit", 6),
    ("LTc5", "Location & Transportation", "Bicycle Facilities", 1),
    ("LTc6", "Location & Transportation", "Reduced Parking Footprint", 1),
    ("LTc7", "Location & Transportation", "Green Vehicles", 1),
    ("SSc1", "Sustainable Sites", "Site Assessment", 1),
    ("SSc2", "Sustainable Sites", "Site Development - Protect or Restore Habitat", 2),
    ("SSc3", "Sustainable Sites", "Open Space", 1),
    ("SSc4", "Sustainable Sites", "Rainwater Management", 3),
    ("SSc5", "Sustainable Sites", "Heat Island Reduction", 2),
    ("SSc6", "Sustainable Sites", "Light Pollution Reduction", 1),
    ("SSc7", "Sustainable Sites", "Tenant Design and Construction Guidelines", 1),
    ("WEc1", "Water Efficiency", "Cooling Tower Water Use", 2),
    ("WEc2", "Water Efficiency", "Water Metering", 1),
    ("WEc3", "Water Efficiency", "Outdoor Water Use Reduction", 2),
    ("WEc4", "Water Efficiency", "Indoor Water Use Reduction", 6),
    ("EAc1", "Energy & Atmosphere", "Enhanced Commissioning", 6),
    ("EAc2", "Energy & Atmosphere", "Advanced Energy Metering", 1),
    ("EAc3", "Energy & Atmosphere", "Demand Response", 2),
    ("EAc4", "Energy & Atmosphere", "Renewable Energy Production", 3),
    ("EAc5", "Energy & Atmosphere", "Enhanced Refrigerant Management", 1),
    ("EAc6", "Energy & Atmosphere", "Green Power and Carbon Offsets", 2),
    ("EAc7", "Energy & Atmosphere", "Optimize Energy Performance", 18),
    ("MRc1", "Materials & Resources", "Building Life-Cycle Impact Reduction", 6),
    ("MRc2", "Materials & Resources", "Environmental Product Declarations", 2),
    ("MRc3", "Materials & Resources", "Sourcing of Raw Materials", 2),
    ("MRc4", "Materials & Resources", "Material Ingredients", 2),
    ("MRc5", "Materials & Resources", "Construction and Demolition Waste Management", 2),
    ("EQc1", "Indoor Environmental Quality", "Enhanced Indoor Air Quality Strategies", 2),
    ("EQc2", "Indoor Environmental Quality", "Low-Emitting Materials", 3),
    ("EQc3", "Indoor Environmental Quality", "Construction Indoor Air Quality Management Plan", 1),
    ("EQc4", "Indoor Environmental Quality", "Daylight", 3),
    ("EQc5", "Indoor Environmental Quality", "Quality Views", 1),
    ("INc1", "Innovation", "Innovation", 5),
    ("INc2", "Innovation", "LEED Accredited Professional", 1),
    ("RPc1", "Regional / Project Priority", "Regional Priority Credits", 4),
))

V41_IDC_CREDITS = tuple(_credit(*row) for row in (
    ("IPc1", "Integrative Process", "Integrative Process", 2),
    ("LTc1", "Location & Transportation", "Surrounding Density and Diverse Uses", 8),
    ("LTc2", "Location & Transportation", "Access to Quality Transit", 7),
    ("LTc3", "Location & Transportation", "Bicycle Facilities", 1),
    ("LTc4", "Location & Transportation", "Reduced Parking Footprint", 2),
    ("WEc1", "Water Efficiency", "Indoor Water Use Reduction", 12),
    ("EAc1", "Energy & Atmosphere", "Optimize Energy Performance", 24),
    ("EAc2", "Energy & Atmosphere", "Enhanced Commissioning", 5),
    ("EAc3", "Energy & Atmosphere", "Advanced Energy Metering", 2),
    ("EAc4", "Energy & Atmosphere", "Renewable Energy", 6),
    ("EAc5", "Energy & Atmosphere", "Enhanced Refrigerant Management", 1),
    ("MRc1", "Materials & Resources", "Interiors Life-Cycle Impact Reduction", 5),
    ("MRc2", "Materials & Resources", "Environmental Product Declarations", 2),
    ("MRc3", "Materials & Resources", "Sourcing of Raw Materials", 2),
    ("MRc4", "Materials & Resources", "Material Ingredients", 2),
    ("MRc5", "Materials & Resources", "Construction and Demolition Waste Management", 2),
    ("MRc6", "Materials & Resources", "Long-Term Commitment", 1),
    ("EQc1", "Indoor Environmental Quality", "Enhanced Indoor Air Quality Strategies", 2),
    ("EQc2", "Indoor Environmental Quality", "Low-Emitting Materials", 3),
    ("EQc3", "Indoor Environmental Quality", "Construction Indoor Air Quality Management Plan", 1),
    ("EQc4", "Indoor Environmental Quality", "Indoor Air Quality Assessment", 2),
    ("EQc5", "Indoor Environmental Quality", "Thermal Comfort", 1),
    ("EQc6", "Indoor Environmental Quality", "Interior Lighting", 2),
    ("EQc7", "Indoor Environmental Quality", "Daylight", 3),
    ("EQc8", "Indoor Environmental Quality", "Quality Views", 1),
    ("EQc9", "Indoor Environmental Quality", "Acoustic Performance", 2),
    ("INc1", "Innovation", "Innovation", 5),
    ("INc2", "Innovation", "LEED Accredited Professional", 1),
    ("RPc1", "Regional / Project Priority", "Regional Priority Credits", 4),
))

V4_OM_CREDITS = tuple(_credit(*row) for row in (
    ("LTc1", "Location & Transportation", "Alternative Transportation Performance", 15),
    ("SSc1", "Sustainable Sites", "Site Management", 2), ("SSc2", "Sustainable Sites", "Rainwater Management", 3),
    ("SSc3", "Sustainable Sites", "Heat Island Reduction", 2), ("SSc4", "Sustainable Sites", "Light Pollution Reduction", 1),
    ("SSc5", "Sustainable Sites", "Site Improvement Plan", 2),
    ("WEc1", "Water Efficiency", "Indoor Water Use Reduction", 5), ("WEc2", "Water Efficiency", "Cooling Tower Water Use", 3),
    ("WEc3", "Water Efficiency", "Water Metering", 2), ("WEc4", "Water Efficiency", "Outdoor Water Use Reduction", 2),
    ("EAc1", "Energy & Atmosphere", "Existing Building Commissioning", 6), ("EAc2", "Energy & Atmosphere", "Optimize Energy Performance", 20),
    ("EAc3", "Energy & Atmosphere", "Advanced Energy Metering", 2), ("EAc4", "Energy & Atmosphere", "Demand Response", 3),
    ("EAc5", "Energy & Atmosphere", "Renewable Energy", 5), ("EAc6", "Energy & Atmosphere", "Enhanced Refrigerant Management", 1),
    ("EAc7", "Energy & Atmosphere", "Green Power and Carbon Offsets", 1),
    ("MRc1", "Materials & Resources", "Purchasing", 5), ("MRc2", "Materials & Resources", "Facility Maintenance and Renovation", 2),
    ("MRc3", "Materials & Resources", "Solid Waste Management", 1),
    ("EQc1", "Indoor Environmental Quality", "Indoor Air Quality Management Program", 2), ("EQc2", "Indoor Environmental Quality", "Green Cleaning", 4),
    ("EQc3", "Indoor Environmental Quality", "Integrated Pest Management", 2), ("EQc4", "Indoor Environmental Quality", "Occupant Comfort", 2),
    ("EQc5", "Indoor Environmental Quality", "Indoor Air Quality Assessment", 2), ("EQc6", "Indoor Environmental Quality", "Daylight and Quality Views", 2),
    ("EQc7", "Indoor Environmental Quality", "Facility Alterations", 2), ("EQc8", "Indoor Environmental Quality", "Enhanced Indoor Air Quality", 1),
    ("INc1", "Innovation", "Innovation", 5), ("INc2", "Innovation", "LEED Accredited Professional", 1),
    ("RPc1", "Regional / Project Priority", "Regional Priority Credits", 4),
))

V41_OM_CREDITS = tuple(_credit(*row) for row in (
    ("LTc1", "Location & Transportation", "Transportation Performance", 14),
    ("WEc1", "Water Efficiency", "Water Performance", 15),
    ("EAc1", "Energy & Atmosphere", "Energy Performance", 33),
    ("EAc2", "Energy & Atmosphere", "Enhanced Refrigerant Management", 1),
    ("MRc1", "Materials & Resources", "Purchasing", 4), ("MRc2", "Materials & Resources", "Waste Performance", 8),
    ("EQc1", "Indoor Environmental Quality", "Indoor Environmental Quality Performance", 20),
    ("EQc2", "Indoor Environmental Quality", "Green Cleaning", 3), ("EQc3", "Indoor Environmental Quality", "Integrated Pest Management", 1),
    ("INc1", "Innovation", "Innovation", 1),
))

V5_IDC_CREDITS = tuple(_credit(*row) for row in (
    ("IPc1", "Integrative Process", "Integrative Design Process", 1),
    ("LTc1", "Location & Transportation", "Connected and Equitable Location", 6), ("LTc2", "Location & Transportation", "Transportation Demand Management", 5),
    ("LTc3", "Location & Transportation", "Electric Vehicles and Low-Carbon Mobility", 4),
    ("WEc1", "Water Efficiency", "Water Metering and Leak Detection", 1), ("WEc2", "Water Efficiency", "Enhanced Water Efficiency", 8),
    ("EAc1", "Energy & Atmosphere", "Electrification", 5), ("EAc2", "Energy & Atmosphere", "Reduce Peak Thermal Loads", 5),
    ("EAc3", "Energy & Atmosphere", "Enhanced Energy Efficiency", 10), ("EAc4", "Energy & Atmosphere", "Renewable Energy", 5),
    ("EAc5", "Energy & Atmosphere", "Enhanced Commissioning", 4), ("EAc6", "Energy & Atmosphere", "Grid Interactive", 2),
    ("EAc7", "Energy & Atmosphere", "Enhanced Refrigerant Management", 2), ("EAc8", "Energy & Atmosphere", "Advanced Energy Metering", 2),
    ("MRc1", "Materials & Resources", "Interiors and Materials Reuse", 5), ("MRc2", "Materials & Resources", "Reduce Embodied Carbon", 6),
    ("MRc3", "Materials & Resources", "Low-Emitting Materials", 3), ("MRc4", "Materials & Resources", "Building Product Selection and Procurement", 5),
    ("MRc5", "Materials & Resources", "Construction and Demolition Waste Diversion", 2), ("MRc6", "Materials & Resources", "Circular Procurement", 4),
    ("EQc1", "Indoor Environmental Quality", "Enhanced Air Quality", 2), ("EQc2", "Indoor Environmental Quality", "Occupant Experience", 7),
    ("EQc3", "Indoor Environmental Quality", "Accessibility and Inclusion", 1), ("EQc4", "Indoor Environmental Quality", "Resilient Spaces", 2),
    ("EQc5", "Indoor Environmental Quality", "Air Quality Testing and Monitoring", 2), ("EQc6", "Indoor Environmental Quality", "Acoustic Performance", 1),
    ("PPc1", "Regional / Project Priority", "Project Priorities", 9), ("PPc2", "Regional / Project Priority", "LEED Accredited Professional", 1),
))

V5_OM_CREDITS = tuple(_credit(*row) for row in (
    ("IPc1", "Integrative Process", "Resilience, Occupant Needs, and Decarbonization Planning", 5),
    ("LTc1", "Location & Transportation", "Transportation Performance", 10),
    ("WEc1", "Water Efficiency", "Water Performance and Leak Detection", 15),
    ("EAc1", "Energy & Atmosphere", "Operational Carbon Performance", 25), ("EAc2", "Energy & Atmosphere", "Energy Efficiency and Grid Interaction", 8),
    ("EAc3", "Energy & Atmosphere", "Enhanced Refrigerant Management", 2),
    ("MRc1", "Materials & Resources", "Waste Performance and Circular Purchasing", 10), ("MRc2", "Materials & Resources", "Embodied Carbon in Alterations", 5),
    ("EQc1", "Indoor Environmental Quality", "Indoor Environmental Quality Performance", 12),
    ("EQc2", "Indoor Environmental Quality", "Green Cleaning and Integrated Pest Management", 4),
    ("EQc3", "Indoor Environmental Quality", "Occupant Experience and Resilient Operations", 4),
    ("PPc1", "Regional / Project Priority", "Project Priorities", 9), ("PPc2", "Regional / Project Priority", "LEED Accredited Professional", 1),
))

V4_BDC_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("SSp1", "Sustainable Sites", "Construction Activity Pollution Prevention"),
    ("WEp1", "Water Efficiency", "Outdoor Water Use Reduction"), ("WEp2", "Water Efficiency", "Indoor Water Use Reduction"),
    ("WEp3", "Water Efficiency", "Building-Level Water Metering"), ("EAp1", "Energy & Atmosphere", "Fundamental Commissioning and Verification"),
    ("EAp2", "Energy & Atmosphere", "Minimum Energy Performance"), ("EAp3", "Energy & Atmosphere", "Building-Level Energy Metering"),
    ("EAp4", "Energy & Atmosphere", "Fundamental Refrigerant Management"), ("MRp1", "Materials & Resources", "Storage and Collection of Recyclables"),
    ("MRp2", "Materials & Resources", "Construction and Demolition Waste Management Planning"),
    ("EQp1", "Indoor Environmental Quality", "Minimum Indoor Air Quality Performance"),
    ("EQp2", "Indoor Environmental Quality", "Environmental Tobacco Smoke Control"),
))

V41_IDC_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("WEp1", "Water Efficiency", "Indoor Water Use Reduction"), ("EAp1", "Energy & Atmosphere", "Fundamental Commissioning and Verification"),
    ("EAp2", "Energy & Atmosphere", "Minimum Energy Performance"), ("EAp3", "Energy & Atmosphere", "Fundamental Refrigerant Management"),
    ("MRp1", "Materials & Resources", "Storage and Collection of Recyclables"), ("MRp2", "Materials & Resources", "Construction and Demolition Waste Management Planning"),
    ("EQp1", "Indoor Environmental Quality", "Minimum Indoor Air Quality Performance"),
    ("EQp2", "Indoor Environmental Quality", "Environmental Tobacco Smoke Control"),
))

V4_OM_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("SSp1", "Sustainable Sites", "Site Management Policy"), ("WEp1", "Water Efficiency", "Indoor Water Use Reduction"),
    ("WEp2", "Water Efficiency", "Building-Level Water Metering"), ("EAp1", "Energy & Atmosphere", "Energy Efficiency Best Management Practices"),
    ("EAp2", "Energy & Atmosphere", "Minimum Energy Performance"), ("EAp3", "Energy & Atmosphere", "Building-Level Energy Metering"),
    ("EAp4", "Energy & Atmosphere", "Fundamental Refrigerant Management"), ("MRp1", "Materials & Resources", "Ongoing Purchasing and Waste Policies"),
    ("EQp1", "Indoor Environmental Quality", "Minimum Indoor Air Quality Performance"), ("EQp2", "Indoor Environmental Quality", "Environmental Tobacco Smoke Control"),
    ("EQp3", "Indoor Environmental Quality", "Green Cleaning Policy"),
))

V41_OM_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("LTp1", "Location & Transportation", "Transportation Performance"), ("WEp1", "Water Efficiency", "Water Performance"),
    ("EAp1", "Energy & Atmosphere", "Energy Efficiency Best Management Practices"), ("EAp2", "Energy & Atmosphere", "Fundamental Refrigerant Management"),
    ("EAp3", "Energy & Atmosphere", "Energy Performance"), ("MRp1", "Materials & Resources", "Purchasing Policy"),
    ("MRp2", "Materials & Resources", "Facility Maintenance and Renovations Policy"), ("MRp3", "Materials & Resources", "Waste Performance"),
    ("EQp1", "Indoor Environmental Quality", "Minimum Indoor Air Quality"), ("EQp2", "Indoor Environmental Quality", "Environmental Tobacco Smoke Control"),
    ("EQp3", "Indoor Environmental Quality", "Green Cleaning Policy"), ("EQp4", "Indoor Environmental Quality", "Indoor Environmental Quality Performance"),
))

V5_IDC_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("IPp1", "Integrative Process", "Climate Resilience Assessment"), ("IPp2", "Integrative Process", "Human Impact Assessment"),
    ("IPp3", "Integrative Process", "Carbon Assessment"), ("WEp1", "Water Efficiency", "Minimum Water Efficiency"),
    ("EAp1", "Energy & Atmosphere", "Operational Carbon Projection and Decarbonization Plan"), ("EAp2", "Energy & Atmosphere", "Minimum Energy Efficiency"),
    ("EAp3", "Energy & Atmosphere", "Fundamental Commissioning"), ("EAp4", "Energy & Atmosphere", "Energy Metering and Reporting"),
    ("EAp5", "Energy & Atmosphere", "Fundamental Refrigerant Management"), ("MRp1", "Materials & Resources", "Planning for Zero Waste Operations"),
    ("MRp2", "Materials & Resources", "Quantify and Assess Embodied Carbon"), ("EQp1", "Indoor Environmental Quality", "Construction Management"),
    ("EQp2", "Indoor Environmental Quality", "Fundamental Air Quality"), ("EQp3", "Indoor Environmental Quality", "No Smoking or Vehicle Idling"),
))

V5_OM_PREREQUISITES = tuple(_prereq(*row) for row in (
    ("IPp1", "Integrative Process", "Climate Resilience Assessment"), ("IPp2", "Integrative Process", "Occupant Needs Assessment"),
    ("IPp3", "Integrative Process", "Operational Decarbonization Plan"), ("WEp1", "Water Efficiency", "Water Metering and Performance Data"),
    ("EAp1", "Energy & Atmosphere", "Energy and Operational Carbon Performance Data"), ("EAp2", "Energy & Atmosphere", "Fundamental Refrigerant Management"),
    ("MRp1", "Materials & Resources", "Waste and Purchasing Policies"), ("EQp1", "Indoor Environmental Quality", "Minimum Indoor Air Quality"),
    ("EQp2", "Indoor Environmental Quality", "No Smoking"), ("EQp3", "Indoor Environmental Quality", "Green Cleaning Policy"),
))

RATING_SYSTEM_SOURCES = {
    "LEED v4": "https://www.usgbc.org/leed/v4",
    "LEED v4.1": "https://www.usgbc.org/leed/v41",
    "LEED v5": "https://www.usgbc.org/leed/v5",
}


def project_family(project_type: str) -> str:
    """Return the broad rating-system family for applicability checks."""

    if project_type.startswith("ID+C"):
        return "ID+C"
    if project_type.startswith("O+M"):
        return "O+M"
    return "BD+C"


def is_applicable(applicability: tuple[str, ...], project_type: str) -> bool:
    """Match exact project types first, then broad BD+C/ID+C families."""

    return project_type in applicability or project_family(project_type) in applicability


def credits_for(project_type: str, rating_version: str = "LEED v5") -> tuple[Credit, ...]:
    family = project_family(project_type)
    if rating_version == "LEED v5":
        if family == "ID+C":
            return V5_IDC_CREDITS
        if family == "O+M":
            return V5_OM_CREDITS
        return tuple(c for c in CREDITS if is_applicable(c.applicability, project_type))
    if family == "ID+C":
        return V41_IDC_CREDITS
    if family == "O+M":
        return V41_OM_CREDITS if rating_version == "LEED v4.1" else V4_OM_CREDITS
    return V4_BDC_CREDITS


def prerequisites_for(project_type: str, rating_version: str = "LEED v5") -> tuple[Prerequisite, ...]:
    family = project_family(project_type)
    if rating_version == "LEED v5":
        if family == "ID+C":
            return V5_IDC_PREREQUISITES
        if family == "O+M":
            return V5_OM_PREREQUISITES
        return tuple(p for p in PREREQUISITES if is_applicable(p.applicability, project_type))
    if family == "ID+C":
        return V41_IDC_PREREQUISITES
    if family == "O+M":
        return V41_OM_PREREQUISITES if rating_version == "LEED v4.1" else V4_OM_PREREQUISITES
    return V4_BDC_PREREQUISITES


def scorecard_total(project_type: str, rating_version: str = "LEED v5") -> int:
    return sum(credit.points for credit in credits_for(project_type, rating_version))
