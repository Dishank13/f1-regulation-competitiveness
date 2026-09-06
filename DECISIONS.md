# Decision ledger

Every judgment call in this analysis that the data does not make for us.

**This file is append-only.** Resolving a decision adds a new entry; it never
edits an earlier one. Reversing a decision adds an entry saying so. The status of
any decision is given by its most recent entry. There is deliberately no summary
index at the top, because maintaining one would require editing.

Decisions listed as OPEN or DEFERRED are recorded here with no answer. A reader
should be able to see **which questions existed from the start**, not only the
ones that were resolved — an analysis that only documents its answered questions
hides the shape of what it chose not to ask.

Roles: the analyst (Dishank Shah) owns every decision below. The engineering
role presents options, trade-offs, and a recommendation, and does not resolve
them.

---

## 2026-09-06 — Entry 001 — A — Representative-lap thresholds

**Question.** What percentage-off-best cutoff excludes a non-representative lap?
What traffic gap counts as clean air? What is the minimum lap count for a team to
have an observation at an event? How are wet and mixed sessions handled?

**Status.** DEFERRED to Phase 2.

**Option chosen.** None yet. Provisional working values, explicitly not decided:
107% of the driver's own session best, traffic gap 1.0 s, minimum 5 laps.

**Alternatives rejected.** None yet — deciding now would be rejecting
alternatives without evidence.

**Reason for deferral.** Every one of these numbers is arbitrary until the
row-loss ledger exists. A 107% cutoff that removes 4% of laps and one that
removes 40% are different decisions wearing the same number. The analyst has
required the ledger before any threshold is set, and R7 sweeps the range
regardless of what is chosen.

---

## 2026-09-06 — Entry 002 — B — Primary competitiveness metric

**Question.** Which of M1–M6 leads the memo, and why are the others secondary?

**Status.** DEFERRED to Phase 4.

**Option chosen.** None yet.

**Alternatives rejected.** None yet.

**Reason for deferral.** The candidates must be computed and their behaviour
shown before one is chosen, and the choice must be frozen before the confirmatory
tests are run. Choosing now would be guessing; choosing after seeing test results
would be fishing. Phase 4 is the only correct point. Note that R8 (Entry 003) was
deliberately moved *earlier* than this decision, because the segment rule
interacts with the time-series structure and must be settled first.

---

## 2026-09-06 — Entry 003 — B′ — Qualifying segment rule

**Question.** A team's qualifying representative time can be its best lap in any
segment, its Q1 lap only, or a segment-evolution-adjusted best. Which is primary?

**Status.** DECIDED.

**Option chosen.** Segment-evolution adjusted (plan section 4.1). The per-event
offset between adjacent segments is estimated from within-driver differences
among drivers who set times in more than one segment, so car and driver quality
cancel. R8 additionally runs **before** the metric freeze, not after.

**Alternatives rejected.**
- *Best lap in any segment* — retained as an R8 robustness variant, not primary.
- *Q1 only* — retained as an R8 robustness variant, not primary.

**Reason.** The engineering role originally recommended best-of-any-segment for
interpretability. The analyst reversed it, on the grounds that the plan's own
section 4.1 states the Q1/Q3 track-evolution bias *varies with format changes
over time*. A time-varying bias sitting inside a time-series analysis of exactly
the quantity being biased is not acceptable as a primary specification — the bias
would be partly indistinguishable from the effect being estimated. Interpretability
is worth less than not confounding the estimand. The same reasoning moved R8
ahead of the metric freeze: if the segment rule changes the answer, that must be
known before the primary metric is chosen, not discovered as a Phase 6 footnote.

---

## 2026-09-06 — Entry 004 — C1 — Team continuity mapping

**Question.** Is a rebranded constructor a continuation of the same entity or a
new one?

**Status.** DECIDED.

**Option chosen.** Continuity mapping as primary — a constructor lineage is one
entity across rebrands. Strict mapping built and run as R2.

