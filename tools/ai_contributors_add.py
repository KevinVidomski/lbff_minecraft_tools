#!/usr/bin/env python3
"""Safely append an AI contributor row to .github/AI_CONTRIBUTORS.csv.

Usage:
  python tools/ai_contributors_add.py --nickname NAME --model MODEL --date YYYY-MM-DD
"""
import argparse
import csv
from pathlib import Path
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / ".github" / "AI_CONTRIBUTORS.csv"


def validate_date(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD")


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--nickname", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--date", required=True, type=validate_date)
    args = p.parse_args(argv)

    if not CSV.exists():
        CSV.parent.mkdir(parents=True, exist_ok=True)
        with CSV.open("w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["nickname", "model", "current_date"])

    with CSV.open("a", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([args.nickname, args.model, args.date])

    print(f"Appended {args.nickname} to {CSV}")


if __name__ == "__main__":
    sys.exit(main())
