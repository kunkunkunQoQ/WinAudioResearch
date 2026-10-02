#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"


def read_rows():
    catalog = json.loads((API_DIR / "catalog.json").read_text(encoding="utf-8"))
    for spec in catalog.get("tables", []):
        path = ROOT / spec["path"]
        if path.suffix.lower() != ".csv" or not path.exists():
            continue
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                row["_table"] = path.name
                row["_type"] = spec.get("type", "")
                row["_catalog_family"] = spec.get("family", "")
                yield row


def searchable_text(row: dict[str, str]) -> str:
    return " ".join(str(v) for k, v in row.items() if not k.startswith("_")).lower()


def display_name(row: dict[str, str]) -> str:
    if row.get("symbol"):
        return row["symbol"]
    if row.get("interface") and row.get("method"):
        return f"{row['interface']}::{row['method']}"
    if row.get("type") and row.get("member"):
        return f"{row['type']}.{row['member']}"
    if row.get("capability"):
        return row["capability"]
    if row.get("sample"):
        return row["sample"]
    if row.get("source") and row.get("relation") and row.get("target"):
        return f"{row['source']} --{row['relation']}--> {row['target']}"
    return "(unnamed)"


def main() -> int:
    p = argparse.ArgumentParser(description="Search the WinAudioResearch API database.")
    p.add_argument("query", nargs="?", default="", help="Text search, e.g. IAudioClient")
    p.add_argument("--status", help="Filter by status, e.g. Public or Undocumented")
    p.add_argument("--family", help="Filter by row/catalog family substring")
    p.add_argument("--type", dest="record_type", help="symbol/method/member/capability/dependency/sample/relationship")
    p.add_argument("--table", help="Filter by CSV filename substring")
    args = p.parse_args()

    q = args.query.lower()
    matches = []

    for row in read_rows():
        if q and q not in searchable_text(row):
            continue
        if args.status and (row.get("status") or "").lower() != args.status.lower():
            continue
        family = (row.get("family") or row.get("_catalog_family") or "")
        if args.family and args.family.lower() not in family.lower():
            continue
        if args.record_type and row.get("_type", "").lower() != args.record_type.lower():
            continue
        if args.table and args.table.lower() not in row["_table"].lower():
            continue
        matches.append(row)

    for row in matches:
        print(f"[{row['_table']} / {row['_type']}] {display_name(row)}")
        for key in (
            "kind", "member_kind", "family", "header_or_namespace", "header",
            "namespace", "status", "min_client", "introduced",
            "changed_or_removed", "iid_or_guid", "library", "dll_or_runtime",
            "package", "source", "relation", "target", "purpose", "docs_url", "source_url", "notes",
        ):
            value = (row.get(key) or "").strip()
            if value:
                print(f"  {key}: {value}")
        print()

    print(f"{len(matches)} match(es)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
