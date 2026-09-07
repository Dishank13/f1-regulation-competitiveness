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

---

## 2026-09-06 — Entry 020 — D1a — condition 3 tested, not detected

**Question.** Does the composition of the `E(Q1→Q2)` offset shift across the
2010 line, biasing the §4.1.1 adjustment in a way median comparison conceals?
(Entry 014 condition 3.)

**Status.** DECIDED — **tested, not detected at achievable resolution.**
Explicitly **not** recorded as "concern resolved."

**Result.** Front-minus-back offset −0.3035 s in 2006–09, −0.3330 s in 2010+.
Shift +0.0295 s, bootstrap 95% CI [−0.0472, +0.0938], containing zero.

**Reason for the wording.** A confidence interval containing zero is not an
equivalence test. This result rules out composition shifts larger than roughly
**0.09 s** and says nothing about smaller ones. The early era contributes 70
events against 337, so the asymmetry in precision is structural and cannot be
improved with the available data. A composition shift below the detection floor
remains possible and is not claimed to be absent.

**Analyst note.** Stating the detection floor rather than reading the CI as
equivalence was called out as the standard to hold. It is now the standard for
every null in this project, including the Tier B ledger and the Finding E test.

---

## 2026-09-06 — Entry 021 — D1b — unresolved; restriction rule pre-committed

**Question.** Front-third teams draw 0% of representative times from Q3 before
2010 and 57.7% after, with their Q1 share falling 42.6% → 20.7%. Is this benign?

**Status.** DECIDED — **unresolved, not benign.** Restriction rule fixed in
advance of D1c.

**Option chosen.** A measurement discontinuity located inside a study designed to
detect discontinuities, concentrated exactly where M4 and M5 measure, is treated
as a live threat rather than a caveat. Two commitments, both made before D1c runs
in Phase 4:

1. **Restriction rule.** If M4 or M5 shows a level shift at the 2010 season
   boundary at least half the median absolute level shift across the five reset
   boundaries on the same metric, then **M4 and M5 cannot carry a cross-2010
   claim**. They are restricted to within-era comparison and any boundary
   estimate spanning 2010 is **withdrawn from the memo, not caveated in it**.
2. **2010 joins the placebo battery** as a known measurement-artifact boundary,
   reported separately from the 9-boundary pool. A "reset effect" at a season
   with no reset but a large measurement change is diagnostic of **the method**,
   not of Formula 1, and is reported before any boundary result because it bears
   on whether the other estimates mean anything.

**Reason.** Written now precisely so it cannot be decided after seeing D1c.
"Comparable in magnitude" is given a numeric definition in advance for the same
reason.

---

## 2026-09-06 — Entry 022 — Stratum misspecification in the evolution offset

**Question.** D1a incidentally established that front-runners gain ~0.3 s more
than backmarkers between Q1 and Q2, in **both** eras, against a field-wide offset
of ~−0.43 s. Track evolution improves the track for everyone equally; this
differential does not. What follows?

**Status.** DECIDED — promoted from observation to confound 16, with a
robustness check and a restriction on claims.

**Option chosen.** Three consequences, all binding:

1. **R16 added** to the battery: the evolution offset re-estimated separately by
   field position (stratified offset) and everything re-run, testing directly
   whether the misspecification reaches the metrics. Battery grows to 16 checks;
   the two-thirds reporting threshold becomes **11 of 16** (10.67 rounded up —
   a robustness bar is not relaxed by arithmetic convenience).
2. **Confound 16** in its own right, not a sub-clause of confound 15.
3. **Restriction on absolute-level claims.** Because the differential is
   era-stable it biases the *level*, not the *trend*, so boundary estimates
   difference it out and survive. But the memo may **not** state a standalone
   field-spread figure without noting that it carries a stratum-dependent offset
   bias of order 0.3 s in the underlying lap times. Boundary comparisons are
   unaffected; absolute-level statements are not.

**Reason.** The §4.1 field-wide median offset is a weighted average of two
distinct quantities — track evolution and a position-dependent sandbagging
differential — and is therefore misspecified by stratum. The engineering role's
reasoning that era-stability confines the damage to level rather than trend was
accepted by the analyst as correct; the finding is nonetheless recorded in the
plan rather than left in a progress report.

---

## 2026-09-06 — Entry 023 — B1 — Brawn 2009 mapping robustness

**Question.** The Brawn 2009 transition is the most contestable call in the
continuity mapping (Entry 004) and sits inside the window of the least
contaminated boundary (confound 14). Does the 2009 result depend on it?

**Status.** DECIDED — targeted robustness run added.

**Option chosen.** **B1**: the 2009 boundary estimated under both
Brawn-as-continuation and Brawn-as-new-entity. **If the 2009 result depends on
that choice, the memo says so in the body**, not in a footnote.

**Placement.** B1 is a **boundary-specific** check and is reported separately
from the 16-check battery, not counted in it. Folding a one-boundary check into
the bar that gates every headline claim would misrepresent both — it would
inflate the battery with a check irrelevant to four of the five boundaries, and
dilute the specific warning B1 exists to raise.

**Reason.** Those two facts together — most contestable mapping call, inside the
least contaminated boundary — make this the single place where a mapping
judgement could most plausibly manufacture a result.

---

## 2026-09-06 — Entry 024 — Tier A ledger defects found by analyst review

Four defects in the first Tier A row-loss ledger, all found by the analyst, all
fixed. Recorded because the ledger is a correctness instrument and its own
failures belong in the audit trail.

**1. Event count did not reconcile — 412 in coverage §1, 411 in the ledger.**
Cause: **2025 r6 Miami Grand Prix**. The source returns 20 classified qualifying
entries but **every** `Q1`/`Q2`/`Q3` field is an empty string, so the event
produced zero cells and vanished from a cell-level ledger without ever being
logged as removed. This is an upstream data gap, not a parsing or format issue —
five other 2025 sprint-weekend rounds carry full times.
**Fix:** an explicit `E1` filter row now logs it, and the ledger gained a third
parallel unit track (events, alongside cells and team-events). Event-level
attrition was invisible in a cell-level ledger, which is exactly how this got
through. The final team-event count is unchanged at 4,327 — the fix is about
visibility, which was the point.

**2. Step kinds conflated.** L0 was typed `filter` but is a baseline; L3 was
typed `filter` but is a transformation. Neither can remove rows. The ledger's own
preamble says conflating step types is the failure it exists to prevent.
**Fix:** kinds are now `baseline`, `filter`, `transform`, `aggregate`, `guard`,
and only `filter`/`guard` carry a removal percentage.

**3. Unnamed L3 fallback event — and it was a bug.** The event was **2015 r16
United States Grand Prix**. Austin 2015 was rain-disrupted and produced Q1 (20
times) and Q2 (15 times) but **no Q3 times at all**, so the Q2→Q3 offset was
unestimable — and also unnecessary, because there were no Q3 times to adjust.
The flag was over-triggering: it fired whenever an offset could not be estimated,
including when that offset was not needed.
**Fix:** the flag now fires only when an offset is required for a segment that
actually carries times. There are now **zero** fallbacks; no observation in the
study carries a different measurement basis. The event sits in the placebo pool
(2015) and inside the 2014 and 2017 boundary windows, so getting this right
mattered; it stays, with no special status.

**4. T2 not validated to the standard of L2 and T1.** L2 and T1 were validated
against the distributions they screen (smallest session 18 entries vs threshold
12; smallest event 9 teams vs threshold 6). T2 was not.
**Fix:** T2 is now typed `guard` and stated plainly as **tautological** — `delta`
is built from a per-event minimum, so it is non-negative and finite by
construction and has no distribution to screen. It is retained as a runtime
assertion and is explicitly **not** presented as a validated filter.

