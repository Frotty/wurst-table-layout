#!/usr/bin/env python3
"""Small diff-oriented guardrail for WC3 TableUi code.

This deliberately checks only added lines. Existing projects can adopt it without first
rewriting their whole UI, while every new violation is caught in CI and during review.
The checker is intentionally narrow: layout sizing and geometry belong to TableLayout's
headless Wurst validation; this file only covers frame hazards that geometry cannot prove.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AddedLine:
    path: str
    number: int
    text: str


HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
FRAME_PARENTING_IMPLEMENTATION = {"wurst/TableLayout.wurst"}
AMBIENT_PARENT_IMPLEMENTATIONS = {
    "wurst/TableLayout.wurst",
    "wurst/MultiboardAttach.wurst",
}
AMBIENT_PARENT_IMPLEMENTATION_PREFIX = "wurst/components/"
SCALE_CALL_RE = re.compile(r"\b(?:setScale|BlzFrameSetScale)\s*\(")
PARENT_CALL_RE = re.compile(r"\b(?:setParent|BlzFrameSetParent)\s*\(")


def mask_comments_and_strings(text: str) -> str:
    """Replace comments and string contents while preserving line structure.

    Callers should pass the complete source file when possible. That preserves
    lexical state across an additions block that starts inside a pre-existing
    block comment.
    """
    masked: list[str] = []
    index = 0
    in_string = False
    in_line_comment = False
    in_block_comment = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                masked.append(char)
            else:
                masked.append(" ")
        elif in_block_comment:
            if char == "*" and next_char == "/":
                masked.extend((" ", " "))
                index += 1
                in_block_comment = False
            elif char == "\n":
                masked.append(char)
            else:
                masked.append(" ")
        elif in_string:
            if char == "\n":
                masked.append(char)
            else:
                masked.append(" ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            masked.append(" ")
            in_string = True
        elif char == "/" and next_char == "/":
            masked.extend((" ", " "))
            index += 1
            in_line_comment = True
        elif char == "/" and next_char == "*":
            masked.extend((" ", " "))
            index += 1
            in_block_comment = True
        else:
            masked.append(char)
        index += 1
    return "".join(masked)


def added_line_blocks(lines: list[AddedLine]) -> list[list[AddedLine]]:
    """Group consecutive additions so multiline source hazards are checked together."""
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


def violations(lines: list[AddedLine]) -> list[str]:
    errors: list[str] = []
    masked_sources: dict[str, str | None] = {}
    for block in added_line_blocks(lines):
        first = block[0]
        location = f"{first.path}:{first.number}"
        if first.path not in masked_sources:
            try:
                masked_sources[first.path] = mask_comments_and_strings(
                    Path(first.path).read_text(encoding="utf-8")
                )
            except OSError:
                masked_sources[first.path] = None
        masked_source = masked_sources[first.path]
        if masked_source is None:
            text = mask_comments_and_strings("\n".join(added.text for added in block))
        else:
            source_lines = masked_source.splitlines()
            text = "\n".join(
                source_lines[added.number - 1]
                for added in block
                if 0 < added.number <= len(source_lines)
            )

        if SCALE_CALL_RE.search(text):
            errors.append(f"{location}: do not use setScale()/BlzFrameSetScale(); change declared width/height instead")

        if PARENT_CALL_RE.search(text) and first.path not in FRAME_PARENTING_IMPLEMENTATION:
            errors.append(f"{location}: create the frame under its eventual parent with withParent(...) or an explicit-parent helper")

        if (
            "defaultFrameParent" in text
            and first.path not in AMBIENT_PARENT_IMPLEMENTATIONS
            and not first.path.startswith(AMBIENT_PARENT_IMPLEMENTATION_PREFIX)
        ):
            errors.append(f"{location}: create application frames under their parent with withParent(...) or an explicit-parent helper")

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
