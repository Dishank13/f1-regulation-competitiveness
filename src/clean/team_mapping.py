"""Constructor continuity mapping (ANALYSIS_PLAN.md section 7, DECISIONS.md 004).

Two mappings, both built, both run:
  * CONTINUITY (primary) — a constructor lineage is one entity across rebrands.
  * STRICT (R2)          — each constructorId is its own entity.

Ambiguous cases are listed here explicitly with reasoning rather than resolved
silently. The plan requires that the cost of this choice be measurable, not
assumed away.

Lineages are keyed on the operating entity — factory, wind tunnel, and staff —
because that is what produces car performance, not the name on the entry.
"""

from __future__ import annotations

# lineage_id -> ordered list of constructorIds belonging to it
LINEAGES: dict[str, list[str]] = {
    "ferrari":   ["ferrari"],
    "mclaren":   ["mclaren"],
    "williams":  ["williams"],
    "red_bull":  ["red_bull"],
    "haas":      ["haas"],
    "toyota":    ["toyota"],
    "super_aguri": ["super_aguri"],
    "hrt":       ["hrt"],
    "cadillac":  ["cadillac"],

    # Silverstone (Jordan lineage). Midland -> Spyker MF1 -> Spyker ->
    # Force India -> Racing Point -> Aston Martin.
    "silverstone": ["mf1", "spyker_mf1", "spyker", "force_india",
                    "racing_point", "aston_martin"],

    # Hinwil. BMW bought Sauber for 2006 and sold it back for 2010; the factory
    # never moved. Alfa Romeo and Audi are title/ownership rebrands of the same
    # operation.
    "hinwil": ["bmw_sauber", "sauber", "alfa", "audi"],

    # Faenza. Toro Rosso -> AlphaTauri -> RB.
    "faenza": ["toro_rosso", "alphatauri", "rb"],

    # Enstone. Renault -> Lotus F1 -> Renault -> Alpine.
    "enstone": ["renault", "lotus_f1", "alpine"],

    # Brackley. BAR/Honda -> Brawn -> Mercedes. SEE AMBIGUOUS CASES.
    "brackley": ["honda", "brawn", "mercedes"],

    # Hingham/Leafield. Lotus Racing -> Caterham.
    "caterham_lineage": ["lotus_racing", "caterham"],

    # Dinnington/Banbury. Virgin -> Marussia -> Manor.
    "manor_lineage": ["virgin", "marussia", "manor"],
}

CONTINUITY: dict[str, str] = {
    cid: lineage for lineage, cids in LINEAGES.items() for cid in cids
}


def strict(constructor_id: str) -> str:
    """R2 mapping: every constructorId is its own entity."""
    return constructor_id


def continuity(constructor_id: str) -> str:
    """Primary mapping: lineage identity. Unknown ids fall back to themselves."""
    return CONTINUITY.get(constructor_id, constructor_id)


# --- Ambiguous cases, recorded rather than resolved silently -------------------
#
# Each entry states the call, the reason, and the cost of being wrong. All are
# treated as continuous under CONTINUITY and as separate under STRICT, so R2
# measures the cost of every one of them at once.

AMBIGUOUS_CASES = {
    "brackley/brawn-2009": (
        "Honda withdrew in Dec 2008; the team was bought out by its management "
        "and raced in 2009 as Brawn GP, becoming Mercedes in 2010. Treated as "
        "CONTINUOUS: same Brackley factory, same wind tunnel, largely the same "
        "staff, and the 2009 car was developed under Honda funding. But the "
        "legal entity, ownership and engine supplier all changed, and the 2009 "
        "season saw a near-total collapse in budget mid-development. This is "
        "the single most contestable call in the mapping and it sits INSIDE the "
        "2009 boundary window (plan confound 14)."
    ),
    "silverstone/force-india-2018": (
        "Force India entered administration mid-2018 and was bought by a "
        "consortium; the championship recorded the pre- and post-administration "
        "entries separately that season. Treated as CONTINUOUS: uninterrupted "
        "operation, same site, same staff, cars raced without a break."
    ),
    "hinwil/bmw-2006-2009": (
        "BMW acquired Sauber for 2006 and sold it back to Peter Sauber for "
        "2010. Treated as CONTINUOUS: the Hinwil operation persisted throughout "
        "and the works engine deal is a supply change, not an entity change."
    ),
    "enstone/renault-gap": (
        "Enstone ran as Renault 2006-2011, Lotus F1 2012-2015, Renault again "
        "2016-2020, Alpine from 2021. Treated as CONTINUOUS throughout: one "
        "site, continuous operation, name and title sponsor changes only."
    ),
    "mf1/spyker_mf1-2006": (
        "Both ids appear in 2006 because the entry was renamed mid-season "
        "(Midland MF1 to Spyker MF1). Same entity within one season; collapsing "
        "them is not a judgement call so much as undoing a source artifact. "
        "Under STRICT these become two one-season entities, which is a known "
        "artifact of that mapping rather than a real discontinuity."
    ),
    "caterham/lotus-naming-collision": (
        "Two unrelated entities used the Lotus name concurrently: "
        "'lotus_racing' (Hingham, later Caterham) and 'lotus_f1' (Enstone, "
        "formerly Renault). They are assigned to DIFFERENT lineages. Merging "
        "them on the shared name would be straightforwardly wrong."
    ),
}
