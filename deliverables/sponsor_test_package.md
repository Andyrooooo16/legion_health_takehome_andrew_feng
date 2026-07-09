# Sponsor Test Package

**Prepared by:** Sponsor Test Agent
**Scope:** Operational package to run the sponsor side validation test (H2, "will credible buyers pay enough under acceptable constraints?"). This document elaborates the lead approved parameters in execution brief §21; it does not change scope, targets, or thresholds, and it does not answer the underlying strategic question (proceed/modify/stop) for Legion.
**Companion inputs:** `decision_framework.md`, `comparable_notes.md`, `regulatory_notes.md`, `model/assumptions.csv`, `model/outputs.csv`.

**Note:** Prices here are formulas and benchmarks, not quoted rates. Populate after buyer interviews and model thresholds are confirmed.

## 1. Sponsorship Concepts, One Page Value Proposition per Package

Each package below is designed so the answer to "what does the sponsor never get" is identical across all three: **no PHI, no patient level data, no influence over clinical recommendations, no prescribing/referral linkage.** This is non negotiable per `decision_framework.md` Gate 4 and the regulatory risk table (`research/regulatory_notes.md` §7), it is restated in every package rather than stated once, because it is the thing most likely to erode under commercial pressure during negotiation.

### Package A, Access Underwriting

**Concept statement (verbatim, for use in interviews):** *"Sponsor X funds free access for 1,000 eligible patients."*

| | |
| | |
| **What the sponsor gets** | Association with a defined cohort level outcome ("Sponsor X funded access for N patients this quarter"); aggregate impact reporting (patients served, aggregate de identified engagement/completion stats, cohort level satisfaction); co brandable impact materials (case study, press mention, ESG/CSR reporting language) usable in the sponsor's own external communications; a renewal option tied to aggregate program metrics, not individual outcomes. |
| **What the sponsor never gets** | Any patient identity, contact information, diagnosis, treatment record, or session content; any ability to select, exclude, or target specific patients (e.g., by diagnosis, demographic, or geography beyond a broad, clinically neutral eligibility rule set by Legion, not the sponsor); any input into clinical protocols, provider assignment, or care plans; any linkage between funding and a specific patient's prescribing or treatment outcome. |
| **Example placement** | A named cohort ("The Sponsor X Access Program") funding a fixed number of intake to stabilization episodes for financially eligible patients in a defined pathway (e.g., the "mostly AI driven care episode" pathway per `decision_framework.md`); eligibility determined solely by Legion's clinical/financial need criteria. |
| **Reporting to sponsor** | Aggregate only, on a quarterly cadence: patients served (count), aggregate completion/engagement rate, aggregate (not patient level) satisfaction score, program spend to date vs. commitment. No cohort smaller than a pre agreed minimum cell size (to prevent re identification) is ever reported. |
| **Closest regulatory analog** | Favorable OIG Advisory Opinion pattern (AO 21 01, AO 24 12, AO 25 07 per `regulatory_notes.md` §3.3): eligibility unconnected to provider/plan choice, no identifiable data returned to sponsor. This is the **most defensible** of the three packages on AKS/CMP grounds, provided eligibility is never conditioned on the sponsor's product. |

### Package B, Category Sponsorship

**Concept statement (verbatim, for use in interviews):** *"This care experience is supported by Sponsor X."* No patient level targeting.

| | |
| | |
| **What the sponsor gets** | Brand association with the care experience as a category (e.g., "mental health support," "psychiatric care access"), analogous to a PBS style underwriting credit, a name/logo mention shown identically to every patient in a given pathway, not selected or targeted by any patient characteristic; aggregate reach reporting (total patients who saw the pathway in a period); optional category exclusivity (e.g., one sponsor per care pathway per period) as a negotiable, priced term. |
| **What the sponsor never gets** | Any targeting logic tied to diagnosis, condition, medication, or any other clinical signal; any patient level exposure or engagement data; any right to reference a specific clinical outcome, prescription, or treatment in its messaging; any influence over the clinical content or sequencing of the experience it sponsors. |
| **Example placement** | A static "supported by" credit on the pathway's intake or waiting room screen, shown identically to all patients in that pathway during the sponsorship period, no message variation, no product mention beyond name/logo, no call to action tied to the sponsor's product. |
| **Reporting to sponsor** | Aggregate exposure counts (impressions/patients reached) by period; no click level, session level, or patient level detail; no ad tech pixel or SDK on any authenticated clinical page (per `regulatory_notes.md` §1.2 and the BetterHelp/GoodRx precedent in §2). |
| **Closest regulatory analog** | Public broadcasting style underwriting credit, the lowest risk package on FDA/FTC grounds because there is no personalization, no product claim, and no targeting; still requires HIPAA marketing definition review if the credit is deemed to "encourage use" of the sponsor's product (`regulatory_notes.md` §1.1). |

