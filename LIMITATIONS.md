# Limitations — what would change my mind

Companion to [`memo.md`](memo.md). Everything here is traceable to a committed
artifact; decision numbers refer to [`DECISIONS.md`](DECISIONS.md).

---

## 1. Confounds that remain wholly unaddressed

Listed first, because a limitations section that leads with solved problems is
decoration.

1. **The cost cap and the aerodynamic testing restrictions cannot be separated
   from the 2022 aero reset** (plan confounds 1–2). They arrive together and are
   collinear in time, with one treated unit. Any 2021–22 statement is about the
   regulatory *package*. This is why the two seasons are merged into one boundary
   rather than tested separately (Entry 005).

2. **Wet sessions are unfiltered in both tiers** (confound 18). No uniform wet
   flag was implementable — see section 3 — and wet events are not randomly
   distributed across seasons or circuits. At least one confirmed wet qualifying
   session (Austin 2015) sits inside the placebo pool and inside two boundary
   windows.

3. **The evolution offset is misspecified by stratum** (confound 16). Front
   runners gain roughly 0.3 s more between Q1 and Q2 than backmarkers, so a
   field-wide offset is a weighted average of track evolution and a
   position-dependent sandbagging differential. **Every absolute-level statement
   about field spread inherits this.** Boundary comparisons difference it out,
   which is why they survive. R16 quantifies it — see section 2.

4. **Errors-in-variables inflation** (confound 20). The minimum-laps threshold is
   set at 3, chosen on anti-bias grounds because low-lap team-races are
   disproportionately slow teams and a higher threshold would selectively remove
   backmarkers, narrowing measured dispersion in the direction of the hypothesis.
   The cost is that 3–4 lap estimates carry a median SEM of 0.29 s against 0.13 s
   at 20+ laps, and measurement error **inflates** dispersion metrics. Direction
   known, magnitude not.

5. **Intent-C is untestable.** The sport explicitly promised a closer *field*
   once in twenty years. A one-versus-four contrast is not a test. An analysis of
   field convergence is measuring something the regulator, on its own public
   record, mostly did not claim to be delivering (Entry 016).

6. **Raceability is not measured at all.** Every null in this analysis is
   consistent with the regulations having succeeded completely at the thing they
   were actually aiming for. This is a limitation of the estimand, not of the
   estimator, and no amount of additional timing data addresses it.

---

## 2. R16 — run because the red team said it would overturn the result

**R16 was executed because the Phase 6 red team named it first on its own
"what would change my mind" list, and it was run *before the memo existed*
rather than after.** The check had been left unexecuted in the first battery
pass; the red team's attack is what caused it to be run.

The stratified offset flips the 2021–22 sign, from −0.0033 to +0.0661. The
pre-commitment fires on the letter and was honoured: the flip is reported before
any conclusion, in the memo body. It does not change the substantive result —
both estimates are indistinguishable from zero, the movement is one-ninth of its
own confidence-interval width, and the Phase 5 statement was never a narrowing
claim.

What does change: **under the stratified offset no boundary in the study carries
a negative point estimate.** Under the field-wide offset exactly one did, and it
was −0.003.

The other four boundaries keep their sign under R16 and shift by at most 0.11.

---

## 3. Measurement limitations discovered during the work

Each was found by checking rather than assumed, and each is recorded with the
resolution limit of the check.

- **Race-fuel qualifying, 2006–2009.** Q3 was run on race fuel in those seasons;
  `median(Q3−Q2)` is positive in all four and negative in all seventeen from
  2010, with no overlap and the sign flipping exactly on the refuelling ban. Q3
  is excluded from the metric in those seasons (Entry 014). The cost is an
  era-dependent measurement basis at the front of the field, quantified by
  diagnostic D1.

- **No wet flag is implementable.** Jolpica exposes no weather field; FastF1
  weather begins in 2018. A uniform external source (Open-Meteo reanalysis) was
  built and **rejected**: whole-day resolution over-flagged a third of all events,
  exclusions clustered heavily by season, and decisively, scheduled qualifying
  dates are systematically wrong on postponed sessions — and postponement is
  *caused by* the weather being detected, so the error correlates with the
  quantity measured. Suzuka 2019, the wettest event in the dataset, is a
  confirmed false positive: Saturday was cancelled for a typhoon and qualifying
  ran dry on Sunday. The rejected module is retained, unused, with its diagnosis
  (Entry 031).

- **No deleted-lap field exists** in any season, so that filter was removed
  rather than left as a rule that never fires. The resulting bias is
  time-varying, because track-limits enforcement tightened across the window
  (confound 13).

