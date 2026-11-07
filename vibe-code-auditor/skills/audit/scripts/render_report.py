#!/usr/bin/env python3
"""Render vibe-audit findings.json into a self-contained, printable HTML report.

Usage: render_report.py <findings.json> <out.html>
"""
import html
import json
import os
import sys
from collections import Counter, defaultdict

SEV_ORDER = ["critical", "high", "medium", "low", "info"]
SEV_W = {"critical": 10, "high": 7, "medium": 4, "low": 2, "info": 0}
CONF_W = {"high": 1.0, "medium": 0.7, "low": 0.4}
EFF_W = {"S": 1, "M": 2, "L": 3}
PHASES = [("immediate", "Immediate (critical)"), ("quick-win", "Quick wins"),
          ("short-term", "Short term"), ("strategic", "Strategic")]
CATEGORY_LABEL = {
    "security": "Security", "architecture": "Architecture", "design-pattern": "Design patterns",
    "duplication": "Duplication", "dead-code": "Dead code", "bloat": "Bloat",
    "complexity": "Complexity", "maintainability": "Maintainability", "testing": "Testing",
    "performance": "Performance",
}

e = lambda s: html.escape("" if s is None else str(s))


def priority(f):
    if isinstance(f.get("priority"), (int, float)):
        return float(f["priority"])
    return round(SEV_W.get(f.get("severity"), 0) * CONF_W.get(f.get("confidence"), 0.7)
                 / EFF_W.get(f.get("effort"), 2), 1)


def phase_of(f):
    if f.get("severity") == "critical":
        return "immediate"
    if f.get("phase") in {"quick-win", "short-term", "strategic"}:
        return f["phase"]
    return {"S": "quick-win", "M": "short-term", "L": "strategic"}.get(f.get("effort"), "short-term")


def loc_str(loc):
    if not loc:
        return ""
    s = loc.get("file", "")
    if loc.get("start_line"):
        s += f":{loc['start_line']}"
        if loc.get("end_line") and loc["end_line"] != loc["start_line"]:
            s += f"-{loc['end_line']}"
    return s


CSS = """
:root{--ink:#1d2433;--muted:#5b6475;--line:#e3e6ec;--bg:#f7f8fa;--accent:#2f5bea;
--critical:#b42318;--high:#d9480f;--medium:#b7791f;--low:#2b6cb0;--info:#5b6475}
*{box-sizing:border-box}body{font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);margin:0;background:#fff}
.wrap{max-width:1000px;margin:0 auto;padding:48px 32px}
h1{font-size:30px;margin:0 0 6px}h2{font-size:21px;margin:44px 0 14px;padding-bottom:6px;border-bottom:2px solid var(--line)}
h3{font-size:17px;margin:0 0 8px}.muted{color:var(--muted)}
.cover{border-left:6px solid var(--accent);padding:6px 0 6px 20px;margin-bottom:28px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px}
.card{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:14px}
.num{font-size:28px;font-weight:700}.lbl{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--bg);font-weight:600}
.sev{display:inline-block;font-size:11px;font-weight:700;text-transform:uppercase;padding:2px 8px;border-radius:999px;color:#fff}
.sev.critical{background:var(--critical)}.sev.high{background:var(--high)}.sev.medium{background:var(--medium)}.sev.low{background:var(--low)}.sev.info{background:var(--info)}
.grade{display:inline-block;width:30px;height:30px;line-height:30px;text-align:center;border-radius:6px;font-weight:700;color:#fff}
.gA{background:#2f855a}.gB{background:#68a33a}.gC{background:#b7791f}.gD{background:#d9480f}.gE{background:#b42318}
.finding{border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:16px 0;page-break-inside:avoid}
.meta{font-size:13px;color:var(--muted);margin-bottom:10px}.meta b{color:var(--ink)}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12.5px}
pre{background:#0f172a;color:#e2e8f0;padding:12px 14px;border-radius:8px;overflow:auto;white-space:pre;margin:6px 0 0}
.ba{display:grid;grid-template-columns:minmax(0,1fr);gap:10px;margin-top:12px}.ba>div{min-width:0}.ba .lbl{margin-bottom:2px}
.before .lbl{color:var(--critical)}.after .lbl{color:#2f855a}
.loc{font-family:ui-monospace,monospace;font-size:13px;background:var(--bg);padding:1px 6px;border-radius:4px}
ul.road{padding-left:18px}ul.road li{margin:4px 0}
@media (max-width:760px){.ba{grid-template-columns:1fr}}
@media print{.wrap{padding:0}h2{page-break-after:avoid}pre{white-space:pre-wrap;word-break:break-word}a{color:inherit}}
"""


