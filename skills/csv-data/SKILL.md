---
name: csv-data
description: Clean, filter, summarize, and convert CSV files to JSON and Markdown tables, offline, with Python. Use when the user or agent wants to work with spreadsheet data in a CSV file.
---

# CSV Data

Work with CSV files without opening a spreadsheet. Clean messy data,
filter rows, get a quick summary, or convert to JSON or a Markdown table.
No cloud, no upload. Files stay local.

## When to use

- "Clean up this CSV"
- "Show me only the rows where city is Paris"
- "Summarize this CSV — how many rows, what columns?"
- "Convert this CSV to JSON"

## Workflow

1. Look at the file first. If it is not a CSV, say so and stop.
2. Summarize before changing anything:
   ```sh
   python tools/csvtool.py summary data.csv
   ```
   Report the row count, columns, and anything odd (empty values, duplicates).
3. Clean — strips whitespace, drops empty rows and exact duplicates:
   ```sh
   python tools/csvtool.py clean data.csv clean.csv
   ```
4. Filter — exact match or substring:
   ```sh
   python tools/csvtool.py filter data.csv out.csv --column city --equals Paris
   python tools/csvtool.py filter data.csv out.csv --column name --contains ali
   ```
5. Convert when asked:
   ```sh
   python tools/csvtool.py to-json data.csv data.json
   python tools/csvtool.py to-md data.csv table.md
   ```
6. Confirm the output file exists and report rows in / rows out.

## Examples

**Clean a messy export**
```sh
python tools/csvtool.py clean export.csv clean.csv
# Cleaned: 120 rows -> 114 rows. Saved: clean.csv
```

**Only the Paris customers, as a Markdown table**
```sh
python tools/csvtool.py filter customers.csv paris.csv --column city --equals Paris
python tools/csvtool.py to-md paris.csv paris.md
```

**A quick look before doing anything**
```sh
python tools/csvtool.py summary sales.csv
# Rows: 2431 — Columns (6): date, product, price, qty, city, channel
```

## Rules

- Never overwrite the input file. Always write to a new output file.
- Do not guess column names — use the summary output, or ask the user.
- Do not delete rows the user did not ask to remove; `clean` only removes empty and exact-duplicate rows.
- If a filter matches zero rows, say so — do not write an empty file silently and call it done.
- For very large files, prefer `summary` and `filter` over loading the whole file into a reply.
