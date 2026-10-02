#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "api"

HEADERS = {
    "symbol": [
        "symbol", "kind", "family", "header_or_namespace", "status", "min_client",
        "iid_or_guid", "acquisition", "purpose", "docs_url", "verified", "notes",
    ],
    "method": [
        "interface", "method", "header", "status", "min_client",
        "purpose", "docs_url", "verified", "notes",
    ],
    "member": [
        "type", "member", "member_kind", "namespace", "status", "min_client",
        "purpose", "docs_url", "verified", "notes",
    ],
    "capability": [
        "capability", "family", "introduced", "changed_or_removed", "status",
        "api_or_component", "purpose", "docs_url", "verified", "notes",
    ],
    "dependency": [
        "symbol", "family", "header", "library", "dll_or_runtime", "package",
        "status", "min_client", "docs_url", "verified", "notes",
    ],
    "sample": [
        "sample", "source_repo", "path", "family", "language", "status",
        "purpose", "source_url", "verified", "notes",
    ],
}

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
        return reader.fieldnames or [], list(reader)


def record_key(table_type: str, row: dict[str, str]) -> tuple[str, ...]:
    if table_type == "symbol":
        return (
            (row.get("symbol") or "").strip(),
            (row.get("kind") or "").strip(),
            (row.get("family") or "").strip(),
        )
    if table_type == "method":
        return (
            (row.get("interface") or "").strip(),
            (row.get("method") or "").strip(),
        )
    if table_type == "member":
        return (
            (row.get("type") or "").strip(),
            (row.get("member") or "").strip(),
            (row.get("member_kind") or "").strip(),
        )
    if table_type == "capability":
        return (
            (row.get("capability") or "").strip(),
            (row.get("introduced") or "").strip(),
        )
    if table_type == "dependency":
        return (
            (row.get("symbol") or "").strip(),
            (row.get("family") or "").strip(),
        )
    if table_type == "sample":
        return (
            (row.get("source_repo") or "").strip(),
            (row.get("path") or "").strip(),
        )
    raise ValueError(table_type)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    catalog_path = API_DIR / "catalog.json"
    if not catalog_path.exists():
        fail(errors, "api/catalog.json is missing.")
        catalog = {"tables": []}
    else:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

    table_specs = {
        t["path"]: t for t in catalog.get("tables", [])
    }
    csv_files = sorted(API_DIR.glob("*.csv"))
    actual_counts: dict[str, int] = {}
    counts_by_type: dict[str, int] = {}

    if not csv_files:
        fail(errors, "No API CSV files found.")

    for path in csv_files:
        rel = path.relative_to(ROOT).as_posix()
        spec = table_specs.get(rel)
        if spec is None:
            fail(errors, f"{rel}: missing from api/catalog.json")
            continue

        table_type = spec.get("type")
        if table_type not in HEADERS:
            fail(errors, f"{rel}: unsupported catalog type {table_type!r}")
            continue

        header, rows = load_rows(path)
        actual_counts[rel] = len(rows)
        counts_by_type[table_type] = counts_by_type.get(table_type, 0) + len(rows)

        expected_header = HEADERS[table_type]
        if header != expected_header:
            fail(errors, f"{rel}: unexpected header: {header!r}")

        if spec.get("records") != len(rows):
            fail(
                errors,
                f"{rel}: catalog says {spec.get('records')} records but CSV has {len(rows)}",
            )

        seen: set[tuple[str, ...]] = set()

        for lineno, row in enumerate(rows, start=2):
            label = f"{rel}:{lineno}"

            status = (row.get("status") or "").strip()
            if status not in ALLOWED_STATUS:
                fail(errors, f"{label}: invalid status {status!r}")

            verified = (row.get("verified") or "").strip()
            if not DATE_RE.match(verified):
                fail(errors, f"{label}: verified must be YYYY-MM-DD, got {verified!r}")

            url_key = "source_url" if table_type == "sample" else "docs_url"
            url = (row.get(url_key) or "").strip()
            if url and not url.startswith("https://"):
                fail(errors, f"{label}: {url_key} must use https://, got {url!r}")

            key = record_key(table_type, row)
            if any(not value for value in key):
                fail(errors, f"{label}: incomplete primary key {key}")
            if key in seen:
                fail(errors, f"{label}: duplicate key {key}")
            seen.add(key)

            if status.startswith("Public") and table_type in {"symbol", "method", "member"} and not url:
                warnings.append(f"{label}: public record has no official/source URL")

    for rel in table_specs:
        if rel.endswith(".csv") and rel not in actual_counts:
            fail(errors, f"api/catalog.json references missing CSV: {rel}")

    actual_total = sum(actual_counts.values())
    if catalog.get("total_records") != actual_total:
        fail(
            errors,
            f"catalog total_records={catalog.get('total_records')} but actual total={actual_total}",
        )

    for type_name, actual in counts_by_type.items():
        field = f"{type_name}_records"
        if field in catalog and catalog.get(field) != actual:
            fail(errors, f"catalog {field}={catalog.get(field)} but actual={actual}")

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"\nAPI DB validation failed: {len(errors)} error(s).", file=sys.stderr)
        return 1

    detail = ", ".join(
        f"{k}={v}" for k, v in sorted(counts_by_type.items())
    )
    print(
        f"API DB OK: {len(csv_files)} CSV files, {actual_total} records"
        + (f" ({detail})" if detail else "")
        + "."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