**Alternatives rejected.**
- *Strict mapping as primary* — each constructor name its own entity.
- *Case-by-case adjudication* — rejected as unfalsifiable; it would let the
  mapping be tuned to the result.

**Reason.** A rebrand usually retains the factory, the wind tunnel, and most of
the staff, which is what actually produces car performance. Under strict mapping
the Jordan → Aston Martin lineage becomes five short unrelated series, fragmenting
time-series windows that plan section 8.5 already shows to be badly collided. The
cost is real and recorded: genuine entity changes such as Brawn in 2009 are
treated as continuous when they arguably are not. Both mappings are built, so the
cost is measurable rather than assumed away. Ambiguous cases are listed
individually in the mapping file with reasoning.

---

## 2026-09-06 — Entry 005 — C2 — Reset list and boundary definition

**Question.** Which regulation changes count as resets to be tested?

**Status.** DECIDED.

**Option chosen.** Five boundaries: 2009, 2014, 2017, **2021–22 merged**, 2026.

**Alternatives rejected.**
- *2021 and 2022 as two separate boundaries* — rejected.
- *Adding 2010 (refuelling ban) or 2019 (front wing) as resets* — rejected;
  retained instead as flagged discontinuities excluded from the placebo pool.

**Reason.** Merging 2021 and 2022 was the analyst's revision. Plan section 10
confounds 1 and 2 argue that the cost cap, the sliding-scale aerodynamic testing
restrictions, and the ground-effect aero reset are collinear in time and cannot
be separated; testing them as independent boundaries would contradict the plan's
own stated limitation and would count one intervention twice, inflating the
multiplicity budget with a test that is not independent.

**Consequence recorded at decision time.** The merge creates a staged
intervention — cost cap and ATR begin in 2021, aero in 2022 — that a single
breakpoint cannot represent. Plan section 2.4 therefore fits two specifications
(breakpoint at 2021; and a two-season transition window excluded from both
segments) and reports both. This consequence was surfaced by the engineering role
at the time of the decision, not discovered later.

---

## 2026-09-06 — Entry 006 — C3 — Intent classification of each reset

**Question.** Was each reset publicly justified as a convergence or closer-racing
measure? Does the regulator's stated aim predict anything about the outcome?

**Status.** DECIDED, with a limitation recorded.

**Option chosen.** Two intent columns, not one (plan section 2.1):
- **Intent-R** — publicly justified as closer racing / more overtaking.
  Yes: 2009, 2021–22, 2026. No: 2014, 2017.
- **Intent-C** — publicly justified as *field performance convergence*.
  Yes: 2021–22 only. No: all others.

Classification verified against contemporaneous sources, cited in plan section
2.1. Phase 1 attempts to upgrade each from press reporting to a primary FIA
source; any that cannot be upgraded is marked press-sourced in the memo.

**Alternatives rejected.**
- *A single binary intent column* — rejected. "Closer racing" and "a closer
  field" are different claims that the regulator makes separately. Collapsing
  them would score raceability-justified resets against a convergence metric they
  never claimed to move.
- *Assuming intent from the nature of the change* — rejected by explicit analyst
  instruction; every classification is sourced.

**Reason.** The analyst added intent classification to ask a question the placebo
test cannot: placebo asks whether resets differ from ordinary seasons, intent
asks whether the regulator's stated aim predicts anything at all.

**Limitation recorded at decision time.** The Intent-R contrast is 3 boundaries
versus 2 — severely underpowered, able to detect only an enormous difference, and
close to uninformative if null. **Intent-C cannot be tested at all**: only one
boundary is convergence-intended, and it is the boundary most contaminated by
confounds 1 and 2. Since Intent-C is the dimension our metric actually measures,
the honest statement is that the sport rewrote its rules five times in this period
and explicitly promised a closer *field* once. Both limitations are stated in the
memo alongside the estimate rather than in a footnote.

---

## 2026-09-06 — Entry 007 — D — Sprint weekends