---

## 2026-09-06 — Entry 025 — Decision D format indicator, implemented and verified

**Question.** Where is the sprint format-version indicator attached, which
session does Jolpica's qualifying endpoint return on sprint weekends, and does
any event yield two qualifying sessions? (Decision D, Entry 007.)

**Status.** DECIDED — implemented and empirically verified.

**Findings, all from data:**

- **Exactly one qualifying session per round in every season 2006–2026.** No
  round yields two. Checked by counting duplicate round numbers in the
  qualifying endpoint for every season: zero duplicates throughout.
- **The endpoint returns the Grand Prix qualifying** — the session that sets the
  race grid. Sprint shootouts are not in it; sprint races live on a separate
  `/sprint` endpoint. Confirmed by inspection: 2025 sprint rounds return normal
  Q1/Q2/Q3 with ~45 parseable times each, identical in structure to conventional
  rounds.
- **Therefore sprint weekends add, duplicate and remove no rows**, and do **not**
  interact with the Miami event-reconciliation fix in Entry 024. Miami 2025 was a
  sprint weekend, but so were five other 2025 rounds that carry full times; the
  gap is unrelated to format.
- **Four format versions, derived empirically**, from two cross-checked sources —
  the Jolpica `/sprint` endpoint (all seasons) and FastF1 `EventFormat` (2018+):
  `conventional`, `sprint` (2021–22, 3 events each), `sprint_shootout` (2023, 6),
  `sprint_qualifying` (2024–26, 6/6/5-so-far). **Zero cross-source
  disagreements.** This matches the plan's provisional expectation of four
  versions — but the schedule data is what makes it true, not the expectation.

**Attachment point.** `format_version` and `has_sprint_race` are event-level
columns on the team-event table, added by a `transform` step (F0) asserted to
change no row counts.

---

## 2026-09-06 — Entry 026 — Wet-session detection unavailable in Tier A pre-2018

**Question.** Plan §6.1 requires wet sessions be flagged and the primary analysis
run dry-only. Can Tier A do this?

**Status.** **OPEN** — gap identified, analyst decision required. Raised with the
Tier B ledger.

**Finding.** **No.** Tier A has no weather source: Jolpica exposes no weather
field in any season, and FastF1 weather begins in 2018. Systematic wet-session
detection is unavailable for Tier A across **2006–2017** — twelve of twenty-one
seasons, containing three of the five boundaries.

**Surfaced by** Austin 2015 (Entry 024, defect 3), which should have been caught
by the wet flag and was not.

**Explicitly rejected.** A spread-based proxy — inferring wetness from anomalous
within-event spread — is **circular** and will not be implemented. Spread is the
metric being estimated; inferring the filter from the outcome would launder the
result into the exclusion rule.

**Not resolved here.** Recorded as confound 17 and brought to the analyst rather
than papered over with a proxy.

---

## 2026-09-07 — Entry 027 — Format-version event-count bug

**Question.** The format-version table reported events summing to 46 against 411
in the final table.

**Status.** FIXED.

**Cause.** The aggregation counted distinct round *numbers* rather than distinct
`(season, round)` pairs. Round 1 recurs in all 21 seasons, so `conventional`
reported 23 — the number of distinct round numbers, not events. Team-events were
never affected, which is why they reconciled exactly (4042+60+165+60 = 4327) and
the join was sound.

**Fix.** Count distinct `(season, round)` pairs. Two assertions added so the
table cannot silently fail to reconcile again: event counts must equal the
final-table event count, and team-event counts must equal the final table length.
Corrected figures: conventional 383, sprint 6, sprint_shootout 6,
sprint_qualifying 16 — summing to 411.

---

## 2026-09-07 — Entry 028 — Confound 17 — uniform wet flag, source built

**Question.** Can a wet-qualifying filter be applied uniformly across 2006–2026,
rather than one that is strict from 2018 and absent before it?

**Status.** SOURCE BUILT AND CHARACTERISED. **Filtering decision NOT yet made** —
the FastF1 agreement test required by condition 2 is queued behind the 500
calls/hour rate limit, which the Tier B race acquisition holds and which is not
parallelised around per instruction.

**Framing accepted.** The analyst's reframing is recorded because it changed the
work: the problem was never that twelve seasons lack a wet filter. It was that
applying §6.1 as written yields a **time-varying exclusion rule inside a study
built to detect time-varying changes** — the same failure class as Finding B and
D1b, but self-inflicted. Uniform in both eras, or absent in both.

**Built.** Circuit coordinates and qualifying date from Jolpica; precipitation
from the Open-Meteo historical reanalysis archive. Non-circular by construction.
412 of 422 events have data; the 10 without are unraced 2026 rounds, recorded as
`future_session`.

**Condition 3 — resolution, stated plainly.** Qualifying *date* is available for
100% of events in all 21 seasons. Qualifying *time* is available **only from
2022**. A session-window flag is therefore impossible before 2022 and would
recreate the same cliff at a different year. The flag is **whole-day
precipitation at the venue on the qualifying date**, applied identically to every
season. A fixed local-time afternoon window was considered and **rejected**: it
is uniform in rule but not in accuracy, because night qualifying sessions grow as
a share of the calendar across the study window, so its error rate would drift
with time — reintroducing the failure class through the calendar.

---

## 2026-09-07 — Entry 029 — Confound 17 — three problems found

**Status.** Recorded ahead of the formal validation, because they bear on it.

**1. Over-flagging.** 33.6% of events flagged at daily ≥ 1.0 mm, 40.8% at
≥ 0.5 mm, 15.6% at ≥ 5.0 mm. Genuinely wet or mixed F1 qualifying is a small
minority of sessions; a third is trace and overnight rain counted as wet.

**2. Condition 5 — heavy season-level clustering.** At ≥ 1.0 mm: 2018 flags
71.4%, 2010 57.9%, 2017 50.0%, against 2026 at 7.7%. At ≥ 5.0 mm: 2010 42.1% and
2018 33.3% against **0.0%** for both 2007 and 2025. Not noise around a constant
rate. 2010 and 2018 both sit inside boundary windows.

**3. The date field is the SCHEDULED date, not the actual date — and it fails
hardest where it matters most.** Both of the two highest-precipitation events in
the dataset were hand-verified (condition 4) and both were postponed *because of*
the weather being detected:

- **2019 r17 Suzuka, 134.4 mm — the highest in the dataset. FALSE POSITIVE.**
  All Saturday running on 12 October was cancelled for Typhoon Hagibis;
  qualifying ran Sunday 13 October **in dry conditions**. The flag reports the
  wettest session in the study for a session that was dry.
- **2015 r16 Austin, 91.7 mm — TRUE POSITIVE, WRONG DAY.** Saturday qualifying
  was abandoned; the session ran Sunday 25 October with Q3 cancelled by rain.
  Genuinely wet, but on a different day from the one measured. Correct by
  coincidence.

This is structural, not two unlucky cases: sessions are postponed *because of*
severe weather, so the date field is systematically least reliable on exactly the
events a wet filter exists to catch, and the error correlates with the quantity
being measured.

**What the source gets right.** The high end is credible — Suzuka 2019 and 2010,
Austin 2015, Monza 2008 and 2017, Sochi 2021, Styria 2020, Imola 2022, Interlagos
2010. The reanalysis measures real rain at the right venues on the right
weekends. The failure is resolution and date accuracy, not meteorology.

