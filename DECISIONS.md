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
