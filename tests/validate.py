#!/usr/bin/env python3
"""Dependency-free static checks for the public AstraBooster package."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "astra-booster" / "SKILL.md"
ERRORS = []

if not SKILL.is_file():
    ERRORS.append("Missing SKILL.md")
else:
    data = SKILL.read_text(encoding="utf-8")
    front = re.match(r"\A---\n(.*?)\n---\n", data, re.S)
    if not front:
        ERRORS.append("Missing YAML frontmatter")
    else:
        for expected in (r"^name:\s*astra-booster\s*$", r"^description:\s*\S"):
            if not re.search(expected, front.group(1), re.M):
                ERRORS.append(f"Invalid frontmatter: {expected}")
    for link in re.findall(r"\]\((references/[^)#]+)\)", data):
        if not (SKILL.parent / link).is_file():
            ERRORS.append(f"Broken skill reference: {link}")

for required in (
    "README.md", "README.ru.md", "LICENSE", "NOTICE.md",
    "docs/STRATEGY.md", "docs/STRATEGY.ru.md",
    "astra-booster/agents/openai.yaml",
):
    if not (ROOT / required).is_file():
        ERRORS.append(f"Missing {required}")

for p in ROOT.rglob("*.md"):
    for link in re.findall(r"(?<!!)\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path = link.split("#", 1)[0]
        if path and not (p.parent / path).exists():
            ERRORS.append(f"Broken link: {p.relative_to(ROOT)} -> {link}")

if ERRORS:
    print("FAILED:\n" + "\n".join("- " + e for e in ERRORS))
    sys.exit(1)
print("OK: AstraBooster manifest, references, docs and links")
