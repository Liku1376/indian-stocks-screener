# Multibagger Screener — Indian equities

A command-line tool that collects company data from
[Screener.in](https://www.screener.in) and runs every stock through the
**Value Investing Process — Indian Equities** guide, then ranks them so the
strongest candidates for an *enduring* multibagger appear first
(BUY → WATCH → REJECT).

It uses only the Python standard library — nothing to install.

```bash
python multibagger_cli.py --symbols PIDILITIND ASTRAL PAGEIND
python multibagger_cli.py --symbols-file examples/watchlist.txt
python multibagger_cli.py --save-login    # once: save your screener.in login (private file, asks in your terminal)
python multibagger_cli.py --stage1          # the guide's Stage 1 screen, using the saved login
python multibagger_cli.py --excel exports/*.xlsx
```

Each run prints a ranked table and writes `multibagger_report.html` and
`multibagger_report.csv`.

See [docs/MULTIBAGGER.md](docs/MULTIBAGGER.md) for what each stage checks, the
verdict rules and the options.

## Use it from Claude Code

The repo includes a Claude skill, `.claude/skills/screen-indian-stocks`. Open
this folder in Claude Code and ask, for example, *"screen these Indian stocks:
PIDILITIND, ASTRAL, PAGEIND"* or *"run the Stage 1 screen and show me the
strongest candidates"*. Claude runs the tool, reads the report and summarises
the BUY / WATCH / REJECT results with the reasoning and the manual checks still
to do. You can also invoke it directly with `/screen-indian-stocks`.

### Claude Cowork

`cowork/screen-indian-stocks.zip` is a self-contained version of the skill (the
instructions plus the tool's code, so nothing has to be cloned). In Claude, open
**Settings → Capabilities → Skills**, upload the zip, and ask Cowork to screen
some Indian stocks. After changing the code or the skill, rebuild it with
`python scripts/build_cowork_skill.py`.

## Tests

```bash
pip install pytest
python -m pytest
```
