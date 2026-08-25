"""Clean CSV files with only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def normalize_header(value: str, index: int) -> str:
    cleaned = "_".join(value.strip().lower().split())
    return cleaned or f"column_{index + 1}"


def clean_csv(source: Path, destination: Path) -> dict[str, int]:
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    if not rows:
        raise ValueError("The input CSV is empty.")

    headers = [normalize_header(value, index) for index, value in enumerate(rows[0])]
    width = len(headers)
    cleaned_rows: list[tuple[str, ...]] = []
    seen: set[tuple[str, ...]] = set()
    blank_rows = 0
    duplicate_rows = 0

    for raw_row in rows[1:]:
        row = tuple((raw_row + [""] * width)[:width])
        row = tuple(value.strip() for value in row)
        if not any(row):
            blank_rows += 1
            continue
        if row in seen:
            duplicate_rows += 1
            continue
        seen.add(row)
        cleaned_rows.append(row)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    return {
        "input_rows": max(len(rows) - 1, 0),
        "output_rows": len(cleaned_rows),
        "blank_rows_removed": blank_rows,
        "duplicate_rows_removed": duplicate_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean a CSV file and print a JSON report.")
    parser.add_argument("input", type=Path, help="Input CSV path")
    parser.add_argument("output", type=Path, help="Cleaned CSV path")
    args = parser.parse_args()

    report = clean_csv(args.input, args.output)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
