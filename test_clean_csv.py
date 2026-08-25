import csv
import tempfile
import unittest
from pathlib import Path

from clean_csv import clean_csv


class CleanCsvTests(unittest.TestCase):
    def test_cleans_headers_whitespace_blanks_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.csv"
            source.write_text(
                " Full Name , Email Address \n Alice , alice@example.com \n\n Alice , alice@example.com \n Bob,bob@example.com\n",
                encoding="utf-8",
            )

            report = clean_csv(source, output)

            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))
            self.assertEqual(rows[0], ["full_name", "email_address"])
            self.assertEqual(rows[1:], [["Alice", "alice@example.com"], ["Bob", "bob@example.com"]])
            self.assertEqual(report["blank_rows_removed"], 1)
            self.assertEqual(report["duplicate_rows_removed"], 1)


if __name__ == "__main__":
    unittest.main()