**Question.** Include sprint weekends, exclude them, or handle them separately?

**Status.** DECIDED.

**Option chosen.** Include, carrying a **format-version indicator** derived
empirically from observed session structure per event in Phase 1. R5 retained.

**Alternatives rejected.**
- *Exclude sprint weekends* — would drop a substantial share of recent events and
  create a calendar-composition confound of its own, precisely in the seasons
  bracketing the most recent boundaries.
- *A binary sprint / non-sprint flag* — rejected by the analyst. The sprint format
  has itself changed more than once, and the versions differ in how much running
  precedes the grid-setting qualifying session, which is the mechanism by which
  the format could affect measured spread. A binary flag would pool formats that
  differ in exactly the relevant way.
- *Hardcoding the version boundaries from recollection* — rejected. Versions are
  derived from data; any contradiction is corrected in the coverage report and
  committed.

---

## 2026-09-06 — Entry 008 — E — Partial 2026 season

**Question.** Include the in-progress 2026 season, or exclude it?

**Status.** DECIDED.

**Option chosen.** Include, labelled provisional **in every chart caption** and
everywhere else it appears. R11 re-runs the analysis without it.

**Alternatives rejected.**
- *Exclude entirely* — the memo would then have nothing to say about the reset
  that prompted the question.
- *Include without a provisional label* — indefensible.

**Reason.** Both the inclusion and the caveat are required; neither alone is
honest. Recorded consequence: 2026 is simultaneously the partial season and the
boundary with only one post-period season (plan section 8.5), so its estimate is
the weakest of the five on two independent grounds.

**Related instruction.** The analyst directed that the number of constructors per
season be **verified empirically in the coverage report and stated as fact**,
replacing conditional speculation about grid expansion in the confound list. Plan
section 10 confound 4 was rewritten accordingly.

---

## 2026-09-06 — Entry 009 — F — Effect horizon

**Question.** Does the year-one level change (H1) or the post-reset slope (H2)
lead the memo?

**Status.** DECIDED, with H2 subsequently downgraded on technical grounds.

**Option chosen.** H1 leads; H2 gets equal billing. Two binding constraints added
by the analyst:

1. **Pooled estimate leads.** Because plan section 8.2 gives one treated unit per
   boundary, the memo leads with a random-effects pooled estimate across
   boundaries (plan section 8.3), with per-boundary estimates as underlying
   detail. Between-boundary heterogeneity is reported alongside the pooled value
   always, and small-k confidence intervals use the Hartung–Knapp–Sidik–Jonkman
   adjustment.
2. **No directional prior may be stated anywhere** — not in this plan, not in
   code comments, not in memo drafts. The framing must read identically whether
   H1 is positive, negative, or null. Plan section 1 was rewritten to remove a
   directional expectation the engineering role had included, and plan section 9
   was rewritten so the narrowing, widening, and null outcomes are stated in
   parallel.

**Alternatives rejected.**
- *H2 leads* — would let a convergence trajectory bury the year-one result.
- *H1 alone* — would omit whether the field subsequently converges.
- *Per-boundary estimates as the headline* — rejected; one treated unit per
  boundary cannot carry a headline, and a within-boundary bootstrap resamples
  events, not histories, so it cannot represent that uncertainty.

**Downgrade recorded at pre-registration.** Plan section 8.5.1 computes that the
longest uninterrupted stable-regulation period in 2006–2026 is **three seasons**.
H2 is defined against "a comparable stable-regulation period," and three seasons
cannot support a credible comparison slope. H2 is therefore downgraded from
hypothesis to descriptive estimate; the phrase "faster than in a stable period"
is not used. Its confirmatory slot is retained so the multiplicity budget is not
quietly reduced. This is a limitation of the sport's regulatory cadence, not of
the data source: F1 has not left the rules alone long enough to establish a
baseline.

---

## 2026-09-06 — Entry 010 — G — Seasons in scope per tier

**Question.** Which seasons does each tier cover?

