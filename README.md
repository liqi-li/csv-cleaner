# CSV Cleaner

A small, dependency-free Python utility for cleaning CSV exports before analysis or import.

## Features

- Normalizes column names to `snake_case`
- Trims whitespace from every cell
- Removes blank rows
- Removes exact duplicate rows
- Handles UTF-8 BOM files
- Prints a machine-readable JSON report

## Usage

```bash
python clean_csv.py sample.csv cleaned.csv
```

Example report:

```json
{
  "input_rows": 4,
  "output_rows": 2,
  "blank_rows_removed": 1,
  "duplicate_rows_removed": 1
}
```

## Test

```bash
python -m unittest -v
```

## Why this project exists

CSV files exported from business systems often contain inconsistent headers, extra whitespace, blank records, and duplicates. This tool provides a reproducible first cleaning pass without uploading sensitive data to a third-party service.

## License

MIT
