# Did F1's regulation resets close up the field?

**Five technical regulation boundaries, 2006–2026. Qualifying-pace dispersion,
pre-registered before any data was touched.**

---

## Before any number: what this measures, and what F1 promised

This study measures **field convergence** — whether the cars are closer together
in outright pace. Formula 1 mostly promises something else: **raceability**,
meaning cars that can follow and overtake. Those are different claims, and a
reset can deliver one without the other.

The distinction is not academic here. We classified each reset against
contemporaneous sources for what the regulator publicly claimed
([`ANALYSIS_PLAN.md`](ANALYSIS_PLAN.md) §2.1). Four of the five were justified on
closer racing or on something else entirely — thermal efficiency and road
relevance in 2014, lap time and spectacle in 2017. **The sport explicitly
promised a closer *field* once in twenty years**: the 2021–22 package, through
the cost cap and the sliding-scale aerodynamic testing restrictions.

That one boundary is also the one most contaminated by confounding. The cost cap,
the testing restrictions and the ground-effect aero reset arrive together and are
collinear in time; no design can separate them. A reader should hold both facts
before reading any estimate: **we are measuring a quantity the regulator mostly
did not claim to be delivering, and the single time it did claim it, the claim
cannot be isolated from two other simultaneous interventions.**

---

## Finding

### 1. The boundaries do not share a common effect

**I² = 86.1%.** The five resets do not behave as five measurements of one thing.
The pooled estimate (+0.480) describes no boundary in the study and is not the
result. **The per-boundary table is the result.**

Primary metric M2, robust field spread (interquartile range of team pace, as
percent off the fastest car), segmented interrupted time series, level change
`b2`. Positive means the field **widened** at the reset.

| boundary | b2 (field-wide) | 95% CI | b2 (stratified, R16) | Holm |
|---|---:|---|---:|:---:|
| 2009 **⚑ contaminated** | **+0.973** | [+0.633, +1.382] | +0.888 | **survives** |
| 2014 | +0.449 | [+0.062, +0.849] | +0.468 | does not |
| 2017 | +0.133 | [−0.113, +0.382] | +0.025 | does not |
| 2021–22 | −0.003 | [−0.455, +0.343] | +0.066 | does not |
| 2026 | **+0.834** | [+0.621, +1.073] | +0.741 | **survives** |

### ⚑ The 2009 estimate is contaminated, and we found it late

The 2009 boundary's estimation window runs to 2012, so **its post-period
contains the 2010 measurement discontinuity** — the season the grid went from
ten constructors to twelve with three new backmarkers, refuelling was banned, and
the qualifying segment basis changed. M2 steps at 2010 by 1.93× the median reset
shift. That step is measurement, not racing, and the 2009 estimate is fitted
against it.

Re-estimating on a window truncated at 2009, which removes the artifact entirely:

| window | b2 | 95% CI | seasons | slope estimable |
|---|---:|---|---:|:---:|
| full (2006–2012, contains the artifact) | **+0.973** | [+0.628, +1.373] | 7 | yes |
| truncated at 2009 (artifact excluded) | **+0.461** | [+0.089, +0.980] | 4 | **no** |

**The 2009 estimate roughly halves.** It stays positive with an interval
excluding zero, but the truncated version rests on four seasons with a
single post-boundary season, so its slope term is not identifiable at all and
the level estimate is weak.

**This does not change the direction of the conclusion.** Removing or halving
2009 removes a *widening*, not a narrowing. The statement "no boundary narrowed
beyond trend" holds on four boundaries instead of five, and 2026 — the other
Holm-surviving widening — is untouched by this.

We should have caught it earlier. The D1c pre-commitment named M4 and M5 and was
applied to them; its logic was never extended to the primary metric even after
Phase 4 showed M1 and M2 stepping at 2010 more strongly than M4 did. It was found
in review after this memo was first drafted. Recorded as such in
[`DECISIONS.md`](DECISIONS.md) Entry 060 rather than written up as though it had
been anticipated.

