# ANALYSIS PLAN — Did F1 regulation resets make the field more competitive?

**Status: PRE-REGISTRATION, AMENDED 2026-09-06 (Amendments 1 and 2).**

**Amendment 2 — what changed and why.** Driven by diagnostic D1 (§4.1.3–4.1.4)
and by four defects the analyst found in the first Tier A row-loss ledger.
No boundary estimate, metric value, or test statistic existed when any of it was
decided.

1. **D1a recorded as tested-not-detected**, not as concern-resolved: the CI
   rules out composition shifts above ~0.09 s and is not an equivalence test.
2. **D1b restriction rule pre-committed** before D1c runs: if M4 or M5 steps at
   2010 by at least half the median reset-boundary shift, those metrics are
   restricted to within-era comparison and cross-2010 claims are withdrawn.
3. **2010 added to the placebo battery** as a known measurement-artifact
   boundary, reported separately (§8.6).
4. **Stratum misspecification** promoted from an observation to confound 16 with
   robustness check R16, plus an explicit restriction on absolute-level claims
   (§4.1.4). Battery grows to 16; threshold becomes 11 of 16.
5. **B1 added** (§11.1): the 2009 boundary estimated under both Brawn mappings,
   reported separately from the headline battery.
6. **Confound 17**: wet-session detection is unavailable for Tier A before 2018,
   and a spread-based proxy is rejected as circular. Open gap, analyst decision.

---

**Status of Amendment 1: PRE-REGISTRATION, AMENDED 2026-09-06.**
The original was committed *before* any analysis code existed and is tagged
`pre-registration`. That tag is never moved and history before it is never
rewritten. This amendment is a new commit stating what changed and why.

**Amendment 1 — what changed and why.** The Phase 1 coverage report
([`data/processed/coverage_report.md`](data/processed/coverage_report.md))
established two facts the original plan had assumed rather than verified, and
one it did not anticipate:

1. Jolpica exposes no deleted-lap field in any season, so the §6.3 filter is
   **removed as unimplementable** and the bias it would have caught is added to
   the confound list (confound 13).
2. FastF1's lap-data floor is **2018**, verified rather than assumed. Decision G
   is closed: Tier A 2006–2026, Tier B 2018–2026.
3. **Qualifying was run on race fuel in 2006–2009.** `median(Q3−Q2)` is positive
   in all four of those seasons and negative in all seventeen from 2010, with no
   overlap. The original §4.1 adjustment would have read that offset as track
   evolution and credited heavy-fuel laps by up to 1.7 s. §4.1 is revised
   accordingly, R8 is promoted to a four-way sweep, and a new diagnostic (§4.1.2)
   and confound (15) quantify the cost of the revision.

Additionally, the intent contrast is **demoted from confirmatory to descriptive**
(§2.3), which returns a slot to the multiplicity budget and reduces the
confirmatory count from 3 to 2.

No result existed when any of this was decided. The coverage report contains no
competitiveness metric, no boundary estimate, and no test statistic.

---

## 1. Question and hypotheses

**Question.** At each major Formula 1 technical regulation boundary, did the
dispersion of car performance across the field measurably change?

**Primary hypothesis (H1, level).** At a regulation reset boundary, the
competitiveness metric shows a step change in season `Y` relative to season
`Y-1`, beyond what ordinary season-to-season variation produces.

**Secondary hypothesis (H2, slope).** In the seasons following a reset, the rate
of change of the metric differs from its rate of change in a stable-regulation
period. See section 8.5 — the data may not support this hypothesis at the
intended resolution, and the plan commits in advance to saying so.

H1 and H2 are directionally agnostic. A reset may narrow the field, widen it, or
do nothing, and the same is true of the post-reset trajectory. **This plan states
no expectation about the sign of either coefficient.** Two-sided tests
throughout. The reporting language in section 9 is symmetric by construction, and
that symmetry is a requirement on the memo, the code comments, and the figure
captions, not only on this document. Any reader should be unable to infer from
the framing which result was anticipated.

**Null.** Regulation boundaries are indistinguishable from arbitrary season
boundaries. Operationalised via the placebo test in section 8.6.

### What this analysis does NOT measure

Stated up front because it bounds every conclusion:

- **Raceability.** F1's stated goal is usually cars that can follow and overtake.
  We measure lap-time dispersion. Cars can converge in pace without racing
  better, and vice versa. We are testing a proxy for the promise, not the
  promise. Section 2 shows this distinction is not academic: most resets were
  justified on raceability, and only one was explicitly justified on performance
  convergence, which is the thing we actually measure.
- **Championship excitement.** Driver skill, reliability, and strategy are
  deliberately stripped out or controlled for. A season can be thrilling with a
  dispersed field.
- **Causation.** Every design here is observational with one treated unit per
  boundary. We can measure that a metric moved. We cannot attribute the movement
  to the regulations alone. See section 10.

---

## 2. Regulation resets in scope

Five boundaries. **2021 and 2022 are merged into a single boundary.** Section 10
confounds 1 and 2 argue that the cost cap, the sliding-scale aerodynamic testing
restrictions, and the ground-effect aero reset are collinear in time and cannot
be statistically separated; testing them as two independent boundaries would
contradict that and would double-count one intervention.

### 2.1 Boundary table

| Boundary | Change | Mechanism class | Intent-R: publicly justified as closer racing / more overtaking? | Intent-C: publicly justified as *field performance convergence*? | Tier |
|---|---|---|---|---|---|
| 2009 | Aero reset; slick tyres return; KERS | Major aero | **Yes** — Overtaking Working Group formed expressly to make overtaking easier | No | A |
| 2014 | 1.6L V6 turbo hybrid power units | Major PU | **No** — justified on thermal efficiency, road relevance, manufacturer engagement | No | A |
| 2017 | Wider cars, wider tyres, larger aero | Major aero | **No** — justified on lap-time reduction and spectacle; reduced overtaking was raised as a contemporaneous objection, not an aim | No | A |
| 2021–22 | Cost cap; sliding-scale ATR; floor cuts; ground-effect aero reset; 18in wheels | Mixed financial + aero | **Yes** — explicit target of cutting the following car's performance loss from ~50% to under 10% | **Yes** — cost cap and ATR are explicit financial/development convergence mechanisms | A + B |
| 2026 | New PU formula; active aero; smaller/lighter cars | Major PU + aero | **Yes** — FIA states closer racing and increased overtaking among the goals | No | A + B (partial) |

**Sources.** These are secondary reports of contemporaneous statements, not
primary regulatory documents. Phase 1 attempts to upgrade each to a primary FIA
source (regulation preamble, FIA World Motor Sport Council minutes, or FIA press
release); any that cannot be upgraded is marked as press-sourced in the memo.

