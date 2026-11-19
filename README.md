# agent-csv-skills

> **Agent Skills for CSV data — clean, filter, summarize, and convert CSV files to JSON and Markdown tables. Offline, stdlib-only Python.**

**1 skill · 1 CLI · 0 dependencies · 100% offline**

[![GitHub stars](https://img.shields.io/github/stars/megaartaiking-cmd/agent-csv-skills?style=social)](https://github.com/megaartaiking-cmd/agent-csv-skills/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](tools/csvtool.py)

AI agents are great at code, but working with a CSV still means opening a spreadsheet, or writing a one-off script every time. This repo fixes that gap: a small Agent Skill (SKILL.md) plus a tiny Python CLI that cleans, filters, summarizes, and converts CSV files — in the terminal, on the user's own PC.

Works with Claude Code, Cursor, GitHub Copilot, Codex, Gemini CLI, and any agent that reads SKILL.md files.

## Why this exists

Agent Skills are the fastest-growing category on GitHub — small, composable skill bundles, one job per skill, install in one step. Data files are the missing piece: agents get handed messy CSVs every day, and there is no small, offline, agent-native way to clean them up.

This one is:

- **Agent-native** — a skill in the open SKILL.md format, one job, clear rules
- **Offline** — no upload, no cloud, files never leave the PC
- **Lightweight** — stdlib-only Python, no pip install, no heavy app
- **Safe** — it never overwrites the input file; every command writes a new file

## Skills

| Skill | What it does | Command |
|---|---|---|
| `csv-data` | Clean, filter, summarize, convert CSV | `csvtool.py` |

The skill lives in `skills/csv-data/SKILL.md` — copy that folder into your agent's skills folder, or point your agent at this repo.

## Quick start

```sh
git clone https://github.com/megaartaiking-cmd/agent-csv-skills.git
cd agent-csv-skills

# 1. Summarize the sample CSV
python tools/csvtool.py summary examples/sample.csv

# 2. Clean it
python tools/csvtool.py clean examples/sample.csv clean.csv

# 3. Keep only the Paris rows
python tools/csvtool.py filter examples/sample.csv paris.csv --column city --equals Paris
```

No installation needed — Python 3.9+ is the only requirement.

## Usage

```sh
# Row/column counts and per-column stats
python tools/csvtool.py summary data.csv

# Strip whitespace, drop empty and duplicate rows
python tools/csvtool.py clean data.csv clean.csv

# Exact match filter
python tools/csvtool.py filter data.csv out.csv --column city --equals Paris

# Substring filter (case-insensitive)
python tools/csvtool.py filter data.csv out.csv --column name --contains ali

# Convert to a JSON array
python tools/csvtool.py to-json data.csv data.json

# Convert to a Markdown table
python tools/csvtool.py to-md data.csv table.md
```

See [examples/commands.md](examples/commands.md) for all commands, and [examples/sample.csv](examples/sample.csv) for a small file to try them on.

## How it works

1. You (or your agent) describe the job in plain words: "clean this CSV and keep only the Paris rows".
2. The skill in `skills/csv-data/` tells the agent the exact workflow, the command to run, and the rules — never overwrite the original, always write to a new file.
3. `tools/csvtool.py` (stdlib-only Python) does the work locally and reports the output path.
4. Nothing is uploaded. The edit happens on your PC.

## Works with

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini CLI
- Any agent that reads Agent Skills (SKILL.md)

Copy `skills/csv-data/` into your agent's skills directory, or ask your agent to read the SKILL.md file in this repo directly.

## FAQ

**Does it need the internet?**
No. After `git clone`, everything runs offline.

**Does it need Excel or Google Sheets?**
No. It reads and writes plain CSV files.

**Will it run on an old PC?**
Yes — that is the point. It is a small Python script with no dependencies, and it streams rows instead of loading a spreadsheet app.

**What does `clean` actually remove?**
Whitespace around values, fully empty rows, and exact duplicate rows. Nothing else is deleted.

**What if a filter matches zero rows?**
The tool says so. It does not write an empty file and call it done.

**Can I add a skill?**
Yes — copy `skills/csv-data/` as a template, write a SKILL.md with a clear name, description, workflow, and rules, and open a pull request.

## Contributing

Issues and pull requests are welcome. Keep skills small, one job per skill, with a tested command in `tools/csvtool.py`. Please do not add dependencies — stdlib only.

## License

MIT — see [LICENSE](LICENSE).

## More Agent Skills

More offline Agent Skills by the same author — one focused skill per repo:

- [agent-audio-skills](https://github.com/megaartaiking-cmd/agent-audio-skills) — Trim podcasts, normalize volume, extract audio from video
- [agent-json-skills](https://github.com/megaartaiking-cmd/agent-json-skills) — Validate, format, flatten, query, and diff JSON
- [agent-markdown-skills](https://github.com/megaartaiking-cmd/agent-markdown-skills) — Markdown to HTML, table of contents, link check, word count
- [agent-git-skills](https://github.com/megaartaiking-cmd/agent-git-skills) — Commit messages, changelogs, repo health, branch cleanup
- [agent-text-skills](https://github.com/megaartaiking-cmd/agent-text-skills) — Summarize text, extract keywords, readability, dedupe
- [agent-file-skills](https://github.com/megaartaiking-cmd/agent-file-skills) — Organize folders, find duplicates, batch rename
- [agent-sql-skills](https://github.com/megaartaiking-cmd/agent-sql-skills) — Explore SQLite, run queries, export to CSV
- [agent-video-skills](https://github.com/megaartaiking-cmd/agent-video-skills) — Edit video offline — trim, make Shorts, add titles, colour-grade
- [LiteCut Pro](https://github.com/megaartaiking-cmd/LIGHT-CUT-VIDEO-EDITOR) — lightweight offline video editor for Windows 10

---

**Keywords:** agent skills, AI agent CSV, CSV cleaning, CSV to JSON, CSV to Markdown, Claude Code skills, Cursor skills, offline CSV tool, Python CSV CLI, data cleaning
