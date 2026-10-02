#!/usr/bin/env python3
"""Check Core Audio identifiers/dependencies against the pinned audit evidence."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import tempfile
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUID_RE = re.compile(r"[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}")
DECLARATION_RE = re.compile(
    r'MIDL_INTERFACE\("([0-9A-Fa-f-]+)"\)\s+(\w+)\s*:'
    r'|DECLARE_INTERFACE_IID_\((\w+),\s*\w+,\s*"([0-9A-Fa-f-]+)"\)'
    r'|class\s+DECLSPEC_UUID\("([0-9A-Fa-f-]+)"\)\s+(\w+)'
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def parse_declarations(text: str) -> dict[str, tuple[str, str]]:
    declarations = {}
    for match in DECLARATION_RE.finditer(text):
        guid1, name1, name2, guid2, guid3, name3 = match.groups()
        name = name1 or name2 or name3
        declarations[name] = ((guid1 or guid2 or guid3).upper(), "class" if name3 else "interface")
    return declarations


def validate_audit(root: Path, headers_dir: Path | None = None) -> tuple[list[str], int]:
    errors: list[str] = []
    manifest = json.loads((root / "api/core-audio-audit.json").read_text(encoding="utf-8"))
    if manifest["version"] != 1:
        errors.append("Unsupported Core Audio audit version")
    date.fromisoformat(manifest["verified"])
    if manifest["source_repository"] != "https://github.com/microsoft/win32metadata":
        errors.append("Core Audio audit must identify the Microsoft SDK source repository")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]):
        errors.append("Core Audio source must be pinned to a full commit SHA")

    dependencies = {}
    for row in read_rows(root / "api/dependencies.csv"):
        key = (row["symbol"], row["family"])
        if key in dependencies:
            errors.append(f"Duplicate dependency: {key}")
        dependencies[key] = row

    count = 0
    seen_identifiers = {}
    for group in manifest["groups"]:
        table = group["table"]
        rows = [r for r in read_rows(root / table) if r["kind"] in {"interface", "class"}]
        indexed = {r["symbol"]: r for r in rows}
        expected = {name: (guid, "interface") for name, guid in group["interfaces"].items()}
        expected.update({name: (guid, "class") for name, guid in group["classes"].items()})
        excluded = group["excluded_declarations"]
        if expected.keys() & excluded.keys():
            errors.append(f"{table}: declaration is both covered and excluded")
        if any(not reason.strip() for reason in excluded.values()):
            errors.append(f"{table}: excluded declarations require a coverage explanation")
        if not re.fullmatch(r"[0-9a-f]{64}", group["header_sha256"]):
            errors.append(f"{table}: source header requires a SHA-256 digest")
        if len(indexed) != len(rows):
            errors.append(f"{table}: duplicate interface/class symbol")
        for name in expected.keys() - indexed.keys():
            errors.append(f"{table}: audited identifier missing from CSV: {name}")
        for name in indexed.keys() - expected.keys():
            errors.append(f"{table}: identifier needs source audit: {name}")
        for name, (guid, kind) in expected.items():
            count += 1
            if not GUID_RE.fullmatch(guid):
                errors.append(f"{table}: invalid canonical source GUID for {name}")
            if guid in seen_identifiers:
                errors.append(f"{table}: duplicate identifier value for {name} and {seen_identifiers[guid]}")
            seen_identifiers[guid] = name
            row = indexed.get(name)
            if row is None:
                continue
            if row["iid_or_guid"] != guid:
                errors.append(f"{table}: {name} IID/CLSID differs from pinned source: {row['iid_or_guid']!r}")
            if row["kind"] != kind:
                errors.append(f"{table}: {name} must be a {kind}")
            if row["header_or_namespace"].casefold() != group["header"].casefold():
                errors.append(f"{table}: {name} has the wrong header")
            dep = dependencies.get((name, row["family"]))
            if dep is None:
                errors.append(f"{table}: missing dependency record for {name}")
            else:
                for field, symbol_field in (("header", "header_or_namespace"), ("status", "status"), ("min_client", "min_client")):
                    if dep[field].casefold() != row[symbol_field].casefold():
                        errors.append(f"{table}: {name} dependency {field} differs from its symbol record")
                if dep["library"]:
                    errors.append(f"{table}: {name} is a COM ABI; this audit does not assert an interface import library")

        if headers_dir is not None:
            header_path = headers_dir / group["header"]
            if not header_path.exists():
                errors.append(f"Source header missing: {header_path}")
                continue
            data = header_path.read_bytes()
            if hashlib.sha256(data).hexdigest() != group["header_sha256"]:
                errors.append(f"{group['header']}: source header hash differs from the pinned snapshot")
            declarations = parse_declarations(data.decode("utf-8-sig"))
            for name, identity in expected.items():
                if declarations.get(name) != identity:
                    errors.append(f"{group['header']}: source declaration differs for {name}")
            for name in declarations.keys() - expected.keys() - excluded.keys():
                errors.append(f"{group['header']}: source declaration not classified: {name}")
            for name in excluded.keys() - declarations.keys():
                errors.append(f"{group['header']}: excluded declaration no longer present: {name}")

    for name, spec in manifest["function_dependencies"].items():
        dep = dependencies.get((name, spec["family"]))
        if dep is None:
            errors.append(f"Missing function dependency: {name}")
            continue
        for field, value in spec.items():
            if dep[field] != value:
                errors.append(f"{name}: dependency {field} differs from audited Requirements")
    return errors, count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--headers-dir", type=Path, help="Optional directory of the six unmodified pinned SDK headers")
    source.add_argument("--fetch-headers", action="store_true", help="Download the six pinned Microsoft headers into a temporary directory and verify their hashes/declarations")
    args = parser.parse_args()
    try:
        if args.fetch_headers:
            manifest = json.loads((ROOT / "api/core-audio-audit.json").read_text(encoding="utf-8"))
            with tempfile.TemporaryDirectory(prefix="core-audio-audit-") as folder:
                headers_dir = Path(folder)
                for group in manifest["groups"]:
                    url = f"https://raw.githubusercontent.com/microsoft/win32metadata/{manifest['source_commit']}/{manifest['source_path']}/{group['header']}"
                    with urllib.request.urlopen(url, timeout=30) as response:
                        (headers_dir / group["header"]).write_bytes(response.read())
                errors, count = validate_audit(ROOT, headers_dir)
        else:
            errors, count = validate_audit(ROOT, args.headers_dir)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: Core Audio audit could not be read: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Core Audio audit OK: {count} IID/CLSID records and their dependencies" + ("; pinned header hashes/declarations verified." if args.headers_dir or args.fetch_headers else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
