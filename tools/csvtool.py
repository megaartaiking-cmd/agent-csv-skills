#!/usr/bin/env python3
"""csvtool.py — tiny offline CSV CLI for agent-csv-skills.

Stdlib only. No dependencies, no network, no cloud.
Cleans, filters, summarizes, and converts CSV files.

Usage:
  python tools/csvtool.py clean data.csv clean.csv
  python tools/csvtool.py filter data.csv out.csv --column city --equals Paris
  python tools/csvtool.py summary data.csv
  python tools/csvtool.py to-json data.csv data.json
  python tools/csvtool.py to-md data.csv table.md
"""
import argparse
import csv
import json
import os
import sys
from collections import Counter


def fail(msg):
    print(f"csvtool: error: {msg}", file=sys.stderr)
    return 2


def read_csv(path):
    if not os.path.isfile(path):
        print(f"csvtool: error: file not found: {path}", file=sys.stderr)
        return None, None
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
            fields = rows[0].keys() if rows else []
            # Re-read fieldnames properly even for an empty file.
            with open(path, newline="", encoding="utf-8-sig") as f2:
                fields = csv.DictReader(f2).fieldnames or []
            return fields, rows
    except (csv.Error, UnicodeDecodeError) as e:
        print(f"csvtool: error: cannot read {path}: {e}", file=sys.stderr)
        return None, None


def write_csv(path, fields, rows):
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def cmd_clean(a):
    fields, rows = read_csv(a.input)
    if fields is None:
        return 2
    seen, out = set(), []
    for row in rows:
        cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        if all(v in (None, "") for v in cleaned.values()):
            continue  # drop fully empty rows
        key = tuple(cleaned.get(f, "") for f in fields)
        if key in seen:
            continue  # drop exact duplicate rows
        seen.add(key)
        out.append(cleaned)
    write_csv(a.output, fields, out)
    print(f"Cleaned: {len(rows)} rows -> {len(out)} rows. Saved: {a.output}")
    return 0


def cmd_filter(a):
    fields, rows = read_csv(a.input)
    if fields is None:
        return 2
    if a.column not in fields:
        return fail(f"no column '{a.column}'. Columns: {', '.join(fields)}")
    out = []
    for row in rows:
        value = (row.get(a.column) or "")
        if a.equals is not None and value == a.equals:
            out.append(row)
        elif a.contains is not None and a.contains.lower() in value.lower():
            out.append(row)
    write_csv(a.output, fields, out)
    print(f"Filtered: {len(out)} of {len(rows)} rows match. Saved: {a.output}")
    return 0


def cmd_summary(a):
    fields, rows = read_csv(a.input)
    if fields is None:
        return 2
    print(f"File: {a.input}")
    print(f"Rows: {len(rows)}")
    print(f"Columns ({len(fields)}): {', '.join(fields)}")
    for col in fields:
        values = [r.get(col, "") for r in rows]
        non_empty = [v for v in values if v not in (None, "")]
        line = f"  {col}: {len(non_empty)} filled, {len(set(non_empty))} unique"
        nums = []
        for v in non_empty:
            try:
                nums.append(float(v))
            except (TypeError, ValueError):
                pass
        if nums and len(nums) == len(non_empty):
            line += f", min={min(nums):g} max={max(nums):g} mean={sum(nums)/len(nums):.2f}"
        else:
            top = Counter(non_empty).most_common(3)
            if top:
                line += ", top: " + ", ".join(f"{v} ({c})" for v, c in top)
        print(line)
    return 0


def cmd_to_json(a):
    fields, rows = read_csv(a.input)
    if fields is None:
        return 2
    parent = os.path.dirname(os.path.abspath(a.output))
    os.makedirs(parent, exist_ok=True)
    with open(a.output, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Converted: {len(rows)} rows. Saved: {a.output}")
    return 0


def cmd_to_md(a):
    fields, rows = read_csv(a.input)
    if fields is None:
        return 2
    parent = os.path.dirname(os.path.abspath(a.output))
    os.makedirs(parent, exist_ok=True)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(fields) + " |\n")
        f.write("| " + " | ".join("---" for _ in fields) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(str(row.get(c, "")) for c in fields) + " |\n")
    print(f"Converted: {len(rows)} rows. Saved: {a.output}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="csvtool", description="Tiny offline CSV CLI (stdlib only).")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("clean", help="Strip whitespace, drop empty and duplicate rows")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_clean)

    s = sub.add_parser("filter", help="Keep rows matching a column value")
    s.add_argument("input"); s.add_argument("output")
    s.add_argument("--column", required=True)
    s.add_argument("--equals", default=None, help="Exact match")
    s.add_argument("--contains", default=None, help="Case-insensitive substring match")
    s.set_defaults(fn=cmd_filter)

    s = sub.add_parser("summary", help="Row/column counts and per-column stats")
    s.add_argument("input")
    s.set_defaults(fn=cmd_summary)

    s = sub.add_parser("to-json", help="Convert CSV to a JSON array")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_to_json)

    s = sub.add_parser("to-md", help="Convert CSV to a Markdown table")
    s.add_argument("input"); s.add_argument("output")
    s.set_defaults(fn=cmd_to_md)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