### Package C, Sponsored Education

**Concept statement (verbatim, for use in interviews):** Sponsor content is clearly separated from clinical recommendations.

| | |
| | |
| **What the sponsor gets** | Placement of unbranded or lightly branded disease awareness/educational content (not product promotion) in a clearly labeled, structurally separate section of the patient experience (e.g., a "resources" tab, not the clinical chat/session flow); aggregate content engagement reporting (views, completion of an education module); sponsor attribution ("education provided by Sponsor X") on the content itself. |
| **What the sponsor never gets** | Any placement inside or adjacent (in timing or visual proximity) to an active clinical session or a specific patient's care plan such that a reasonable patient could confuse it with a clinical recommendation; any product specific claim, dosing information, or efficacy/safety claim (this would convert the content into FDA regulated promotional material, per `regulatory_notes.md` §4); any patient level data on who viewed what; any sponsor review or approval rights over Legion's own clinical content. |
| **Example placement** | A general "Understanding Depression" or "Understanding ADHD" explainer module, unbranded or bearing only a sponsor name/logo with no product reference, hosted in a distinct, labeled section, with a documented firewall (staffing, timing, hosting) from any branded material, reviewed by Legion clinical staff before publication with no sponsor edit rights over clinical claims. |
| **Reporting to sponsor** | Aggregate module views/completions by period; no patient identity or clinical linkage. |
| **Closest regulatory analog** | FDA disease awareness vs. product promotion distinction (`regulatory_notes.md` §4.2), favorable only if the firewall is real and documented; FDA's own OPDP research shows patients conflate disease awareness and branded content when they are proximate, so this package carries the **highest execution risk** of the three even though its concept is the most common in comparable pharma education programs. |

**Cross package constant (do not vary in negotiation):** zero patient level data to sponsor, zero clinical influence, zero prescribing/referral linkage, aggregate only reporting, sponsor eligibility criteria set by Legion clinical/financial need rules never by the sponsor. If a buyer's requested terms require relaxing any of these, that is a **red flag** (Section 5) requiring redesign or walk away, not a negotiation point.

## 2. Rate Card Structure (Formula, Not Fake Precision)

No per patient price is set in this document. The purpose of this section is the **pricing logic**, the formula each package's price should satisfy, anchored to external benchmarks and to the the model's threshold output.

### 2.1 The governing constraint (from `decision_framework.md` Gate 1 / H1)

> Required sponsor revenue per eligible patient ≥ fully loaded incremental cost per patient ÷ (1 − target contribution margin)

The the model (`model/assumptions.csv`, `model/outputs.csv`) computes this as `required_arpu_usd_per_patient_per_yr` for each pathway × monetization model scenario. **This package treats that figure as an input variable, `T` (required threshold ARPU), not a number to be reproduced here**, it varies by pathway (traditional / AI supported / AI driven), cost scenario (low/base/high), and target margin (20 30% per assumption A14), and the model is still being finalized concurrently. As of the most recent model run, `required_arpu_usd_per_patient_per_yr` for the fixed fee sponsorship model (Model B) ranges from roughly $61/patient/yr (high cost scenario, ai_driven pathway) to several thousand dollars/patient/yr (low cost scenario, traditional pathway), illustrating that **the threshold is pathway dependent by 1 2 orders of magnitude**, so any rate card must specify which pathway it prices, not a single company wide number.

### 2.2 Formula per package

**Package A, Access Underwriting (cohort level fixed fee)**

```
Sponsor commitment ($) = N_patients × price_per_patient

where price_per_patient must satisfy:
 price_per_patient ≥ T (required_arpu_usd_per_patient_per_yr, from the model,
 for the specific pathway being underwritten)

Anchor candidates for price_per_patient (benchmark derived, NOT Legion specific):
 * Low anchor: ~$10 15/patient/yr (GoodRx pharma manufacturer solutions line
 ARPU proxy, comparable_notes.md §4; assumption A05 low/base case)
 * High anchor: ~$36 4,200/patient/yr (employer/payer PEPM range translated to
 annual terms, comparable_notes.md; assumption A15), applicable
 mainly if the "sponsor" is closer to an employer/payer archetype
 than a pure brand/media sponsor
 * Do NOT anchor to physician audience CPM/ARPU ($120 230+; OpenEvidence/Doximity), patient audiences are a structurally different, lower yield market
 (comparable_notes.md §5); using this anchor would overstate achievable price.
```

