#!/usr/bin/env python3
"""Validate .github/AI_CONTRIBUTORS.csv rows.

Checks:
- header contains nickname,model,current_date
- each row has 3 columns
- date is ISO YYYY-MM-DD
"""
import csv
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / ".github" / "AI_CONTRIBUTORS.csv"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main() -> int:
    """
    Validate the .github/AI_CONTRIBUTORS.csv file and report any format errors.
    
    Performs existence and content checks on the CSV and prints error messages for problems found. It verifies the header equals ["nickname", "model", "current_date"], skips empty rows, ensures each non-empty row has exactly three columns, and checks that the date column matches the YYYY-MM-DD pattern. Prints "[OK] AI contributors CSV looks good" when no issues are found.
    
    Returns:
        int: Exit code where `0` indicates the CSV passed all checks, and `1` indicates any error (missing file, empty file, unexpected header, wrong column count, or invalid date format).
    """
    if not CSV.exists():
        print(f"[ERROR] {CSV} not found")
        return 1

    with CSV.open(newline="") as fh:
        reader = csv.reader(fh)
        try:
            header = next(reader)
        except StopIteration:
            print("[ERROR] CSV is empty")
            return 1

        if header != ["nickname", "model", "current_date"]:
            print(f"[ERROR] Unexpected header: {header}")
            return 1

        ok = True
        for i, row in enumerate(reader, start=2):
            if not row or all(not c.strip() for c in row):
                continue
            if len(row) != 3:
                print(f"[ERROR] Line {i}: expected 3 columns, got {len(row)}")
                ok = False
                continue
            nick, model, date = row
            if not DATE_RE.match(date.strip()):
                print(f"[ERROR] Line {i}: bad date format '{date}' (expected YYYY-MM-DD)")
                ok = False

    if ok:
        print("[OK] AI contributors CSV looks good")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())