**Preliminary assessment, explicitly not a decision.** Three independent problems
point the same way. If the FastF1 agreement rate is poor, the pre-agreed fallback
applies: no wet filtering in either era, stated as a limitation, wet-session
contamination added to the confound list. A filter that is wrong on the wettest
event in the study is worse than no filter, because it removes real sessions
while claiming rigour.

---

## 2026-09-07 — Entry 030 — Correction to an Entry 024 claim

**Question.** Entry 024 (defect 3) stated that Austin 2015's Q1/Q2 observations
"are adjusted on the same basis as every other event and carry no special
measurement status." Is that right?

**Status.** **CORRECTED. It was wrong.**

**What is wrong.** Austin 2015 qualifying ran on Sunday 25 October in wet
conditions, with Q3 cancelled by worsening rain. Its Q1 and Q2 observations are
**wet-session observations** and do not share a measurement basis with dry
events.

**What stands.** The L3 fallback *flag* was a genuine bug and its fix is correct:
the flag fired when an offset could not be estimated even where that offset was
not needed. Zero fallbacks remain. What does not stand is the reassurance
appended to it.

**Why recorded.** The claim was made in a committed ledger and in a commit
message. Correcting it in the ledger only, without an entry, would leave the
audit trail asserting something known to be false.
## 2026-09-07 — Entry 031 — Confound 17 RESOLVED — no wet filtering in either era

**Question.** Should Tier A apply a wet-session exclusion?

**Status.** DECIDED. **No wet-session filtering in either era.** Fallback applies.

**Option chosen.** Uniform treatment by *omission*: no wet filter anywhere in
Tier A, 2006–2026, stated as a limitation.

**Alternatives rejected.**
- *Open-Meteo whole-day flag as an exclusion rule* — rejected on three
  documented grounds (Entry 029): over-flagging (33.6% of events at ≥1 mm),
  heavy season-level clustering (2010 at 42.1% and 2018 at 33.3% versus 0.0% for
  2007 and 2025 at ≥5 mm, with 2010 and 2018 both inside boundary windows), and a
  date field that is the *scheduled* date rather than the actual one.
- *FastF1-only wet flag (2018+)* — rejected as the original problem: a filter
  strict from 2018 and absent before it is a time-varying exclusion rule inside a
  study built to detect time-varying changes.
- *Spread-based proxy* — rejected as circular.

**Deciding argument.** The date-accuracy failure is not a resolution problem that
a better threshold could fix. Sessions are postponed **because of** severe
weather, so the scheduled date is systematically wrong on exactly the events a
wet filter exists to catch, and the error **correlates with the quantity being
measured**. Suzuka 2019 — the highest-precipitation event in the entire dataset
at 134.4 mm — is a confirmed false positive: Saturday was cancelled for Typhoon
Hagibis and qualifying ran dry on Sunday. A filter that is wrong on the wettest
event in the study is worse than no filter, because it removes real sessions
while claiming rigour.

**Condition-2 validation deliberately NOT run.** The analyst directed that the
FastF1 agreement test be skipped: the decision does not hinge on it and it costs
rate-limit quota needed for Tier B acquisition. Recorded so the audit trail shows
this was a decision, not an omission.

**Consequences.**
1. Wet-session contamination is **unfiltered in Tier A** and enters the
   confound list as confound 18.
2. The contamination is **not randomly distributed** across seasons or circuits,
   so it is not white noise that averages out.
3. The Open-Meteo module stays in the repository, **unused**, with its failure
   written up. A rejected approach with a diagnosis is worth more than silence,
   and it stops the same idea being re-attempted from scratch later.

---

## 2026-09-07 — Entry 032 — R6 redefined

**Question.** R6 was "wet sessions in / out," which presupposes a wet flag that
now does not exist.

**Status.** DECIDED — redefined.

**Option chosen.** R6 becomes **sensitivity to excluding a small set of
hand-verified wet qualifying sessions**, confirmed individually from
contemporaneous sources, rather than a threshold sweep over a systematic flag.

**Confirmed members at time of writing:** 2015 r16 United States Grand Prix
(qualifying postponed to Sunday, Q3 cancelled by rain, pole set on a Q2 time).
Others are added only when confirmed from contemporaneous reporting and named
individually in the memo.

**Reason.** A hand-verified list is small, auditable, and honest about its own
incompleteness. A systematic flag would be larger, appear more rigorous, and be
wrong in a way that correlates with the outcome. R6 can no longer claim to test
sensitivity to *all* wet sessions and does not pretend to; it tests sensitivity
to the ones we can name.

---

## 2026-09-07 — Entry 033 — Process and environment changes

**Question.** Two operational failures and a scope change to how work proceeds.

**Status.** DECIDED.

**1. Shell text-processing banned.** Time and correctness were lost three times
to Git Bash quoting: heredocs failing twice, and an `awk '$1>1'` parsed as a
redirect that created a stray file *and* silently duplicated seven ledger
entries. A later duplication of entries 27–30 was committed in 3bbd4b7 before
being caught.

**Rule going forward:** no shell heredocs, no inline quoted awk/sed. Files are
written with the editor tool; text processing lives in Python modules under
`src/`. Shell is used only for git, running Python modules, and simple
inspection.

**2. Ledger reconciliation now fails loudly.** `src/ledger.py` is the only path
that mutates `DECISIONS.md`. It enforces on every append that entry numbers are
unique, contiguous from 1, in order, and that the post-append count equals the
pre-append count plus entries added. A failed append restores the file to its
pre-append content and raises. It caught the committed 27–30 duplication on its
first run, and its `repair` command refuses to act when duplicate blocks differ
in content rather than silently discarding one.

**3. Execution proceeds without approval checkpoints.** The analyst has directed
that design decisions are settled and what remains is execution. Tier B
acquisition, the Tier B ledger, the Finding E compound test, the Phase 3 pace
model with all §4.4 ship gates, and Phase 4 metrics including D1c all run
straight through. Findings are written up, logged here, committed, and the work
continues.

Work stops and returns to the analyst for only three things: Decision A
thresholds, Decision B primary metric freeze, and anything that **invalidates a
committed plan decision**. A finding that changes interpretation is recorded and
does not stop the run; only one that blocks the next step does.
## 2026-09-07 — Entry 034 — D1c result: M4 restriction TRIGGERED

**Question.** Does M4 or M5 show a 2010 level shift at least half the median
absolute reset-boundary shift, triggering the Entry 021 restriction?

**Status.** DECIDED by pre-committed rule. **M4 restricted. M5 not restricted.**

**Result.** M4 front gap shifts +0.827 at 2010 [95% CI 0.643, 1.118] against a
threshold of 0.306. Triggered. M5 front pair shifts +0.021 [−0.057, 0.132],
CI containing zero. Not triggered.

**Applied as written.** M4 cannot carry a cross-2010 claim and is restricted to
within-era comparison. Any M4 boundary estimate spanning 2010 is withdrawn from
the memo rather than caveated in it.

---

## 2026-09-07 — Entry 035 — D1c controls failed; interpretation changed, rule unchanged

**Question.** Plan §4.1.2 predicted the bias signature would be a step in
front-of-field metrics that the whole-field controls do not show. Did the
controls behave as controls?

**Status.** **No.** Recorded as a finding; does not block the run.

**Result.** M1 and M2 — the designated whole-field controls — also step sharply
at 2010, and more strongly in relative terms than M4:

| metric | 2010 shift ÷ median abs reset shift |
|---|---:|
| M2 IQR (control) | 1.93× |
| M1 sd (control) | 1.46× |
| M4 front gap | 1.35× |
| M5 front pair | 0.21× |

M2, a control, has the largest relative 2010 step of any metric.

**Consequence.** The 2010 discontinuity is **not specific to front-of-field
measurement**, so D1c cannot attribute it to segment-eligibility bias. Three
causes are collinear at 2010 and none is separable: grid composition (10 → 12
constructors, three new backmarkers; M6 moves 1.664 → 6.122), the refuelling ban,
and segment eligibility. The D1c design assumed the first two were not competing
explanations at that boundary. They are.

**The M4 restriction is NOT weakened by this.** It was pre-committed on observed
magnitude, not on a diagnosis of cause. Granting an exemption now, because a
competing explanation has appeared *after* seeing the result, is precisely what
pre-commitment exists to prevent. The restriction stands.

---

## 2026-09-07 — Entry 036 — A non-reset season out-moves the reset boundaries

**Question.** How large is the 2010 shift relative to the reset boundaries the
study exists to measure?

**Status.** RECORDED, not interpreted. Interpretation is Decision H.

**Finding.** The 2010 step exceeds the median absolute reset-boundary shift on
M1 (1.46×), M2 (1.93×) and M4 (1.35×). **2010 is not a reset season.** This is
the placebo logic arriving early and pointing at the method rather than at
Formula 1: if ordinary season-to-season churn — chiefly grid composition — moves
these metrics further than regulation resets do, then reset estimates are being
read against a baseline noisier than the effect.

**Bearing on Decision B, flagged now.** A metric highly sensitive to grid
composition is a poor primary in a study window containing three grid expansions
(2010, 2016, 2026) — one of which is the partial current season carrying the
headline reset. This is put to the analyst with the Decision B package rather
than resolved here.

---

## 2026-09-07 — Entry 037 — M5 is below the driver-noise floor in recent seasons

**Question.** Is M5 interpretable as a car-performance measure?

**Status.** RECORDED. Constrains Decision B.

**Finding.** Plan §4.3 requires M7 be reported alongside any best-of-team result,
because a between-team difference smaller than the within-team driver spread is
not interpretable as a car effect. M7 sits at 0.27–0.46 across the whole window.
**M5 is below M7 in most seasons** — 2025: M5 = 0.237 vs M7 = 0.297; 2026:
M5 = 0.141 vs M7 = 0.280.

In those seasons the gap between the two fastest cars is smaller than the typical
gap between two drivers in the same car. M5 is therefore not interpretable as a
car-performance measure in the recent era, **whatever its statistical
significance**. This is a measurement-floor problem, not a power problem; more
events would not fix it.

**Consequence.** M5 should not be selected as primary for any analysis spanning
the recent era. Recorded for the Decision B package.
## 2026-09-07 — Entry 038 — Tier B acquisition: one genuine data gap

**Question.** Did Tier B acquisition complete, and are all failures accounted for?

**Status.** COMPLETE. 185 of 196 sessions loaded.

**Failures, all logged by the acquisition ledger rather than skipped silently:**
- **10 are unraced 2026 rounds** (14–23). Scheduled, not yet run. Not a data gap.
- **1 is genuine: 2018 r14 Italian Grand Prix.** The source API returns "Failed
  to load timing data". Reproduced on a direct retry, so it is an upstream gap,
  not a transient error and not a rate-limit casualty. 2018 therefore contributes
  20 of 21 races.

**Rate limiting.** The 500 calls/hour limit was honoured with cache-first resume
and no parallelisation. One accidental second process was started and killed
immediately.

---

## 2026-09-07 — Entry 039 — Tier B cleaning: Spa 2021 lost, and logged

**Question.** One session vanished between the session baseline and the final
Tier B table. Which, and why?

**Status.** RESOLVED and now logged by name.

**Finding.** **2021 r12 Belgian Grand Prix.** 60 raw laps, 20 drivers,
rainfall=True. This is the race that ran a handful of laps behind the safety car
in torrential rain before being declared. After the structural filters it
retained **no representative lap**, which is correct — there was no green-flag
racing to measure.

**Fix.** A session-track close-out row now names any session that loses every
lap, rather than letting it disappear between two counts. Same defect class as
the Tier A Miami event (Entry 024) and caught by applying the same reconciliation
discipline.

---

## 2026-09-07 — Entry 040 — Traffic filter is the dominant exclusion, and its proxy is imperfect

**Question.** How much does the traffic filter remove, and is the gap measure sound?

**Status.** RECORDED. Bears directly on Decision A.

**Finding 1 — dominance.** L8 removes **19.5%** of surviving laps, more than any
other filter except track status. It is also the most threshold-sensitive knob in
the pipeline: 0.5 s keeps 90.6% of the base, 1.0 s keeps 77.6%, 2.0 s keeps
59.0%. A third of the Tier B data rides on this single choice.

**Finding 2 — the proxy is imperfect, measured not assumed.** `Position` is race
classification, not track position, so for lapped or out-of-sequence cars the car
"ahead" by Position can have a *later* lap start time, producing a negative gap.
This affects **6.36%** of non-null gaps (1st percentile −13.5 s). Negative gaps
fail the `>= threshold` comparison and are dropped, so they are removed rather
than mis-signed — but that means the traffic filter removes a small, non-random
set of laps for a reason unrelated to traffic.

**Recorded as confound 19.** Not fatal, but it means the traffic filter is doing
slightly more than it claims, and the excess is concentrated on lapped cars,
which are disproportionately backmarkers — i.e. it is not neutral with respect to
the dispersion being measured.

---

## 2026-09-07 — Entry 041 — Pace model ships: all four gates pass

**Question.** Does the Phase 3 pace model clear the §4.4 ship gates?

**Status.** **YES on all four.** The model ships.

**Gate 1, residual structure.** Residual slopes: +0.00010 against fitted value,
+0.00143 s/lap against lap number, +0.00110 s/lap against tyre age. The leftover
fuel slope is 2.4% of the fuel coefficient itself. Binned medians visually flat.

**Gate 2, fit quality.** 180/184 races fitted. Residual SD median 0.544 s,
pseudo-R² median 0.809. The fuel coefficient is **negative in every race**, median
−0.059 s/lap — estimated, not imposed, and it landed in the range normally quoted.

**Gate 3, recovered order.** Median Spearman ρ 0.855 against qualifying order and
0.891 against finishing order.

**Gate 4, backmarker sanity.** Fastest-team counts: Brackley 69, Red Bull 63,
McLaren 28, Ferrari 19, Silverstone 1. **No backmarker is ever ranked fastest.**
The single Silverstone race is Monaco 2023, where Aston Martin finished second —
plausible, not a failure.

**Rank deficiency diagnosed and fixed.** 12 races originally failed with a
singular design. Cause: a compound used on only a handful of laps gives a dummy
and an age-slope term that are effectively collinear. Compounds with fewer than
10 laps in a race are now dropped, costing 166 laps across 31 races and
recovering 8 of the 12. Four remain excluded and are logged.

---

## 2026-09-07 — Entry 042 — Gate 3 needed both comparators, and that mattered

**Question.** The first gate-3 run used only the finishing-order comparator and
flagged 6 races below ρ 0.5. Were those model failures?

**Status.** **No — the comparator was noisy, not the model.**

**Finding.** Plan §4.4 requires comparison against both the qualifying order and
the finishing order. Only the second had been implemented. Adding the first
resolved 5 of the 6 flags:

| race | ρ vs quali | ρ vs finish |
|---|---:|---:|
| 2019 Brazilian GP | 0.648 | 0.371 |
| 2020 Austrian GP | 0.927 | 0.415 |
| 2020 Italian GP | 0.758 | 0.200 |
| 2024 Miami GP | 0.842 | 0.486 |
| 2025 Monaco GP | 0.915 | 0.406 |

All five are races where the finishing order was scrambled by safety cars,
penalties or retirements. The model recovers a pace order consistent with
qualifying in every one.

**One race fails both comparators:** 2022 Emilia Romagna (0.43 / 0.32), a wet
race. Under Amendment 3 wet sessions are not filtered, so it stays in and is
named rather than quietly dropped.

**Lesson recorded.** Had gate 3 shipped with one comparator, five sound races
would have been investigated as model failures — or worse, the model would have
been "fixed" to match a scrambled finishing order.

---

## 2026-09-07 — Entry 043 — M5 measurement floor confirmed independently in Tier B

**Question.** Entry 037 found M5 at or below the M7 driver-noise floor in Tier A.
Does race pace show the same?

**Status.** **Yes — independently confirmed.**

**Finding.** In Tier B, M5 sits at or below M7 in most seasons: 2018 M5 = 0.151
against M7 = 0.237; 2022 M5 = 0.134 against M7 = 0.357; 2026 M5 = 0.268 against
M7 = 0.275.

Because Tier A measures qualifying and Tier B measures fuel-corrected race pace
through an entirely separate pipeline, this is corroboration rather than an
artefact of the qualifying metric. **M5 should not be selected as primary in
either tier.** Carried into the Decision B package.

---

## 2026-09-07 — Entry 044 — Self-inflicted bug: Tier B run clobbered Tier A D1c

**Question.** Recorded because it briefly corrupted a committed result.

**Status.** FIXED.

**What happened.** `src/metrics.py` was parameterised by tier, but the D1c block
wrote to a fixed filename. Running the Tier B metrics overwrote
`d1c_results.parquet` — the Tier A D1c output, which carries the pre-committed
M4 restriction — with NaNs, because 2010 predates the Tier B window entirely.

**Fix.** D1c is now explicitly guarded as a Tier A test and returns before
writing when run under any other tier. Tier A was re-run and the result restored
identically: M4 shift +0.827 [0.643, 1.118], restriction still triggered.

**Why it is logged.** The corrupted file would have silently replaced a
pre-committed diagnostic with nulls. Nothing downstream had consumed it yet, but
the same class of error later would be invisible.
## 2026-09-07 — Entry 045 — A — traffic gap: circular baseline found, re-estimated

**Question.** What gap to the car ahead counts as clean air?

**Status.** DECIDED — **5.0 s**, by a rule pre-committed before the output was seen.

**The defect.** My first traffic curve used each stint's median lap at
`gap >= 3 s` as the clean-air baseline. That forces every bin at or beyond 3 s to
zero **by construction**. The table did not show the penalty reaching zero at
3.0 s; it assumed it. Caught by the analyst.

**Re-estimated** against a distant baseline — stint median at `gap >= 8 s`,
requiring at least 3 reference laps — with bins extended to 8 s. The circular
version understated the 1 s penalty by **42%**: +0.38 s against a true +0.65 s.

| gap (s) | median penalty (s) |
|---|---:|
| 0.75–1.00 | +0.811 |
| 1.00–1.25 | +0.653 |
| 1.50–2.00 | +0.418 |
| 2.00–2.50 | +0.236 |
| 3.00–3.50 | +0.120 |
| 4.00–5.00 | +0.064 |
| **5.00–6.00** | **+0.039** |
| 6.00–7.00 | +0.031 |

**Pre-committed rule** (analyst, fixed before the curve was seen): the smallest
gap at which the residual median penalty falls below 0.05 s against the distant
baseline; if that lands above 3.0 s, use the higher value and do not prefer 3.0 s
for retention. **The rule returns 5.0 s.** Taken as written.

**Retention check, as required.** No race falls below the 40-lap floor at 5.0 s
(minimum 76 laps, median 306). Team-races fall from 1,847 to 1,733 at k = 3, a
loss of **6.17%**; the lost set is mildly skewed slow (median field rank 0.60
against 0.56 overall), less skewed than the k = 5 case that motivated k = 3.

**Reported for the analyst's trade, not decided here.** The stricter cutoff costs
model quality. Median laps per driver-race falls from ~35 to **16**, and gate 3
degrades from 1 race failing both comparators to **9** — three of them Monaco,
where clean air at 5 s barely exists. Gates 1, 2 and 4 still pass. This is a real
bias–variance trade: 5.0 s removes contamination that exceeded the signal in some
metrics, and pays for it in estimator noise.

---

## 2026-09-07 — Entry 046 — A — percent off own session best

**Status.** DECIDED — **107%**, unchanged from provisional.

**Reason.** 107% sits at roughly the 96.5th percentile of the own-best
distribution, at the knee where the tail begins (97th pct 107.7, 98th 111.7).
Below it the distribution is dense — a 103% cutoff would remove 28.6% of laps,
cutting into ordinary race pace. Above it the curve flattens. The choice is not
knife-edge, which is the best argument for keeping the value the sport uses.

---

## 2026-09-07 — Entry 047 — A — minimum laps per team-race

**Status.** DECIDED — **k = 3**, on anti-bias grounds.

**Reason.** Low-lap team-races are disproportionately **slow** teams: median
field rank 0.80 for under 3 laps, and 0.79 for those dropped at k = 5, against
0.56 for all team-races. The filter selectively removes backmarkers, which
narrows measured dispersion — the direction of the hypothesis. A threshold that
quietly makes the field look closer is the last place to be generous.

**The countervailing cost, stated as the analyst required.** Team-race pace
estimates from 3–4 lap samples carry a median SEM of about 0.29 s against 0.13 s
at 20+ laps. Because M1 and M2 are **dispersion** measures, measurement error
inflates them: k = 3 trades a narrowing bias (selective backmarker removal) for a
widening one (errors-in-variables). Recorded as confound 20.

The widening bias affects the **absolute level** more than boundary comparisons,
because the distribution of team-race sample sizes is broadly stable across
seasons, so it largely differences out at a boundary. **R7 sweeps k**, so the
size of the trade is measured rather than assumed.

---

## 2026-09-07 — Entry 048 — M5 formally retired from Decision B candidates

**Question.** M5 sits at or below the M7 driver-noise floor in most seasons, in
both tiers, through separate pipelines. Should it remain a candidate?

**Status.** DECIDED — **excluded from the Decision B primary candidates.**

**Option chosen.** M5 is retired as a primary candidate but **not deleted**. It
remains computed, plotted and reported, and every M5 figure is marked as below
the driver-noise floor wherever it appears.

**Reason.** This is a resolution floor, not a power problem: the gap between the
two fastest cars is smaller than the typical gap between two drivers in the same
car, so no amount of additional data resolves it. A metric that cannot resolve
its target is a **reportable result about the limits of the measurement**, which
is why it is retained rather than dropped.

**Corroborated by the placebo battery.** No boundary shift on M5 exceeds the
placebo maximum anywhere — exactly what a metric operating below its resolution
floor looks like.

---

## 2026-09-07 — Entry 049 — M4 restriction is wider than first stated

**Question.** The D1c restriction withdraws M4 estimates spanning 2010. Which
boundaries does that actually cost?

**Status.** RECORDED — the restriction costs the 2009 boundary as well.

