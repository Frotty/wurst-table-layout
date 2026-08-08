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

        for match in re.finditer(r"\.\.add\(\s*(?:p|p2|p3|h[1-5])\(\s*[^)]*\)\s*\)", text):
            # A text cell may intentionally take the remaining row width.  The
            # grow marker is commonly chained onto the same line after add(...).
            if not re.search(r"\.\.(?:growX|growY)\(\)", text[match.end():]):
                errors.append(f"{location}: size text cells explicitly or mark the cell growX()/growY()")
                break

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
