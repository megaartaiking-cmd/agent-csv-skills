# Example commands

```sh
# Summarize the sample CSV
python tools/csvtool.py summary examples/sample.csv

# Clean it (strips whitespace, drops empty and duplicate rows)
python tools/csvtool.py clean examples/sample.csv clean.csv

# Keep only the Paris rows
python tools/csvtool.py filter examples/sample.csv paris.csv --column city --equals Paris

# Keep rows whose name contains "ali"
python tools/csvtool.py filter examples/sample.csv ali.csv --column name --contains ali

# Convert to JSON
python tools/csvtool.py to-json examples/sample.csv data.json

# Convert to a Markdown table
python tools/csvtool.py to-md examples/sample.csv table.md
```
