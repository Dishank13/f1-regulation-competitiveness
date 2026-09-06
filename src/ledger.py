"""Append-only decision ledger, with reconciliation that fails loudly.

WHY THIS EXISTS. A shell `awk '$1>1'` was parsed as a redirect, which created a
stray file AND silently appended seven DECISIONS.md entries twice. The
duplication was invisible until a later `git status` happened to show it. An
append that silently doubles the ledger is worse than one that crashes, because
the ledger is the audit trail the whole pre-registration rests on.

All ledger mutation goes through this module. No shell heredocs, no inline
quoted awk/sed anywhere in this project.

Invariants enforced on every append (and by `verify` standalone):
  * entry numbers are unique
  * entry numbers are contiguous from 1
  * the post-append count equals pre-append count plus entries added

If any invariant fails, the file is restored to its pre-append content and the
error is raised. The ledger is never left in a corrupt state.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from src import config

LEDGER = config.ROOT / "DECISIONS.md"
ENTRY_RE = re.compile(r"^## \d{4}-\d{2}-\d{2} — Entry (\d+)\b", re.MULTILINE)


class LedgerError(RuntimeError):
    """Ledger invariant violated."""


def entry_numbers(text: str) -> list[int]:
    return [int(m) for m in ENTRY_RE.findall(text)]


def verify(text: str) -> list[int]:
    """Raise LedgerError unless entry numbers are unique and contiguous from 1."""
    nums = entry_numbers(text)
    if not nums:
        raise LedgerError("no entries found — is the heading format intact?")

    dupes = sorted({n for n in nums if nums.count(n) > 1})
    if dupes:
        raise LedgerError(
            f"duplicate entry numbers: {dupes}. This is the silent-double-append "
            f"failure this module exists to prevent."
        )

    expected = list(range(1, len(nums) + 1))
    if sorted(nums) != expected:
        missing = sorted(set(expected) - set(nums))
        extra = sorted(set(nums) - set(expected))
        raise LedgerError(
            f"entry numbers are not contiguous from 1. missing={missing} "
            f"unexpected={extra}"
        )
    if nums != sorted(nums):
        raise LedgerError(f"entries are out of order: {nums}")
    return nums


def append(new_entries_path: str | Path) -> tuple[int, int]:
    """Append entries from a file, verifying before and after. Atomic on failure."""
    new_path = Path(new_entries_path)
    if not new_path.exists():
        raise LedgerError(f"no such file: {new_path}")

    before_text = LEDGER.read_text(encoding="utf-8")
    before_nums = verify(before_text)

    addition = new_path.read_text(encoding="utf-8")
    add_nums = entry_numbers(addition)
    if not add_nums:
        raise LedgerError(f"{new_path} contains no ledger entries")

    overlap = sorted(set(add_nums) & set(before_nums))
    if overlap:
        raise LedgerError(
            f"refusing to append: entries {overlap} are already in the ledger. "
            f"This append has already been applied."
        )

    after_text = before_text.rstrip("\n") + "\n" + addition
    LEDGER.write_text(after_text, encoding="utf-8", newline="\n")
    try:
        after_nums = verify(LEDGER.read_text(encoding="utf-8"))
    except LedgerError:
        LEDGER.write_text(before_text, encoding="utf-8", newline="\n")
        raise

    if len(after_nums) != len(before_nums) + len(add_nums):
        LEDGER.write_text(before_text, encoding="utf-8", newline="\n")
        raise LedgerError(
            f"count reconciliation failed: {len(before_nums)} + {len(add_nums)} "
            f"!= {len(after_nums)}"
        )
    return len(before_nums), len(after_nums)


def split_entries(text: str) -> tuple[str, list[tuple[int, str]]]:
    """Split into (preamble, [(entry_number, block_text), ...])."""
    matches = list(ENTRY_RE.finditer(text))
    if not matches:
        return text, []
    preamble = text[: matches[0].start()]
    blocks: list[tuple[int, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((int(m.group(1)), text[m.start(): end]))
    return preamble, blocks


def repair() -> tuple[int, int]:
    """Drop duplicate entry blocks, keeping the first occurrence.

    Refuses to act unless every duplicate is byte-identical to the copy it
    kept — otherwise the duplicate carries content that would be silently
    discarded, which is a different and worse problem.
    """
    text = LEDGER.read_text(encoding="utf-8")
    preamble, blocks = split_entries(text)
    def body(block: str) -> str:
        """Entry text without the trailing separator, which belongs to the
        NEXT block and is an artefact of where we cut, not of content."""
        s = block.strip()
        while s.endswith("---"):
            s = s[: -len("---")].strip()
        return s

    kept: dict[int, str] = {}
    order: list[int] = []
    dropped = 0
    for num, block in blocks:
        if num in kept:
            if body(block) != body(kept[num]):
                raise LedgerError(
                    f"entry {num} appears twice with DIFFERENT content. "
                    f"Refusing to repair automatically — resolve by hand."
                )
            dropped += 1
            continue
        kept[num] = block
        order.append(num)

    rebuilt = preamble + "\n\n---\n\n".join(body(kept[n]) for n in order) + "\n"
    verify(rebuilt)
    LEDGER.write_text(rebuilt, encoding="utf-8", newline="\n")
    return dropped, len(order)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "repair":
        dropped, total = repair()
        print(f"repaired: dropped {dropped} duplicate blocks, {total} entries remain")
        return
    if len(sys.argv) < 2:
        nums = verify(LEDGER.read_text(encoding="utf-8"))
        print(f"ledger OK: {len(nums)} entries, contiguous 1..{max(nums)}")
        return
    if sys.argv[1] == "verify":
        nums = verify(LEDGER.read_text(encoding="utf-8"))
        print(f"ledger OK: {len(nums)} entries, contiguous 1..{max(nums)}")
        return
    before, after = append(sys.argv[1])
    print(f"appended {after - before} entries: {before} -> {after}")


if __name__ == "__main__":
    main()