**Package B, Category Sponsorship (fixed fee, impression/exposure based logic without patient targeting)**

```
Sponsor commitment ($) = (exposed_patients / 1000) × eCPM_equivalent × sessions_per_patient_per_yr

Anchor for eCPM_equivalent: ~$20 45 (Facebook healthcare vertical / patient health 
vertical CPM benchmark, comparable_notes.md §4, assumption A06), explicitly NOT
the $70 1,000+ physician audience CPM range.

This is a STRUCTURAL anchor (how comparable non targeted health vertical media is
priced), not a claim that Legion's placement will clear this rate; contextual,
non personalized placement (the only kind permitted here) typically prices at or
below general health vertical CPM, not above it.
```

**Package C, Sponsored Education (fixed fee per content placement/period, not per patient)**

```
Sponsor commitment ($) = flat fee per content module per quarter (subscription like,
not CPM), reflecting production, clinical review, and firewall compliance cost, plus
a margin, analogous to a Doximity style modular sponsored content subscription
(comparable_notes.md §1, "account based media buy" model) rather than an open
ad exchange CPM. No public per module benchmark exists for this exact unit; price
discovery for Package C should rely primarily on interview elicited WTP (Section 3),
not a pre set formula.
```

### 2.3 What finalizes the rate card

The rate card converts from formula to number only when: (1) the the model publishes a stable `required_arpu_usd_per_patient_per_yr` per pathway, and (2) the interview program (Section 3) returns a median stated/qualified WTP. The rate card is the **higher of** the model's required threshold and whatever floor emerges from interviews, with the two numbers compared explicitly, if buyer WTP sits below the model threshold, that is itself the H2 kill signal (`decision_framework.md` Kill Criteria), not a reason to lower the rate card.

## 3. Buyer Interview Guide (45 Minutes)

**Purpose reminder read at the top of every interview (not a script line, an internal note to the interviewer):** the goal is to elicit real WTP and real constraints, not to sell. Do not let the conversation become a pitch meeting. Positive sentiment without a number, a next step, or a named budget is not evidence (`decision_framework.md` Gate 2).

### Segment 1, Background and role (5 min)

* "Tell me about your role and how your organization currently spends on [media / sponsorship / patient access programs / employee benefits / grants], whichever frame fits their category."
* "Walk me through a recent example of a similar spend decision you made, what was it, and how did it get approved?"

### Segment 2, Budget ownership qualification (5 min)

This segment determines whether the person meets the qualified buyer bar (control/influence budget, own procurement, or directly understand the buying process, Section 4 turns these answers into a score).

* "Do you personally control a budget line that could fund something like this, or do you influence someone who does?"
* "Whose sign off would be required to commit spend at [$X $Y placeholder range], and roughly how many people/approvals sit between you and a signed contract?"
* "Is there an existing budget category this would fall under (e.g., patient assistance, CSR/ESG, HCP marketing, employee benefits, foundation grants), or would this require a new budget line?"

### Segment 3, Concept reactions per package (10 min)

Show all three concept statements verbatim (Section 1). For each:

* "What's your first reaction to this concept?"
* "Who inside your organization would need to be convinced, and what would they push back on?"
* "Which of these three feels most fundable to you, and why?"

### Segment 4, WTP elicitation (Van Westendorp style, adapted for B2B) (10 min)

Standard Van Westendorp asks about a *consumer's* price for a *product*; here it is adapted to a *budget owner's* price for a *sponsorship commitment* at a *stated cohort size* (anchor explicitly to "1,000 eligible patients" from the Package A concept so answers are comparable across interviews):

* "At what price for sponsoring 1,000 eligible patients would this feel **too expensive** to consider, a number that would take it off the table regardless of the concept?"
* "At what price would this feel **so cheap that you'd question whether it's a serious/credible program**, cheap enough to raise doubts about impact or legitimacy?"
* "At what price would this start to feel **expensive, but you'd still seriously consider it** if the reporting and concept were right?"
* "At what price would this feel like **a genuine bargain**, good value, still credible?"
* Follow up (critical, do not skip): "Is that a number you could actually commit budget to in the next two quarters, or a number that sounds reasonable in the abstract?", this distinguishes stated WTP from qualified WTP (Section 6, L2 vs L3).

### Segment 5, Required targeting, reporting, exclusivity (5 min)

