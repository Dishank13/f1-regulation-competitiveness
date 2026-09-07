# Phase 6 — Red Team

**Written before any memo exists**, as plan §6 requires. The job is to attack
the analysis, not to defend it. Where an attack succeeds, it says so.

---

## Attack 1 — The headline result is an artifact of the trend control

**The attack.** The two specifications disagree at the boundary that matters
most. A simple pre/post difference puts 2021–22 at −0.385 (78th placebo
percentile, a visible narrowing). The segmented ITS puts it at −0.003 (nothing
at all). The analysis reports the ITS. That choice — and it *is* a choice —
converts the one boundary the regulator explicitly promised would close the
field from a modest success into a null.

**Does it succeed?** Partially, and it must be reported as a specification
dependence rather than a result. The ITS is the pre-registered specification
(plan §8.2, committed before any data was touched), so this is not
post-hoc selection. But the plan did not anticipate that the two would diverge
this sharply, and "we used the pre-registered model" is a procedural defence, not
an evidential one. **Both numbers belong in the memo body.**

The substantive question is whether the pre-boundary trend is a nuisance to
remove or part of the effect. If the accumulated regulatory regime is what drove
two decades of convergence, controlling for the trend removes the very thing the
study is looking for. The design cannot distinguish these.

---

## Attack 2 — The pooled estimate is meaningless and the memo may still lead with it

**The attack.** I² = 86%. The five boundaries do not measure a common effect:
2009 and 2026 show large positive shifts, 2021–22 shows exactly nothing. Pooling
them produces +0.48, a number that describes no boundary in the study. Plan §8.3
says the heterogeneity must be reported "in place of, not after" the headline —
a rule that is easy to write and easy to soften in drafting.

**Does it succeed?** Yes, as a warning. The pooled estimate should not be the
memo's first sentence. Plan §9 criterion 5 fires on its own terms, and the honest
top-line is that the boundaries behave differently from one another, with the
per-boundary table as the actual result.

---

## Attack 3 — Traffic filtering is endogenous to the outcome (Tier B)

**The attack, and this one is new.** Traffic retention correlates with measured
field spread at **r = +0.950 (p < 0.001)** across the nine Tier B seasons. The
mechanism is mechanical: a tighter field puts more cars within 5 s of each other,
so more laps are filtered. The filter's strictness is therefore a *function of
the quantity being estimated*.

Worse, the induced bias runs the other way from the mechanism: fewer surviving
laps means noisier per-team pace estimates, and because M1 and M2 are dispersion
measures, measurement error **inflates** them. So the seasons where the field is
genuinely tightest are exactly the seasons where the estimator is noisiest and
most inflated.

**Does it succeed?** Yes, against Tier B specifically — and there is no clean
escape. Not filtering is worse: the un-filtered contamination (+0.65 s at 1 s
gap) also scales with field tightness. Both the filter and its absence are
endogenous. This is a fundamental limitation of race-pace dispersion analysis,
not a bug in this implementation.

**Tier A is immune** — qualifying laps carry no traffic filter — which is a third
independent reason the plan is right to make Tier A primary and Tier B
corroboration only.

---

## Attack 4 — The traffic gap is a time-varying filter by circuit

**The attack.** A fixed 5 s gap is far stricter at short circuits than long ones.
Retention ranges from **24.4% (Sakhir) to 49.8% (Turkey) — a 25.4 point spread**.
If the calendar's circuit mix drifts, filter strictness drifts with it.

**Does it succeed?** The mechanism is confirmed; the drift is not detected.
Season retention trends at −0.54 pp/season, p = 0.41, 95% CI [−1.77, +0.68].
**Stated honestly: with n = 9 seasons this rules out drift beyond about 1.8 pp
per season — roughly 14 points across the window — and nothing smaller.** That is
a weak bound, not a clean bill of health. R3 (constant-circuit subset) is
therefore **load-bearing, not precautionary**, and R3 is one of the three checks
that changes the significance verdict.

---

## Attack 5 — Three robustness checks make the effect significant, and the battery scores that as failure

**The attack.** R3 (constant-circuit), R4 (constant-constructor) and R12 at a
±3-season window all produce pooled estimates with CIs **excluding zero**, where
the headline's CI includes it. The battery rule counts a change in significance
verdict as a failure, so the reported score is 12 of 15 — but the "failures" all
push the *same direction* as the headline, more strongly, and all three roughly
halve the heterogeneity (I² 86% → 56–62%).

**Does it succeed?** Yes, against the battery's design rather than the result.
A pass/fail rule keyed on significance treats "the effect became clearer on a
cleaner subset" as evidence of fragility. The substantive reading is the
opposite: restricting to constant circuits and constant constructors *reduces*
heterogeneity and sharpens the estimate, which is what should happen if calendar
and grid composition are the noise the plan said they were. **Both the mechanical
score and this reading must appear in the memo.**

---

## Attack 6 — The battery cannot reach its own threshold

