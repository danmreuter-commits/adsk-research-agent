"""Guidewire competitive landscape knowledge base used to power research prompts."""

GUIDEWIRE_CONTEXT = """
ABOUT GUIDEWIRE (GWRE):
Guidewire Software is the system of record for Property & Casualty (P&C) insurance companies globally.

CORE PRODUCTS:
- PolicyCenter: Policy administration system — underwriting, policy lifecycle management, rating
- BillingCenter: Billing management — premium collection, payment processing, disbursements
- ClaimCenter: Claims management — FNOL, adjudication, payments, litigation management
- InsuranceSuite: Combined platform (PolicyCenter + BillingCenter + ClaimCenter)
- Guidewire Cloud: Cloud-hosted SaaS version of InsuranceSuite
- InsuranceNow: Lightweight SaaS for smaller/regional carriers
- Guidewire Marketplace: Ecosystem of 200+ partner apps
- DataHub / InfoCenter: Analytics, data warehouse, reporting

TARGET CUSTOMERS: Tier 1, 2, and 3 P&C insurers globally — auto, homeowners, commercial, specialty lines
BUSINESS MODEL: Annual cloud SaaS subscriptions + professional services
MARKET POSITION: #1 core systems vendor for P&C insurance globally; ~500 carrier customers

---

DIRECT COMPETITORS — core system replacements (highest priority):
- Duck Creek Technologies: Policy, billing, claims suite; owned by Vista Equity Partners
- Majesco: Cloud-native insurance platform (Nasdaq: MJCO); CloudInsurer product
- Sapiens International: P&C and L&H insurance software globally (Nasdaq: SPNS)
- Insurity: Policy, billing, claims for specialty and personal lines; owned by GI Partners
- OneShield Enterprise: Mid-market P&C software
- Applied Systems: Commercial lines management software
- EIS Group: Modern core insurance platform targeting greenfield carriers
- Socotra: Cloud-native, API-first policy administration platform; backed by TCV
- Instanda: No-code policy administration; backed by MS&AD Ventures
- FINEOS: Claims and benefits management for L&H/Workers Comp (ASX: FCL)
- Unqork: No-code enterprise platform used by carriers for policy/claims
- Appian: Low-code platform used in insurance workflows (Nasdaq: APPN)
- Salesforce Financial Services Cloud: CRM expanding into insurance workflows
- ServiceNow: Workflow platform expanding into insurance operations

INDIRECT COMPETITORS — AI/ML point solutions expanding into core system territory (medium priority):
- Shift Technology: AI-powered fraud detection and claims automation; Series D (~$220M raised)
- Gradient AI: ML for underwriting pricing and claims severity prediction
- Snapsheet: Digital claims management, virtual appraisals; backed by Insight Partners
- Five Sigma: AI-native claims management platform
- CLARA Analytics: AI for claims management (litigation, medical)
- Tractable: AI for accident and disaster recovery claims
- Bdeo: Visual intelligence for claims (Europe/LatAm)
- Betterview: Property intelligence/aerial imagery for underwriting
- Cape Analytics: AI property analytics for underwriting
- Verisk (Nasdaq: VRSK): Data analytics for insurance; Property Estimating Solutions
- LexisNexis Risk Solutions (RELX): Data and analytics for underwriting
- CCC Intelligent Solutions: Auto claims ecosystem (Nasdaq: CCCS)
- Mitchell International: Auto physical damage claims
- Solera / Audatex: Auto claims workflow

EMERGING THREAT — new carrier platforms bypassing Guidewire entirely (watch closely):
- Lemonade (NYSE: LMND): Tech-forward carrier; selling AI/tech platform to other insurers
- Kin Insurance: Home insurance tech platform; cloud-native stack
- Branch Insurance: Bundled auto/home with proprietary tech
- Openly: Home insurance MGA on modern platform
- Clearcover: Auto insurance on proprietary modern stack
- Wisk / Covie / other MGAs: Cloud-native platforms potentially replacing legacy core systems

---

WHAT MAKES A FINDING RELEVANT TO GUIDEWIRE:
HIGH relevance:
- Direct competitor raises funding, acquires company, or launches major product update
- New cloud-native P&C core system platform raises significant capital
- A carrier publicly announces switching FROM Guidewire to a competitor
- AI claims/policy company expands from point solution into full platform

MEDIUM relevance:
- Insurtech raises Series B+ from a top VC for claims/policy/billing tech
- Established carrier tech company announces new AI features competing with Guidewire modules
- Major VC publishes blog/research positioning insurtech as core system disruption
- New MGA/carrier startup chooses a modern alternative platform over Guidewire

LOW relevance (exclude):
- Pure consumer/D2C insurers (car insurance apps, pet insurance, etc.)
- Life/health/dental insurance technology (not P&C)
- Pure distribution/brokerage tech (comparative raters, agency management)
- Small pre-seed / seed rounds under $5M
- International markets with no Guidewire presence
"""

# Keywords and company names for relevance detection (used in prompts)
DIRECT_COMPETITOR_NAMES = [
    "duck creek", "majesco", "sapiens", "insurity", "oneshield", "applied systems",
    "eis group", "socotra", "instanda", "fineos", "unqork", "appian",
]

INDIRECT_COMPETITOR_NAMES = [
    "shift technology", "gradient ai", "snapsheet", "five sigma", "clara analytics",
    "tractable", "bdeo", "betterview", "cape analytics", "ccc intelligent",
    "mitchell international", "solera", "audatex",
]

COMPETITOR_DOMAIN_KEYWORDS = [
    "policy administration", "policy management", "claims management", "claims automation",
    "billing management", "insurance platform", "insurance core system", "insurance SaaS",
    "p&c insurance software", "property casualty software", "insurtech platform",
    "insurance modernization", "carrier technology", "core insurance", "underwriting platform",
    "FNOL", "first notice of loss", "claims adjudication", "insurance suite",
]