* "What reporting would you need to justify this spend internally, what specific metrics?"
* "Would you need any patient level or diagnosis level information to feel comfortable, or is aggregate reporting sufficient?" *(This question is a deliberate red flag probe, see Segment 7.)*
* "Would you expect category exclusivity (no competing sponsor in the same pathway), and what would that be worth to you?"
* **Minimum-scale hypothesis probe** (see `sponsor_value_prop.md`): "We are pitching premium association and access, not reach. Would a high-intent cohort of roughly 1,000 to 5,000 eligible patients be enough inventory for you to engage on a fee-for-benefit or access-underwriting deal? If not, what minimum exposed-patient count would you need before this is worth a conversation?" *(KILL CONDITION: if qualified buyers consistently require more than ~25,000 exposed patients before engaging, the association/access value proposition fails and only the employer PEPM route remains.)*

### Segment 6, Procurement process and timeline (5 min)

* "If you decided today this was worth pursuing, what are the actual next steps at your organization, procurement, legal, compliance review?"
* "Realistically, how long from 'I'm interested' to a signed contract, based on how deals like this normally move at your organization?"
* "What has killed similar deals in the past, at your organization or ones you've seen?"

### Segment 7, Red flag probes (explicit, do not skip)

Ask directly, do not infer from silence:

* "Would your organization require any patient level data, diagnosis information, or the ability to target specific conditions for this to be worth funding?"
* "Would this need to be linked in any way to prescribing, referrals, or a specific product recommendation?"
* "Would you need any influence over clinical content or care recommendations as part of this?"

If yes to any: mark as a **red flag** per Section 5/6, this buyer's structure is incompatible with the model regardless of price, and the interview should note this explicitly rather than averaging their WTP into the "credible WTP" pool.

### Segment 8, Close on pilot interest (5 min)

* "If we ran a paid pilot at a smaller scale first, say, a defined test cohort over one quarter, would that be something you could bring to your organization?"
* "What would you need to see from a pilot to make the case for renewing or expanding it?"
* "Is there a next step that makes sense, a follow up conversation with [legal/procurement/your team], a term sheet to react to, anything?"

**Interviewer note:** end every interview by recording, verbatim if possible: (1) the stated too expensive/too cheap/expensive but considered/bargain price points, (2) whether the person confirmed a real budget and approval path, (3) any red flag triggered, (4) whether a concrete next step was agreed. These four fields feed directly into the qualification scorecard (Section 4) and the evidence ladder (Section 6).

### 3.1 Model D / employer underwriter addendum

Run this addendum **in addition to** Segments 1, 8 whenever the contact is an employer, payer benefits buyer, or foundation funder being evaluated for Model D/E (not pure brand sponsorship).

**Utilization / engagement (maps to model A21):**
* "If you paid a PEPM rate for this benefit, what utilization rate would you assume for budgeting, what share of eligible employees would actually use it in year one?"
* "What utilization rate would make the program a failure internally, even if the PEPM looked affordable on paper?"
* Record stated low/base/high utilization assumptions separately from headline PEPM, both feed the model.

**Narrow benefit vs. platform WTP:**
* "Would you pay the same PEPM for a *narrow* AI psychiatry episode benefit as you pay for a full behavioral health platform (Lyra/Spring style coaching + therapy + psychiatry)? If not, what discount would you apply?"
* "Is this a standalone line item, or must it bundle with your existing EAP/vendor?"

**Hybrid employer branded sponsorship:**
* Present: "Your company logo appears on a 'covered by [Employer]' tier, no patient targeting, no clinical influence, aggregate reporting only. The cash is employer PEPM, not a media CPM buy."
* Ask: "Does the branding change your WTP versus an invisible employer benefit? Would legal/comms require it, or forbid it?"
* **Scoring note:** if cash source is employer PEPM, record WTP under Model D economics regardless of sponsor framing, do not double count as Model B ARPU.

**Prerequisite:** Integrate Legion's operating data before employer/payer interviews (complete — see `30_day_plan.md`).

## 4. Qualification Scorecard

Score each interviewed contact on four dimensions, 0 3 each (max 12). This operationalizes the lead approved qualified buyer definition ("controls/influences budget, owns procurement, or directly understands the buying process").