- **The Q2 starting-tyre rule was real and time-varying.** Q2 MEDIUM usage among
  Q3-reaching drivers runs 24.9% / 28.6% / 34.2% across 2019–21 then collapses to
  0.5% in 2022 (χ² p = 1.9 × 10⁻⁹). It changes what the Q2 segment measures,
  landing exactly on the only boundary that promised field convergence.
  **Contamination tested and not detected** through the channel that matters —
  the front-minus-back Q1→Q2 differential shifts −0.034 s [−0.075, +0.019] — which
  rules out contamination above roughly 0.075 s and says nothing below it
  (Entry 055).

- **The traffic filter is endogenous to the outcome (Tier B).** Retention
  correlates with measured field spread at **r = +0.950, p < 0.001**: a tighter
  field puts more cars within 5 s, so more laps are filtered. The induced bias
  runs the other way — fewer laps means noisier estimates, and dispersion metrics
  are inflated by measurement error — so measured convergence is **attenuated**.
  There is no clean escape: not filtering is worse, because the unfiltered
  contamination (+0.65 s at a 1 s gap) also scales with field tightness. Tier A
  carries no traffic filter and is immune. This is a third independent reason
  Tier A leads and Tier B corroborates only (Entry 053).

- **Circuit-dependent filter strictness.** Retention at 5 s ranges from 24.4%
  (Sakhir) to 49.8% (Turkey). Season drift was **not detected** — −0.54
  pp/season, p = 0.41 — but with n = 9 seasons that rules out drift beyond about
  1.8 pp/season and nothing smaller. R3 is therefore load-bearing rather than
  precautionary.

- **Monaco is structurally unfittable.** Three of nine gate-3 failures are
  Monaco, and it is *not* a data-scarcity problem: Monaco retention is 36.9%,
  ranking 28th of 37 circuits, with among the healthiest fits in the study. Race
  pace at Monaco reflects track position and tyre management rather than car
  performance. Stated as a circuit-level limitation (Entry 054).

---

## 4. Design limitations that were computed in advance

Recorded before any result existed, in the plan.

- **Window collisions.** Five boundaries across 21 seasons with ±4-season windows
  collide almost everywhere. 2009 is the only boundary with no intruding reset,
  and even it is "least contaminated," not clean — it carries three simultaneous
  technical changes, Honda's withdrawal producing Brawn inside the window, and
  the 2008 financial crisis reshaping budgets in its pre-period (confound 14).

- **H2 was downgraded before it was tested.** The longest uninterrupted
  stable-regulation period in 2006–2026 is **three seasons**. H2 is defined
  against "a comparable stable-regulation period," and none exists. This is a
  limitation of the sport's regulatory cadence, not of the data.

- **Placebo pools are small.** Tier A has nine eligible control boundaries;
  **Tier B has two**. A null placebo result in Tier B is not reassurance.

- **The robustness threshold cannot be applied as pre-registered.** Three of the
  sixteen checks (R7, R13, R16 in its original battery form) are not executable
  on the Tier A primary. Twelve of fifteen executable arms survive. The
  pre-registered 11-of-16 bar was **not met as written**, and this is stated
  rather than the denominator quietly changed.

- **The battery rule mis-scores three checks.** R3, R4 and R12(±3) produce
  intervals *excluding* zero where the headline's includes it, so a rule keyed on
  significance verdicts counts them as failures — yet all three point the same
  direction as the headline, more strongly, and roughly halve heterogeneity
  (I² 86% → 56–62%). Both the mechanical score and this reading are reported.

---

## 5. What would change my mind

Carried verbatim from the Phase 6 red team, written before the memo existed.

- If R16 (stratified offset) reversed the sign of any per-boundary estimate.
  *Executed. It reversed one — 2021–22, from −0.0033 to +0.0661 — at an estimate
  that is null under both specifications. Reported in the memo body.*
- If the Tier B endogeneity could be broken by an exogenous traffic measure —
  telemetry-derived following distance rather than classification position.
- If a longer post-2026 series showed the 2026 widening converging on the pattern
  of 2009 and 2014, which would make "resets widen then converge" a
  three-instance regularity rather than an anecdote.
- If the pre-boundary trend could be shown to be independent of the regulatory
  regime, which would make trend-controlled estimates the clearly correct read.

To which one more should be added, from the memo:

- If the pre-boundary trend were shown to *be* the accumulated effect of
  regulation, the simple-difference specification becomes correct, 2021–22
  becomes a genuine convergence at the 78th placebo percentile, and the headline
  reverses. This is the single most plausible route to the opposite conclusion
  and this design cannot rule it out.
