#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"


def read_rows():
    for path in sorted(API_DIR.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                row["_table"] = path.name
                yield row


def searchable_text(row: dict[str, str]) -> str:
    return " ".join(str(v) for k, v in row.items() if not k.startswith("_")).lower()


def main() -> int:
    p = argparse.ArgumentParser(description="Search the WinAudioResearch API database.")
    p.add_argument("query", nargs="?", default="", help="Text search, e.g. IAudioClient")
    p.add_argument("--status", help="Filter by status, e.g. Public or Undocumented")
    p.add_argument("--family", help="Filter by family substring")
    p.add_argument("--table", help="Filter by CSV filename substring")
    args = p.parse_args()

    q = args.query.lower()
    matches = []

    for row in read_rows():
        if q and q not in searchable_text(row):
            continue
        if args.status and (row.get("status") or "").lower() != args.status.lower():
            continue
        if args.family and args.family.lower() not in (row.get("family") or "").lower():
            continue
        if args.table and args.table.lower() not in row["_table"].lower():
            continue
        matches.append(row)

    for row in matches:
        name = row.get("symbol") or (
            f"{row.get('interface', '')}::{row.get('method', '')}"
        )
        print(f"[{row['_table']}] {name}")
        for key in ("kind", "family", "header_or_namespace", "header", "status",
                    "min_client", "iid_or_guid", "purpose", "docs_url", "notes"):
            value = (row.get(key) or "").strip()
            if value:
                print(f"  {key}: {value}")
        print()

    print(f"{len(matches)} match(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