**The attack.** Plan §11 sets the bar at 11 of 16. Three checks (R7 threshold
sweep, R13 PU-supplier grouping, R16 stratified offset) are **not executable on
the Tier A primary** — R7 and R13 are Tier B constructs, R16 requires a cleaning
re-run. So the denominator is 15 executed arms across 12 executable R-numbers,
and the "11 of 16" rule cannot be applied as written.

**Does it succeed?** Yes. The reporting rule was written when the battery was
assumed to be tier-agnostic. Reporting "12 of 15" against a threshold of "11 of
16" silently changes the denominator. **The memo must state the executable
denominator explicitly and not claim the pre-registered threshold was met.**

---

## Attack 7 — The 2021–22 boundary sits exactly on a qualifying-format change

**The attack.** Finding E is now confirmed: the Q2 starting-tyre rule was in
force through 2021 and abolished for 2022. Q2 MEDIUM usage among Q3-reaching
drivers runs 24.9% / 28.6% / 34.2% in 2019–21 and collapses to **0.5% in 2022**
(differ-rate 32.0% vs 15.3%, χ² p = 1.9 × 10⁻⁹). That is a change in what the Q2
segment *measures*, landing precisely on the boundary with Intent-C = Yes.

**Does it succeed?** The mechanism is real and confirmed. The contamination is
**tested and not detected** through the channel that would matter: the
front-minus-back Q1→Q2 offset differential shifts by −0.034 s across the
abolition, 95% CI [−0.075, +0.019]. The min-across-adjusted-segments rule absorbs
most of it, because a front-runner's slow MEDIUM Q2 lap simply loses the minimum
to their Q1 or Q3 lap.

**Stated with its floor:** this rules out contamination above roughly 0.075 s,
not below. Recorded as confound 21.

It also **retrospectively vindicates rejecting Option 2** (Q1+Q2 only) at
Decision B″. Option 2 would have rested the entire metric on the one segment now
confirmed to be contaminated in a time-varying way across the headline boundary.

---

## Attack 8 — 2026 is a partial season carrying an eleventh team

**The attack.** The season most readers care about has 13 of 23 rounds and a new
constructor. Its +0.834 is the second-largest estimate in the study.

**Does it succeed?** It is quantified rather than dismissed: 29% of the shift is
attributable to the eleventh entrant, and 71% survives the constant-constructor
check with a CI excluding zero. But the partial-season problem is not fixable —
2026 also has one post-period season, which is why its `b3` is not estimable at
all. Any 2026 claim is provisional twice over.

---

## Attack 9 — M4 was restricted, and the restriction's rationale turned out to be wrong

**The attack.** D1c triggered the M4 restriction on the grounds of a
front-of-field measurement discontinuity at 2010. But the whole-field controls
M1 and M2 *also* stepped at 2010, more strongly in relative terms. So the
premise — that the 2010 step was front-of-field-specific — was false, and M4 was
restricted for a reason that does not hold.

**Does it succeed?** No, and deliberately so. The restriction was pre-committed
on observed *magnitude*, not on a diagnosis of cause. Lifting it after
discovering a competing explanation is precisely the move pre-commitment exists
to prevent. It stands. But the attack correctly identifies that the plan's stated
*rationale* for D1c was wrong, and the memo should say the restriction was
applied mechanically rather than because the diagnosis was confirmed.

---

## Attack 10 — Confounds that remain wholly unaddressed

Stated plainly, because a red team that only lists solved problems is decoration.

1. **Cost cap and ATR are inseparable from the 2022 aero reset** (confounds 1–2).
   Unchanged since the plan. Any 2021–22 statement is about the package.
2. **Wet sessions are unfiltered in both tiers** (confound 18) and wet events are
   not randomly distributed across seasons or circuits. At least one confirmed
   wet qualifying session sits in the placebo pool.
3. **The stratum-misspecified evolution offset** (confound 16) biases every
   absolute-level statement, and R16 was not executed.
4. **Errors-in-variables inflation from k = 3** (confound 20) inflates dispersion
   metrics; the direction is known, the magnitude is not.
5. **Intent-C is untestable.** The sport promised a closer field once. An
   analysis of field convergence is measuring something the regulator mostly did
   not claim to be delivering.
6. **Raceability is not measured at all.** Every "no effect" in this analysis is
   consistent with the regulations having succeeded completely at the thing they
   were actually aiming for.

---

## What would change my mind

- If R16 (stratified offset) reversed the sign of any per-boundary estimate.
- If the Tier B endogeneity (Attack 3) could be broken by an exogenous traffic
  measure — telemetry-derived following distance rather than classification
  position.
- If a longer post-2026 series showed the 2026 widening converging on the pattern
  of 2009 and 2014, which would make "resets widen then converge" a
  three-instance regularity rather than an anecdote.
- If the pre-boundary trend could be shown to be independent of the regulatory
  regime, which would make trend-controlled estimates the clearly correct read.