**Status.** DEFERRED to Phase 1, pending the coverage report.

**Option chosen.** None yet. Working assumptions to be tested, not asserted:
Tier A 2006–2026 (2006 being the first knockout-qualifying season, so the
earliest with a comparable format); Tier B from the earliest FastF1 season with
complete lap, stint, compound, and track-status data, commonly cited as 2018 but
**to be verified season by season**.

**Alternatives rejected.** None yet.

**Reason for deferral.** Explicit analyst instruction, and correct on the merits:
the tier boundaries determine the window collisions in plan section 8.5 and the
placebo pool sizes in section 8.6, both of which are already tight. Assuming
coverage and discovering later that it does not exist would invalidate those
computations.

---

## 2026-09-06 — Entry 011 — H — Interpretation of results

**Question.** What do the results mean?

**Status.** OPEN — permanently, by design.

**Option chosen.** None. This decision does not close.

**Reason.** The engineering role reports what moved and by how much. The analyst
decides what it means. This entry exists so that a reader of the ledger can see
that interpretation was never delegated, rather than inferring it from the memo's
authorship.

---

## 2026-09-06 — Entry 012 — Plan corrections applied at pre-registration

Not decisions in the A–H sense, but recorded because they changed the plan
materially before it was frozen. All were raised by the analyst reviewing the
engineering role's draft.

1. **Rank hardcoding (plan 4.2).** M3 hardcoded ranks 4–7 as the midfield, which
   is not comparable across a study period in which grid size varies. M3 and M4
   redefined by percentile; M5 retained as rank-based because "the second-fastest
   car" is grid-size invariant in meaning; M6 retained as grid-size sensitive *by
   construction* and repurposed as a diagnostic for confound 4. Fixed-rank forms
   kept as R15. All metrics audited for the same fault.
2. **Window collisions (plan 8.5).** The draft understated the problem. The
   collision table is now computed in advance: 2009 is the only boundary with no
   intruding reset, and its pre-period is truncated to three seasons. Consequence
   for H2 recorded in Entry 009.
3. **Placebo pool size (plan 8.6).** The draft did not state it. Computed:
   Tier A has 9 clean control boundaries, **Tier B has 2**. A null placebo result
   in Tier B is not reassurance and is never presented as such. This is a second,
   independent reason Tier A leads.
4. **Deleted qualifying laps (plan 6.3).** The draft assumed the source marks
   deleted lap times. Phase 1 now probes for the field explicitly; if it does not
   exist the filter is **removed from the plan** rather than left as a rule that
   silently never fires, and the resulting bias is stated.
5. **Driver quality in team pace (plan 4.3).** Best-of-team imports driver skill
   into a car metric, unevenly across the period. Kept as primary for cross-tier
   consistency; both-drivers variant added as R14; reporting M7 alongside any
   best-of-team result made mandatory on the Writer role.
6. **R13 added.** Confound 8 named power-unit supply but no check tested it.
   Customer teams share a PU and are not independent observations, and two of the
   five boundaries are PU-led.
7. **Battery size and reporting rule (plan 11).** Battery grew from 12 to 15
   (R13, R14, R15). The two-thirds threshold set by the original "fewer than 8 of
   12" rule is preserved exactly: **fewer than 10 of 15** downgrades a claim from
   "finding" to "suggestive," in those words.
8. **Exact test counts (plan 8.4).** With the reset list final at five
   boundaries, the approximate counts were replaced with exact ones: 3
   confirmatory tests (Holm at alpha = 0.05), 10 secondary estimates (Holm within
   family), everything else exploratory (Benjamini–Hochberg at q = 0.10).

**Confirmed unchanged by explicit analyst instruction:** the placebo test runs
regardless of outcome (8.6); the falsification criteria (9); the raw-median
baseline comparator (4.3); the pace model ship gates (4.4); confounds 1 and 2
stay in the memo body rather than LIMITATIONS.md; and the section 11 reporting
rule keeps its wording.
