"""Portable one-command rebuild (ANALYSIS_PLAN.md §13).

    python -m src.pipeline            full pipeline: acquisition -> deliverables
    python -m src.pipeline analysis   everything downstream of acquisition
    python -m src.pipeline --list     show stages without running
    python -m src.pipeline --dry-run  print the commands only

The Makefile does the same thing, but `make` is not installed by default on
Windows, so this is the portable entry point and the one the README leads with.

ACQUISITION IS NOT OPTIONAL ON A FRESH CLONE. The raw caches and processed
Parquet are gitignored, so `analysis` cannot run until `acquire` has populated
them. Running `analysis` first fails with an explicit message rather than a
confusing traceback deep in a module.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time

from src import config

# (stage, module, args, description)
STAGES: list[tuple[str, str, list[str], str]] = [
    ("acquire", "src.coverage_tier_a", [], "Tier A coverage scan (Jolpica)"),
    ("acquire", "src.coverage_tier_b", [], "Tier B coverage probe (FastF1)"),
    ("acquire", "src.ingest.weather", [], "precipitation source (retained, unused)"),
    ("acquire", "src.ingest.fastf1_races", [], "race session acquisition (slow)"),

    ("clean", "src.clean.session_format", [], "sprint format versions"),
    ("clean", "src.clean.tier_a", [], "Tier A cleaning + row-loss ledger"),
    ("clean", "src.clean.tier_b", [], "Tier B cleaning + threshold sweep"),

    ("model", "src.pace_model", [], "pace model + §4.4 ship gates"),

    ("metrics", "src.metrics", ["a"], "Tier A metrics + D1c"),
    ("metrics", "src.metrics", ["b"], "Tier B metrics"),

    ("tests", "src.placebo", ["a"], "placebo battery"),
    ("tests", "src.phase5", [], "confirmatory pooled tests"),
    ("tests", "src.robustness", [], "16-check robustness battery"),
    ("tests", "src.r16_stratified", [], "R16 stratified offset"),
    ("tests", "src.trend_decomposition", [], "trend decomposition"),

    ("diagnostics", "src.diagnostics_d1", [], "D1 era-composition diagnostic"),
    ("diagnostics", "src.decision_a_evidence", [], "Decision A threshold evidence"),
    ("diagnostics", "src.traffic_bias", [], "traffic filter time-variance"),
    ("diagnostics", "src.gate3_investigation", [], "gate-3 failure investigation"),

    ("figures", "src.figures", [], "gate-1 residual diagnostics"),
    ("figures", "src.figures", ["decision_b"], "metric candidate charts"),
    ("figures", "src.figures", ["readme"], "README publication charts"),

    ("docs", "src.data_dictionary", [], "data dictionary for every processed table"),
]

# Stages that need acquisition to have happened first.
NEEDS_DATA = {"clean", "model", "metrics", "tests", "diagnostics", "figures", "docs"}

GROUPS = {
    "all": [s for s, *_ in STAGES],
    "analysis": ["clean", "model", "metrics", "tests", "diagnostics", "figures",
                 "docs"],
    "acquire": ["acquire"],
}


def acquisition_done() -> bool:
    return (config.DATA_PROCESSED / "laps_raw.parquet").exists()


def run(selected: list[str], dry_run: bool) -> int:
    todo = [s for s in STAGES if s[0] in selected]
    if NEEDS_DATA & set(selected) and not acquisition_done():
        print(
            "ERROR: acquisition has not run in this working copy.\n"
            f"       Expected {config.DATA_PROCESSED / 'laps_raw.parquet'}\n\n"
            "The raw caches and processed tables are gitignored, so a fresh\n"
            "clone must acquire before it can analyse. Run:\n\n"
            "    python -m src.pipeline acquire\n\n"
            "This downloads from the FastF1 live-timing API, which is rate\n"
            "limited to 500 calls/hour. It is resumable and cache-first, so\n"
            "re-running costs nothing for sessions already on disk, but the\n"
            "first full run takes several hours.",
            file=sys.stderr)
        return 2

    failures = []
    for i, (stage, module, args, desc) in enumerate(todo, 1):
        cmd = [sys.executable, "-m", module, *args]
        print(f"\n[{i}/{len(todo)}] {stage}: {desc}\n    $ {' '.join(cmd[1:])}",
              flush=True)
        if dry_run:
            continue
        t0 = time.monotonic()
        r = subprocess.run(cmd, cwd=config.ROOT)
        dt = time.monotonic() - t0
        if r.returncode != 0:
            print(f"    FAILED (exit {r.returncode}) after {dt:.0f}s", flush=True)
            failures.append(module)
        else:
            print(f"    ok ({dt:.0f}s)", flush=True)

    print("\n" + "=" * 60)
    if failures:
        print(f"PIPELINE FAILED: {len(failures)} stage(s): {', '.join(failures)}")
        return 1
    print(f"PIPELINE OK: {len(todo)} stage(s) completed")
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="python -m src.pipeline")
    p.add_argument("group", nargs="?", default="all", choices=sorted(GROUPS))
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--list", action="store_true")
    a = p.parse_args()

    if a.list:
        for stage, module, args, desc in STAGES:
            print(f"  {stage:<12} {module} {' '.join(args):<12} {desc}")
        return
    sys.exit(run(GROUPS[a.group], a.dry_run))


if __name__ == "__main__":
    main()