def render(data):
    meta = data.get("meta", {})
    findings = sorted(data.get("findings", []),
                      key=lambda f: (-priority(f), SEV_ORDER.index(f.get("severity", "info")) if f.get("severity") in SEV_ORDER else 9))
    sev_count = Counter(f.get("severity", "info") for f in findings)
    out = []
    w = out.append
    title = meta.get("project") or "Codebase"
    w(f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
      f"<title>Code Audit Report — {e(title)}</title><style>{CSS}</style></head><body><div class='wrap'>")
    sub = " · ".join(x for x in [
        f"Prepared for {e(meta['client'])}" if meta.get("client") else "",
        f"by {e(meta['consultant'])}" if meta.get("consultant") else "",
        e(meta.get("date", "")), f"Depth: {e(meta['depth'])}" if meta.get("depth") else ""] if x)
    w(f"<div class='cover'><div class='lbl'>Code audit report</div><h1>{e(title)}</h1><div class='muted'>{sub}</div></div>")

    w("<h2>Executive summary</h2>")
    if meta.get("executive_summary"):
        w(f"<p>{e(meta['executive_summary'])}</p>")
    w("<div class='grid'>")
    for s in SEV_ORDER:
        w(f"<div class='card'><div class='num'>{sev_count.get(s, 0)}</div><div class='lbl'><span class='sev {s}'>{s}</span></div></div>")
    w("</div>")

    w("<h2>Scope</h2><table>")
    for k, label in [("scope", "Scope"), ("stacks", "Stacks"), ("loc", "Lines of code"), ("files", "Files")]:
        v = meta.get(k)
        if v:
            v = ", ".join(v) if isinstance(v, list) else (f"{v:,}" if isinstance(v, int) else v)
            w(f"<tr><th style='width:180px'>{label}</th><td>{e(v)}</td></tr>")
    w("</table>")

    if meta.get("scorecard"):
        w("<h2>Health scorecard</h2><table><tr><th>Area</th><th>Grade</th></tr>")
        for area, g in meta["scorecard"].items():
            g = str(g).strip().upper()[:1]
            w(f"<tr><td>{e(area)}</td><td><span class='grade g{e(g)}'>{e(g)}</span></td></tr>")
        w("</table><p class='muted' style='font-size:13px'>A = no medium+ issues · E = multiple critical issues.</p>")

    # severity x category matrix
    cats = sorted({f.get("category", "other") for f in findings}, key=lambda c: list(CATEGORY_LABEL).index(c) if c in CATEGORY_LABEL else 99)
    if findings:
        w("<h2>Findings by category</h2><table><tr><th>Category</th>" + "".join(f"<th>{s.title()}</th>" for s in SEV_ORDER) + "<th>Total</th></tr>")
        for c in cats:
            row = [f for f in findings if f.get("category", "other") == c]
            cc = Counter(f.get("severity") for f in row)
            w(f"<tr><td>{e(CATEGORY_LABEL.get(c, c))}</td>" + "".join(f"<td>{cc.get(s, 0) or ''}</td>" for s in SEV_ORDER) + f"<td><b>{len(row)}</b></td></tr>")
        w("</table>")

        w("<h2>Top priorities</h2><table><tr><th>ID</th><th>Finding</th><th>Severity</th><th>Effort</th><th>Location</th></tr>")
        for f in findings[:10]:
            w(f"<tr><td><a href='#{e(f.get('id'))}'>{e(f.get('id'))}</a></td><td>{e(f.get('title'))}</td>"
              f"<td><span class='sev {e(f.get('severity'))}'>{e(f.get('severity'))}</span></td><td>{e(f.get('effort'))}</td>"
              f"<td><span class='loc'>{e(loc_str(f.get('location')))}</span></td></tr>")
        w("</table>")

    if meta.get("architecture_summary"):
        w(f"<h2>Architecture assessment</h2><p>{e(meta['architecture_summary'])}</p>")

    if meta.get("themes"):
        w("<h2>Refactoring themes</h2>")
        for t in meta["themes"]:
            ids = ", ".join(f"<a href='#{e(i)}'>{e(i)}</a>" for i in t.get("finding_ids", []))
            w(f"<div class='card' style='margin:10px 0'><h3>{e(t.get('title'))}</h3><div>{e(t.get('summary'))}</div>"
              f"<div class='muted' style='font-size:13px;margin-top:6px'>Findings: {ids}</div></div>")

    w("<h2>Remediation roadmap</h2>")
    by_phase = defaultdict(list)
    for f in findings:
        if f.get("severity") != "info" and f.get("status") not in ("declined", "wont-fix"):
            by_phase[phase_of(f)].append(f)
    for key, label in PHASES:
        if by_phase.get(key):
            w(f"<h3>{label}</h3><ul class='road'>")
            for f in by_phase[key]:
                w(f"<li><a href='#{e(f.get('id'))}'>{e(f.get('id'))}</a> — {e(f.get('recommendation') or f.get('title'))} "
                  f"<span class='muted'>(effort {e(f.get('effort', '?'))})</span></li>")
            w("</ul>")

    w("<h2>Detailed findings</h2>")
    for c in cats:
        group = [f for f in findings if f.get("category", "other") == c]
        w(f"<h3 style='margin-top:28px'>{e(CATEGORY_LABEL.get(c, c))}</h3>")
        for f in group:
            tags = [f"<b>Severity:</b> <span class='sev {e(f.get('severity'))}'>{e(f.get('severity'))}</span>",
                    f"<b>Confidence:</b> {e(f.get('confidence', '—'))}", f"<b>Effort:</b> {e(f.get('effort', '—'))}"]
            if f.get("cwe"):
                tags.append(f"<b>CWE:</b> {e(f['cwe'])}")
            if f.get("owasp"):
                tags.append(f"<b>OWASP:</b> {e(f['owasp'])}")
            if f.get("status") and f["status"] != "open":
                tags.append(f"<b>Status:</b> {e(f['status'])}")
            w(f"<div class='finding' id='{e(f.get('id'))}'><h3>{e(f.get('id'))} · {e(f.get('title'))}</h3>"
              f"<div class='meta'>{' · '.join(tags)}</div>")
            locs = [f.get("location")] + list(f.get("additional_locations") or [])
            locs = [l for l in locs if l]
            if locs:
                sym = f" (<code>{e(f['location'].get('symbol'))}</code>)" if f.get("location", {}).get("symbol") else ""
                w("<div class='meta'><b>Location:</b> " + ", ".join(f"<span class='loc'>{e(loc_str(l))}</span>" for l in locs) + sym + "</div>")
            for k, label in [("description", "What"), ("why_it_matters", "Why it matters"), ("recommendation", "Recommendation")]:
                if f.get(k):
                    w(f"<p><b>{label}:</b> {e(f[k])}</p>")
            if f.get("before") or f.get("after"):
                w("<div class='ba'>")
                if f.get("before"):
                    w(f"<div class='before'><div class='lbl'>Before</div><pre><code>{e(f['before'])}</code></pre></div>")
                if f.get("after"):
                    w(f"<div class='after'><div class='lbl'>After</div><pre><code>{e(f['after'])}</code></pre></div>")
                w("</div>")
            if f.get("references"):
                w("<p class='muted' style='font-size:13px'>References: " + ", ".join(
                    f"<a href='{e(r)}'>{e(r)}</a>" if str(r).startswith("http") else e(r) for r in f["references"]) + "</p>")
            w("</div>")

    if meta.get("limitations"):
        w("<h2>Limitations</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in meta["limitations"]) + "</ul>")
    w("<p class='muted' style='margin-top:48px;font-size:12px'>Generated with vibe-code-auditor.</p></div></body></html>")
    return "".join(out)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as fh:
        data = json.load(fh)
    html_out = render(data)
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[2])), exist_ok=True)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(html_out)
    print(f"Wrote {sys.argv[2]} ({len(data.get('findings', []))} findings)")


if __name__ == "__main__":
    main()
