---
name: screen-indian-stocks
description: Screen Indian stocks for enduring multibagger candidates using the Value Investing Process (2-minute test, quality gates, moat x growth matrix, five valuation models, buy/sell ladders) with data from Screener.in. Use when the user asks to screen, rank, analyse or find multibagger / value / quality stocks in India, to run the Stage 1 screen, or to analyse specific NSE/BSE symbols or Screener Excel exports.
---

# Screen Indian stocks

Runs `multibagger_cli.py` (standard library only, no installs) and turns its output into a ranked shortlist with the reasoning. The process: 11-point 2-minute test → quality gates (ROE, cash flow, debt, SSGR, dilution, promoter holding) → profitability and Moat × Growth matrices → five valuation models averaged into one intrinsic value → entry/exit ladders. Details are in `docs/MULTIBAGGER.md`.

## 1. Find the tool

Work from the repo root (the folder containing `multibagger_cli.py`). If it is not in the current directory or a parent, clone it:

```bash
git clone https://github.com/Liku1376/indian-stocks-screener && cd indian-stocks-screener
```

## 2. Pick the input

Match what the user asked for:

| The user wants | Command |
| --- | --- |
| Specific companies | `python multibagger_cli.py --symbols TCS PIDILITIND` (the code in the screener.in URL) |
| A list or the whole market | `--symbols-file FILE` (text, one symbol per line, or NSE `EQUITY_L.csv`) |
| "Find me candidates" | `--stage1` (runs the guide's quality screen on screener.in; needs `SCREENER_USERNAME` and `SCREENER_PASSWORD`, or `SCREENER_SESSIONID`, in the environment) |
| Their own screen query | `--query "Market Capitalization > 500 AND ..."` (login needed) |
| Downloaded Excel exports | `--excel exports/*.xlsx` |

If the user gave no input and has no login, use `examples/watchlist.txt` and say so. Never ask the user to paste their password into chat; tell them to set the environment variables.

Useful options: `--limit N` (cap the run, sensible for a first try), `--discount 14` (the guide says use 14–15% for moatless businesses, cyclicals and anything under ₹2,000 cr), `--gsec`, `--exit-pe`, `--min-cap`, `--standalone`, `--json`, `-o NAME` (output path). Large runs are slow on purpose (2 s between requests, cached for a day); for more than ~50 symbols run in the background and tell the user.

## 3. Run it and read the results

The run prints a ranked table and writes `multibagger_report.html` and `.csv` (and `.json` with `--json`). If screener.in cannot be reached (network policy, rate limit, layout change), say exactly that — do not invent data. `MULTIBAGGER_DEBUG=1` shows the full error for a symbol that fails. For symbols that fail, report them as "could not fetch", not as rejected.

## 4. Report back

Lead with the answer, then the evidence:

1. **BUY** (clears every gate, price at or below the phase-1 buy price, projected capital gain ≥ 15% with the business supplying most of it): for each, give score, quadrant, 10-year ROE, FCF/sales, profit CAGR, intrinsic value, the three buy prices and the sell ladder.
2. **WATCH** (good business, wrong price): give the "Buy ≤" price to set an alert at.
3. **REJECT**: one line each with the failed gates. Call out value traps, meaning cheap on relative valuation but failing the quality gate.
4. Counts for skipped companies (banks, NBFCs, insurers need a different method; too little history; fetch errors).

Always flag:
- When the five valuation models disagree by more than 1.6× the entry prices are anchored on the lowest two; show the five values, not just the average.
- Valuation growth above SSGR.
- Companies under ₹5,000 cr ("sweet spot", under-covered).

## 5. Never present a result as a buy recommendation

The numbers only screen a business. For every shortlisted name, end with what is still to do by hand: circle of competence; annual reports, auditor and related-party checks (the forensic checklist and 18-point Satyam test); naming the moat and judging management; the fragility test; the written five-sentence thesis; the behavioural gate and 48-hour wait. The process is backward-looking and cannot detect a well-executed fraud. This is analysis support, not investment advice.

Point the user to `multibagger_report.html` (sortable, with expandable workings for each shortlisted stock) and `multibagger_report.csv`.