- 2009 OWG: <https://www.racefans.net/2009/01/16/how-the-f1-rules-changes-for-2009-are-meant-to-improve-racing-part-13/>, <https://www.f1technical.net/news/11415>
- 2014 PU: <https://www.fia.com/sites/default/files/publication/file/FIA%20F1%20Power%20Unit%20leaflet.pdf>
- 2017: <https://www.motorsportmagazine.com/articles/single-seaters/f1/2017-f1-regulations-explained-pat-symonds/>, <https://www.skysports.com/f1/news/12433/10253792/f1-2017-where-are-plans-with-rules-for-faster-more-aggressive-cars-at>
- 2021–22: <https://africa.espn.com/f1/story/_/id/31822505/formula-one-releases-vision-2022-car>
- 2026: <https://www.fia.com/news/new-era-competition-fia-showcases-future-focused-formula-1-regulations-2026-and-beyond>, <https://www.formula1.com/en/latest/article/fia-unveils-formula-1-regulations-for-2026-and-beyond-featuring-more-agile.75qJiYOHXgeJqsVQtDr2UB>

### 2.2 Why intent is split into two columns

"Closer racing" and "a closer field" are different claims and the regulator makes
them separately. Intent-R is about *raceability* — whether a car can follow and
pass. Intent-C is about *performance convergence* — whether the cars are closer
in outright pace. **Our metric measures Intent-C and cannot measure Intent-R.**
Collapsing them into one column would let a raceability-justified reset be scored
against a convergence metric it never claimed to move.

### 2.3 The intent contrast — descriptive only (Amendment 1)

**Both intent contrasts are DESCRIPTIVE. Neither occupies a confirmatory slot.**

Intent-R compares boundaries the regulator justified as closer racing (2009,
2021–22, 2026) against those it did not (2014, 2017). That is a 3-versus-2
contrast on boundary-level estimates. A contrast that thin cannot justify a
multiplicity slot: it can detect only an enormous difference, a null result is
close to uninformative, and reserving a confirmatory test for it would spend
family-wise error budget on a question the data cannot answer. It is reported as
a descriptive comparison with its group sizes stated alongside it, always.

**Intent-C cannot be tested at all.** Only one boundary (2021–22) is
convergence-intended, and it is the boundary most contaminated by confounds 1
and 2.

**This is a finding about the question, not a failed test**, and it belongs in
the memo's opening framing beside the raceability-versus-convergence gap in §1:
*the sport rewrote its technical rules five times in this period and explicitly
promised a closer field once.* An analysis measuring pace convergence is
therefore measuring something the regulator, on its own public record, mostly did
not claim to be delivering. That reframes what a null result would even mean.

### 2.4 Intent evidence — regulator's own statements

Recorded here because it is the raw material of the intent classification in
§2.1, not because it bears on what we expect to find.

On 2021-05-13, ahead of the 2022 reset, Ross Brawn — then F1's managing director
for motorsports and a principal author of the regulations — publicly stated that
the field could be expected to spread initially under the new rules, while
expressing confidence that the gap would narrow in subsequent seasons as teams
converged on the new car concept. He also noted that following remained difficult
under the outgoing rules, which was the problem the reset targeted.
Source: Motorsport Week, 13 May 2021,
<https://www.motorsportweek.com/2021/05/13/brawn-expects-field-to-spread-under-new-2022-regulations/>

**Handling rule, binding.** This statement is intent evidence and nothing else.
It substantiates that the 2021–22 package was publicly framed as a long-run
convergence measure. It must **not** appear in the results narrative, the memo
abstract, the figure captions, or any text adjacent to an estimate, and it must
never be described as a prediction our results confirm or contradict. The
prohibition in §1 on stating a directional prior covers third-party predictions
quoted approvingly, not only our own.

### 2.5 Merged-boundary modelling note

Merging 2021 and 2022 creates a staged intervention: the cost cap and ATR begin
in 2021, the aero reset in 2022. A single breakpoint cannot represent both.
Two specifications are fitted and **both reported**:

- **S1 (primary).** Breakpoint at 2021, with 2021 and 2022 both flagged as
  treatment-onset seasons.
- **S2.** Two-season transition window (2021, 2022) excluded from both segments;
  the level change is estimated between the pre-2021 segment and the 2023+
  segment.

If S1 and S2 disagree, that disagreement is reported as a finding about the
merge, not resolved by preference.

---

## 3. Two-tier design

FastF1's lap-level timing does not reach the older resets. Rather than paper over
that, we run two independent pipelines and compare them.

**Tier A — long history, coarse metric.** Qualifying-derived field spread from
Jolpica (Ergast-compatible). Covers all five boundaries at lower resolution.

**Tier B — recent history, rich metric.** Fuel- and tyre-corrected race pace from
FastF1. Covers the two most recent boundaries at high resolution.

**Tier A is the primary tier.** Qualifying is low fuel, fresh tyres, maximum
attack, minimal traffic — a cleaner read on car performance than race pace, and
it needs far less modelling to extract. Tier B is an *independent* measurement of
the same underlying quantity over the recent era. Where the tiers agree,
confidence rises. Where they disagree, the disagreement is a reported finding,
not something to reconcile away. Section 8.6 gives a second, harder reason Tier A
must lead: Tier B's placebo pool is too small to defend a Tier B result on its own.

### 3.1 Tier A coverage floor

Qualifying format is not comparable across all of Ergast/Jolpica's history:

- 1996–2002: one-hour, 12-lap sessions
- 2003–2005: single-lap qualifying
- 2006–present: knockout Q1/Q2/Q3

**2006 is the Tier A floor** — the earliest season under a format comparable to
today. This brackets all five boundaries. Extending earlier would mix formats and
the measured "spread" would partly be a format artifact.

### 3.2 Session format versioning

Sprint weekends are included with a **format-version indicator, not a binary
flag** (Decision D), because the sprint format has itself changed more than once
and the versions differ in how much running precedes the grid-setting qualifying
session.

Format versions are **derived empirically from the observed session structure per
event in Phase 1**, not hardcoded from recollection. The provisional expectation
— to be confirmed or corrected by the coverage report — is that at least four
versions exist: conventional weekends; the 2021–22 sprint format; the 2023
sprint-shootout format; and a revised 2024+ ordering. The 2026 format is
determined from data. Any version boundary the data contradicts is corrected in
the coverage report, and the correction is committed.

Also flagged for Tier A: the 2016 elimination-qualifying experiment in the
opening rounds of that season.

