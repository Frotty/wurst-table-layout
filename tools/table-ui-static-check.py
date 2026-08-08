#!/usr/bin/env python3
"""Small diff-oriented guardrail for WC3 TableUi code.

This deliberately checks only added lines. Existing projects can adopt it without first
rewriting their whole UI, while every new violation is caught in CI and during review.
The checker is intentionally conservative: it reports patterns that have caused real WC3
layout bugs, not general Wurst style preferences.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class AddedLine:
    path: str
    number: int
    text: str


HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
NUM_RE = re.compile(r"(?<![A-Za-z_])(?:\d+\.\d*|\.\d+|\d+)(?![A-Za-z_])")
SPACING_RE = re.compile(r"\b(?:padding|gap|padTop|padRight|padBot|padLeft|pad)\s*\(([^)]*)\)")
TEXT_PRESET_RE = re.compile(r"^\s*(?:p|p2|p3|h[1-5])\s*\(")
SIZE_CHAIN_RE = re.compile(
    r"\.\.(?:setSize|prefSize|prefWidth|fixedWidth|minWidth|growX|growY|grow)\s*\("
)


def matching_paren(text: str, opening: int) -> int | None:
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    return None


def unsized_text_cell(lines: str) -> bool:
    """Return whether an added line contains an unsized text cell.

    Wurst text helpers can contain nested calls, and several cells are often
    chained on one line. A balanced scan keeps the guard conservative without
    mistaking an inner ')' or a later cell's grow marker for the current cell.
    """
    cursor = 0
    while True:
        added = lines.find("..add(", cursor)
        if added < 0:
            return False
        opening = added + len("..add")
        closing = matching_paren(lines, opening)
        if closing is None:
            return False
        cell = lines[opening + 1 : closing]
        if TEXT_PRESET_RE.match(cell):
            next_add = lines.find("..add(", closing + 1)
            next_row = lines.find("..row(", closing + 1)
            boundaries = [position for position in (next_add, next_row) if position >= 0]
            boundary = min(boundaries) if boundaries else len(lines)
            suffix = lines[closing + 1 : boundary]
            if not SIZE_CHAIN_RE.search(cell) and not SIZE_CHAIN_RE.search(suffix):
                return True
        cursor = closing + 1


def added_line_blocks(lines: list[AddedLine]) -> list[list[AddedLine]]:
    """Group consecutive additions so multiline cell expressions are checked whole."""
    blocks: list[list[AddedLine]] = []
    current: list[AddedLine] = []
    for added in lines:
        if current:
            previous = current[-1]
            if added.path != previous.path or added.number != previous.number + 1:
                blocks.append(current)
                current = []
        current.append(added)
    if current:
        blocks.append(current)
    return blocks


def git_diff(base: str | None) -> str:
    if base:
        revision = f"{base}...HEAD"
    else:
        revision = "HEAD"
    result = subprocess.run(
        ["git", "diff", "--unified=0", revision, "--", "*.wurst"],
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout


def added_lines(diff: str) -> list[AddedLine]:
    result: list[AddedLine] = []
    path = None
    line_number = 0
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            continue
        match = HUNK_RE.match(line)
        if match:
            line_number = int(match.group(1))
            continue
        if line.startswith("+") and not line.startswith("+++"):
            if path is not None:
                result.append(AddedLine(path, line_number, line[1:]))
            line_number += 1
            continue
        if line and not line.startswith("-"):
            line_number += 1
    return result


def nonzero_numbers(value: str) -> list[str]:
    values = []
    for token in NUM_RE.findall(value):
        try:
            if float(token) != 0.0:
                values.append(token)
        except ValueError:
            pass
    return values


def violations(lines: list[AddedLine]) -> list[str]:
    errors: list[str] = []
    for added in lines:
        text = added.text
        location = f"{added.path}:{added.number}"

        if re.search(r"tableWarnings\s*=\s*false", text):
            errors.append(f"{location}: do not disable TableLayout warnings; fix the reported layout")

        if "setScale(" in text:
            errors.append(f"{location}: do not use setScale(); change declared width/height instead")

        if "setParent(" in text:
            errors.append(f"{location}: create the frame under its eventual parent with withParent(...) or an explicit-parent helper")

        if "defaultFrameParent =" in text and added.path not in {
            "wurst/TableLayout.wurst",
            "wurst/components/TableUiLayers.wurst",
        }:
            errors.append(f"{location}: use withParent(...) / inLayer(...) instead of assigning defaultFrameParent")

        if "defaultFrameParent" in text and "createFrame" in text and not added.path.startswith("wurst/components/"):
            errors.append(f"{location}: create application frames under their parent with withParent(...) or an explicit-parent helper")

        for match in SPACING_RE.finditer(text):
            numbers = nonzero_numbers(match.group(1))
            if numbers:
                errors.append(
                    f"{location}: use SPACE_2XS..SPACE_XL or a named geometry constant instead of raw spacing {numbers}"
                )
                break

    for block in added_line_blocks(lines):
        block_text = "\n".join(added.text for added in block)
        if unsized_text_cell(block_text):
            first = block[0]
            errors.append(
                f"{first.path}:{first.number}: size text cells explicitly or mark the cell growX()/growY()/grow()"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check added Wurst lines for unsafe TableUi patterns")
    parser.add_argument(
        "--base",
        help="git revision to compare with (defaults to the current working tree against HEAD)",
        default=os.environ.get("TABLE_UI_BASE") or os.environ.get("GITHUB_BASE_SHA"),
    )
    args = parser.parse_args()

    try:
        errors = violations(added_lines(git_diff(args.base)))
    except subprocess.CalledProcessError as error:
        print(error.stderr or "table-ui-static-check: unable to read git diff", file=sys.stderr)
        return 2

    if errors:
        print("table-ui-static-check: violations found:")
        for error in errors:
            print(f"- {error}")
        return 1

    compared = args.base or "working tree"
    print(f"table-ui-static-check: passed ({compared})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
