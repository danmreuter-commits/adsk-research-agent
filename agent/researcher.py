"""
Research engine: uses Claude with the web_search tool to scan VC firm activity
and surface competitive intelligence relevant to Guidewire (GWRE).
"""

import logging
from datetime import datetime, timedelta

import anthropic

import config
from data.vc_firms import VC_FIRMS, INSURTECH_FOCUSED_VCS
from data.competitors import GUIDEWIRE_CONTEXT

logger = logging.getLogger(__name__)

# ── Prompt construction ───────────────────────────────────────────────────────

def _build_system_prompt() -> str:
    vc_list_lines = []
    for f in VC_FIRMS:
        label = " [INSURANCE/FINTECH FOCUS]" if f["insurtech_focus"] else ""
        blog = f"  blog: {f['blog']}" if f["blog"] else ""
        vc_list_lines.append(f"  - {f['name']} ({f['website']}){label}{blog}")
    vc_list = "\n".join(vc_list_lines)

    insurtech_vcs = ", ".join(INSURTECH_FOCUSED_VCS)

    return f"""You are a senior competitive intelligence analyst for Guidewire Software (GWRE), \
the #1 system-of-record software platform for Property & Casualty (P&C) insurance carriers.

{GUIDEWIRE_CONTEXT}

---

TOP 40 VC FIRMS YOU MUST MONITOR:
{vc_list}

Priority search targets (insurance/fintech focused):
{insurtech_vcs}

---

YOUR RESEARCH MANDATE:
Using web search, find all competitive intelligence from the PAST 7 DAYS. Specifically:

1. NEW INVESTMENTS — funding rounds by any of the 40 VC firms above in insurance tech/software
2. PRODUCT LAUNCHES — new products or major releases by Guidewire direct or indirect competitors
3. FINANCIAL METRICS — ARR, revenue, growth rates, or customer counts disclosed by competitors
4. PARTNERSHIPS & ACQUISITIONS — strategic moves by competitors (carrier wins, M&A, integrations)
5. VC SIGNALS — blog posts, LinkedIn or X/Twitter posts from VC partners about insurtech bets
6. PLATFORM SHIFTS — carriers or MGAs publicly choosing a modern alternative to Guidewire
7. AI EXPANSION — AI/ML companies announcing they are moving into core insurance system territory

For EACH finding you identify, output it on its own line in EXACTLY this pipe-delimited format:
FINDING|||[Company Name]|||[investment|product|metrics|partnership|platform_shift|vc_signal]|||[HIGH|MEDIUM]|||[VC firm name or N/A]|||[One-sentence description including key detail: dollar amount, product name, carrier name, etc.]|||[Source URL]

Only output HIGH and MEDIUM relevance findings (see relevance guide above).
Do NOT include LOW relevance findings.
Search broadly using multiple queries — be thorough, not superficial.
After all findings are listed, output exactly: RESEARCH_COMPLETE
"""


def _build_user_prompt() -> str:
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    date_range = f"{week_ago.strftime('%B %d')}–{today.strftime('%B %d, %Y')}"

    return f"""Search the internet for Guidewire (GWRE) competitive intelligence from the past 7 days \
({date_range}).

Run searches across ALL of the following areas — use multiple distinct queries:

SEARCH BLOCK 1 — Direct competitor news:
• "Duck Creek Technologies" news 2025 2026
• "Majesco" insurance platform announcement 2025 2026
• "Sapiens International" product news 2025 2026
• "Insurity" OR "OneShield" OR "EIS Group" insurance software news
• "Socotra" OR "Instanda" policy administration funding news

SEARCH BLOCK 2 — AI/insurtech funding:
• insurtech funding round 2026 Series B C D
• insurance software startup investment {today.strftime('%B %Y')}
• P&C insurance AI claims underwriting investment 2026

SEARCH BLOCK 3 — VC portfolio announcements:
• Anthemis OR "QED Investors" OR "Munich Re Ventures" portfolio insurance announcement
• "Insight Partners" OR "TCV" OR "General Catalyst" insurtech investment 2026
• "Nationwide Ventures" OR "XL Innovate" OR "Aquiline" insurance tech portfolio news

SEARCH BLOCK 4 — Competitive displacement:
• carrier "replaced Guidewire" OR "migrated from Guidewire" OR "alternative to Guidewire"
• "Shift Technology" OR "Gradient AI" OR "Snapsheet" OR "Five Sigma" news funding 2026
• "CLARA Analytics" OR "Tractable" OR "Betterview" insurance AI news 2026

SEARCH BLOCK 5 — VC partner signals:
• site:linkedin.com OR site:x.com insurance software investment VC 2026
• VC partner blog insurtech investment thesis 2026
• Guidewire competitor investment announcement {today.strftime('%B %Y')}

Search each block and compile all relevant findings in the FINDING||| format specified in your instructions.
"""