All coverage claims in this section are **assumptions to be tested empirically in
Phase 1**, not asserted facts. The coverage report supersedes them.

---

## 4. Metric definitions

### 4.1 Tier A — qualifying-based

For event `e`, driver `d`, team `t`, segment `s` in {Q1, Q2, Q3}, let `T(d,s,e)`
be the lap time.

**Primary rule: segment-evolution adjusted.** Teams reaching Q3 set their best
lap on a more rubbered-in track than teams eliminated in Q1. That bias inflates
measured spread, and — decisively for this project — **the size of the bias
varies over time with format and tyre-allocation changes.** A time-varying bias
inside a time-series analysis of exactly the quantity being biased is not an
acceptable primary specification.

Estimate a per-event segment offset from drivers who set a valid time in more
than one segment:

```
For event e, for each adjacent segment pair (s, s+1):
    E(s -> s+1, e) = median over drivers d with times in both
                     of  ( T(d, s+1, e) - T(d, s, e) )
```

`E` is the track-evolution gain between segments, estimated from within-driver
differences so that car and driver quality cancel. Referencing all times to the
Q1 baseline:

```
offset(Q1, e) = 0
offset(Q2, e) = E(Q1 -> Q2, e)
offset(Q3, e) = E(Q1 -> Q2, e) + E(Q2 -> Q3, e)
T_adj(d, s, e) = T(d, s, e) - offset(s, e)
q(t, e)        = min over d in t, over s of T_adj(d, s, e)
```

This removes the mechanical component of the Q1/Q3 track difference. It does not
remove strategic effects (a front-runner not fully attacking in Q1), which
remains an acknowledged limitation.

**Guard.** `E` is estimated per event and requires a minimum number of
multi-segment drivers (proposed 5; Decision A). Where the estimate is
unavailable or implausible in sign, the event falls back to the unadjusted rule
and is flagged; the count of such events is reported.

### 4.1.1 Segment eligibility by era (Amendment 1)

Phase 1 established that **Q3 in 2006–2009 was run on race fuel** and is
therefore not an observation of low-fuel maximum-attack pace at all. Evidence:
`median(Q3−Q2)` is positive in every season 2006–2009 (+0.45 to +1.70 s) and
negative in every season 2010–2026 (−0.15 to −0.37 s), with no overlap between
the eras and the sign flipping exactly on the refuelling ban.

```
eligible_segments(season) = {Q1, Q2}          if 2006 <= season <= 2009
                          = {Q1, Q2, Q3}      if season >= 2010
```

**The rule is constant; its realisation is not.** The rule is "use every segment
that measures low-fuel maximum-attack pace." What changed is which segments
satisfy that, because the sport changed what Q3 was. Excluding a non-observation
is not the same as changing the estimator to suit an era — the distinction that
made this preferable to raising the Tier A floor to 2010, which would have
deleted the 2014-and-earlier boundaries including the least contaminated one.

For 2006–2009 the adjustment therefore needs only `E(Q1→Q2)`, which Phase 1
found era-stable (2006–09 median −0.428 s; 2010+ median −0.439 s).

### 4.1.2 Diagnostic D1 — era-dependent attack bias (Amendment 1)

**The cost this revision carries, stated before it is measured.** In 2006–2009
front-running teams are represented by a Q1 or Q2 lap. From 2010 the same teams
can be represented by a full-attack Q3 lap. If front-runners do not fully attack
in Q1 and Q2 — and the −0.43 s Q1→Q2 delta indicates they do not — then the
measured front-of-field gap is biased in an era-dependent way, concentrated at
exactly the ranks M4 and M5 measure.

**The §4.1.1 stability evidence does not settle this.** Equal median offsets
across eras do not establish equal *composition* of those offsets. The Q1→Q2
delta is a sum of track evolution and change in attack level, and two eras can
share a median while mixing those components differently. If the 2006–09 mix
carries more sandbagging and less evolution (or the reverse), the adjustment is
biased in a way a median comparison conceals. D1 tests the composition directly
rather than assuming it from the aggregate.

**D1a — offset by competitive stratum.** Track evolution improves the track for
everyone equally; sandbagging does not. Estimate `E(Q1→Q2)` separately for teams
that reach Q3 and teams eliminated before it:

```
Delta_strat(e) = E_front(Q1->Q2, e) - E_back(Q1->Q2, e)
```

A `Delta_strat` near zero implies the offset is predominantly track evolution. A
positive `Delta_strat` implies front-runners gain more between Q1 and Q2 than the
track alone explains — i.e. sandbagging. **The quantity of interest is whether
`Delta_strat` differs across the 2010 line.** If it is stable, the composition is
stable and the §4.1.1 adjustment is sound for both eras. If it shifts, it is not.

**D1b — segment-source composition by field position.** Per era, the share of
representative times drawn from each segment, split by whether the team finished
in the fastest third of the field. Quantifies mechanical exposure to the bias.

**D1c — front-of-field discontinuity at 2010.** Test M4 and M5 for a step at the
2010 season boundary under the §4.1.1 rule, alongside M1 and M2 as controls.
The bias signature is a step in the front-of-field metrics that the whole-field
metrics do not show. Note that 2010 is already a flagged discontinuity (the
refuelling ban), so this test cannot fully separate the two, and it is reported
with that stated.

**Pre-committed reporting.** If the front-of-field metrics behave differently
across the 2010 line under this rule, **that is a reported finding**, stated in
the memo body, whether or not it complicates the headline. D1 is added to
confound 15 and its results are reported regardless of outcome.

### 4.1.3 D1 results and the rules they trigger (Amendment 2)

**D1a — tested, not detected at achievable resolution.** The front-minus-back
`E(Q1→Q2)` offset is −0.3035 s in 2006–09 and −0.3330 s in 2010+. The shift
across the 2010 line is +0.0295 s, bootstrap 95% CI [−0.0472, +0.0938],
containing zero.

This is recorded as **"condition 3 tested, not detected at achievable
resolution," not "concern resolved."** The CI is not an equivalence test. It
rules out composition shifts larger than roughly **0.09 s**; it says nothing
about smaller ones, and the early era contributes 70 events against 337. A
composition shift below the detection floor remains possible and is not claimed
to be absent.

**D1b — unresolved, and not benign.** Front-third teams draw **0%** of their
representative times from Q3 before 2010 and **57.7%** after, with their Q1
share falling from 42.6% to 20.7%. The back two-thirds barely move. This is a
**measurement discontinuity sitting inside a study designed to detect
discontinuities**, located precisely at the ranks M4 and M5 measure.

