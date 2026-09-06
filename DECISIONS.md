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

---

## 2026-09-06 — Entry 013 — G — Seasons in scope per tier

**Question.** Which seasons does each tier cover? (Supersedes Entry 010, which
deferred this pending the coverage report. The original entry is left intact.)

**Status.** CLOSED.

**Option chosen.** Tier A 2006–2026 (21 seasons). Tier B 2018–2026 (9 seasons).

**Alternatives rejected.** None on Tier B — the boundary is a fact about the data
source, not a preference. FastF1 returns no lap data whatsoever for 2014–2017 on
every probe; 2018–2026 return `LapTime` at 92.6–99.9%, `Compound` at 100%,
`TyreLife` at 97.3–100% and `TrackStatus` at 100% in every probed session.

**Reason.** Verified empirically per the plan's requirement rather than adopting
the commonly cited 2018 figure on trust. The figure happened to be right; the
verification was still necessary, and it also produced the field-completeness
numbers the pace model depends on.

**Consequence recorded.** Tier B is **corroboration only** and cannot carry an
independent conclusion: its placebo pool is 2 boundaries, and the 2021–22
boundary's Tier B pre-period is 2018–2020 of which 2019 and 2020 are both flagged
discontinuities, leaving one unflagged pre-season. Stated in the plan, in the
memo wherever a Tier B result appears, and in the README so a reader need not
find it.

---

## 2026-09-06 — Entry 014 — B″ — Tier A segment eligibility by era

**Question.** Phase 1 found that qualifying in 2006–2009 was run on race fuel:
`median(Q3−Q2)` is positive in all four of those seasons (+0.45 to +1.70 s) and
negative in all seventeen from 2010 (−0.15 to −0.37 s), with no overlap and the
sign flipping exactly on the refuelling ban. The Entry 003 evolution adjustment
reads that offset as track evolution, so in 2006–09 it credits heavy-fuel laps by
up to 1.7 s — a systematic bias correlated with fuel strategy, affecting roughly
a quarter of team observations in those seasons. How should Tier A scope respond?

**Status.** DECIDED.

**Option chosen.** **Option 3** — Q3 excluded in 2006–2009; all three segments
from 2010; evolution adjustment as in Entry 003, needing only `E(Q1→Q2)` for the
earlier era.

**Alternatives rejected.**
- *Option 1, raise the Tier A floor to 2010.* Rejected as primary: it deletes the
  2009 boundary, which §8.5 identifies as the least contaminated in the study,
  and starts the series on the refuelling-ban discontinuity — so it buys less
  cleanliness than it appears to. **Retained as R8 variant O1.**
- *Option 2, Q1+Q2 only in every season.* Rejected: Finding E (the Q2
  starting-tyre rule) lands directly on it, and option 2 rests its entire weight
  on Q2. **Retained as R8 variant O2.**
- *Option 4, Q1 only.* Rejected: the −0.43 s Q1→Q2 delta *is* the sandbagging,
  and it is worst at the front, where M4 and M5 measure. **Retained as R8
  variant O4.**

