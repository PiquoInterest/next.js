#!/usr/bin/env python3
"""Deterministic candidate entrypoint inventory for a pinned Next.js checkout.

This is an inventory heuristic, NOT a sound control-flow graph or formal proof.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess

ROOTS = ("packages/next/src", "packages/next-swc", "crates", "turbopack")
PATTERNS = [
    ("http_handler", re.compile(r"\\b(?:createServer|handleRequest|requestHandler|handleUpgrade)\\b")),
    ("route_handler", re.compile(r"\\b(?:routeModule|RouteModule|handleAction|runHandler|resolveRoutes)\\b")),
    ("middleware", re.compile(r"\\b(?:middleware|rewrite|redirect)\\b", re.I)),
    ("cache", re.compile(r"\\b(?:revalidate|incrementalCache|cacheHandler)\\b", re.I)),
    ("image_asset", re.compile(r"\\b(?:imageOptimizer|serveStatic|sendStatic|metadataRoute)\\b")),
    ("build_cli", re.compile(r"\\b(?:nextBuild|nextDev|nextStart|runCompiler)\\b")),
    ("edge", re.compile(r"\\b(?:edgeRuntime|EdgeRuntime|adapter)\\b")),
]
SUFFIXES = {".ts", ".tsx", ".js", ".mjs", ".rs"}
EXCLUDE = ("__tests__", "/test/", "/tests/", "/fixtures/", "/node_modules/", "/target/")

def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()

def inventory(root):
    records = []
    for prefix in ROOTS:
        base = root / prefix
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            rel = path.relative_to(root).as_posix()
            if not path.is_file() or path.suffix not in SUFFIXES or any(x in "/" + rel + "/" for x in EXCLUDE):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                continue
            for number, line in enumerate(content.splitlines(), 1):
                if len(line) > 2000:
                    continue
                for category, pattern in PATTERNS:
                    if pattern.search(line) and (re.search(r"\\b(export|pub|function|async|class|const|fn)\\b", line) or "=>" in line):
                        records.append({"path": rel, "line": number, "category": category, "candidate": line.strip()[:240], "verified_entrypoint": False})
    return records

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--output", default="formal-verification/inventory/candidates.json")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()
    commit = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    tree = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], text=True).strip()
    records = inventory(root)
    obj = {"schema": 1, "source_commit": commit, "source_tree": tree, "method": "heuristic regex candidates; requires manual reachability confirmation", "count": len(records), "candidates": records}
    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{len(records)} candidates written to {out}")

if __name__ == "__main__":
    main()