**Pre-committed restriction rule, fixed here before D1c runs in Phase 4.** If
M4 or M5 shows a level shift at the 2010 season boundary comparable in magnitude
to the shifts attributed to reset boundaries, then:

> **M4 and M5 cannot carry a cross-2010 claim.** They are restricted to
> within-era comparison, and any boundary estimate from them spanning 2010 is
> withdrawn from the memo rather than caveated in it.

"Comparable in magnitude" is fixed in advance as: the absolute 2010 level shift
is at least half the median absolute level shift across the five reset
boundaries, on the same metric. This rule is written now precisely so it cannot
be decided after seeing D1c.

**2010 joins the placebo battery as a known measurement-artifact boundary**
(§8.6). If the method reports a "reset effect" at a season with no reset but a
large measurement change, that is diagnostic of **the method**, not of F1.

### 4.1.4 Stratum misspecification in the evolution offset (Amendment 2)

D1a established something the plan did not anticipate and that is a finding in
its own right, independent of the era question:

**The `E(Q1→Q2)` offset is not pure track evolution in either era.**
Front-runners gain approximately 0.3 s *more* than backmarkers between Q1 and
Q2, against a field-wide offset of roughly −0.43 s. Track evolution improves the
track for everyone equally; this differential does not. The §4.1 field-wide
median offset is therefore a **weighted average of two distinct quantities** —
track evolution, and a sandbagging differential that varies by field position —
and is misspecified by stratum.

**What survives and what does not.** The differential is stable across the 2010
line (D1a), so it biases the *level* of measured field spread, not the *trend*.
Boundary estimates, which are differences across a boundary, difference it out
and survive. But:

> **Any absolute-level statement about field spread inherits this bias**, even
> though boundary comparisons do not. The memo may say "the field converged by
> X% at boundary Y." It may **not** say "the field spread was X%" as a
> standalone quantity without stating that the figure carries a stratum-dependent
> offset bias of order 0.3 s in the underlying lap times.

Mitigation: **R16** re-estimates the offset separately by field position
(stratified offset) and re-runs everything, testing directly whether the
misspecification reaches the metrics. Recorded as confound 16.

**Normalisation.** Percentage off the fastest team, so circuits of different lap
length are comparable:

```
delta(t,e) = 100 * ( q(t,e) / min over u of q(u,e)  -  1 )
```

`delta` is 0 for the fastest team by construction, positive for everyone else.

**R8 runs before the metric freeze, not after**, and is a **four-way sweep**
(Amendment 1). All four Tier A scope options tabled in the coverage report are
run as robustness, not merely the segment-rule variants originally scoped:

| Variant | Rule |
|---|---|
| **O3 (primary)** | Q3 excluded 2006–09; all three segments 2010+; evolution-adjusted |
| O1 | Tier A floor raised to 2010; all three segments throughout |
| O2 | Q1+Q2 only, every season |
| O4 | Q1 only, every season |

They are computed and compared in Phase 4 *before* the primary metric is frozen,
because the choice demonstrably interacts with the time-series structure.

**Pre-committed decision rule for the 2009 boundary, fixed before results
exist.** O1 excludes the 2009 boundary entirely; O3 retains it on Q1/Q2 evidence.
These are the two defensible treatments of that boundary and they rest on
different data. Therefore: **if the sign or the significance of the 2009 boundary
estimate differs between O1 and O3, the memo reports 2009 as INDETERMINATE.** We
do not select whichever option produces the cleaner story. This commitment is
made here, in advance, precisely because it will be tempting to break later.

### 4.2 Tier A — competitiveness metrics per event

**Fixed rank windows are not comparable across seasons** because grid size varies
over the study period (verified empirically per season in the coverage report —
see section 10, confound 4). Every metric below is therefore defined by
percentile of the field where a percentile definition is meaningful, with the
fixed-rank form retained as an explicit robustness variant (R15).

Let `N` be the number of teams at event `e`, ranked by `delta` ascending.

| ID | Name | Primary definition (percentile) | Fixed-rank variant (R15) | Question it answers |
|---|---|---|---|---|
| M1 | Field spread | `sd(delta)` over all teams | — | How dispersed is the whole grid? |
| M2 | Robust field spread | `IQR(delta)` over all teams | — | Same, insensitive to one outlier team |
| M3 | Leader-to-midfield | `median(delta)` over teams in the 30th–70th percentile of the field by `delta` | `median(delta ranks 4..7)` | How far is the midfield off the front? |
| M4 | Front-group vs rest | `mean(delta above 20th pct) - mean(delta in fastest 20%)` | `mean(ranks 3..N) - mean(ranks 1..2)` | Is there a breakaway at the front? |
| M5 | Front-pair gap | `delta(rank 2)` — rank-based by definition; "second-fastest team" is grid-size invariant in meaning | — | Is the fight for wins close? |
| M6 | Backmarker gap | `delta(rank N)` — grid-size sensitive by construction | — | How bad is the tail? |
| M7 | Teammate delta | `median over t of abs(delta(d1) - delta(d2))` | — | Driver-noise floor — not a competitiveness metric but the denominator telling us what car differences are even resolvable |

**Hardcoding audit.** M1, M2 and M7 are grid-size invariant. M3 and M4 were
rank-hardcoded and are redefined by percentile above. M5 is rank-based but its
meaning ("the second-fastest car") does not change with grid size, so it stays.
M6 is grid-size sensitive *by construction* — adding an eleventh, slow team
changes it mechanically. M6 is retained precisely because that sensitivity makes
it a diagnostic for confound 4, and it is never used as a primary metric. M2 is
the mitigation for the same confound.

**Season aggregate.** Median across events in the season, not mean — one wet or
disrupted qualifying should not move the season value. Uncertainty by cluster
bootstrap resampling events within season (10,000 resamples, seed recorded).

### 4.3 Tier B — race pace

Per race `r`, fit on representative laps only, robustly (Huber loss, to resist
residual outliers that survive filtering):

```
laptime = sum_d gamma_d * I[driver = d]
        + sum_c ( a_c + b_c * tyre_age ) * I[compound = c]
        + phi * lap_number
        + epsilon
```

- `gamma_d` — driver fixed effect; the quantity of interest. It absorbs the car,
  which is what we want; driver skill contaminates it, which is what M7
  quantifies.
- `b_c` — per-compound degradation slope, **estimated, not assumed**.
- `phi * lap_number` — fuel-burn proxy. Linear, because fuel mass declines
  approximately linearly with laps completed. Estimated per race, not fixed at a
  folk constant such as 0.03 s/lap.
- Circuit, weather, and track surface are absorbed by fitting per race.

