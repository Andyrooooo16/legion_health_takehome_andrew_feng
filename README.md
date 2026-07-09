# Legion Health Take-Home — Andrew Feng

**Can patient-facing ads or sponsorships fund free care for uninsured patients?**

Office of the Founders take-home · July 2026

## Answer in one line

For a **new uninsured-only pipeline** (0 of ≈3,000 actives today are uninsured; core FFS unchanged), ads and sponsorship cannot fully fund free care (**≈2%** and **≈13%** of break-even on the cheapest AI pathway) — but a **$10–25K test** can falsify whether sponsorship works as a co-funder before Legion acquires uninsured patients at scale.

---

## How I reached this answer

| Step | What I did | Link |
|------|------------|------|
| 1 | Framed the decision (five gates, five funding models, kill criteria) | [`decision_framework.md`](deliverables/decision_framework.md) |
| 2 | Researched comparables, regulation, and uninsured TAM (134 sources) | [`sources.csv`](research/sources.csv) · [`comparable_notes.md`](research/comparable_notes.md) |
| 3 | Built unit economics and stress-tested assumptions | [`legion_sponsorship_model.xlsx`](model/legion_sponsorship_model.xlsx) · [`model_readme.md`](model/model_readme.md) |
| 4 | Integrated Legion operating data when provided | [`ceo_data_integration.md`](data/ceo_data_integration.md) |
| 5 | Documented open questions and validation plan | [`open_questions.md`](deliverables/open_questions.md) · [`30_day_plan.md`](deliverables/30_day_plan.md) |
| 6 | Designed sponsor and patient test kits | [`sponsor_test_package.md`](deliverables/sponsor_test_package.md) · [`experiment_spec.md`](deliverables/experiment_spec.md) |

