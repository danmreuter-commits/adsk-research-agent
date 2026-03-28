import logging, time
from datetime import datetime, timedelta
import anthropic, config
from data.competitors import COMPETITOR_DOMAIN_KEYWORDS, DIRECT_COMPETITOR_NAMES, INDIRECT_COMPETITOR_NAMES

logger = logging.getLogger(__name__)

_SEARCH_SYSTEM = """\
You are a competitive intelligence analyst for Autodesk (ADSK), \
the world's leading design and make software company (AutoCAD, Revit, Fusion 360, BIM, construction cloud).

DIRECT competitors: Bentley Systems, Trimble (SketchUp, Tekla), Dassault Systemes (SOLIDWORKS, CATIA), \
PTC (Creo), Siemens PLM (NX), Nemetschek (Vectorworks, ArchiCAD, Bluebeam), Procore, Hexagon/BricsCAD.

INDIRECT competitors: Alice Technologies, Buildots, OpenSpace, TestFit, \
Maket.ai, Nvidia Omniverse, Speckle, AI generative design startups.

For each finding output one line:
FINDING|||[Company]|||[investment|product|metrics|partnership|platform_shift|vc_signal]|||[HIGH|MEDIUM]|||[VC firm or N/A]|||[One sentence description]|||[Source URL]

HIGH: direct competitor raises funding/launches AI design product/major enterprise win;
large AEC/manufacturing firm migrating from AutoCAD/Revit; AI-native generative design tool gaining traction.
MEDIUM: AEC/CAD/construction software raises Series B+; major architecture firm announces competitor;
VC thesis on AEC technology or construction software disruption.
Skip LOW. When done: BLOCK_COMPLETE
"""

def _date_range():
    today = datetime.now()
    return f"{(today - timedelta(days=7)).strftime('%B %d')}-{today.strftime('%B %d, %Y')}"

_SEARCH_BLOCKS = [
    {"name": "direct_competitors", "prompt_template": "Search for news from the past 7 days ({date_range}) about Autodesk direct competitors:\n- Bentley Systems (BSY): product launches, earnings, AEC customer wins, M&A\n- Trimble (TRMB): SketchUp, Tekla, Trimble Connect product news, construction tech\n- Dassault Systemes: SOLIDWORKS, CATIA, 3DEXPERIENCE product news, manufacturing wins\n- PTC (PTC): Creo, Windchill product news, manufacturing customer announcements\n- Procore (PCOR): product updates, earnings, construction management news\n- Nemetschek: Allplan, ArchiCAD, Vectorworks, Bluebeam product news\n- Hexagon / BricsCAD: AutoCAD alternative product news, customer wins\nOutput all HIGH and MEDIUM FINDING||| lines, then: BLOCK_COMPLETE"},
    {"name": "ai_design_and_vc", "prompt_template": "Search for news from the past 7 days ({date_range}) about:\nPART A - AI-native design, construction, and engineering technology:\n- Alice Technologies: construction scheduling AI, funding, customer news\n- Buildots: AI construction monitoring, funding, enterprise wins\n- OpenSpace: 360 construction documentation AI, funding, customer news\n- TestFit: automated building design, funding, new features\n- Maket.ai OR Archistar: AI architectural design, funding news\n- Nvidia Omniverse: AEC or manufacturing industry adoption news\n- AI generative design: new CAD OR BIM OR architecture tool funding 2026\nPART B - VC investments in AEC and manufacturing technology:\n- Search: Andreessen Horowitz OR Sequoia AEC technology OR construction software 2026\n- Search: Insight Partners OR General Catalyst CAD OR engineering software investment 2026\n- Search: Bessemer OR Index Ventures construction technology startup 2026\n- Search: Fifth Wall OR Congruent AEC OR construction tech investment 2026\nOutput all HIGH and MEDIUM FINDING||| lines, then: BLOCK_COMPLETE"},
    {"name": "market_signals", "prompt_template": "Search for news from the past 7 days ({date_range}) about broader AEC design and construction technology market signals:\n- CAD OR BIM software Series B OR C OR D 2026\n- construction technology OR AEC software funding 2026\n- architecture firm replaced OR migrated from AutoCAD OR Revit 2026\n- generative design OR AI-native CAD platform raised funding {month_year}\n- Autodesk competitor announcement {month_year}\n- VC blog AEC technology OR construction software investment thesis 2026\nAlso: Speckle AEC platform, VIKTOR engineering apps, SketchUp Trimble updates,\nRhino news, Alice Technologies construction AI, Buildots construction monitoring funding.\nOutput all HIGH and MEDIUM FINDING||| lines, then: BLOCK_COMPLETE"},
]

def _parse_findings(text):
    findings = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("FINDING|||"):
            continue
        parts = line.split("|||")
        if len(parts) < 7:
            continue
        findings.append({"company": parts[1].strip(), "type": parts[2].strip().lower(), "relevance": parts[3].strip().upper(), "vc_firm": parts[4].strip(), "description": parts[5].strip(), "source": parts[6].strip(), "found_at": datetime.now().isoformat()})
    return findings

def _run_block(client, block):
    user_prompt = block["prompt_template"].format(date_range=_date_range(), month_year=datetime.now().strftime("%B %Y"))
    messages = [{"role": "user", "content": user_prompt}]
    accumulated = ""
    continuations = 0
    while continuations <= 3:
        response = client.messages.create(model="claude-sonnet-4-6", max_tokens=1500, system=_SEARCH_SYSTEM, tools=[{"type": "web_search_20260209", "name": "web_search"}], messages=messages)
        for cb in response.content:
            if hasattr(cb, "text"):
                accumulated += cb.text + "\n"
        if response.stop_reason == "end_turn":
            break
        elif response.stop_reason == "pause_turn":
            messages.append({"role": "assistant", "content": response.content})
            continuations += 1
        else:
            break
    return _parse_findings(accumulated)

BLOCK_PAUSE_SECONDS = 15

def run_research():
    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY, timeout=180.0)
    all_findings = []
    for i, block in enumerate(_SEARCH_BLOCKS):
        logger.info("Search block %d/%d - %s", i + 1, len(_SEARCH_BLOCKS), block["name"])
        try:
            findings = _run_block(client, block)
            all_findings.extend(findings)
            logger.info("  -> %d finding(s)", len(findings))
        except anthropic.RateLimitError:
            logger.warning("Rate limit on '%s' - waiting 60s", block["name"])
            time.sleep(60)
        except Exception as exc:
            logger.error("Block '%s' failed: %s", block["name"], exc)
        if i < len(_SEARCH_BLOCKS) - 1:
            time.sleep(BLOCK_PAUSE_SECONDS)
    seen = set()
    deduped = []
    for f in all_findings:
        key = f"{f['company'].lower()}|{f['type'].lower()}"
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    deduped.sort(key=lambda f: (0 if f.get("relevance") == "HIGH" else 1))
    logger.info("Research complete - %d unique findings", len(deduped))
    return deduped