**Team pace: best-of-team, with a stated cost.** Team pace is the faster of its
two drivers' `gamma`, mirroring the Tier A best-of-team convention so both tiers
measure the same construct. This **imports driver quality into a car-performance
metric, and does so unevenly across the study period** — a team with one
exceptional and one weak driver reads faster than a team with two average drivers
in the same car, and the size of that effect depends on how lopsided each
driver pairing happens to be in a given season.

Three consequences, all binding:

1. **R14** re-runs everything with team pace defined as the mean of both drivers.
2. **M7 must be reported alongside any best-of-team result.** M7 is the scale of
   within-team driver variation; a measured between-team convergence smaller than
   the prevailing M7 is not interpretable as a car effect. The memo states the
   M7 value next to the headline estimate.
3. Any interpretation of a best-of-team result explicitly references M7. This is
   a requirement on the Writer role, not a suggestion.

Then normalise to percent off fastest exactly as in 4.1 and compute M1–M7
identically.

**Baseline comparator.** The same metrics computed from the plain median
clean-air lap time per team, with no regression at all. If the elaborate model
and the crude median tell the same story, the model is not doing the work and we
should say so. If they diverge, we investigate before trusting the model.

### 4.4 Pace model diagnostics — ship gates

The model does not ship until all of these are produced and reviewed:

1. Residual vs fitted, residual vs lap number, residual vs tyre age, per race.
2. R-squared and residual SD per race, plotted across all races; outlier races
   listed by name.
3. **Sanity check:** Spearman rank correlation between recovered team pace order
   and (a) that event's qualifying order, (b) the finishing order of each team's
   lead car. Any race with rho below 0.5 on both is flagged and manually
   investigated before inclusion.
4. Explicit check that no known backmarker is ranked fastest. If that happens the
   model is wrong; we debug it rather than shipping it with a caveat.

---

## 5. Seasons in scope

**Decision G is CLOSED** (Amendment 1), resolved by the Phase 1 coverage report.
These are now verified facts, not assumptions:

- **Tier A: 2006–2026**, 21 seasons. All return per-segment qualifying times;
  no season is missing. Q3 is ineligible in 2006–2009 per §4.1.1.
- **Tier B: 2018–2026**, 9 seasons. Verified empirically: 2014–2017 return no
  lap data at all, on every probe; 2018–2026 return `LapTime` (92.6–99.9%),
  `Compound` (100%), `TyreLife` (97.3–100%), `TrackStatus` (100%), plus stint
  and pit fields, in every probed session.

**Tier B is corroboration only and cannot carry an independent conclusion.**
Its placebo pool is 2 boundaries (§8.6), and the 2021–22 boundary's Tier B
pre-period is 2018–2020, of which 2019 and 2020 are both flagged discontinuities
— leaving **one unflagged pre-season**. The memo states this wherever a Tier B
result appears, and the README states it too so that a reader need not find it.

---

## 6. Exclusion rules

Every filter logs the row count it removes, individually and in order. A filter
that removes an unexpected share of rows is a bug until proven otherwise. The
row-loss ledger goes to the analyst before any threshold is finalised
(Decision A).

### 6.1 Session-level

- Wet or mixed-condition sessions: **flagged, analysed separately, never silently
  dropped.** Primary analysis is dry-only; a wet-inclusive robustness run is
  reported (R6).
- Red-flagged or shortened sessions: flagged; included only if the surviving
  representative-lap count clears the per-session minimum.
- Sprint weekends: included, carrying the format-version indicator of section 3.2.
- Minimum viable session: fewer than `K` representative laps for a team means
  that team has no observation at that event (proposed `K = 5`, Decision A).

### 6.2 Lap-level (Tier B)

Applied in this order, each logged:

1. In-laps and out-laps (pit entry or exit on the lap)
2. Lap 1 of the race
3. Any lap where track status is not green for its full duration (SC, VSC, yellow)
4. Laps in a formation or restart sequence
5. Laps slower than `X` percent of the driver's own session best (Decision A)
6. Traffic: laps started within `G` seconds of the car ahead (Decision A) — a
   filter, not a covariate, because the effect of traffic on lap time is strongly
   non-linear
7. First lap of each stint (tyre warm-up)
8. Laps with missing compound, stint, or track-status data

### 6.3 Qualifying-level (Tier A)

- A team with no time set in any segment has no observation at that event.
- Sessions where a red flag prevented a majority of the field from setting a
  representative time are excluded, and each exclusion is listed by name.
- **Deleted lap times (track limits): FILTER REMOVED** (Amendment 1). Phase 1
  probed the API as this plan required. Every qualifying result in all 21 seasons
  carries exactly `number, position, Driver, Constructor, Q1, Q2, Q3` and nothing
  else; there is no deleted-lap, invalidated-lap, or track-limits marker in any
  season. Per the original instruction, the filter is **declared unimplementable
  and removed** rather than left as a rule that silently never fires. The
  resulting bias is recorded as confound 13.

---

## 7. Team continuity

Constructors rebrand, change engine suppliers, change owners, and occasionally
change legal entity. Whether a rebrand is the same team is a modelling decision
that directly affects every season-boundary comparison, and there is no
data-driven answer to it.

Two mappings are built and **both are run**:

- **Continuity mapping (primary, Decision C)** — a constructor lineage is one
  entity across rebrands (for example the Jordan / Midland / Spyker / Force India
  / Racing Point / Aston Martin lineage as a single series). Chosen because a
  rebrand usually retains the factory, the wind tunnel, and most of the staff;
  under the strict alternative that lineage becomes five short unrelated series
  and the time-series windows fragment further than section 8.5 already
  documents.
- **Strict mapping (R2)** — each constructor name is its own entity; a rebrand
  starts a new series.

Genuinely ambiguous cases (the 2009 Brawn transition, the 2018 Force India
administration) are listed explicitly in the mapping file with reasoning for each,
not resolved silently in code.

---

## 8. Statistical approach

### 8.1 Unit of analysis

Event-level metric values, clustered within season. Season-level values are the
median of event values.

### 8.2 Per-boundary estimate — segmented interrupted time series

Per metric, per boundary at season `Y`:

```
metric_s = b0 + b1*(s - Y) + b2*I[s >= Y] + b3*(s - Y)*I[s >= Y] + error
```

- `b2` — level change at the boundary. Tests H1.
- `b3` — slope change after the boundary. Tests H2.

Intended window: 4 seasons either side. Standard errors clustered by season.
Confidence intervals by cluster bootstrap over events (10,000 resamples, seed
recorded), not from the asymptotic OLS formula, because n is small and the
residuals are not plausibly iid. Two-sided throughout.