**Finding.** The 2009 boundary's estimation window is 2006–2013, which contains
2010 in its post-period. Under the Entry 021 restriction, **M4 cannot carry the
2009 boundary either** — not only cross-2010 comparisons in the narrow sense.
M4 survives for 2014 onward.

This matters because 2009 is the least contaminated boundary in the study
(§8.5). Any metric that forfeits it forfeits the cleanest natural experiment
available, and that is now a cost attached to M4 specifically.

---

## 2026-09-07 — Entry 050 — Placebo battery run across all nine control boundaries

**Question.** Plan §8.4 asks for the full placebo distribution, not a single
boundary. How large are ordinary season-to-season shifts?

**Status.** RUN. Reported, not interpreted — Decision H is the analyst's.

**Design.** Nine eligible Tier A control boundaries (2007, 2008, 2011, 2012,
2013, 2015, 2018, 2024, 2025). **2010 is reported separately** as a
measurement-artifact boundary and never inside the clean pool: it carries a grid
expansion from 10 to 12 constructors with three new backmarkers, the refuelling
ban, and the segment-eligibility change simultaneously. Letting a boundary known
to be contaminated set the scale for everything else would be circular.

**Result summary — each reset as a percentile of the placebo |shift|
distribution:**

- **M1** (placebo median 0.440, max 0.653): 2009 +0.719 exceeds all; 2026 +0.653
  exceeds all; 2014 −0.584 at 89th; 2017 −0.263 and 2021–22 −0.390 both at 44th.
- **M2** (median 0.186, max 0.586): 2009 and 2026 exceed all; 2014 and 2021–22 at
  78th; 2017 at 11th.
- **M3** (median 0.332, max 0.469): **2021–22 −0.650 exceeds all**; everything
  else at or below the 89th.
- **M4** (median 0.343, max 0.599): 2021–22 −0.642 and 2026 +0.612 exceed all;
  2009 withdrawn per Entry 049.
- **M5**: no boundary exceeds the placebo maximum anywhere.
- **M6** (diagnostic): 2010 and 2009 exceed all — M6 doing the job it was kept
  for, flagging grid-composition change.

**Recorded for Decision H.** The placebo distribution is wide: ordinary season
boundaries move M1 by a median of 0.44 and up to 0.65. Two of the five resets sit
inside that ordinary range on M1. Whether a reset that moves the field no more
than an average season counts as "no effect" is the analyst's call, and it now
rests on nine control boundaries rather than on 2010 alone.
## 2026-09-07 — Entry 051 — B — primary metric FROZEN: M2, with M3 designated secondary

**Question.** Which metric leads the confirmatory tests?

**Status.** **DECIDED AND FROZEN** before Phase 5 ran.

**Option chosen.** **M2 (robust field spread, IQR) primary. M3
(leader→midfield) pre-registered as designated secondary**, reported alongside
M2 at every boundary, not competing for a confirmatory slot.

**Rationale, recorded before the confirmatory run so the choice is
answer-independent.** The intent classification (Entry 006) established that the
sport promised a closer **field** exactly once. The estimand of this study is
whole-field convergence. **M2 measures that construct directly; M3 measures a
different one** — the leader-to-midfield gap. The primary metric should match the
estimand, and that reasoning holds regardless of what either metric shows.
Grid-expansion robustness is a supporting argument, not the deciding one.

**Their disagreement is a finding, not a nuisance.** On the simple level shift,
M3's 2021–22 result exceeds every placebo while M2's sits at the 78th percentile.
If that survives, the reading is that the package pulled the midfield toward the
leaders **without compressing the field as a whole**. Those are different claims
and the memo makes both.

**Verified before freezing, as required.** M3 is computed as
`M3_midfield_pct` — the median of the 30th–70th **percentile** band, not
hardcoded ranks 4..7. The rank-based form exists separately as
`M3_midfield_rank47` and is used only for R15. The placebo battery and all Phase
5 results used the percentile definition, so the grid-robustness comparison
against M2 is valid.

---

## 2026-09-07 — Entry 052 — Traffic gap stays at 5.0 s; 3.0 s becomes a mandatory R7 arm

**Status.** DECIDED by the analyst. 5.0 s stands.

**Reason given, recorded because it is the governing principle.** Reversing to
3.0 s after learning that 5.0 s costs gate-3 quality would be choosing the
threshold on its consequences — the exact thing the pre-commitment existed to
prevent. The bias 5.0 s removes is also the more dangerous kind: traffic exposure
correlates with car pace, and the amount of traffic in a race is a function of
field spread, so the contamination correlates with the outcome across seasons.
Estimator noise inflates level, not boundary comparisons.

**Condition.** 3.0 s is a **mandatory R7 arm reported with equal prominence**,
not a footnote. If the headline differs between 3.0 s and 5.0 s, the memo says so
in the body.

---

## 2026-09-07 — Entry 053 — Traffic filter endogeneity (confound 21)

**Question.** Is the fixed traffic gap a time-varying filter?

**Status.** **Circuit mechanism CONFIRMED. Season drift not detected, with a weak
bound. A separate and worse endogeneity FOUND.**

**Circuit strictness.** Retention at 5.0 s ranges from **24.4% (Sakhir) to 49.8%
(Turkey)** — a 25.4 point spread. A fixed absolute gap is far stricter at short
circuits. Mechanism confirmed.

**Season drift: not detected.** −0.544 pp/season, p = 0.411, 95% CI
[−1.765, +0.677]. **Stated with its floor:** with n = 9 seasons this rules out
drift beyond about 1.8 pp/season — roughly 14 points across the window — and
nothing smaller. A weak bound, not a clean result. **R3 (constant-circuit) is
therefore load-bearing, not precautionary**, and it is one of three checks that
changes the significance verdict.

**The worse finding — endogeneity.** Traffic retention correlates with measured
field spread at **r = +0.950 (p < 0.001)** across the nine Tier B seasons
(Spearman ρ = +0.967). A tighter field puts more cars within 5 s, so more laps
are filtered: **the filter's strictness is a function of the quantity being
estimated.**

The induced bias runs opposite to the mechanism. Fewer surviving laps means
noisier per-team estimates, and because M1 and M2 are dispersion measures,
measurement error **inflates** them. The seasons where the field is genuinely
tightest are the seasons where the estimator is noisiest and most inflated, so
measured convergence is **attenuated** — the bias is conservative but the
magnitudes are understated.

**No clean escape exists.** Not filtering is worse: the unfiltered contamination
(+0.65 s at a 1 s gap) also scales with field tightness. Both the filter and its
absence are endogenous. This is a fundamental limitation of race-pace dispersion
analysis, not an implementation defect.

**Tier A is immune** — qualifying carries no traffic filter. A third independent
reason Tier A leads and Tier B corroborates.

**Not fixed by switching to a lap-time-relative gap.** That would be a metric
change and is not made.

---

## 2026-09-07 — Entry 054 — Gate 3: nine failures investigated, none is a model failure

**Question.** Plan §4.4 requires races failing both comparators to be manually
investigated before inclusion, not auto-excluded.

**Status.** ALL NINE INVESTIGATED. **All retained.** No genuine model failure.