| Dimension | 0 | 1 | 2 | 3 |
| | | | | |
| **Budget authority** | No budget role; cannot name an approver | Influences but does not control budget | Controls a relevant budget line directly | Controls budget AND has prior authority to sign deals of this size without escalation |
| **Budget existence** | No existing or plausible budget category; would require net new approval with no precedent | Adjacent budget category exists, but this specific use case is unprecedented there | An existing budget category plausibly covers this (e.g., CSR, patient assistance, HCP marketing) | Named, currently funded budget line this would draw from, confirmed by the contact |
| **Category fit** | Category is excluded per Section 6 (e.g., requires targeting) | Conditional category (Section 6) with unresolved compliance questions | Acceptable category (Section 6) with minor open questions | Acceptable category, prior experience funding comparable non targeted sponsorship/underwriting |
| **Constraint acceptance** | Explicitly requires a red flag item (PHI, targeting, clinical influence, prescribing linkage) as a condition of funding | Expressed discomfort with aggregate only reporting but did not demand a red flag item | Accepted no PHI/no targeting/no influence constraints with minor negotiation on reporting detail | Proactively affirmed the constraints as a positive (e.g., cited GoodRx/Cerebral/BetterHelp precedent as a reason they *want* a no data sharing structure) |

**Qualified buyer threshold:** a contact counts as a **qualified buyer** for the primary metrics (buyers entering procurement, contract value, etc.) only if Budget Authority ≥ 1 **or** Budget Existence ≥ 2 **or** the contact directly and credibly described owning/understanding the procurement process for this category (i.e., is not merely enthusiastic). A score of 0 on Constraint Acceptance is an automatic red flag regardless of the other three scores and should be logged in the red flag tracker (Section 5), not blended into the WTP median.

**Aggregate reporting fields per cohort of interviews:** count of contacts scoring ≥6/12 ("qualified"); count scoring 9+/12 ("highly qualified"); count triggering a Constraint Acceptance = 0 ("disqualifying red flag").

## 5. Evidence Ladder, Interest to Paid Commitment

Defines what counts as evidence at each level, and, as important, what does **not** count, per `decision_framework.md` Gate 2's explicit statement that "interest alone is not evidence."

| Level | Name | Counts as evidence | Does NOT count as evidence |
| | | | |
| **L1** | Polite interest | Contact agreed to take the meeting; expressed general positive sentiment about the concept; asked clarifying questions | "This sounds interesting," "we'd love to explore this," enthusiasm with no number, no named approver, no next step. A full slate of L1 only interviews is not progress toward H2. |
| **L2** | Stated WTP | Contact gave specific Van Westendorp price points (Section 3, Segment 4) for at least one package, even if described as "a number I could imagine," AND named at least one internal stakeholder who would need to approve | A price mentioned in the abstract with an explicit caveat that it's not connected to real budget ("if we had infinite budget, sure"); a price given by someone who scored 0 on Budget Authority and Budget Existence |
| **L3** | Qualified WTP above threshold | The Segment 4 follow up ("is that a number you could actually commit budget to in the next two quarters") was answered affirmatively, AND the stated price clears the the model's `required_arpu_usd_per_patient_per_yr` (or package appropriate equivalent) for the relevant pathway, AND the contact scores ≥6/12 on the qualification scorecard (Section 4) | A high stated price from a contact who scores <6/12; a price that clears the threshold only under the low cost/high margin model scenario but not under the base case |
| **L4** | Procurement engaged | Contact has initiated an actual internal process, looped in procurement, legal, or compliance; requested a term sheet, SOW, or pilot proposal in writing; set a specific internal review date | A contact saying "I'll take this to my team" with no confirmed date or document exchanged in the following 2 3 weeks |
| **L5** | Signed paid pilot / design partner LOI | A signed pilot agreement or letter of intent with a specified fee (even if a placeholder/introductory fee), duration, and the aggregate reporting/no data/no clinical influence clauses (Section 8) accepted in writing | A verbal "yes, let's do it"; an unsigned draft term sheet still under the sponsor's internal review; a pilot proposed at $0 (a free pilot is not evidence of WTP, see kill criteria note below) |

**Kill criteria linkage:** per `decision_framework.md`, H2 fails (or requires redesign) if the interview program cannot move a credible number of contacts past L2 to L3, or if reaching L4/L5 requires conceding a red flag item (Section 6). A program that produces many L1s and few L2s or above should be treated as a negative signal on commercial viability, not as "early stage, needs more time."

**Reporting cadence:** track every interviewed contact's current ladder level in a running log (name/org withheld from this document; log lives with the sponsor test agent's working notes) updated after each interview, so the "≥1 paid design partner" and "≥2 additional qualified prospects continuing" success criteria can be checked against real counts rather than impression.

## 6. Sponsor Category Matrix