### 8.3 Pooled estimate — the headline

Section 8.2 gives **one treated unit per boundary**. A single boundary estimate
carries irreducible uncertainty that no within-boundary bootstrap can represent,
because the bootstrap resamples events, not histories. The memo therefore leads
with a **pooled estimate across boundaries**, with per-boundary estimates as
underlying detail (Decision F).

Random-effects meta-analysis over the five boundary-level `b2` estimates,
weighted by inverse variance from the cluster bootstrap:

```
b2_k = mu + u_k + e_k,   u_k ~ N(0, tau^2),   e_k ~ N(0, v_k)
```

- `mu` — pooled level change. **The headline number.**
- `tau^2`, `I^2` — between-boundary heterogeneity. **Reported alongside `mu`
  always.** If boundaries are strongly heterogeneous, the pooled estimate is an
  average of things that are not the same and the memo says so in place of, not
  after, the headline.
- With k = 5, `tau^2` is poorly estimated. Confidence intervals use the
  **Hartung–Knapp–Sidik–Jonkman adjustment**, which is the standard correction
  for small numbers of studies and is materially more conservative than
  DerSimonian–Laird here.

The same pooling is applied to `b3` for H2, subject to section 8.5.

### 8.4 Multiplicity — exact counts

The reset list is final at five boundaries, so the test counts are exact rather
than approximate.

**Confirmatory family — 2 tests** (Amendment 1; was 3). Holm–Bonferroni at
alpha = 0.05 across:

1. Pooled `mu` for `b2` (H1, level)
2. Pooled `mu` for `b3` (H2, slope) — subject to section 8.5.1

Both on the single primary metric chosen in Decision B, pre-registered before
results exist.

The third slot previously held the Intent-R contrast. It is **returned to the
budget, not reallocated** — the family is 2, and the Holm correction is
correspondingly less severe. Intent contrasts are now descriptive only (§2.3),
because a 3-versus-2 comparison does not justify spending family-wise error
budget on a question the data cannot answer.

**Secondary family — 10 estimates.** Per-boundary `b2` and `b3` for each of the
5 boundaries, on the primary metric. Holm-corrected within the family. Reported
as detail underlying the pooled result, never as standalone conclusions.

**Exploratory — everything else.** All non-primary metrics, all tier
comparisons, the entire robustness battery. Benjamini–Hochberg FDR at q = 0.10,
labelled exploratory in every table and chart, never stated as conclusions.

The total number of tests run is reported in the memo as an exact figure.

### 8.5 Window collisions — computed in advance

Five boundaries across 21 seasons with ±4-season windows collide almost
everywhere. This is computed here rather than discovered later.

Tier A range 2006–2026. Reset seasons: 2009, 2014, 2017, 2021, 2022, 2026.
Flagged discontinuities: 2010 (refuelling ban), 2016 (Tier A: elimination
qualifying), 2019 (front wing), 2020 (COVID calendar), 2023 (floor edge).

| Boundary | Intended window | Actual window | Truncated by | Intruding resets | Flagged seasons inside |
|---|---|---|---|---|---|
| 2009 | 2005–2013 | **2006–2013** | Tier A floor (pre = 3 seasons) | none | 2010 |
| 2014 | 2010–2018 | 2010–2018 | — | **2017 (in post)** | 2010, 2016 |
| 2017 | 2013–2021 | 2013–2021 | — | **2014 (in pre), 2021 (in post)** | 2016, 2019, 2020 |
| 2021–22 | 2017–2025 | 2017–2025 | — | **2017 (at pre edge)** | 2019, 2020, 2023 |
| 2026 | 2022–2030 | **2022–2026** | end of data (post = 1 partial season) | **2022 (in pre, = package year 2)** | 2023 |

**2009 is the least contaminated boundary — not a clean one** (Amendment 1). It
is the only boundary with no intruding *reset*, and its pre-period is truncated
to three seasons by the Tier A floor. Every other boundary has at least one reset
inside its window. But "no intruding reset" is a narrow claim and the earlier
draft's use of "clean" overstated it. The 2009 boundary carries at least four
co-occurring shocks that no model here separates, listed as confound 14:

1. **Three simultaneous technical changes** — the aero reset, the return of slick
   tyres, and the introduction of KERS all land in 2009. Whatever moves, we
   cannot attribute it to any one of them.
2. **Honda's withdrawal producing Brawn** — a constructor exits and its successor
   enters *inside the window*, and under the continuity mapping (Decision C1) that
   transition is treated as continuous when it arguably is not.
3. **The 2008 financial crisis**, which reshaped budgets across the grid during
   the pre-period, an uncontrolled shock to exactly the resource asymmetry the
   metric is sensitive to.
4. **Race-fuel qualifying** across 2006–2009 (§4.1.1), meaning the entire
   pre-period and the boundary season itself are measured on Q1/Q2 only, with the
   attack-level bias D1 quantifies.

The word "clean" is not used of this or any boundary, in this plan or the memo.
"Least contaminated" is the accurate description and the only one permitted.

### 8.5.1 Consequence for H2 — stated in advance

H2 is defined against "a comparable stable-regulation period." Removing reset
seasons and flagged discontinuities from 2006–2026 leaves eligible seasons
2006, 2007, 2008, 2011, 2012, 2013, 2015, 2018, 2024, 2025 — in consecutive runs
of **3, 3, 1, 1, and 2 seasons**. The longest uninterrupted stable-regulation
period in the entire study window is three seasons.

**A three-season run cannot support a credible slope estimate to compare a
post-reset slope against.** Therefore:

- H2 is **downgraded from hypothesis to descriptive estimate**. Post-reset slopes
  are reported with confidence intervals, but the phrase "faster than in a stable
  period" is not used, because no adequate stable period exists in this data.
- H2's confirmatory slot in section 8.4 is retained so the multiplicity budget is
  not quietly reduced, but any H2 result is reported with this limitation stated
  in the same sentence.
- If the Phase 1 coverage report changes the season range enough to create a
  longer uninterrupted run, H2 may be restored — as a new commit stating the change and
  its reason, never a silent edit.

This is a limitation of the sport's regulatory cadence, not of the data source.
F1 has not left the rules alone for long enough to establish a baseline.

### 8.6 Placebo test — pool sizes computed in advance

The same segmented model is fitted at every eligible non-reset season boundary. If
real reset boundaries do not produce larger shifts, more often, than placebo
boundaries, then regulation resets are not distinguishable from ordinary
season-to-season churn — and that is the finding. **This test runs regardless of
outcome.**