| race | ρ quali | ρ finish | laps/driver | wet | disposition |
|---|---:|---:|---:|:---:|---|
| 2018 German | 0.31 | 0.39 | 10.8 | yes | wet + thin fit; retain |
| 2022 Monaco | 0.07 | −0.07 | 11.6 | yes | wet + Monaco; retain |
| 2023 Belgian | 0.20 | 0.11 | 10.2 | yes | wet + thin fit; retain |
| 2024 Monaco | 0.35 | 0.47 | 25.5 | no | **Monaco structural**; retain |
| 2025 Bahrain | 0.47 | 0.44 | 9.3 | no | thinnest fit in the study; retain |
| 2025 Emilia Romagna | 0.28 | 0.42 | 13.1 | no | thin fit; retain |
| 2025 Monaco | 0.22 | 0.33 | 24.3 | no | **Monaco structural**; retain |
| 2025 São Paulo | 0.35 | 0.45 | 19.1 | no | pace IQR 0.384% — field too close to rank; retain |
| 2025 Qatar | 0.28 | 0.43 | 11.8 | no | thin fit; retain |

**Monaco is a circuit-level limitation, not a threshold problem.** The initial
hypothesis was that clean air is scarce at Monaco under a 5 s gap. **It is not:**
Monaco retention is 36.9%, ranking **28th of 37 circuits** — mid-pack, not
strict. The 2024 and 2025 Monaco races have 25.5 and 24.3 laps per driver, among
the healthiest fits in the study, and the highest pace spread. The failure is
that **race pace at Monaco reflects track position and tyre management rather
than car performance** — everyone runs to a delta behind the car ahead. This is
stated as a circuit-level limitation, not used as a reason to move the threshold.

**São Paulo 2025 is the opposite case:** pace IQR of 0.384% against a
passing-race median of 1.081%. The teams were genuinely too close to rank, so a
rank correlation against any comparator is uninformative. Not a model failure.

**Season concentration noted.** 2025 contributes 5 of 9 failures (22.7% of its
races against ~5% elsewhere) and has the lowest median laps per driver-race
(12.0). This is the Entry 053 endogeneity showing through: 2025 had the tightest
field in the study, therefore the most traffic, therefore the fewest surviving
laps, therefore the thinnest fits.

---

## 2026-09-07 — Entry 055 — Finding E CONFIRMED (confound 21b)

**Question.** Was the Q2 starting-tyre rule real, and does it contaminate the
metric?

**Status.** **CONFIRMED as a phenomenon. Contamination TESTED and NOT DETECTED at
achievable resolution.**

**Evidence.** Q2 compound choice among Q3-reaching drivers, from FastF1
qualifying laps:

| season | Q2 on MEDIUM | Q2 on SOFT |
|---|---:|---:|
| 2019 | 24.9% | 75.1% |
| 2020 | 28.6% | 58.9% |
| 2021 | 34.2% | 57.1% |
| **2022** | **0.5%** | **85.6%** |
| 2023 | 11.8% | 80.5% |

Share of Q3-reaching drivers whose Q2 compound differs from their Q3 compound:
**32.0% in 2018–21 against 15.3% in 2022+, χ² p = 1.9 × 10⁻⁹.**

The rule was in force through 2021 and abolished for 2022. It is a **time-varying
change in what the Q2 segment measures**, landing precisely on the 2021–22
boundary — the only boundary with Intent-C = Yes.

**Contamination test.** The channel through which it would bias the metric is the
front-minus-back Q1→Q2 offset differential used by the evolution adjustment. That
shifts by **−0.034 s across the abolition, 95% CI [−0.075, +0.019]** — CI
contains zero. **Recorded as tested-not-detected, not as resolved:** this rules
out contamination above roughly 0.075 s and says nothing about smaller.

**Why the metric survives it.** The min-across-adjusted-segments rule absorbs
most of the effect: a front-runner's slow MEDIUM Q2 lap simply loses the minimum
to their Q1 or Q3 lap.

**Retrospective vindication.** This confirms that rejecting Option 2 (Q1+Q2 only)
at Entry 014 was correct. Option 2 would have rested the entire metric on the one
segment now confirmed to be contaminated in a time-varying way across the
headline boundary.

---

## 2026-09-07 — Entry 056 — Phase 5 confirmatory result

**Status.** RUN. **Neither confirmatory test rejects.** Reported, not interpreted.

**Exact test count: 2 confirmatory + 9 secondary = 11 formally corrected tests.**
The secondary family is 9, not the projected 10: the 2026 boundary has one
post-period season, so its `t × post` column is degenerate and `b3` is **not
estimable**. Excluded rather than reported as zero.

**Confirmatory (Holm at α = 0.05):**
- Pooled b2 (H1, level): μ = **+0.4804** [−0.0457, +1.0066], p = 0.0643 against a
  Holm threshold of 0.025. **Does not reject.**
- Pooled b3 (H2, slope): μ = +0.1502 [−0.2239, +0.5242], p = 0.2913. Does not
  reject.

**Heterogeneity is dominant: I² = 86.1% (b2), 87.4% (b3).** Plan §8.3 requires
this be reported in place of, not after, the headline. **Two §9 falsification
criteria fire independently:** (1) the pooled CI contains zero, and (5)
heterogeneity is large enough that the pooled estimate averages incompatible
effects.

**Per-boundary b2 (M2):** 2009 +0.973, 2014 +0.449, 2017 +0.133,
**2021–22 −0.003**, 2026 +0.834. Secondary family Holm-corrected: 2026 b2,
2009 b2, 2009 b3 and 2014 b3 survive; 2014 b2 does not.

**The trend control changes 2021–22 completely.** The simple pre/post difference
gives −0.385 (78th placebo percentile); the segmented ITS gives −0.003. Every
boundary has a negative pre-slope — the field was **already converging** before
four of the five resets. This is Decision H item 1 and both numbers are reported.

---

## 2026-09-07 — Entry 057 — Robustness battery: the reporting rule cannot be applied as written

**Status.** RUN, with a defect in the rule recorded.

**Result.** 12 of 15 executed arms survive.

**Defect 1 — the denominator.** Three checks are **not executable on the Tier A
primary**: R7 (threshold sweep, a Tier B construct), R13 (PU-supplier grouping,
Tier B), R16 (stratified offset, requires a cleaning re-run). Plan §11 sets the
bar at **11 of 16**. Reporting "12 of 15" against that threshold silently changes
the denominator. **The memo must state the executable denominator and must not
claim the pre-registered threshold was met.**

**Defect 2 — the rule mis-scores three checks.** R3 (constant-circuit,
μ = +0.682 [+0.326, +1.038]), R4 (constant-constructor, μ = +0.315
[+0.041, +0.590]) and R12 at ±3 seasons (μ = +0.524 [+0.179, +0.869]) all produce
CIs **excluding** zero where the headline's includes it. The battery scores a
changed significance verdict as failure — but all three point the **same
direction** as the headline, more strongly, and all three roughly **halve the
heterogeneity** (I² 86% → 56–62%).

The substantive reading is the opposite of the mechanical score: restricting to
constant circuits and constant constructors sharpens the estimate and reduces
heterogeneity, which is what should happen if calendar and grid composition are
the noise the plan said they were. **Both the mechanical score and this reading
go in the memo.**

---

## 2026-09-07 — Entry 058 — B1 and the 2026 constant-constructor check

**B1 — the 2009 boundary does not depend on the Brawn mapping.**
Continuation b2 = +0.9726 [+0.633, +1.382]; Brawn-as-new-entity b2 = +0.9726
[+0.631, +1.381]. **Identical to four decimal places.** The most contestable call
in the continuity mapping, inside the least contaminated boundary, turns out not
to matter — Brawn occupies the same position in the distribution either way and
M2's IQR is unaffected by the lineage label. A worry checked and dismissed on
evidence rather than assumed away.

