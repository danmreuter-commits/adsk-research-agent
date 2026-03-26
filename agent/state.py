"""
State manager: persists seen findings to avoid duplicating stories across daily runs.

Uses a simple JSON file (state.json) — no database dependency required.
Keys expire automatically after LOOKBACK_DAYS so the state file stays small.
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

import config

logger = logging.getLogger(__name__)

STATE_FILE = Path("state.json")


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Could not read state file (%s) — starting fresh", exc)
    return {"seen": {}}


def _save(state: dict) -> None:
    try:
        with open(STATE_FILE, "w") as fh:
            json.dump(state, fh, indent=2)
    except OSError as exc:
        logger.error("Could not write state file: %s", exc)


def _finding_key(finding: dict) -> str:
    """
    Stable hash key for a finding based on company + type + first 80 chars of description.
    Insensitive to capitalisation and minor wording changes.
    """
    raw = (
        finding.get("company", "").lower().strip()
        + "|"
        + finding.get("type", "").lower().strip()
        + "|"
        + finding.get("description", "")[:80].lower().strip()
    )
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


# ── Public interface ──────────────────────────────────────────────────────────

def filter_new_findings(findings: list[dict]) -> list[dict]:
    """
    Return only findings not already sent within the lookback window.
    Also updates the state file with the newly accepted findings.
    """
    state = _load()
    seen: dict = state.get("seen", {})

    # Purge expired entries to keep the file lean
    cutoff = (datetime.now() - timedelta(days=config.LOOKBACK_DAYS)).isoformat()
    seen = {k: v for k, v in seen.items() if v >= cutoff}

    new_findings: list[dict] = []
    for finding in findings:
        key = _finding_key(finding)
        if key not in seen:
            new_findings.append(finding)
            seen[key] = datetime.now().isoformat()
            logger.debug("New finding: %s — %s", finding["company"], finding["description"][:60])
        else:
            logger.debug("Duplicate (skipping): %s", finding["company"])

    state["seen"] = seen
    _save(state)

    logger.info(
        "Dedup: %d in → %d new (skipped %d duplicates)",
        len(findings),
        len(new_findings),
        len(findings) - len(new_findings),
    )
    return new_findings