Season-to-season boundaries in 2007–2026: 20. Excluding reset boundaries (2009,
2014, 2017, 2021, 2022, 2026) and flagged discontinuities (2010, 2019, 2020,
2023):

| Pool | Eligible boundaries | Count |
|---|---|---|
| **Tier A** (2006–2026, also excluding 2016) | 2007, 2008, 2011, 2012, 2013, 2015, 2018, 2024, 2025 | **9** |
| **Tier B** (2018–2026, verified) | 2024, 2025 | **2** |

**2010 is added as a known measurement-artifact boundary** (Amendment 2). It is
not a reset and not an ordinary control: it is the season at which Tier A's
front-of-field measurement basis changes (§4.1.2, D1b — front-third Q3 sourcing
goes 0% → 57.7%) and at which the refuelling ban lands. It is therefore run as a
**diagnostic placebo, reported separately from the 9-boundary pool**, and it
carries a distinct interpretation:

> A "reset effect" detected at 2010 — a season with no reset but a large
> measurement change — is diagnostic of **the method**, not of Formula 1. If the
> method fires at 2010, the memo reports that before it reports any boundary
> result, because it bears on whether the other estimates mean anything.

**Caveats that travel with every placebo result:**

- **Tier B's placebo pool is 2 boundaries.** A null placebo result in Tier B is
  not reassurance; it is an absence of evidence from a test with almost no power.
  The memo states the pool size wherever a placebo result appears. This is the
  second and harder reason Tier A leads (section 3).
- Tier A's pool of 9 is workable but not comfortable.
- These are *naive* counts, requiring only that the boundary season itself be
  reset-free and unflagged. A stricter requirement — that the boundary's ±4 window contain no reset
  — is satisfied by close to zero boundaries, per section 8.5. The exact strict
  count is computed in Phase 5 and reported; if it is zero, that is reported as
  zero.

---

## 9. What would prove the hypothesis wrong

Committed in advance so the answer cannot be reverse-engineered from the result.
The three outcomes below are stated in parallel and the memo must be equally
willing to print any of them.

**We report a narrowing effect** if the pooled `mu` for `b2` is negative with a
Holm-corrected bootstrap 95% CI excluding zero, heterogeneity is not dominant,
and the result survives the robustness threshold in section 11.

**We report a widening effect** if the pooled `mu` for `b2` is positive under the
identical conditions.

**We report no measurable effect** if any of the following hold:

1. The pooled `mu` has a Holm-corrected 95% CI containing zero; **or**
2. Placebo boundaries produce shifts of comparable magnitude at a comparable
   rate (subject to the pool-size caveats in section 8.6); **or**
3. Tier A and Tier B disagree in sign at a boundary both cover, and neither is
   demonstrably more reliable there; **or**
4. The conclusion flips under a reasonable alternative metric, segment rule, or
   team-continuity mapping (section 11); **or**
5. Between-boundary heterogeneity is large enough that the pooled estimate
   averages incompatible effects.

---

## 10. Known confounds, listed before results exist

1. **Cost cap.** Financial regulations arrived in 2021, immediately before the
   2022 aero reset. Their effects **cannot be statistically separated** from the
   aero reset — one treated unit, treatments collinear in time. This is why the
   two are merged into one boundary (section 2). Stated plainly in the memo body,
   not in a footnote. Any 2021–22 finding is a finding about the *package*.
2. **Sliding-scale aero testing restrictions.** Introduced 2021; gives
   lower-placed teams more wind tunnel time. A mechanism *designed* to converge
   the field, operating independently of the aero rules, on the same timeline.
   Same collinearity; same merge.
3. **Calendar composition.** The circuit mix changes between seasons and some
   circuits spread the field more than others. Mitigation: R3.
4. **Grid composition.** Teams enter and leave. New entrants are typically slow
   and widen measured spread for reasons unrelated to regulations. **The number
   of constructors per season is reported as empirical fact in the coverage
   report; this plan does not assume it.** Mitigations: M2 (IQR) reported
   alongside M1 (SD); M6 retained as a diagnostic for this confound specifically;
   constant-constructor robustness check (R4).
5. **Partial seasons.** The 2026 season is in progress. Its result carries an
   explicit provisional label everywhere it appears, **including in every chart
   caption** (Decision E). R11 re-runs without it. Note the compounding problem:
   2026 is both the partial season and the boundary with only one post-period
   season (section 8.5).
6. **Session format changes.** Sprint weekends change the running available
   before qualifying, which plausibly affects qualifying spread independently of
   the cars. Mitigation: format-version indicator (section 3.2) and R5.
7. **Tyre specification changes.** The tyre supplier changes construction and
   compound allocation on its own schedule, sometimes mid-season. These shift
   degradation and can shift field order with no aero change.
8. **Power unit supply.** A customer team's pace is partly its engine supplier's.
   Both the 2014 and 2026 boundaries are PU-led, and customer teams sharing a PU
   are not independent observations. Mitigation: **R13**, which groups teams by
   PU supplier.
9. **Metric sensitivity.** A different reasonable metric may reverse the
   conclusion. Tested in section 11 and reported whether or not convenient.
10. **Qualifying segment evolution.** Addressed by the primary rule in section
    4.1; residual strategic effects remain.
11. **Sandbagging and engine modes.** Qualifying is maximum attack, but teams do
    manage engine modes and fuel strategically. Unquantifiable here; stated as an
    irreducible limitation.
12. **Driver quality in team pace.** Best-of-team imports driver skill unevenly
    across the period. Mitigations: R14, and the mandatory M7 reporting rule in
    section 4.3.
13. **Deleted qualifying laps, unobservable** (Amendment 1). No source field
    exists (§6.3), so a lap deleted for track limits that nonetheless appears in
    the published times slightly flatters that team. This is **time-varying**:
    automated track-limits enforcement became markedly more aggressive in the
    later seasons, so the bias is plausibly larger at the end of the study window
    than at the start — which places it inside a time-series analysis of exactly
    the quantity it biases. It cannot be bounded from this source and is not
    dismissed as noise.
14. **2009 boundary co-treatments** (Amendment 1). The least contaminated
    boundary still carries four co-occurring shocks that no model here separates:
    three simultaneous technical changes (aero, slicks, KERS); Honda's withdrawal
    producing Brawn as a new entity inside the window; the 2008 financial crisis
    reshaping grid budgets during the pre-period; and race-fuel qualifying across
    the whole pre-period and boundary season. See §8.5.
