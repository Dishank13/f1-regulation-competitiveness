# Phase 5 — confirmatory results (primary metric M2)

**M2 (robust field spread, IQR) frozen as primary before this ran.** M3
(leader→midfield) is a pre-registered designated secondary, reported at every
boundary, not competing for a confirmatory slot.

Tier A, 2006–2026. Thresholds 107% / 5.0 s / k=3.

---

## 1. Exact test count

| family | tests | correction |
|---|---:|---|
| **Confirmatory** | **2** | Holm–Bonferroni at α = 0.05 |
| **Secondary** | **9** | Holm within family |
| **Total formally corrected** | **11** | |

The secondary family is **9, not the 10 the plan projected.** The 2026 boundary
has only one post-period season, so the `t × post` interaction column is
degenerate and `b3` is **not estimable** there. It is excluded rather than
reported as zero.

---

## 2. Confirmatory family — neither test rejects

| test | pooled μ | 95% CI | p | Holm threshold | reject |
|---|---:|---|---:|---:|:---:|
| **Pooled b2 (H1, level)** | **+0.4804** | **[−0.0457, +1.0066]** | 0.0643 | 0.025 | **no** |
| Pooled b3 (H2, slope) | +0.1502 | [−0.2239, +0.5242] | 0.2913 | 0.050 | no |

Random-effects pooling with the Hartung–Knapp–Sidik–Jonkman small-k adjustment,
k = 5 (k = 4 for b3).

### Heterogeneity is dominant, and the plan pre-committed to what that means

**I² = 86.1% for b2, 87.4% for b3.** Plan §8.3 requires this be reported *in
place of, not after,* the headline: at that level the pooled estimate is an
average of boundaries that are not measuring the same thing. Plan §9
falsification criterion 5 is met on its own terms.

Two independent §9 criteria therefore fire: **(1)** the pooled CI contains zero,
and **(5)** between-boundary heterogeneity is large enough that the pooled
estimate averages incompatible effects.

---

## 3. Per-boundary estimates — where the heterogeneity comes from

M2, segmented ITS. `b2` is the level change; `pre_slope` is the pre-boundary
trend the level change is read against.

| boundary | b2 | 95% CI | b3 | pre-slope | events |
|---|---:|---|---:|---:|---:|
| 2009 | **+0.973** | [+0.633, +1.382] | +0.403 | −0.280 | 128 |
| 2014 | +0.449 | [+0.062, +0.849] | +0.306 | −0.326 | 156 |
| 2017 | +0.133 | [−0.113, +0.382] | −0.083 | −0.009 | 157 |
| **2021–22** | **−0.003** | **[−0.455, +0.343]** | −0.004 | −0.093 | 169 |
| 2026 | **+0.834** | [+0.621, +1.073] | *not estimable* | −0.108 | 104 |

Secondary family, Holm-corrected: **2026 b2, 2009 b2, 2009 b3 and 2014 b3
survive correction.** 2014 b2 does not (p = 0.026 against a 0.010 threshold).
Both 2021–22 coefficients are as close to null as the data permits (p = 0.99 and
p = 0.95).

### The trend control changes the 2021–22 picture completely

The simple pre/post level shift used in the placebo battery gave 2021–22 as
**−0.385**, at the 78th placebo percentile. The segmented ITS, which controls
for the pre-existing trend, gives **−0.003**.

The difference is the secular decline. Every boundary has a negative pre-slope:
the field was **already converging** before four of the five resets. Attributing
that ongoing convergence to a reset requires the level to drop *below* the trend,
and at 2021–22 it does not.

---

## 4. Decision H item 1 — the secular trend

Tier A M2 falls across the study window, and every pre-boundary slope is
negative (−0.009 to −0.326 per season). This is the **main alternative
explanation for the entire study**: a field converging steadily for two decades
for reasons unrelated to any individual rules reset.

The ITS specification controls for it by construction — that is what `b1` and
the pre-slope are for — which is why the ITS and simple-difference results
disagree at 2021–22. Both are reported. Whether the secular trend is itself a
consequence of the accumulated regulatory regime is not a question this design
can answer.

---

## 5. Decision H item 2 — is M2 immune at 2026?

**No, and the effect is quantified.** M2's IQR is insensitive to a new entrant
*at the tail*, but an eleventh constructor changes which teams fall inside the
interquartile range.

| 2026 estimate | b2 | 95% CI |
|---|---:|---|
| all constructors | +0.834 | [+0.616, +1.079] |
| **constant-constructor subset (R4)** | **+0.596** | **[+0.388, +0.813]** |

**29% of the measured 2026 widening is attributable to the eleventh entrant.**
The remaining 71% survives, with a CI excluding zero. The 2026 widening is real
but materially smaller than the headline number, and any statement about 2026
must use the constant-constructor figure or state that it does not.

---

## 6. B1 — the 2009 boundary does not depend on the Brawn mapping

| mapping | b2 | 95% CI |
|---|---:|---|
| continuation (primary) | +0.9726 | [+0.633, +1.382] |
| Brawn as new entity | +0.9726 | [+0.631, +1.381] |

**Identical to four decimal places.** The most contestable call in the continuity
mapping, sitting inside the least contaminated boundary, turns out not to matter:
Brawn was fast enough in 2009 that it occupies the same position in the
distribution either way, and M2's IQR is unaffected by which lineage label it
carries. Recorded as a worry that was checked and dismissed on evidence.
