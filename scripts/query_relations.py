#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL_PATH = ROOT / "api" / "relationships.csv"


def load_edges():
    with REL_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def matches_filters(edge, status, family):
    if status and edge["status"].lower() != status.lower():
        return False
    if family and family.lower() not in edge["family"].lower():
        return False
    return True


def traverse(edges, start, direction, depth, status, family):
    selected = []
    seen_edges = set()
    seen_nodes = {start.lower()}
    q = deque([(start, 0)])

    while q:
        node, level = q.popleft()
        if level >= depth:
            continue

        for edge in edges:
            if not matches_filters(edge, status, family):
                continue

            source = edge["source"]
            target = edge["target"]
            next_node = None

            if direction in ("out", "both") and source.lower() == node.lower():
                next_node = target
            elif direction in ("in", "both") and target.lower() == node.lower():
                next_node = source
            else:
                continue

            key = (source, edge["relation"], target)
            if key not in seen_edges:
                seen_edges.add(key)
                selected.append(edge)

            if next_node.lower() not in seen_nodes:
                seen_nodes.add(next_node.lower())
                q.append((next_node, level + 1))

    return selected


def print_text(edges):
    for e in edges:
        print(f"{e['source']} --{e['relation']}--> {e['target']}")
        print(f"  family: {e['family']}")
        print(f"  status: {e['status']}")
        if e["min_client"]:
            print(f"  min_client: {e['min_client']}")
        if e["purpose"]:
            print(f"  purpose: {e['purpose']}")
        if e["docs_url"]:
            print(f"  docs: {e['docs_url']}")
        if e["notes"]:
            print(f"  notes: {e['notes']}")
        print()


def quote_dot(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def print_dot(edges, start):
    print("digraph WinAudioResearch {")
    print("  rankdir=LR;")
    print(f"  {quote_dot(start)} [shape=box];")
    for e in edges:
        label = e["relation"]
        if e["status"] == "Undocumented":
            label += " [Undocumented]"
        print(
            f"  {quote_dot(e['source'])} -> {quote_dot(e['target'])} "
            f"[label={quote_dot(label)}];"
        )
    print("}")


def main():
    p = argparse.ArgumentParser(
        description="Traverse WinAudioResearch API acquisition/relationship graph."
    )
    p.add_argument("node", help="Start node, e.g. IMMDevice or IAudioClient")
    p.add_argument(
        "--direction",
        choices=("out", "in", "both"),
        default="out",
        help="Traverse outgoing, incoming or both directions",
    )
    p.add_argument("--depth", type=int, default=1, help="Traversal depth (default: 1)")
    p.add_argument("--status", help="Filter by stability status")
    p.add_argument("--family", help="Filter by family substring")
    p.add_argument("--dot", action="store_true", help="Emit Graphviz DOT")
    args = p.parse_args()

    if args.depth < 1:
        p.error("--depth must be >= 1")

    edges = load_edges()
    result = traverse(
        edges, args.node, args.direction, args.depth, args.status, args.family
    )

    if args.dot:
        print_dot(result, args.node)
    else:
        print_text(result)
        print(f"{len(result)} relationship(s)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