**Reason.** The estimand is low-fuel maximum-attack pace. In 2006–09 Q3 does not
measure that estimand at all — it measures something else. Excluding a
non-observation preserves the rule ("use every segment that measures the
estimand") while its realisation changes because the sport changed what Q3 was.
That is categorically different from tuning the estimator to suit an era.

**Condition 1 — R8 promoted to a four-way sweep.** All four options run as
robustness, not merely the segment-rule variants originally scoped.

**Condition 2 — pre-committed decision rule, fixed before results exist.** O1
excludes the 2009 boundary; O3 retains it on Q1/Q2 evidence. These are the two
defensible treatments and they rest on different data. **If the sign or the
significance of the 2009 boundary estimate differs between O1 and O3, the memo
reports 2009 as INDETERMINATE.** We do not select whichever option produces the
cleaner story. Committed here, in advance, because it will be tempting to break
later.

**Condition 3 — an unnamed cost, now named and measured.** Option 3 measures
front-running teams on a Q1/Q2 lap in 2006–09 and on a full-attack Q3 lap from
2010. Because front-runners demonstrably do not fully attack in Q1/Q2, that is an
era-dependent bias concentrated at exactly the ranks M4 and M5 measure. The
engineering role had offered Q1→Q2 median stability across eras as reassurance;
the analyst rejected that as insufficient — **identical medians do not establish
identical composition**, and if the 2006–09 offset mixes track evolution and
sandbagging differently, the adjustment is biased in a way the medians conceal.
Diagnostic D1 (plan §4.1.2) now tests composition directly: D1a estimates the
Q1→Q2 offset separately by competitive stratum and asks whether the
front-minus-back difference shifts across the 2010 line; D1b reports
segment-source composition by field position; D1c tests M4 and M5 for a step at
2010 with M1 and M2 as controls. Added as confound 15. **If the front-of-field
metrics behave differently across the 2010 line, that is a reported finding.**

---

## 2026-09-06 — Entry 015 — 2009 boundary framing

**Question.** Is the 2009 boundary correctly described as "clean"?

**Status.** DECIDED — corrected.

**Option chosen.** **"Least contaminated," never "clean."** The word "clean" is
not used of this or any boundary in the plan or the memo.

**Reason.** Analyst correction of the engineering role's framing. "No intruding
reset" is a narrow claim and "clean" overstated it. The 2009 boundary carries at
least four co-occurring shocks that no model here separates, now listed as
confound 14: three simultaneous technical changes (aero reset, slick tyres,
KERS); Honda's withdrawal producing Brawn as a new entity inside the window,
which the continuity mapping treats as continuous when it arguably is not; the
2008 financial crisis reshaping grid budgets during the pre-period, an
uncontrolled shock to precisely the resource asymmetry the metric is sensitive
to; and race-fuel qualifying across the entire pre-period and boundary season.

---

## 2026-09-06 — Entry 016 — C3 revision — intent contrast demoted

**Question.** Should the Intent-R contrast occupy a confirmatory test slot?
(Revises Entry 006, which is left intact.)

**Status.** DECIDED.

**Option chosen.** **No.** Both intent contrasts are descriptive only. The
confirmatory family drops from 3 tests to 2 (pooled `b2`, pooled `b3`), and the
freed slot is **returned to the budget, not reallocated**, so the Holm correction
across the family is correspondingly less severe.

**Alternatives rejected.**
- *Keep Intent-R confirmatory* — a 3-versus-2 contrast does not justify spending
  family-wise error budget on a question the data cannot answer.
- *Reallocate the freed slot to another test* — rejected; the budget shrinks.

**Reason.** Analyst decision. The finding itself stands and is retained in full,
including the two-column split and the source citations. What changes is its
status: **the observation that Intent-C is untestable — because the regulator
almost never publicly promised the thing this analysis measures — is a finding
about the question, not a failed test.** It moves to the memo's opening framing
beside the raceability-versus-convergence gap. An analysis measuring pace
convergence is measuring something the regulator, on its own public record,
mostly did not claim to be delivering, and that reframes what a null result would
even mean.

---

## 2026-09-06 — Entry 017 — Regulator statement as intent evidence

**Question.** During Phase 1 research the engineering role found a contemporaneous
statement by a principal author of the 2022 regulations about how the field would
behave, and excluded it from the plan under the Entry 009 constraint (b)
prohibition on directional priors, flagging rather than silently dropping it.
Should it be included?

**Status.** DECIDED.

**Option chosen.** **Include**, in the intent evidence section (plan §2.4), with
citation, under a binding handling rule.

**Reason.** Analyst ruling: constraint (b) is about not seeding *our own*
expectation of the result, not about suppressing documentation of what the
regulator publicly claimed — which is the raw material of the intent
classification. Excluding it would have left the intent evidence incomplete.

**Handling rule, binding.** The statement substantiates that the 2021–22 package
was publicly framed as a long-run convergence measure. It must not appear in the
results narrative, the memo abstract, the figure captions, or any text adjacent
to an estimate, and must never be described as a prediction our results confirm
or contradict. The §1 prohibition on directional priors covers third-party
predictions quoted approvingly, not only our own.

**Source.** Motorsport Week, 13 May 2021,
<https://www.motorsportweek.com/2021/05/13/brawn-expects-field-to-spread-under-new-2022-regulations/>

---

## 2026-09-06 — Entry 018 — §6.3 deleted-lap filter removed

**Question.** Does Jolpica expose a deleted / invalidated qualifying lap field?
(Plan §6.3 required this be probed, not assumed.)

**Status.** DECIDED — filter removed.

**Option chosen.** **Removed as unimplementable.** Every qualifying result across
all 21 seasons carries exactly `number, position, Driver, Constructor, Q1, Q2,
Q3`. No unknown fields appear in any season. Per the original instruction the
filter is removed rather than left as a rule that silently never fires.

**Reason.** Empirical, and the plan pre-committed to this outcome.

**Bias recorded as confound 13.** A lap deleted for track limits that nonetheless
appears in the published times slightly flatters that team. Critically this is
**time-varying** — automated track-limits enforcement became markedly more
aggressive later in the study window — so it sits inside a time-series analysis
of exactly the quantity it biases. It cannot be bounded from this source and is
not dismissed as noise.

---

## 2026-09-06 — Entry 019 — Confirmed without change

Recorded so the ledger shows what was reviewed and left alone, not only what
moved. All confirmed by the analyst at Amendment 1:

- H2 downgraded to descriptive estimate; "faster than in a stable period" banned;
  confirmatory slot retained so the budget is not quietly reduced. The
  three-season maximum stable-regulation period is a finding about F1's
  regulatory cadence and belongs in the memo body.
- Placebo pools: Tier A 9, Tier B 2. Tier B's placebo is powerless and a null
  there is never presented as reassurance.
- R14 and R15 added; battery of 15; reporting rule becomes "fewer than 10 of 15."
  Two-thirds ratio preserved exactly, wording intact.
- Placebo test runs regardless of outcome; falsification criteria as written;
  raw-median baseline comparator; pace model ship gates; confounds 1 and 2 stay
  in the memo body rather than LIMITATIONS.md.
- Finding E (the Q2 starting-tyre rule) remains **unverified**. The Phase 2
  compound test proceeds; if confirmed it is added to the confound list and the
  robustness battery by amendment commit, not asserted in the meantime.