**Decision H item 2 — M2 is NOT immune at 2026.** M2's IQR is insensitive to a
new entrant at the tail, but an eleventh constructor changes which teams fall
inside the interquartile range.

| 2026 estimate | b2 | 95% CI |
|---|---:|---|
| all constructors | +0.834 | [+0.616, +1.079] |
| constant-constructor (R4) | +0.596 | [+0.388, +0.813] |

**29% of the measured 2026 widening is attributable to the eleventh entrant**;
71% survives with a CI excluding zero. Any 2026 statement must use the
constant-constructor figure or say that it does not.
## 2026-09-07 — Entry 059 — Finding E completed; preliminary figures superseded

**Question.** Entry 055 reported Finding E from a partial run (2018–2023, 120 of
185 sessions) because the acquisition had stalled. The full run has now
completed. Do the final numbers change the conclusion?

**Status.** COMPLETE — all 185 sessions, 2018–2026. **Conclusion unchanged;
the effect is substantially stronger than the preliminary figures showed.**

**Superseded figures.** Entry 055 is append-only and is left intact. The
preliminary numbers it reports (differ-rate 32.0% against 15.3%, χ² p = 1.9 ×
10⁻⁹) are superseded by the complete run below, and the two committed documents
that cited them — `LIMITATIONS.md` and `phase6_red_team.md` — have been updated.

**Final result.** Q2 compound choice among Q3-reaching drivers, all 185 sessions:

| season | Q2 on SOFT | Q2 on MEDIUM |
|---|---:|---:|
| 2019 | 75.1% | 24.9% |
| 2020 | 58.9% | 28.6% |
| 2021 | 57.1% | **34.2%** |
| 2022 | 85.6% | **0.5%** |
| 2023 | 84.9% | 9.1% |
| 2024 | 92.0% | 0.0% |
| 2025 | 89.0% | 6.6% |
| 2026 | 99.2% | 0.0% |

Share of Q3-reaching drivers whose Q2 compound differs from their Q3 compound:
**32.0% in 2018–21 against 8.0% in 2022–26, χ² p = 6.3 × 10⁻³⁹** (n = 801 and
1,028).

**Why the effect strengthened.** The partial run ended at 2023, which at 16.9%
was the highest post-rule season. Adding 2024 (0.8%), 2025 (8.8%) and 2026 (0.8%)
drops the post-rule figure from 15.3% to 8.0% and moves the p-value from
10⁻⁹ to 10⁻³⁹.

**Nothing else changes.** The rule was in force through 2021 and abolished for
2022, exactly as Entry 055 stated. The contamination test is unaffected — it was
computed on the Tier A qualifying table, not on this dataset, and the
front-minus-back Q1→Q2 differential still shifts −0.034 s [−0.075, +0.019] across
the abolition. **Tested and not detected, with the same floor.**

**Not in the memo.** Finding E cites no figure in `memo.md`; it appears only in
`LIMITATIONS.md` and the red team document. The memo required no change.

**Operational note.** The run completed only after being made resumable
(partial results written per session, completed sessions skipped on restart)
following two stalls on hung FastF1 requests with no effective timeout.
## 2026-09-07 — Entry 060 — The 2009 estimate is contaminated by the 2010 artifact; D1c logic was not extended to the primary metric

**Question.** The 2009 boundary's estimation window runs to 2012 and therefore
contains the 2010 measurement discontinuity in its post-period. Was that
accounted for?

**Status.** **No. Caught in review AFTER the memo was drafted.** Recorded here as
it happened rather than retro-fitted into the plan.

**What went wrong.** Entry 021 pre-committed the D1c restriction, and Entry 034
applied it: M4 was withdrawn at 2009 precisely because the 2009 window contains
2010. Entry 035 then recorded that the whole-field controls **also** stepped at
2010, M2 at **1.93× the median reset shift** — the largest relative step of any
metric, larger than M4's.

**The pre-commitment named M4 and M5, so nothing was applied to M2.** The logic
that justified withdrawing M4 at 2009 applies with equal or greater force to the
primary metric, and it was not extended there at the time. Entry 035 recorded the
control failure as an interpretation finding and did not follow it through to the
2009 primary estimate.

This was found by the analyst in review after `memo.md` was written and
committed.

**Quantified (a).** Re-estimated on a window truncated at 2009, which removes the
artifact entirely:

| window | b2 | 95% CI | seasons | events | slope estimable |
|---|---:|---|---:|---:|:---:|
| full (2006–2012, contains the artifact) | +0.9726 | [+0.6279, +1.3726] | 7 | 128 | yes |
| truncated at 2009 | +0.4610 | [+0.0892, +0.9804] | 4 | 70 | **no** |

**The estimate roughly halves.** It remains positive with an interval excluding
zero. The truncated version rests on four seasons with a **single post-boundary
season**, so `t × post` is degenerate and the slope term is **not identifiable at
all** — the same structural problem as 2026. Its level estimate is correspondingly
weak. That the truncated fit is barely estimable is itself part of the answer.

**Flagged wherever it appears (b).** The memo's per-boundary table, Figure 2 (a
flag on the 2009 row plus a footnote giving the truncated value), and
`LIMITATIONS.md` §4.

**Direction of the conclusion is unaffected (c).** Removing or halving 2009
removes a **widening**, not a narrowing. "No boundary narrowed beyond trend"
holds on four boundaries instead of five, and 2026 — the other Holm-surviving
widening — is untouched.

**Why this is a finding and not a repair (d).** The boundary described throughout
this work as the "least contaminated" in the study, and used as such in §8.5,
turns out to have a measurement discontinuity inside its own comparison window.
That belongs in the memo body, and it is there.

**Reproducible.** `src.phase5.boundary_2009_contamination`, written to
`data/processed/boundary_2009_contamination.parquet`.

---

## 2026-09-07 — Entry 061 — Figures 2 and 3 contradicted each other on sight

**Question.** Figure 2 (trend-corrected) put 2014 at +0.449, widening. Figure 3
(raw difference) put 2014 at −0.39 and coloured it green for narrowing. Same
boundary, opposite sign, opposite colour, adjacent in the README.

**Status.** FIXED.

**The defect.** A caption naming the specification was not enough, because
**colour reads before text**. A reader scanning the two charts saw red-for-wider
in one and green-for-narrower in the other for the same season and would
reasonably conclude one of them was wrong.

**Fixes applied.**
1. **Direction colour-coding removed from Figure 3 entirely.** One colour for
   rule-change seasons, one for ordinary seasons. That figure answers "are rule
   changes distinguishable from ordinary seasons," not "which direction did each
   go," and encoding direction invited a comparison the chart does not support.
2. **The specification moved into the figure TITLE on both charts**, not the
   caption — "trend-corrected (the pre-existing decline is removed)" against
   "raw season-to-season change (the pre-existing trend is NOT removed)".
3. **A pull-quote between them in the README** stating that the two use different
   methods, that this is why 2014 and 2017 flip sides, and that the difference is
   whether the pre-existing trend is removed — with the note that which question
   is the right one is the single biggest judgement call in the analysis.
4. **Figure 1 now shades 2006–2009** and draws it as a separate dashed series,
   because Q3 is excluded there and the two eras are not on the same measurement
   basis. Previously a reader saw one continuous line across a break the analysis
   knows to exist.
5. **The memo's "M2 falls from 1.21 in 2006 to 0.45 in 2025"** spanned the 2010
   discontinuity. Restated within-era: 1.21 → 0.58 across 2006–09 and 1.79 → 0.45
   across 2010–25. Both eras decline internally, so the claim survives, but it no
   longer rests on a comparison across the break.
