# GWRE Research Agent

Automated 24/7 competitive intelligence for **Guidewire Software (GWRE)** —
the P&C insurance system-of-record platform.

Every day the agent:
1. Scans the internet for activity at the **top 40 VC firms** (websites, blogs,
   LinkedIn, X/Twitter, Reddit, press releases, podcasts)
2. Surfaces updates about portfolio companies that **compete directly or indirectly
   with Guidewire** (policy administration, claims, billing, AI insurance platforms)
3. Emails you a **≤100-word bullet digest** — just the signal, zero noise

---

## How it works

```
┌────────────────────────────────────────────────────────────┐
│  Claude Opus 4.6  +  web_search tool (Anthropic-hosted)    │
│                                                            │
│  5 search blocks × 5 queries = ~25 targeted web searches  │
│  per daily run covering all 40 VC firms + known competitors│
└─────────────────────────┬──────────────────────────────────┘
                          │ raw findings (FINDING||| format)
                          ▼
              Deduplication (state.json, 7-day window)
                          │ new findings only
                          ▼
           Claude Opus 4.6  →  ≤100-word bullet digest
                          │
                          ▼
                    SMTP email sent
```

**Model:** `claude-opus-4-6` with adaptive thinking for nuanced competitive
analysis, and the `web_search_20260209` server-side tool (no separate search
API key needed).

---

## Quick start

### 1. Clone and install

```bash
git clone https://github.com/danmreuter-commits/gwre-research-agent
cd gwre-research-agent
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set ANTHROPIC_API_KEY and email fields
```

**Gmail users:** create an [App Password](https://myaccount.google.com/apppasswords)
(requires 2FA enabled). Use it as `EMAIL_SMTP_PASS`.

### 3. Test the email pipeline (no live research)

```bash
python main.py --test-email
```

This sends a digest built from mock findings so you can verify SMTP works
before spending API credits on research.

### 4. Run once now

```bash
python main.py
```

### 5. Run on a daily schedule

```bash
# Runs at 8:00 AM local time every day (runs immediately, then on schedule)
python main.py --schedule

# Custom time
python main.py --schedule --time 07:00
```

---

## Production deployment (Linux server / VPS)

### Option A — systemd service (recommended)

```ini
# /etc/systemd/system/gwre-agent.service
[Unit]
Description=GWRE Research Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/opt/gwre-research-agent
ExecStart=/opt/gwre-research-agent/venv/bin/python main.py --schedule --time 07:30
Restart=on-failure
RestartSec=60
EnvironmentFile=/opt/gwre-research-agent/.env

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now gwre-agent
sudo journalctl -fu gwre-agent
```

### Option B — cron (simple)

```bash
# Run daily at 7:30 AM
30 7 * * * cd /opt/gwre-research-agent && /usr/bin/python3 main.py >> logs/agent.log 2>&1
```

```bash
mkdir -p logs
crontab -e   # paste the line above
```

---

## Sample email digest

```
Subject: GWRE Intel Brief – March 26, 2026

• Duck Creek: Raised $80M Series E targeting mid-market P&C
• Socotra: 35 carriers now live on API-first policy platform
• Shift Technology: USAA deal; CEO hints at full claims module
• Anthemis: Blog post calls core-system disruption "imminent"
• Gradient AI: $40M Series C, underwriting + claims expansion
```

---

## What gets monitored

### VC firms (40 total)

| Category | Firms |
|---|---|
| Tier-1 generalist | Sequoia, a16z, Accel, Benchmark, Kleiner Perkins, Greylock, Index, General Catalyst, NEA, Lightspeed, Bessemer, Battery, IVP, Founders Fund, Tiger Global, Coatue, Insight, GV, Khosla, First Round, Spark, TCV, 8VC, USV, SoftBank |
| Insurance/fintech focused | Ribbit, QED, Anthemis, IA Capital, Munich Re Ventures, MS&AD Ventures, Nationwide Ventures, Aquiline, XL Innovate, Mundi |
| International | DST Global, Atomico, Balderton, Northzone, LocalGlobe |

### Competitive signals tracked

| Signal | Example |
|---|---|
| **Investment** | Duck Creek raises Series E |
| **Product** | Socotra launches claims API |
| **Metrics** | Sapiens discloses $200M ARR |
| **Partnership** | Shift Technology × USAA deal |
| **Platform shift** | Erie Insurance migrates off Guidewire |
| **VC signal** | Anthemis blog: "core system disruption coming" |

### Relevance filter

- **HIGH** — direct competitor funding/product; carrier switching off Guidewire
- **MEDIUM** — AI point-solution Series B+; VC positioning signals
- **Excluded** — consumer insurtech, life/health, pre-seed rounds, pure distribution

---

## Configuration reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | — | Anthropic API key |
| `EMAIL_FROM` | For email | — | Sender address |
| `EMAIL_TO` | For email | — | Recipient(s), comma-separated |
| `EMAIL_SMTP_HOST` | For email | `smtp.gmail.com` | SMTP server |
| `EMAIL_SMTP_PORT` | For email | `587` | SMTP port (STARTTLS) |
| `EMAIL_SMTP_USER` | For email | — | SMTP login username |
| `EMAIL_SMTP_PASS` | For email | — | SMTP password / App Password |
| `LOOKBACK_DAYS` | No | `7` | Days before a finding can reappear |

> If SMTP is not configured the digest is printed to stdout — useful for piping
> to other tools or integrating with Slack/Teams webhooks.

---

## Project structure

```
gwre-research-agent/
├── agent/
│   ├── researcher.py   # Claude + web_search research engine
│   ├── emailer.py      # Digest generation + SMTP sending
│   └── state.py        # Deduplication (state.json)
├── data/
│   ├── vc_firms.py     # Top 40 VC firms with metadata
│   └── competitors.py  # Guidewire competitive landscape context
├── config.py           # Environment variable loading + validation
├── main.py             # Entry point + CLI
├── requirements.txt
├── .env.example
└── state.json          # Auto-created; tracks sent findings
```

---

## Extending the agent

**Add more VC firms** — edit `data/vc_firms.py`.

**Update competitor context** — edit `data/competitors.py` (Guidewire's product
list, competitor names, relevance criteria). Changes take effect on the next run.

**Pipe to Slack instead of email** — replace the `_send_smtp` call in
`agent/emailer.py` with a `requests.post` to your Slack webhook.

**Widen the search window** — increase `LOOKBACK_DAYS` or add more search
queries to `_build_user_prompt()` in `agent/researcher.py`.

---

## Cost estimate

Each daily run uses approximately:
- **Research:** ~15,000–25,000 input tokens + ~3,000 output tokens (claude-opus-4-6 + web_search)
- **Digest:** ~800 input tokens + ~150 output tokens (claude-opus-4-6)
- **Total per day:** ~$0.50–$1.50 depending on search depth

Monthly cost: **~$15–$45** at published rates.
