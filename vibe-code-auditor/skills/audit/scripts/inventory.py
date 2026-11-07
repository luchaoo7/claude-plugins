#!/usr/bin/env python3
"""Static inventory of a codebase. Reads files only; never executes project code.

Usage: inventory.py <project_root> [--json out.json] [--top 15]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

EXCLUDE_DIRS = {
    ".git", "node_modules", "dist", "build", "out", "target", ".next", ".nuxt",
    "__pycache__", ".venv", "venv", "env", ".tox", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".gradle", ".idea", ".vscode", "coverage", ".turbo", ".cache",
    "vendor", "bower_components", ".svelte-kit", "vibe-audit", ".terraform",
}

LANG_BY_EXT = {
    ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin", ".scala": "Scala", ".groovy": "Groovy",
    ".ts": "TypeScript", ".tsx": "TypeScript (TSX)", ".js": "JavaScript", ".jsx": "JavaScript (JSX)",
    ".mjs": "JavaScript", ".cjs": "JavaScript", ".vue": "Vue", ".svelte": "Svelte",
    ".py": "Python", ".rb": "Ruby", ".php": "PHP", ".go": "Go", ".rs": "Rust",
    ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C", ".h": "C/C++ header", ".swift": "Swift",
    ".dart": "Dart", ".sql": "SQL", ".sh": "Shell", ".html": "HTML", ".css": "CSS",
    ".scss": "SCSS", ".yml": "YAML", ".yaml": "YAML", ".json": "JSON", ".xml": "XML",
    ".md": "Markdown", ".tf": "Terraform",
}
CODE_LANGS = {
    "Java", "Kotlin", "Scala", "Groovy", "TypeScript", "TypeScript (TSX)", "JavaScript",
    "JavaScript (JSX)", "Vue", "Svelte", "Python", "Ruby", "PHP", "Go", "Rust", "C#", "C++",
    "C", "C/C++ header", "Swift", "Dart", "SQL", "Shell",
}
MANIFESTS = [
    "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "tsconfig.json",
    "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "pyproject.toml",
    "requirements.txt", "Pipfile", "poetry.lock", "setup.py", "manage.py", "go.mod",
    "Cargo.toml", "composer.json", "Gemfile", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml", ".env", ".env.example", "next.config.js", "next.config.mjs",
    "next.config.ts", "vite.config.ts", "vite.config.js", "angular.json", "nest-cli.json",
    ".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", "application.yml",
    "application.properties",
]
FRAMEWORK_HINTS = [
    ("Spring Boot", re.compile(r"spring-boot|org\.springframework\.boot")),
    ("React", re.compile(r'"react"\s*:')),
    ("Next.js", re.compile(r'"next"\s*:')),
    ("Vue", re.compile(r'"vue"\s*:')),
    ("Angular", re.compile(r'"@angular/core"\s*:')),
    ("Svelte", re.compile(r'"svelte"\s*:')),
    ("Express", re.compile(r'"express"\s*:')),
    ("NestJS", re.compile(r'"@nestjs/core"\s*:')),
    ("Prisma", re.compile(r'"prisma"\s*:|"@prisma/client"\s*:')),
    ("Django", re.compile(r"(?i)\bdjango\b")),
    ("FastAPI", re.compile(r"(?i)\bfastapi\b")),
    ("Flask", re.compile(r"(?i)\bflask\b")),
    ("SQLAlchemy", re.compile(r"(?i)\bsqlalchemy\b")),
    ("Hibernate/JPA", re.compile(r"hibernate|spring-boot-starter-data-jpa|jakarta\.persistence")),
]
TEST_PAT = re.compile(r"(^|/)(tests?|__tests__|spec|src/test)(/|$)|(\.|_)(test|spec)\.[a-z]+$|^test_.*\.py$|Test\.java$|Tests?\.kt$")
MARKER_PAT = re.compile(r"\b(TODO|FIXME|HACK|XXX)\b")
GENERATED_PAT = re.compile(r"(\.min\.(js|css)$)|(\.generated\.)|(_pb2\.py$)|(\.d\.ts$)")


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".") or d == ".github"]
        for f in filenames:
            yield os.path.join(dirpath, f)


def count_lines(path):
    try:
        with open(path, "rb") as fh:
            data = fh.read(5_000_000)
        if b"\0" in data[:8192]:
            return None, 0
        text = data.decode("utf-8", errors="replace")
        lines = text.splitlines()
        nonblank = sum(1 for l in lines if l.strip())
        return nonblank, len(MARKER_PAT.findall(text))
    except OSError:
        return None, 0


def git_churn(root, top):
    if not os.path.isdir(os.path.join(root, ".git")):
        return None
    try:
        out = subprocess.run(
            ["git", "-C", root, "log", "--since=12 months ago", "--name-only", "--pretty=format:"],
            capture_output=True, text=True, timeout=60,
        ).stdout
    except Exception:
        return None
    c = Counter(l.strip() for l in out.splitlines() if l.strip())
    return [{"file": f, "commits": n} for f, n in c.most_common(top)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--json")
    ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        sys.exit(f"Not a directory: {root}")

    by_lang = defaultdict(lambda: {"files": 0, "loc": 0})
    sizes, generated = [], []
    test_loc = src_loc = markers = 0
    marker_files = Counter()
    for p in walk(root):
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        ext = os.path.splitext(p)[1].lower()
        lang = LANG_BY_EXT.get(ext)
        if not lang:
            continue
        loc, m = count_lines(p)
        if loc is None:
            continue
        if GENERATED_PAT.search(rel):
            generated.append(rel)
            continue
        by_lang[lang]["files"] += 1
        by_lang[lang]["loc"] += loc
        if lang in CODE_LANGS:
            sizes.append((loc, rel))
            if TEST_PAT.search(rel):
                test_loc += loc
            else:
                src_loc += loc
            if m:
                markers += m
                marker_files[rel] += m

    manifests = [m for m in MANIFESTS if os.path.exists(os.path.join(root, m))]
    # nested manifests (monorepos)
    nested = []
    for p in walk(root):
        b = os.path.basename(p)
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        if b in ("package.json", "pom.xml", "build.gradle", "build.gradle.kts", "pyproject.toml", "requirements.txt") and "/" in rel:
            nested.append(rel)

    frameworks = set()
    for m in [*manifests, *nested]:
        mp = os.path.join(root, m)
        if os.path.isfile(mp):
            try:
                txt = open(mp, encoding="utf-8", errors="replace").read(400_000)
            except OSError:
                continue
            for name, pat in FRAMEWORK_HINTS:
                if pat.search(txt):
                    frameworks.add(name)

    sizes.sort(reverse=True)
    code_loc = sum(v["loc"] for k, v in by_lang.items() if k in CODE_LANGS)
    result = {
        "root": root,
        "code_loc": code_loc,
        "code_files": sum(v["files"] for k, v in by_lang.items() if k in CODE_LANGS),
        "languages": dict(sorted(by_lang.items(), key=lambda kv: -kv[1]["loc"])),
        "frameworks_detected": sorted(frameworks),
        "manifests": manifests,
        "nested_manifests": sorted(nested)[:50],
        "largest_files": [{"file": f, "loc": n} for n, f in sizes[: a.top]],
        "files_over_400_loc": sum(1 for n, _ in sizes if n > 400),
        "files_over_800_loc": sum(1 for n, _ in sizes if n > 800),
        "test_loc": test_loc,
        "source_loc": src_loc,
        "test_to_source_ratio": round(test_loc / src_loc, 2) if src_loc else None,
        "todo_fixme_total": markers,
        "todo_fixme_top_files": [{"file": f, "count": n} for f, n in marker_files.most_common(10)],
        "generated_or_minified_skipped": len(generated),
        "git_churn_12m": git_churn(root, a.top),
        "env_file_present": os.path.exists(os.path.join(root, ".env")),
    }

    if a.json:
        os.makedirs(os.path.dirname(os.path.abspath(a.json)), exist_ok=True)
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)

    print(f"Project: {root}")
    print(f"Code: {result['code_loc']:,} non-blank LOC in {result['code_files']:,} files")
    print("Languages:")
    for k, v in result["languages"].items():
        print(f"  {k:<20} {v['files']:>6} files {v['loc']:>9,} LOC")
    print("Frameworks detected:", ", ".join(result["frameworks_detected"]) or "none")
    print("Manifests:", ", ".join(manifests) or "none")
    if nested:
        print(f"Nested manifests ({len(nested)}):", ", ".join(sorted(nested)[:10]))
    print(f"Files >400 LOC: {result['files_over_400_loc']}, >800 LOC: {result['files_over_800_loc']}")
    print("Largest files:")
    for x in result["largest_files"]:
        print(f"  {x['loc']:>6}  {x['file']}")
    print(f"Test/source LOC ratio: {result['test_to_source_ratio']}")
    print(f"TODO/FIXME/HACK markers: {markers}")
    if result["env_file_present"]:
        print("WARNING: .env file present at project root — check whether it is committed.")
    if result["git_churn_12m"]:
        print("Most-changed files (12 months):")
        for x in result["git_churn_12m"]:
            print(f"  {x['commits']:>4}  {x['file']}")


if __name__ == "__main__":
    main()
