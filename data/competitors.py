"""Autodesk competitive landscape knowledge base."""

DIRECT_COMPETITOR_NAMES = [
    "bentley systems", "trimble", "dassault systemes", "solidworks", "catia",
    "ptc", "creo", "siemens plm", "nemetschek", "procore", "hexagon", "bricsys",
    "bluebeam", "graphisoft", "archicad", "vectorworks",
]
INDIRECT_COMPETITOR_NAMES = [
    "speckle", "alice technologies", "buildots", "openspace", "testfit",
    "maket.ai", "archistar", "viktor", "nvidia omniverse", "aconex",
]
COMPETITOR_DOMAIN_KEYWORDS = [
    "BIM software", "building information modeling", "CAD software", "CAD/CAM",
    "construction management software", "AEC software", "architecture software",
    "civil engineering software", "structural engineering software",
    "3D modeling software", "PLM software", "product lifecycle management",
    "construction project management", "generative design", "digital twin",
    "construction technology", "infrastructure software", "mechanical CAD",
    "engineering simulation", "computational design",
]
AUTODESK_CONTEXT = """
ABOUT AUTODESK (ADSK):
Products: AutoCAD, Revit, Civil 3D, Fusion 360, Maya, 3ds Max, Inventor, Navisworks,
BIM Collaborate Pro, Forma, Autodesk Construction Cloud (ACC).
Business model: SaaS subscriptions per-user/per-product.
Market position: dominant in AEC design; strong in manufacturing CAD; leading in M&E animation.

DIRECT COMPETITORS: Bentley Systems, Trimble (SketchUp, Tekla), Dassault Systemes (SOLIDWORKS, CATIA),
PTC (Creo), Siemens PLM (NX), Nemetschek (Vectorworks, ArchiCAD, Bluebeam), Procore, Hexagon/BricsCAD.
INDIRECT: Alice Technologies, Buildots, OpenSpace, TestFit, Maket.ai, Nvidia Omniverse, Speckle.
EMERGING THREATS: AI-native generative design tools, Nvidia Omniverse for simulation,
AI-native CAD tools targeting Fusion 360 and AutoCAD users.

HIGH relevance: direct competitor raises funding/launches AI design product/major enterprise win;
large AEC/manufacturing firm migrating from AutoCAD/Revit; AI-native generative design tool gaining traction.
MEDIUM relevance: AEC/CAD/construction software raises Series B+; major architecture firm announces competitor;
VC thesis on AEC technology or construction software disruption.
LOW (exclude): consumer 3D printing/hobbyist tools, pre-seed under $5M, healthcare unrelated to design.
"""
