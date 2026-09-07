# R16 and the trend decomposition

Both executions requested before drafting. **R16 produced a sign flip, so this
stops here.**

---

## 1. R16 — stratified evolution offset

The §4.1 primary estimates one field-wide `E(Q1→Q2)` offset per event. D1a showed
that is misspecified by stratum: front-runners gain ~0.3 s more between Q1 and Q2
than backmarkers. R16 re-estimates the offset separately for drivers who set a Q3
time and those who did not, and re-runs the whole pipeline.

Stratum is taken from the **source** data — did this driver set any Q3 time at
this event — so it is available in 2006–09 where Q3 is excluded from the metric,
and it does not depend on the metric being tested.

| boundary | b2 field-wide | 95% CI | b2 stratified | 95% CI | Δ | sign flip |
|---|---:|---|---:|---|---:|:---:|
| 2009 | +0.9726 | [+0.633, +1.382] | +0.8876 | [+0.620, +1.177] | −0.085 | no |
| 2014 | +0.4486 | [+0.062, +0.849] | +0.4683 | [+0.129, +0.801] | +0.020 | no |
| 2017 | +0.1325 | [−0.113, +0.382] | +0.0247 | [−0.224, +0.277] | −0.108 | no |
| **2021–22** | **−0.0033** | **[−0.455, +0.343]** | **+0.0661** | **[−0.268, +0.360]** | +0.069 | **YES** |
| 2026 | +0.8342 | [+0.621, +1.073] | +0.7407 | [+0.528, +0.970] | −0.093 | no |

### The flip is real but it is a flip of a null

Reported plainly because the pre-commitment says a sign flip supersedes the
Phase 5 result, and the rule should not be softened just because the flip is
inconvenient to the narrative in the other direction.

**What flipped:** the 2021–22 estimate, from −0.0033 to +0.0661.

**Why this is not a substantive reversal:**

- Both estimates are **statistically indistinguishable from zero**. The
  field-wide CI is [−0.455, +0.343]; the stratified CI is [−0.268, +0.360]. Zero
  sits near the middle of both.
- The magnitude of the flip (0.069) is about **one ninth of the width of its own
  confidence interval** (0.628). This is an estimate crossing the axis, not a
  conclusion reversing.
- The substantive Phase 5 statement about 2021–22 was **"indistinguishable from
  zero under the pre-registered specification."** That statement is unchanged. It
  was never "the field narrowed at 2021–22," so there is no narrowing claim to
  reverse.

**What is stable:** the other four boundaries keep their sign, and all four shift
by ≤ 0.11. 2009 (+0.97 → +0.89), 2014 (+0.45 → +0.47) and 2026 (+0.83 → +0.74)
remain positive with CIs excluding zero. 2017 remains a null.

**The one substantive change:** under the stratified offset, **no boundary in the
study shows a negative point estimate.** Under the field-wide offset exactly one
did, and it was −0.003.

**Analyst decision required.** The pre-commitment fires on the letter. Whether a
sign flip of an estimate whose CI spans zero in both specifications should
supersede the Phase 5 result is a judgement I should not make unilaterally,
because the answer determines the memo.

---

## 2. Trend decomposition — descriptive only

Of the total decline in M2 across the window, what share occurs across
transitions **into** a reset season versus all other transitions?

**Excluding the partial 2026 season:**

| | n | sum of changes | mean |
|---|---:|---:|---:|
| transitions into a reset season | 5 | −0.2246 | −0.0449 |
| all other transitions | 14 | −0.5358 | −0.0383 |

Restricting to **declining** transitions only, which is what the question asks:

| | share of total decline |
|---|---:|
| occurring into a reset season | **12.8%** (4 transitions) |
| occurring elsewhere | **87.2%** (11 transitions) |
| **even-spread benchmark** | **26.3%** — reset transitions are 26.3% of all transitions |

**Convergence occurs at transitions into reset seasons at roughly half the rate
an even spread would produce** (12.8% observed against a 26.3% benchmark).

Including 2026, the asymmetry widens: transitions into reset seasons net to
**+0.536** (widening) against **−0.536** for all others. On this description the
field converges *between* resets and widens *at* them.

### This identifies nothing causally

Stated because the number is suggestive enough to be misread. Reset seasons are
not randomly assigned. The transitions are not independent. Any concentration —
or the absence of one — is equally consistent with resets responding to
convergence as with resets causing it. There is no null hypothesis here, no
p-value, and no identification strategy. It is a description of where in the
calendar the decline sits, and nothing more.

---

## 3. The b3 observation the analyst raised

`b3` — the post-boundary slope change — is **positive at 2009 (+0.403) and 2014
(+0.306)**, both surviving Holm correction in the secondary family. Convergence
*slowed* after those two resets, from starting points with more room to converge
than usual.

If the secular trend were driven by accumulated regulation, the expected sign is
negative: each reset should add to the convergence rate. It does not.

**Weak evidence against the trend-is-the-effect reading. Four seasons, one
metric, two boundaries, and explicitly not a test.** It is not a claim and does
not belong in a finding.