**The boundary described throughout this work as "least contaminated" turns out
to have a measurement discontinuity inside its comparison window.** That is a
finding about the study, not a repair to it.

### 2. Direction: three of five widened. None narrowed beyond trend.

2009, 2014 and 2026 all show the field **widening** at the reset. Two of the
three survive Holm correction within the secondary family (2009 and 2026; 2014's
level change does not, at p = 0.026 against a 0.010 threshold). 2017 is
indistinguishable from nothing.

**No boundary in the study shows the field narrowing beyond its pre-existing
trend.** That statement survives the 2009 contamination flagged below: setting
2009 aside entirely leaves it holding on four boundaries rather than five,
because what 2009 contributes is a widening.

The 2026 figure carries a specific correction. An eleventh constructor joined
that season, and **29% of the measured widening is attributable to the new
entrant**: the constant-constructor estimate is +0.596 [+0.388, +0.813]. The
remaining 71% survives, but any statement about 2026 should use the smaller
figure. 2026 is also provisional — 13 of 23 rounds — and its slope coefficient is
not estimable at all, having only one post-boundary season.

### 3. The one reset that promised a closer field produced nothing, under three specifications

| specification | 2021–22 estimate |
|---|---:|
| segmented ITS, field-wide offset (**pre-registered primary**) | −0.003 |
| segmented ITS, stratified offset (R16) | +0.066 |
| simple pre/post difference | −0.385 |

The first two are nulls with confidence intervals spanning zero. The third —
−0.385, at the 78th percentile of the nine-boundary placebo distribution — is the
only number in the study that looks like convergence at 2021–22, and it comes
from the specification that does **not** control for the pre-existing trend.

**Three specifications, and no narrowing survives any of them as a finding.**

### 4. The confirmatory test does not reject

Pooled level change **+0.480 [−0.046, +1.007], p = 0.064** against a
Holm-Bonferroni threshold of 0.025. The slope test does not reject either
(p = 0.291). Exact count: **2 confirmatory tests and 9 secondary estimates, 11
formally corrected in total.**

Two of the plan's pre-registered falsification criteria fire independently
(§9): the pooled interval contains zero, **and** heterogeneity is large enough
that the pooled estimate averages incompatible effects.

Using the pre-registered language: **no measurable convergence effect.**

### 5. The field did converge — steadily, across two decades, regardless of resets

The decline is best stated **within each measurement era**, because the 2010
discontinuity sits between them and a single 2006→2025 figure would span it:
1.21 → 0.58 across 2006–2009, and 1.79 → 0.45 across 2010–2025. Both eras
decline steeply and internally, so the claim does not depend on comparing across
the break. Every boundary also has a negative pre-slope: the field was already
converging before four of the five resets. That trend, not the resets, is where
the convergence lives.

**Whether that secular trend is the regulations working slowly, or something
else entirely, is beyond what this design can answer.** It is the study's central
limitation and it is not resolvable by more data of this kind. The two
specifications disagree at 2021–22 precisely because one removes the trend and
one does not, and the choice between them is a judgement about what the trend
*is*.

---

## The R16 pre-commitment

Reported before any conclusion, as committed.

**The stratified offset flips the 2021–22 sign, from −0.0033 to +0.0661.** The
pre-commitment fires on the letter and is honoured: the flip is reported before
any conclusion. It does not change the substantive result. Both estimates are
indistinguishable from zero, the movement is one-ninth of its own CI width, and
the Phase 5 statement was never a narrowing claim. What does change: **under the
stratified offset no boundary in the study carries a negative point estimate.**
Under the field-wide offset exactly one did, and it was −0.003.

Field-wide remains primary because it was pre-registered. Stratified is reported
alongside at every boundary.

---

## Descriptive observations — not findings