**Visual map:** [thinking pathway (live)](https://andyrooooo16.github.io/legion_health_takehome_andrew_feng/deliverables/thinking_pathway.html) — logical flowchart of the full analysis.

> **HTML files on GitHub show source code, not the rendered page.** Use the live links below (GitHub Pages), or clone the repo and open the `.html` files locally in Chrome.

---

## Key assumptions

These are the load-bearing assumptions. Challenge any of these first — full ledger with low/base/high and sources: [`assumptions_summary.md`](deliverables/assumptions_summary.md) and Excel tab `01_Assumptions`.

| # | Assumption | What I used |
|---|------------|-------------|
| **Scope** | "Free care" = new **uninsured** patients on a mostly-AI pathway — not Legion's existing reimbursed book | 0 of ≈3,000 actives uninsured today |
| **Costs** | Legion's per-visit/episode economics | $74 sync visit · $37 AI-supported · ≈$8 AI episode · 5.3 visits/patient/yr |
| **Revenue** | Core FFS today | ≈$153/visit · ≈3,000 actives · ≈$6M/yr |
| **Sponsorship** | Industry anchor for fixed-fee sponsor ARPU | ≈$10.50/patient/yr net (GoodRx proxy) — covers ≈13% of AI-pathway break-even |
| **Ads** | Patient-vertical CPM + engagement placeholder | ≈$1.53/patient/yr — covers ≈2% of break-even |
| **Employer underwriting** | PEPM range from comparables | $600/yr base × 55% utilization → ≈$330/patient/yr (clears AI-pathway break-even) |
| **Population** | Reachable uninsured AMI cohort (not all Americans) | ≈5.9M nationally; model uses 25K / 150K / 750K capture scenarios |
| **Still open** | Trust impact, AI-pathway cadence, sponsor WTP | Placeholders — testable in the 30-day plan |

**What would flip the answer:** [`assumptions_summary.md`](deliverables/assumptions_summary.md)

---

## Start here (10 minutes)

| # | Asset | What it is |
|---|--------|------------|
| 1 | [**Decision deck (live)**](https://andyrooooo16.github.io/legion_health_takehome_andrew_feng/deliverables/deck.html) · [source](deliverables/deck.html) | **Primary deliverable** — 9 slides (arrow keys to navigate) |
| 2 | [`executive_summary.md`](deliverables/executive_summary.md) | One-page prose version |
| 3 | [**Thinking pathway (live)**](https://andyrooooo16.github.io/legion_health_takehome_andrew_feng/deliverables/thinking_pathway.html) · [source](deliverables/thinking_pathway.html) | Logical flowchart of the analysis |
| 4 | [`legion_sponsorship_model.xlsx`](model/legion_sponsorship_model.xlsx) | Editable model — tab `01_Assumptions` drives everything |
| 5 | [**Live survey**](https://legion-take-home-assignment-1rhogocn3.vercel.app/) | Patient trust concept test prototype |

**GitHub Pages (recommended):** Repo → **Settings** → **Pages** → Source: **Deploy from a branch** → Branch: **main** → Folder: **/ (root)** → **Save**. Wait 1–2 minutes, then use the live links above.

> If you use **GitHub Actions** instead and the workflow fails on `configure-pages`, switch to **Deploy from a branch** (above) — it works the same for static HTML and does not need Actions.

---

## Go deeper

| Topic | File |
|-------|------|
| $1B growth reframe | [`growth_contribution_analysis.md`](deliverables/growth_contribution_analysis.md) |
| Uninsured TAM sizing | [`uninsured_population_sizing.md`](data/uninsured_population_sizing.md) |
| Risk map | [`risk_analysis.md`](deliverables/risk_analysis.md) |
| Methods & limits | [`methodology.md`](deliverables/methodology.md) |
| 30-day validation plan | [`30_day_plan.md`](deliverables/30_day_plan.md) |
| Patient experiment | [`experiment_spec.md`](deliverables/experiment_spec.md) |
| Buyer interview kit | [`sponsor_test_package.md`](deliverables/sponsor_test_package.md) |
| Sponsored experience | [`patient_experience_spec.md`](deliverables/patient_experience_spec.md) |
| Sponsor value prop | [`sponsor_value_prop.md`](deliverables/sponsor_value_prop.md) |
| Source ledger | [`sources.csv`](research/sources.csv) · [`lotus_notes.md`](research/lotus_notes.md) · [`regulatory_notes.md`](research/regulatory_notes.md) |

---

## Repository map

```
legion_health_takehome_andrew_feng/
├── README.md                  ← you are here
├── deliverables/              ← deck, summary, plans (16 files)
├── model/                     ← Excel model + Python implementation
├── research/                  ← source ledger + research notes
├── data/                      ← Legion operating data + TAM sizing
├── app/                       ← patient trust survey prototype
└── design/                    ← Legion design system (prototype styling)
```

### Deliverables (`deliverables/`)

| Category | Files |
|----------|--------|
| **Answer** | `deck.html`, `executive_summary.md`, `thinking_pathway.html` |
| **Logic** | `decision_framework.md`, `assumptions_summary.md`, `open_questions.md` |
| **Scale** | `growth_contribution_analysis.md` |
| **Validation** | `30_day_plan.md`, `experiment_spec.md`, `sponsor_test_package.md`, `validation_launch_checklist.md` |
| **Depth** | `methodology.md`, `risk_analysis.md`, `sponsor_value_prop.md`, `patient_experience_spec.md` |
| **Outline** | `deck.md` (slide-by-slide reference) |

### Model (`model/`)

- **`legion_sponsorship_model.xlsx`** — change assumptions on tab `01_Assumptions`
- **`model.py`** + **`tests/`** — Python mirror with unit tests
- **`model_readme.md`** — how to read and challenge the model

### Prototype (`app/`)

```bash
cd app && npm install && npm run dev
```

Then open http://localhost:3000. Details: [`app/prototype_readme.md`](app/prototype_readme.md).

---

## Troubleshooting

### HTML deck or thinking pathway won't display correctly

**On GitHub:** Clicking `deck.html` or `thinking_pathway.html` in the repo shows raw HTML source. Use the [**live links**](https://andyrooooo16.github.io/legion_health_takehome_andrew_feng/deliverables/deck.html) above instead.

**After cloning locally:**

```bash
git clone https://github.com/Andyrooooo16/legion_health_takehome_andrew_feng.git
cd legion_health_takehome_andrew_feng
open deliverables/deck.html          # macOS — opens in your default browser
# or: open -a "Google Chrome" deliverables/deck.html
```

On Windows: right-click `deliverables/deck.html` → **Open with** → Chrome. On Linux: `xdg-open deliverables/deck.html`.

| Problem | Fix |
|---------|-----|
| Page is blank or unstyled | Both HTML files load **Inter** from Google Fonts. Connect to the internet and refresh. |
| Deck won't advance | Click the slide area first, then use **← / →** arrow keys (not scroll). |
| Live GitHub Pages link 404 | **Settings** → **Pages** → Source: **Deploy from a branch** → **main** → **/ (root)** → Save. Wait 1–2 min. (Simpler than GitHub Actions for static HTML.) |
| GitHub Actions deploy failed on `configure-pages` | Use **Deploy from a branch** instead (above). Or: **Settings** → **Environments** → **github-pages** → allow deployments from `main`, then re-run the workflow. |
| Prefer a local server | `python3 -m http.server 8080` from the repo root → open http://localhost:8080/deliverables/deck.html |

### Excel model (`legion_sponsorship_model.xlsx`)

| Problem | Fix |
|---------|-----|
| File won't open | Use Excel, Google Sheets (upload), or LibreOffice Calc. |
| Tabs show old numbers | Edit assumptions on **`01_Assumptions`** only; downstream tabs recalculate automatically. In Excel: **Formulas → Calculate Now** if needed. |
| Want to verify Python output | See **Python model** below — optional; the Excel file is the primary editable model. |

### Python model (`model/`) — optional

```bash
cd model
python3 scenarios.py
python3 sensitivity.py
python3 -m pytest tests/test_model.py -v   # requires: pip install pytest
```

| Problem | Fix |
|---------|-----|
| `No module named pytest` | `pip install pytest` (or `pip3 install pytest`). |
| Permission / environment errors on macOS | Use a venv: `python3 -m venv .venv && source .venv/bin/activate && pip install pytest` |

### Survey prototype (`app/`)

```bash
cd app && npm install && npm run dev
```

| Problem | Fix |
|---------|-----|
| `npm: command not found` | Install [Node.js](https://nodejs.org/) (LTS, v18+). |
| Port 3000 already in use | `npm run dev -- -p 3001` → open http://localhost:3001 |
| Build fails with `Bus error` | Copy `app/` to a local (non-network) folder, run `npm install && npm run build` there. See [`app/prototype_readme.md`](app/prototype_readme.md). |
| Stuck on one survey variant while testing | Open an incognito window, or clear this site's localStorage in browser devtools. |

**Deployed version (no local setup):** https://legion-take-home-assignment-1rhogocn3.vercel.app/

---

## Limitations

Buyer interviews were not conducted within the assignment window (interview kit is ready in `deliverables/sponsor_test_package.md`). The patient survey is built but not fielded at panel scale. Legion's cost figures are from the company directly, not independently audited.

I did reach out via LinkedIn to several business reps at Lotus Health and OpenEvidence to ask about their sponsorship and monetization models, but none were able to respond in the short assignment window. The analysis relies on public sources and comparables as a result. The 30-day plan includes structured buyer interviews as the next step to close that gap.

---

Andrew Feng · July 2026
