#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"

SYMBOL_HEADER = [
    "symbol", "kind", "family", "header_or_namespace", "status", "min_client",
    "iid_or_guid", "acquisition", "purpose", "docs_url", "verified", "notes",
]
METHOD_HEADER = [
    "interface", "method", "header", "status", "min_client",
    "purpose", "docs_url", "verified", "notes",
]
ALLOWED_STATUS = {
    "Public", "Public-WDK", "Public-WinRT", "Legacy",
    "Undocumented", "Observed", "Experimental",
}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        rows = list(reader)
    return header, rows


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    csv_files = sorted(API_DIR.glob("*.csv"))

    if not csv_files:
        fail(errors, "No API CSV files found.")

    actual_counts: dict[str, int] = {}

    for path in csv_files:
        header, rows = load_rows(path)
        actual_counts[path.as_posix().replace(ROOT.as_posix() + "/", "")] = len(rows)

        is_method = path.name.startswith("methods-")
        expected = METHOD_HEADER if is_method else SYMBOL_HEADER
        if header != expected:
            fail(errors, f"{path}: unexpected header: {header!r}")

        seen: set[tuple[str, ...]] = set()

        for lineno, row in enumerate(rows, start=2):
            label = f"{path}:{lineno}"

            status = (row.get("status") or "").strip()
            if status not in ALLOWED_STATUS:
                fail(errors, f"{label}: invalid status {status!r}")

            verified = (row.get("verified") or "").strip()
            if not DATE_RE.match(verified):
                fail(errors, f"{label}: verified must be YYYY-MM-DD, got {verified!r}")

            url = (row.get("docs_url") or "").strip()
            if url and not url.startswith("https://"):
                fail(errors, f"{label}: docs_url must use https://, got {url!r}")

            if is_method:
                interface = (row.get("interface") or "").strip()
                method = (row.get("method") or "").strip()
                if not interface or not method:
                    fail(errors, f"{label}: method rows require interface and method")
                key = (interface, method)
            else:
                symbol = (row.get("symbol") or "").strip()
                kind = (row.get("kind") or "").strip()
                family = (row.get("family") or "").strip()
                if not symbol or not kind or not family:
                    fail(errors, f"{label}: symbol rows require symbol, kind and family")
                key = (symbol, kind, family)

                if status.startswith("Public") and not url:
                    warnings.append(f"{label}: public record has no docs_url")

            if key in seen:
                fail(errors, f"{label}: duplicate key {key}")
            seen.add(key)

    catalog_path = API_DIR / "catalog.json"
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        expected_counts = {t["path"]: t["records"] for t in catalog.get("tables", [])}

        for path, count in actual_counts.items():
            if path not in expected_counts:
                fail(errors, f"{path}: missing from api/catalog.json")
            elif expected_counts[path] != count:
                fail(errors, f"{path}: catalog says {expected_counts[path]} records but CSV has {count}")

        for path in expected_counts:
            if path not in actual_counts:
                fail(errors, f"api/catalog.json references missing CSV: {path}")

        total = sum(actual_counts.values())
        if catalog.get("total_records") != total:
            fail(errors, f"catalog total_records={catalog.get('total_records')} but actual total={total}")

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print(f"\nAPI DB validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"API DB OK: {len(csv_files)} CSV files, {sum(actual_counts.values())} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