*Clearly labelled because neither identifies anything causally and neither should
be read as a claim.* Of the total decline in M2 excluding the partial 2026
season, **12.8% occurs across transitions into a reset season, against an
even-spread benchmark of 26.3%** — convergence happens at resets at roughly half
the rate an even spread would produce, and including 2026 the transitions into
reset seasons net to widening while all others net to narrowing. Separately, the
post-boundary slope change is **positive at 2009 (+0.403) and 2014 (+0.306)**,
both surviving Holm: convergence *slowed* after those resets, where the
trend-is-the-effect reading predicts a negative sign. Reset seasons are not
randomly assigned, the transitions are not independent, and four seasons on one
metric is not a test. Both observations sit weakly against the reading that the
secular trend is accumulated regulation, and neither is offered as evidence for
anything.

---

## What would have to be true for the opposite conclusion

- **That the pre-boundary trend is itself the accumulated effect of regulation.**
  Then removing it removes the finding, the simple-difference specification is
  the correct one, and 2021–22 becomes a genuine convergence at the 78th placebo
  percentile. This is not testable here and is the single most plausible route to
  the opposite answer.
- **That field convergence is the wrong estimand.** Four of five resets promised
  raceability. Every null here is consistent with the regulations having
  succeeded completely at what they were actually aiming for.
- **That the 2026 widening is transient.** If 2026 converges over the next three
  seasons the way 2009 and 2014 did, "resets widen then converge" becomes a
  three-instance regularity rather than a description of one partial season.
- **That the traffic-filter endogeneity in Tier B masks real convergence.**
  Retention correlates with field spread at r = +0.950, and the induced bias
  inflates dispersion exactly when the field is tightest. Tier A is immune, which
  is why it leads — but the direction of that bias is toward understating
  convergence.

**Capability diffusion, a named hypothesis this design cannot evaluate.** The
steady convergence is consistent with capability spreading across the grid rather
than with any rules change: simulation and CFD tools becoming cheaper and more
widely licensed, composites manufacturing maturing into a supplier market,
experienced aerodynamicists and race engineers circulating between teams, and
standardised or shared components narrowing what a large budget can buy. On that
account the field closed up because the knowledge and tooling needed to build a
competitive car diffused outward, and the resets are incidental to it. **Testing
this would require data this study does not have** — team headcount, wind tunnel
and CFD hours, staff movement between constructors, and supplier relationships —
none of which is in timing data. It is named here because it is the most
plausible non-regulatory mechanism and because leaving it unnamed would imply the
field was exhausted. **The tension is worth stating explicitly: the cost cap and
the aerodynamic testing restrictions are themselves resource-equalisation
measures.** If diffusion is the mechanism, part of that diffusion is regulatory,
and the clean separation between "the rules did it" and "something else did it"
does not survive contact with the 2021 package.

---

## Limitations

Full list in [`LIMITATIONS.md`](LIMITATIONS.md). The four that most constrain
this memo:

1. **The cost cap cannot be separated from the 2022 aero reset.** Any 2021–22
   statement is about the package, not about aerodynamics.
2. **The secular trend is unidentifiable** (point 5 above).
3. **Tier B is corroboration only.** Its placebo pool is two boundaries and the
   2021–22 boundary has one unflagged pre-season. No claim here rests on it.
4. **The robustness threshold could not be applied as pre-registered.** Twelve of
   fifteen executable arms survive; three of the sixteen checks are not
   executable on the Tier A primary, so the denominator is fifteen and the
   pre-registered 11-of-16 bar was **not** met as written. Three of the arms
   scored as failures (R3, R4, R12±3) in fact produce intervals *excluding* zero
   in the same direction as the headline while roughly halving heterogeneity —
   the mechanical score and the substantive reading disagree, and both are
   reported.

---

*Every number in this memo is traceable to a committed artifact in this
repository. The analysis plan was committed and tagged before any analysis code
existed; four amendments are recorded with their reasons; 58 decisions are logged
in [`DECISIONS.md`](DECISIONS.md).*