# ── Parsing ───────────────────────────────────────────────────────────────────

def _parse_findings(text: str) -> list[dict]:
    """Extract structured findings from Claude's pipe-delimited output."""
    findings = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("FINDING|||"):
            continue
        parts = line.split("|||")
        if len(parts) < 7:
            logger.warning("Skipping malformed finding line: %s", line[:120])
            continue
        findings.append({
            "company":     parts[1].strip(),
            "type":        parts[2].strip().lower(),
            "relevance":   parts[3].strip().upper(),
            "vc_firm":     parts[4].strip(),
            "description": parts[5].strip(),
            "source":      parts[6].strip(),
            "found_at":    datetime.now().isoformat(),
        })
    return findings


# ── Core research loop ────────────────────────────────────────────────────────

def run_research(max_continuations: int = 5) -> list[dict]:
    """
    Run daily competitive intelligence research.

    Uses Claude (claude-opus-4-6) with the web_search_20260209 server-side tool.
    Handles pause_turn (server-side loop iteration limit) by continuing automatically.

    Returns a list of finding dicts, sorted HIGH relevance first.
    """
    client = anthropic.Anthropic(
        api_key=config.ANTHROPIC_API_KEY,
        timeout=360.0,  # 6-minute timeout for extended web search sessions
    )

    system_prompt = _build_system_prompt()
    user_prompt   = _build_user_prompt()

    messages: list[dict] = [{"role": "user", "content": user_prompt}]

    accumulated_text = ""
    continuations = 0

    logger.info("Starting research session with claude-opus-4-6 + web_search")

    while continuations <= max_continuations:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=8000,
            thinking={"type": "adaptive"},  # Better reasoning about competitive dynamics
            system=system_prompt,
            tools=[{"type": "web_search_20260209", "name": "web_search"}],
            messages=messages,
        )

        # Accumulate any text blocks
        for block in response.content:
            if hasattr(block, "text"):
                accumulated_text += block.text + "\n"

        logger.debug("stop_reason=%s  continuation=%d", response.stop_reason, continuations)

        if response.stop_reason == "end_turn":
            break

        if response.stop_reason == "pause_turn":
            # Server-side web_search loop hit its iteration cap; continue seamlessly.
            # Per API docs: append assistant turn (with trailing server_tool_use block)
            # and re-send — no extra user message needed.
            messages.append({"role": "assistant", "content": response.content})
            continuations += 1
            logger.info("pause_turn received — continuing (%d/%d)", continuations, max_continuations)
            continue

        # Any other stop reason (max_tokens, etc.) — stop and use what we have
        logger.warning("Unexpected stop_reason=%s; using accumulated output", response.stop_reason)
        break

    findings = _parse_findings(accumulated_text)

    # Sort: HIGH first, then MEDIUM
    findings.sort(key=lambda f: (0 if f["relevance"] == "HIGH" else 1))

    logger.info(
        "Research complete: %d findings (%d HIGH, %d MEDIUM)",
        len(findings),
        sum(1 for f in findings if f["relevance"] == "HIGH"),
        sum(1 for f in findings if f["relevance"] == "MEDIUM"),
    )
    return findings
