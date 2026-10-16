"""Build the self-contained Claude Cowork skill: cowork/screen-indian-stocks.zip

Cowork skills are uploaded as a zip with the skill folder at the top level.
This bundles the skill instructions together with the screener code, so the
skill works without cloning anything.

    python scripts/build_cowork_skill.py [-o cowork/screen-indian-stocks.zip]

The SKILL.md is derived from .claude/skills/screen-indian-stocks/SKILL.md (the
Claude Code version) so the two never drift: only the "find the tool" step and
the output location are rewritten. The zip is deterministic (fixed timestamps),
so rebuilding without changes produces an identical file.
"""

import argparse
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "screen-indian-stocks"
SKILL_SRC = os.path.join(ROOT, ".claude", "skills", NAME, "SKILL.md")
BUNDLE = ["multibagger_cli.py", "docs/MULTIBAGGER.md", "examples/watchlist.txt"]
STAMP = (2026, 1, 1, 0, 0, 0)

FIND_TOOL = """## 1. Find the tool

The tool is bundled with this skill: `multibagger_cli.py` and the `multibagger/` package sit next to this SKILL.md. Run every command from that folder (`cd` to the directory that contains this file). Nothing needs installing beyond Python 3. `docs/MULTIBAGGER.md` has the full method, and `examples/watchlist.txt` is a starter list.

Save reports where the user can open them: add `-o <workspace folder>/multibagger_report` to the command, and point the user to the resulting `.html` and `.csv` files.

`--stage1` and `--query` need a screener.in login. The tool reads it from environment variables or from the file `~/.multibagger/login.json` that the user created with `--save-login` (see section 2). That file lives on the user's computer, not in this skill, so it only helps if this skill runs there. If this session cannot see a saved login or set environment variables, do not ask for the password in chat; ask the user to run their screen on screener.in themselves and give you the symbols (or the exported Excel files) to use with `--symbols` or `--excel`.
"""


def skill_md() -> str:
    text = open(SKILL_SRC, encoding="utf-8").read()
    new, n = re.subn(r"## 1\. Find the tool\n.*?(?=\n## 2\.)", FIND_TOOL, text, count=1, flags=re.S)
    if n != 1:
        sys.exit("Could not find the 'Find the tool' section in %s" % SKILL_SRC)
    new = new.replace("(the folder containing `multibagger_cli.py`)", "")
    return new.replace("`-o NAME` (output path)", "`-o PATH` (output path without extension)")


def files():
    out = {"%s/SKILL.md" % NAME: skill_md().encode("utf-8")}
    for rel in BUNDLE:
        with open(os.path.join(ROOT, rel), "rb") as fh:
            out["%s/%s" % (NAME, rel)] = fh.read()
    pkg = os.path.join(ROOT, "multibagger")
    for fn in sorted(os.listdir(pkg)):
        if fn.endswith(".py"):
            with open(os.path.join(pkg, fn), "rb") as fh:
                out["%s/multibagger/%s" % (NAME, fn)] = fh.read()
    return out


def build(path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files().items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    return path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-o", "--out", default=os.path.join(ROOT, "cowork", NAME + ".zip"))
    args = ap.parse_args()
    print("Wrote", build(args.out))
