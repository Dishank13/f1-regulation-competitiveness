# ANALYSIS PLAN — Did F1 regulation resets make the field more competitive?

**Status: PRE-REGISTRATION. Approved by the analyst 2026-09-06.**
This file is committed *before* any analysis code exists and is tagged
`pre-registration`. History before that tag is never rewritten. Any later change
is a new commit stating what changed and why, never an amendment. The git
history is the audit trail.

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

### 2.3 The intent contrast test, and its power

**Confirmatory test.** Does the regulator's stated aim predict anything? Compare
the pooled level change across Intent-R = Yes boundaries (2009, 2021–22, 2026)
against Intent-R = No boundaries (2014, 2017).

**Stated in advance: this test is severely underpowered.** It is a 3-versus-2
contrast on boundary-level estimates. It can detect only an enormous difference,
and a null result is close to uninformative. It is reported with that caveat
attached in the memo, in the same sentence as the estimate, and it never carries
a conclusion on its own.

**Intent-C cannot be tested at all.** Only one boundary (2021–22) is
convergence-intended, and that is the boundary most contaminated by confounds 1
and 2. A one-versus-four contrast is not a test. This is reported as a structural
limitation, not attempted and quietly dropped. It is arguably the single most
uncomfortable fact in the design: the sport has rewritten its rules five times in
this period and explicitly promised a closer *field* once.

### 2.4 Merged-boundary modelling note

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

**Normalisation.** Percentage off the fastest team, so circuits of different lap
length are comparable:

```
delta(t,e) = 100 * ( q(t,e) / min over u of q(u,e)  -  1 )
```

`delta` is 0 for the fastest team by construction, positive for everyone else.

**R8 runs before the metric freeze, not after.** The three candidate segment
rules — evolution-adjusted (primary), best-of-any-segment, Q1-only — are computed
and compared in Phase 4 *before* the primary metric is frozen, because the choice
demonstrably interacts with the time-series structure. If the rules disagree
materially, that is reported to the analyst as part of the Phase 4 decision
package rather than surfacing as a Phase 6 robustness footnote.

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

**Deferred to Decision G**, resolved after the Phase 1 coverage report. Working
assumptions to be tested, not asserted:

- Tier A: 2006 to 2026, subject to Jolpica actually returning per-segment
  qualifying times for those seasons.
- Tier B: the earliest FastF1 season with complete lap, stint, compound, and
  track-status data, through to 2026. Commonly cited as 2018, **to be verified
  season by season rather than assumed.**

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
- **Deleted lap times (track limits): implementability unverified.** This plan
  does *not* assume Jolpica exposes a deleted-lap or invalidated-lap field.
  Phase 1 explicitly probes the API for it. Two outcomes, both reported in the
  coverage report:
  - *Available* — the filter is implemented and its row-loss logged like any other.
  - *Not available* — **the filter is declared unimplementable and removed from
    this plan** rather than left as a rule that silently never fires. The
    resulting bias (a deleted lap that stood in the published times slightly
    flatters that team) is then stated as a limitation, with its likely magnitude
    bounded if possible.

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

**Confirmatory family — 3 tests.** Holm–Bonferroni at alpha = 0.05 across:

1. Pooled `mu` for `b2` (H1, level)
2. Pooled `mu` for `b3` (H2, slope) — subject to section 8.5
3. Intent-R contrast: Intent-R = Yes boundaries versus Intent-R = No boundaries

All three on the single primary metric chosen in Decision B, pre-registered
before results exist.

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

**2009 is the only boundary with no intruding reset**, and its pre-period is
truncated to three seasons by the Tier A floor. Every other boundary has at least
one reset inside its window.

### 8.5.1 Consequence for H2 — stated in advance

H2 is defined against "a comparable stable-regulation period." Removing reset
seasons and flagged discontinuities from 2006–2026 leaves clean seasons
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
  longer clean run, H2 may be restored — as a new commit stating the change and
  its reason, never a silent edit.

This is a limitation of the sport's regulatory cadence, not of the data source.
F1 has not left the rules alone for long enough to establish a baseline.

### 8.6 Placebo test — pool sizes computed in advance

The same segmented model is fitted at every clean non-reset season boundary. If
real reset boundaries do not produce larger shifts, more often, than placebo
boundaries, then regulation resets are not distinguishable from ordinary
season-to-season churn — and that is the finding. **This test runs regardless of
outcome.**

Season-to-season boundaries in 2007–2026: 20. Excluding reset boundaries (2009,
2014, 2017, 2021, 2022, 2026) and flagged discontinuities (2010, 2019, 2020,
2023):

| Pool | Clean boundaries | Count |
|---|---|---|
| **Tier A** (2006–2026, also excluding 2016) | 2007, 2008, 2011, 2012, 2013, 2015, 2018, 2024, 2025 | **9** |
| **Tier B** (2018–2026 provisional) | 2024, 2025 | **2** |

**Caveats that travel with every placebo result:**

- **Tier B's placebo pool is 2 boundaries.** A null placebo result in Tier B is
  not reassurance; it is an absence of evidence from a test with almost no power.
  The memo states the pool size wherever a placebo result appears. This is the
  second and harder reason Tier A leads (section 3).
- Tier A's pool of 9 is workable but not comfortable.
- These are *naive* counts, requiring only that the boundary season itself be
  clean. A stricter requirement — that the boundary's ±4 window contain no reset
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
| R8 | Q-segment rule: evolution-adjusted vs best-of-any vs Q1-only — **runs before the metric freeze** (section 4.1) | Qualifying bias |
| R9 | Tier A vs Tier B on the overlap era | Method dependence |
| R10 | Regression pace model vs raw median clean-air pace | Model overreach |
| R11 | 2026 in / out | Partial season |
| R12 | ITS window width 3 / 4 / 5 seasons | Window arbitrariness |
| R13 | **Teams grouped by power-unit supplier** | Non-independence of customer teams; PU-led boundaries (confound 8) |
| R14 | **Team pace = both drivers' mean vs faster driver** | Driver quality imported into a car metric (confound 12) |
| R15 | **Percentile vs fixed-rank definitions of M3, M4** | Grid-size sensitivity of rank windows |

**Reporting rule.** The battery is 15 checks. The threshold is two-thirds,
preserving the ratio originally set at 8 of 12: a headline claim surviving
**fewer than 10 of 15** is downgraded from "finding" to "suggestive," in the
memo, in those words.

---

## 12. Decision ledger

Full ledger with reasoning, alternatives rejected, and dates in
[`DECISIONS.md`](DECISIONS.md). Summary of status at pre-registration:

| ID | Question | Status |
|---|---|---|
| A | Representative-lap thresholds; wet handling | **DEFERRED** to Phase 2 (row-loss ledger first) |
| B | Primary metric | **DEFERRED** to Phase 4 |
| B′ | Qualifying segment rule | **DECIDED** — evolution-adjusted primary |
| C1 | Team continuity mapping | **DECIDED** — continuity primary, strict as R2 |
| C2 | Reset list | **DECIDED** — five boundaries, 2021–22 merged |
| C3 | Intent classification | **DECIDED** — split Intent-R / Intent-C, sourced |
| D | Sprint weekends | **DECIDED** — include, format-version indicator |
| E | Partial 2026 season | **DECIDED** — include, provisional label, R11 |
| F | Effect horizon | **DECIDED** — H1 leads, pooled; H2 equal billing but downgraded per 8.5.1 |
| G | Seasons in scope per tier | **DEFERRED** to Phase 1 (coverage report) |
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