15. **Era-dependent attack bias from segment eligibility** (Amendment 1). Under
    §4.1.1, front-running teams are represented by a Q1/Q2 lap in 2006–2009 and
    can be represented by a full-attack Q3 lap from 2010. Because front-runners
    do not fully attack in Q1/Q2, this is an era-dependent bias concentrated at
    exactly the ranks M4 and M5 measure. Equal median Q1→Q2 offsets across eras
    do **not** establish equal composition of those offsets. Quantified by
    diagnostic D1 (§4.1.2); any differential behaviour of the front-of-field
    metrics across the 2010 line is a reported finding.
16. **Stratum misspecification in the evolution offset** (Amendment 2). The
    §4.1 field-wide `E(Q1→Q2)` offset is a weighted average of track evolution
    and a sandbagging differential that varies by field position: front-runners
    gain ~0.3 s more than backmarkers, in both eras, against a field-wide offset
    of ~−0.43 s. Because the differential is era-stable it biases the level, not
    the trend, so boundary estimates survive — but **every absolute-level
    statement about field spread inherits it**. Mitigation: R16. See §4.1.4.
17. **Wet qualifying sessions undetectable in Tier A before 2018**
    (Amendment 2). Plan §6.1 requires wet sessions be flagged and the primary
    analysis run dry-only. **Tier A has no weather source**: Jolpica exposes no
    weather field in any season, and FastF1 weather begins in 2018. Systematic
    wet-session detection is therefore unavailable for Tier A across 2006–2017,
    which is twelve of the twenty-one seasons and includes three of the five
    boundaries. A spread-based proxy is **explicitly rejected as circular** —
    spread is the metric being estimated, so inferring wetness from it would
    launder the outcome into the filter. This is an open gap requiring an
    analyst decision, not a solved problem.

---

## 11. Robustness battery (run regardless of outcome)

Every one of these is reported, including the ones that undermine the headline.

| Check | Varies | Guards against |
|---|---|---|
| R1 | Every candidate metric M1–M6 as primary | Metric cherry-picking |
| R2 | Continuity vs strict team mapping | Rebrand modelling |
| R3 | Constant-circuit subset | Calendar composition |
| R4 | Constant-constructor subset | Grid composition |
| R5 | Sprint weekends in / out | Session format |
| R6 | Wet sessions in / out | Condition filtering |
| R7 | Representative-lap threshold swept across a range | Arbitrary cutoffs |
| R8 | **Four-way Tier A scope sweep: O3 (primary) / O1 / O2 / O4** — runs before the metric freeze (§4.1). Carries the pre-committed 2009-indeterminate rule. | Qualifying bias; scope-choice sensitivity |
| R9 | Tier A vs Tier B on the overlap era | Method dependence |
| R10 | Regression pace model vs raw median clean-air pace | Model overreach |
| R11 | 2026 in / out | Partial season |
| R12 | ITS window width 3 / 4 / 5 seasons | Window arbitrariness |
| R13 | **Teams grouped by power-unit supplier** | Non-independence of customer teams; PU-led boundaries (confound 8) |
| R14 | **Team pace = both drivers' mean vs faster driver** | Driver quality imported into a car metric (confound 12) |
| R15 | **Percentile vs fixed-rank definitions of M3, M4** | Grid-size sensitivity of rank windows |
| R16 | **Stratified evolution offset (estimated separately by field position) vs field-wide offset** (Amendment 2) | Stratum misspecification, confound 16 (§4.1.4) |

**Reporting rule.** The battery is 16 checks. The threshold is two-thirds,
preserving the ratio originally set at 8 of 12: a headline claim surviving
**fewer than 11 of 16** is downgraded from "finding" to "suggestive," in the
memo, in those words.

*Rounding note:* two-thirds of 16 is 10.67. The threshold rounds **up** to 11,
never down — a robustness bar is not relaxed by arithmetic convenience. At 12
and 15 the ratio was exact (8/12, 10/15); at 16 it is not, and 11/16 = 0.688 is
marginally stricter than 0.667.

### 11.1 Boundary-specific robustness checks (Amendment 2)

These bear on a single boundary, not the headline claim, and are therefore
**reported separately and excluded from the 16-check battery count** — folding a
one-boundary check into the bar that gates every claim would misrepresent both.

| Check | Varies | Boundary | Reporting rule |
|---|---|---|---|
| B1 | Brawn 2009 as continuation vs as new entity | 2009 | **If the 2009 result depends on this choice, the memo says so in the body**, not in a footnote |

B1 exists because the Brawn transition is simultaneously the most contestable
call in the continuity mapping (DECISIONS.md 004) and located inside the window
of the least contaminated boundary (confound 14). Those two facts together make
it the single place where a mapping judgement could most plausibly manufacture a
result.

---

## 12. Decision ledger

Full ledger with reasoning, alternatives rejected, and dates in
[`DECISIONS.md`](DECISIONS.md). Summary of status at pre-registration:

| ID | Question | Status |
|---|---|---|
| A | Representative-lap thresholds; wet handling | **DEFERRED** to Phase 2 (row-loss ledger first) |
| B | Primary metric | **DEFERRED** to Phase 4 |
| B′ | Qualifying segment rule | **DECIDED** — evolution-adjusted primary |
| B″ | Tier A segment eligibility by era | **DECIDED** (Amdt 1) — O3: Q3 excluded 2006–09; R8 four-way sweep; 2009-indeterminate rule pre-committed |
| C1 | Team continuity mapping | **DECIDED** — continuity primary, strict as R2 |
| C2 | Reset list | **DECIDED** — five boundaries, 2021–22 merged |
| C3 | Intent classification | **DECIDED** — split Intent-R / Intent-C, sourced; **descriptive only** (Amdt 1) |
| D | Sprint weekends | **DECIDED** — include, format-version indicator |
| E | Partial 2026 season | **DECIDED** — include, provisional label, R11 |
| F | Effect horizon | **DECIDED** — H1 leads, pooled; H2 equal billing but downgraded per 8.5.1 |
| G | Seasons in scope per tier | **CLOSED** (Amdt 1) — Tier A 2006–2026, Tier B 2018–2026, both verified |
| H | All interpretation | **OPEN** — analyst owns, permanently |

---

## 13. Reproducibility

- One command (`make all`, or `python -m src.pipeline`) rebuilds every
  intermediate from a clean clone.
- FastF1 cache enabled **before the first request**; raw cache gitignored.
- Jolpica requests rate-limited and cached to disk; no repeat calls.
- Processed tables to Parquet under `data/processed/`, each with a data
  dictionary naming every column, its units, and its provenance.
- Dependencies pinned. Random seeds fixed and recorded for all bootstraps.
- `coverage_report.md` is generated from the data, not written by hand.
