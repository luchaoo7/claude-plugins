#!/usr/bin/env python3
"""Detect duplicated code blocks using normalised sliding windows.

Reads files only; never executes project code. Results are leads to verify by reading.

Usage: find_duplicates.py <project_root> [--min-lines 8] [--json out.json] [--max 50]
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inventory import EXCLUDE_DIRS, GENERATED_PAT  # noqa: E402

CODE_EXT = {".java", ".kt", ".scala", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue",
            ".svelte", ".py", ".rb", ".php", ".go", ".rs", ".cs", ".cpp", ".cc", ".c", ".swift", ".dart"}
COMMENT_LINE = re.compile(r"^\s*(//|#|\*|/\*|\*/|<!--)")
TRIVIAL = re.compile(r"^[\s{}()\[\];,]*$|^\s*(import|from|package|using|#include|export \{)\b|^\s*(\}|\]|\))[;,]?\s*$")
STRING = re.compile(r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)")
NUMBER = re.compile(r"\b\d+(\.\d+)?\b")
IDENT = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
KEYWORDS = set("""if else for while do switch case break continue return function def class
new try catch finally except raise throw throws async await yield const let var public private
protected static final void int long boolean string null None True False true false this self
import from export default extends implements interface type enum lambda with as in of is not
and or elif pass super""".split())


def norm(line):
    s = STRING.sub("S", line.strip())
    s = NUMBER.sub("N", s)
    s = IDENT.sub(lambda m: m.group(0) if m.group(0) in KEYWORDS else "I", s)
    return re.sub(r"\s+", " ", s)


def files(root):
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in fns:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if os.path.splitext(f)[1].lower() in CODE_EXT and not GENERATED_PAT.search(rel):
                yield p, rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--min-lines", type=int, default=8)
    ap.add_argument("--json")
    ap.add_argument("--max", type=int, default=50)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    W = a.min_lines

    index = defaultdict(list)  # hash -> [(rel, start_line, end_line)]
    for p, rel in files(root):
        try:
            raw = open(p, encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            continue
        sig = [(i + 1, norm(l)) for i, l in enumerate(raw)
               if l.strip() and not COMMENT_LINE.match(l) and not TRIVIAL.match(l)]
        for k in range(len(sig) - W + 1):
            chunk = sig[k:k + W]
            h = hashlib.md5("\n".join(x[1] for x in chunk).encode()).hexdigest()
            index[h].append((rel, chunk[0][0], chunk[-1][0]))

    # Merge overlapping windows into regions per (file pair)
    pair_regions = defaultdict(list)
    for h, occ in index.items():
        uniq = []
        for o in occ:
            if not any(o[0] == u[0] and abs(o[1] - u[1]) < W for u in uniq):
                uniq.append(o)
        if len(uniq) < 2:
            continue
        key = tuple(sorted({(u[0]) for u in uniq})) if len({u[0] for u in uniq}) > 1 else (uniq[0][0], uniq[0][0])
        pair_regions[key].append(uniq)

    clusters = []
    for key, groups in pair_regions.items():
        groups.sort(key=lambda g: [x[1] for x in g])
        merged = []
        for g in groups:
            if merged and len(merged[-1]) == len(g) and all(
                m[0] == x[0] and x[1] <= m[2] + 1 for m, x in zip(merged[-1], g)
            ):
                merged[-1] = [(m[0], m[1], max(m[2], x[2])) for m, x in zip(merged[-1], g)]
            else:
                merged.append(list(g))
        for m in merged:
            length = max(x[2] - x[1] + 1 for x in m)
            clusters.append({
                "occurrences": [{"file": x[0], "start_line": x[1], "end_line": x[2]} for x in m],
                "approx_lines": length,
                "cross_file": len({x[0] for x in m}) > 1,
            })

    clusters.sort(key=lambda c: (-c["approx_lines"] * len(c["occurrences"])))
    clusters = clusters[: a.max]
    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        json.dump({"min_lines": W, "clusters": clusters}, open(a.json, "w"), indent=2)

    if not clusters:
        print(f"No duplicate blocks of >= {W} significant lines found.")
        return
    print(f"Top duplicate clusters (window {W} significant lines) — verify each by reading:")
    for i, c in enumerate(clusters, 1):
        tag = "cross-file" if c["cross_file"] else "same-file"
        print(f"\n#{i} ~{c['approx_lines']} lines x{len(c['occurrences'])} ({tag})")
        for o in c["occurrences"]:
            print(f"   {o['file']}:{o['start_line']}-{o['end_line']}")


if __name__ == "__main__":
    main()