Grounded in `research/regulatory_notes.md` (particularly §3.3's OIG Advisory Opinion pattern, §4 FDA rules, and the Risk Table in §7). This matrix determines category fit (Section 4) and outreach sequencing (Section 7).

| Status | Category | Rationale | Package fit |
| | | | |
| **Acceptable (start here)** | Non endemic corporate sponsors (no product touching patient's condition or treatment, e.g., a consumer brand, a financial services or retail sponsor doing CSR/ESG style community health underwriting) | No product prescribing linkage possible; lowest AKS/CMP exposure since there is nothing to steer toward; closest to a pure philanthropic/CSR spend, not an ad buy | A, B |
| **Acceptable (start here)** | Health adjacent consumer brands with no prescription product (e.g., wellness, nutrition, fitness, sleep brands) | Some category relevance aids buyer motivation without creating a prescribing linkage risk; still requires the no targeting firewall since the brand's category is health adjacent | A, B, C (education about the *condition*, not the brand's product) |
| **Acceptable, longer cycle** | Foundations / nonprofit funders | Structurally closest to existing charitable underwriting precedent (comparable_notes.md §3a, PAP foundation model); typically slower procurement (grant cycles) but the lowest regulatory friction of any category | A |
| **Acceptable, longer cycle** | Employers (funding their own employees' access, PEPM style) | Distinct legal basis (a benefits purchase, not a sponsorship media buy) with a strong existing benchmark (Lyra/Spring Health); self interest logic differs from a generic "sponsor," so treat as a related but separate motion, not interchangeable with A/B/C pricing | Adjacent model, not strictly A/B/C, track separately in the model as "Model D" per `decision_framework.md` |
| **Conditional, compliance review required before outreach** | Pharma manufacturer education/disease awareness budgets, PBMs | Real budget and category fit (this is literally what OpenEvidence and Doximity monetize, and what GoodRx's pharma manufacturer solutions line does), but every favorable outcome precedent (`regulatory_notes.md` §3.3) depends on a documented firewall and zero data return to the sponsor; requires counsel sign off on the specific arrangement (per `regulatory_notes.md` §8, Questions 2 5) before any live commercial conversation, not just before signing | C only, with counsel reviewed firewall design; A/B excluded initially because "sponsor funds access for eligible patients" from a pharma manufacturer reads close to the AKS/CMP fact patterns that require an Advisory Opinion |
| **Conditional, compliance review required** | Payers / PBMs considering a sponsorship (not a standard payer contract) | Payer as sponsor (distinct from payer as contracted payer, which is a different, non sponsorship monetization model per `decision_framework.md` Model D) raises novel questions not covered by existing OIG opinions; treat as conditional pending its own legal read | A, B |
| **Excluded initially** | Branded drug advertising / any placement naming or visually identifying a specific prescription product | Squarely inside FDA promotional rules (fair balance, off label) and the highest severity items on the regulatory risk table; also the furthest from any favorable OIG Advisory Opinion pattern | None, out of scope for this test |
| **Excluded initially** | Any sponsor (in any category) that requires diagnosis level or patient level targeting, or any data return enabling patient/provider identification | This is the single most consistent negative factor across every OIG opinion reviewed and the exact fact pattern in the GoodRx and BetterHelp enforcement actions | None, automatic red flag (Section 5) regardless of category or package |

**Outreach implication:** the 15 20 interview slate should be weighted toward the "acceptable" rows first (non endemic corporates, health adjacent consumer brands, foundations) to get clean signal on H2 without the confound of compliance uncertainty, then move into "conditional" categories (pharma, payers) once counsel has reviewed the specific arrangement, sequencing is detailed in Section 7.

## 7. Outreach Sequencing for the 30 Day Plan

Total target: 15 20 conversations across 8 stakeholder categories (execution brief §21). Sequencing below prioritizes categories with the cleanest regulatory read (Section 6) first, so early signal is not confounded by unresolved compliance questions, while still covering every required category within 30 days.

| Week | Focus | Target categories | Target count this week | Cumulative |
| | | | | |
| **Week 1** | Warm up + acceptable categories | Non health corporate sponsors, health adjacent consumer brands, sponsorship intermediaries (who can also help identify the other categories' right contacts) | 4 5 | 4 5 |
| **Week 2** | Continue acceptable categories + intermediary sourced leads | Consumer health brands, foundations, employers | 4 5 | 8 10 |
| **Week 3** | Move into conditional categories, after counsel input requested in parallel | Pharma media buyers, healthcare agencies, payers | 4 5 | 12 15 |
| **Week 4** | Fill gaps, re approach high potential L1/L2 contacts for deeper WTP elicitation, chase L3→L4 conversions | Whichever categories are under represented; second touch on the most qualified Week 1 3 contacts to push toward procurement | 3 5 | 15 20 |

**Sequencing rules:**
* Do not initiate outreach to pharma manufacturer contacts (Section 6 "conditional") until the compliance review question has at least been formally opened with counsel (does not need to be resolved, but the question needs to be in flight per `regulatory_notes.md` §8's questions 2 5), this avoids making commitments in a conversation that later has to be walked back.
* Sponsorship intermediaries should be contacted early (Week 1) specifically because they can shortcut the "who is the right contact" problem across multiple categories at once, treat them as a force multiplier on scheduling, not as a category to be counted 1:1 toward the 15 20 target's diversity requirement.
* Any contact that triggers a red flag (Section 5/6) in the first conversation should be closed out promptly (documented, not chased for a second meeting) rather than allowed to consume Week 3 4 capacity that should go to qualifying additional prospects (needed for the "≥2 additional qualified prospects continuing" success criterion).
* Track weekly against the primary metrics (Section headers reproduced from execution brief §21: WTP per eligible patient, paid pilot willingness, buyers entering procurement, contract value, pilot budget, sales cycle duration) so a stalled week is visible immediately, not discovered at day 30.

## 8. LOI / Pilot Term Sheet Skeleton

**Plain language skeleton for internal use and as a discussion starting point with a candidate design partner. This is NOT a legal document and must be reviewed by counsel before any external commitment, flagged explicitly per the constraint below.**

> **FLAG FOR COUNSEL REVIEW:** every clause below touches at least one issue in `research/regulatory_notes.md` §7's risk table (HIPAA marketing authorization, AKS/CMP, FDA promotional rules, or state consumer health data law). Do not send this skeleton, or any version of it, to a prospective sponsor without counsel sign off on the specific structure (entity, states of operation, sponsor type) per `regulatory_notes.md` §8.

**1. Parties and structure**, Legion [entity/MSO/PC to be determined by counsel per `regulatory_notes.md` §5.1 CPOM considerations] and Sponsor [Name]. Placeholder pending counsel's determination of which Legion entity should be the contracting party.

**2. Purpose**, A time boxed pilot to test Package [A/B/C] as described in Section 1 of this document, for the purpose of validating sponsor willingness to pay and program feasibility; explicitly not a marketing arrangement targeting individual patients by health condition.

**3. Pilot fee**, **[PLACEHOLDER, amount TBD]**, to be set at or above the greater of (a) the the model's `required_arpu_usd_per_patient_per_yr` threshold for the pathway in scope (pro rated for pilot duration and cohort size), and (b) the qualified WTP established in buyer interviews (Section 6, L3). A pilot fee of $0 does not satisfy the "paid pilot" success criterion and should not be represented as a signed pilot for evidence ladder (Section 5) purposes.

**4. Duration**, **[PLACEHOLDER, e.g., one calendar quarter]**, consistent with the "~90 day procurement path" success criterion; renewal contingent on aggregate program metrics only (Section 1's reporting terms), not patient level outcomes.

**5. Cohort/scope definition**, Number of eligible patients or exposure volume covered (per Package A/B pricing logic, Section 2); eligibility criteria set solely by Legion's clinical/financial need rules, with no sponsor input into individual patient selection.

**6. Aggregate reporting only clause**, Sponsor will receive only aggregate, cohort level metrics (patients served, aggregate engagement/completion rate, aggregate satisfaction) on a defined cadence (e.g., quarterly); no report will disclose any cell smaller than [minimum cell size, e.g., n=X] to prevent re identification; no patient identifiable, diagnosis level, or session level data will be provided under any circumstance.

**7. No data clause**, Sponsor receives no PHI, no patient level data, and no data enabling patient or provider re identification, under this agreement or any related analytics/attribution arrangement; no ad tech pixel, SDK, or tracking technology provided by or attributable to Sponsor will be placed on any authenticated clinical page (per the BetterHelp/GoodRx enforcement precedent, `regulatory_notes.md` §2).

**8. No clinical influence clause**, Sponsor has no role in, and no right to review or approve, clinical protocols, provider assignment, patient provider matching, prescribing decisions, or care plans; any sponsor provided educational content (Package C) is subject to Legion clinical review with no sponsor edit rights over clinical claims, and is structurally and visibly separated from clinical recommendations.

**9. No prescribing/referral incentive clause**, No portion of the pilot fee, renewal terms, or any bonus/performance structure is tied to prescribing rates, referral volume, or any patient level clinical or commercial outcome; program eligibility and continuation are never conditioned on the sponsor's product being prescribed, recommended, or discussed.

**10. Termination and kill criteria linkage**, Either party may terminate on [X days'] notice; Legion may terminate immediately, without penalty, if continuing the arrangement would require violating clauses 6 9 above, or if patient side testing (companion `experiment_spec.md` / patient side test per execution brief §22) shows material harm to trust or continuation attributable to the sponsorship, i.e., the commercial term sheet is explicitly subordinate to the patient side kill criteria, not independent of them.

**11. Disclosure to patients**, Patients will be informed, in plain language during intake/consent, that this program is supported by Sponsor [Name], with no clinical influence and no data sharing, consistent with the disclosure practice discussed in `regulatory_notes.md` §6; disclosure language subject to Legion legal/compliance review, not sponsor drafted.

**12. Governing constraints (restated, non negotiable)**, All terms in this skeleton are subject to the constraints in `decision_framework.md` Gate 4 and the risk table in `regulatory_notes.md` §7; any sponsor request to modify clauses 6 9 is a red flag (Section 5/6 of this document) requiring escalation, not routine negotiation.

## Handoff

**Key Findings**

* A complete, execution ready sponsor test package now exists: three sponsor concepts with explicit "never gets" boundaries, a rate card formula (not a number) tied to the the model's `required_arpu_usd_per_patient_per_yr` output and to external benchmarks (GoodRx pharma solutions ~$10 15/patient/yr, employer PEPM $36 4,200/patient/yr, health vertical eCPM $20 45), a 45 minute interview guide with exact question wording including a B2B adapted Van Westendorp module, a 12 point qualification scorecard, a five level evidence ladder (L1 polite interest through L5 signed paid pilot), a sponsor category matrix grounded in the regulatory research's OIG Advisory Opinion pattern, a week by week 30 day outreach sequence, and a plain language LOI/term sheet skeleton with every non negotiable clause flagged for counsel.
* The the model (in progress concurrently) shows `required_arpu_usd_per_patient_per_yr` for the fixed fee sponsorship model spans roughly $61/patient/yr (high cost efficiency, AI driven pathway) to several thousand dollars/patient/yr (traditional pathway, low cost scenario), meaning the sponsor test cannot be scored against a single WTP number; it must be scored against the threshold for the specific pathway under discussion.
* The regulatory research's single most load bearing finding, that sponsor access to any identifiable patient/provider data is the most consistent factor separating favorable from unfavorable OIG outcomes, and the direct cause of the GoodRx and BetterHelp enforcement actions, is now embedded as a structural constant across all three packages, the interview guide's red flag probes, the qualification scorecard, the evidence ladder, and every clause of the term sheet skeleton, rather than appearing once as a caveat.

**Decision Implications**

* This package operationalizes H2 but does not resolve it, resolving H2 requires actually running the 15 20 interviews and recording real WTP, qualification scores, and ladder levels against the thresholds this document defines.
* Because the required ARPU threshold is pathway dependent by 1 2 orders of magnitude, the sponsor test team should agree with the model owner, before interviews begin, on which specific pathway (traditional / AI supported / AI driven) and cost scenario (low/base/high) is being pitched to buyers, pitching an undefined "care experience" risks collecting WTP data that cannot be cleanly compared to any single threshold.
* The category matrix implies a two speed outreach: acceptable categories (non endemic corporates, health adjacent brands, foundations, employers) can proceed immediately; conditional categories (pharma, payers) should not receive outreach until the compliance review conversation with counsel is at least underway, per `regulatory_notes.md` §8.

**Remaining Unknowns**

* No interviews have been conducted yet; every figure in this document is a pre test benchmark or model placeholder, not observed buyer behavior.
* The the model's assumptions (cost per patient, patients per year, target margin) are themselves still labeled placeholder/unresolved in `model/assumptions.csv`, the required ARPU threshold this package references will move as those assumptions firm up.
* Whether any candidate sponsor's legal/compliance function will accept the no data/no influence structure in practice (as opposed to in a first conversation) is unknown until a term sheet is actually negotiated, Section 8's skeleton is untested against a real counterparty's counsel.
* The actual per module pricing logic for Package C (Sponsored Education) has no clean external per unit benchmark (noted in Section 2.2); this package will likely require more interview driven price discovery than A or B before any number can be proposed.

**Recommended Next Action**

Coordinate with the the model owner to fix, before the first interview, which single pathway/scenario combination will be used as the WTP anchor across all 15 20 conversations (to keep responses comparable), and open the counsel review conversation now (per `regulatory_notes.md` §8, questions 2 5) so conditional category outreach (pharma, payers) is not delayed past Week 3 of the 30 day plan in Section 7.
