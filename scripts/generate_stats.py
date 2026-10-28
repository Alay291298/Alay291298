#!/usr/bin/env python3
"""
Generates the README telemetry cards into assets/generated/ using the GitHub GraphQL API.
Runs inside GitHub Actions (see .github/workflows/profile-telemetry.yml) — no third-party
image services are involved, so the cards can never show a "service unavailable" error.

Usage:
  GITHUB_TOKEN=... python scripts/generate_stats.py Alay291298
  python scripts/generate_stats.py Alay291298 --placeholder   # offline placeholder cards
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "generated")
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'DejaVu Sans Mono','Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,'Liberation Sans',sans-serif"
PALETTE = ["#39F1D1", "#71CFFF", "#B1A1FF", "#FFCF80", "#FF9E89", "#7FE3A0", "#FF7AB6", "#8FC7DF"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-telemetry"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def streaks(days):
    counts = [d["contributionCount"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur = 0
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today may not have activity yet
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    return cur, longest


def frame(w, h, title, right):
    return f'''<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" fill="#0A1728" stroke="#39F1D1" stroke-opacity="0.3"/>
<g fill="none" stroke="#39F1D1" stroke-width="2" stroke-opacity="0.8"><path d="M12 32V12H32"/><path d="M{w-32} 12H{w-12}V32"/><path d="M{w-12} {h-32}V{h-12}H{w-32}"/><path d="M32 {h-12}H12V{h-32}"/></g>
<text x="30" y="40" fill="#7FA3BF" font-family="{MONO}" font-size="12" letter-spacing="4">{escape(title)}</text>
<text x="{w-30}" y="40" fill="#39F1D1" font-family="{MONO}" font-size="11" letter-spacing="2" text-anchor="end"><tspan class="b">●</tspan> {escape(right)}</text>'''


STYLE = """<style>.b{animation:b 1.6s ease-in-out infinite}@keyframes b{0%,100%{opacity:.3}50%{opacity:1}}
.pt{animation:pt 2.4s ease-in-out infinite}@keyframes pt{0%,100%{opacity:.55}50%{opacity:1}}</style>"""


def stats_card(m, stamp):
    w, h = 600, 230
    items = [
        ("CONTRIBUTIONS · 1Y", m["total"], "#39F1D1"), ("COMMITS · 1Y", m["commits"], "#71CFFF"),
        ("PULL REQUESTS", m["prs"], "#B1A1FF"), ("ISSUES", m["issues"], "#FFCF80"),
        ("PUBLIC REPOS", m["repos"], "#39F1D1"), ("STARS EARNED", m["stars"], "#71CFFF"),
        ("CURRENT STREAK", m["cur"], "#FF9E89"), ("LONGEST STREAK", m["long"], "#B1A1FF"),
    ]
    cells = []
    for i, (label, val, col) in enumerate(items):
        cx = 30 + (i % 4) * 138
        cy = 64 + (i // 4) * 74
        cells.append(f'''<g>
<rect x="{cx}" y="{cy}" width="128" height="64" rx="8" fill="#0B2236" stroke="{col}" stroke-opacity="0.35"/>
<text x="{cx+12}" y="{cy+34}" fill="{col}" font-family="{SANS}" font-size="24" font-weight="800">{escape(str(val))}</text>
<text x="{cx+12}" y="{cy+52}" fill="#7FA3BF" font-family="{MONO}" font-size="9" letter-spacing="1">{escape(label)}</text></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub statistics for Alaykumar Pandya">
<title>GitHub statistics</title>{STYLE}
{frame(w, h, "GITHUB.TELEMETRY", "LIVE")}
{''.join(cells)}
<text x="{w-30}" y="{h-14}" fill="#4F6E89" font-family="{MONO}" font-size="9" text-anchor="end">{escape(stamp)}</text>
</svg>'''


def langs_card(langs, stamp):
    w, h = 600, 230
    total = sum(v for _, v in langs) or 1
    top = langs[:6]
    bar, x = [], 30.0
    for i, (name, v) in enumerate(top):
        bw = 540 * v / total
        bar.append(f'<rect x="{x:.1f}" y="66" width="{max(bw,2):.1f}" height="10" fill="{PALETTE[i]}"/>')
        x += bw
    rows = []
    for i, (name, v) in enumerate(top):
        cx = 30 + (i % 2) * 280
        cy = 108 + (i // 2) * 34
        pct = f"{100*v/total:.1f}%" if langs else "—"
        rows.append(f'''<g><circle cx="{cx+6}" cy="{cy-4}" r="5" fill="{PALETTE[i]}"/>
<text x="{cx+20}" y="{cy}" fill="#D7E9F7" font-family="{MONO}" font-size="13" font-weight="700">{escape(name)}</text>
<text x="{cx+250}" y="{cy}" fill="#7FA3BF" font-family="{MONO}" font-size="12" text-anchor="end">{pct}</text></g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Top languages across public repositories">
<title>Top languages</title>{STYLE}
{frame(w, h, "LANGUAGE.MATRIX", "PUBLIC REPOS")}
<clipPath id="bc"><rect x="30" y="66" width="540" height="10" rx="5"/></clipPath>
<rect x="30" y="66" width="540" height="10" rx="5" fill="#13314D"/>
<g clip-path="url(#bc)"><g>{''.join(bar)}</g></g>
{''.join(rows)}
<text x="{w-30}" y="{h-14}" fill="#4F6E89" font-family="{MONO}" font-size="9" text-anchor="end">{escape(stamp)}</text>
</svg>'''


def activity_card(days, stamp):
    w, h = 1200, 260
    days = days[-60:]
    n = len(days)
    vals = [d["contributionCount"] for d in days] or [0]
    mx = max(max(vals), 4)
    x0, x1, y0, y1 = 60, 1160, 70, 210
    pts = []
    for i, v in enumerate(vals):
        x = x0 + (x1 - x0) * (i / max(n - 1, 1))
        y = y1 - (y1 - y0) * (v / mx)
        pts.append((x, y))
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    area = f"{line} L{pts[-1][0]:.1f} {y1} L{pts[0][0]:.1f} {y1} Z"
    grid = "".join(
        f'<line x1="{x0}" y1="{y1-(y1-y0)*k/4:.1f}" x2="{x1}" y2="{y1-(y1-y0)*k/4:.1f}" stroke="#39F1D1" stroke-opacity="0.08"/>'
        f'<text x="{x0-10}" y="{y1-(y1-y0)*k/4+4:.1f}" fill="#4F6E89" font-family="{MONO}" font-size="10" text-anchor="end">{round(mx*k/4)}</text>'
        for k in range(5))
    labels = ""
    if days:
        for i in range(0, n, 10):
            x = x0 + (x1 - x0) * (i / max(n - 1, 1))
            labels += f'<text x="{x:.1f}" y="{y1+20}" fill="#4F6E89" font-family="{MONO}" font-size="10" text-anchor="middle">{days[i]["date"][5:]}</text>'
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#A899FF" class="pt"/>' for x, y in pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="GitHub contribution activity over the last 60 days">
<title>Contribution activity — last 60 days</title>{STYLE}
<defs><linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#39F1D1" stop-opacity="0.35"/><stop offset="1" stop-color="#39F1D1" stop-opacity="0"/></linearGradient></defs>
{frame(w, h, "ACTIVITY.SIGNAL  //  LAST 60 DAYS", "CONTRIBUTIONS / DAY")}
{grid}
<path d="{area}" fill="url(#ar)"/>
<path d="{line}" fill="none" stroke="#39F1D1" stroke-width="2.4" stroke-linejoin="round"/>
{dots}
{labels}
<text x="{w-30}" y="{h-12}" fill="#4F6E89" font-family="{MONO}" font-size="9" text-anchor="end">{escape(stamp)}</text>
</svg>'''


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "Alay291298"
    placeholder = "--placeholder" in sys.argv
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("PROFILE_TOKEN")
    os.makedirs(OUT, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if placeholder or not token:
        today = dt.date.today()
        days = [{"date": (today - dt.timedelta(days=59 - i)).isoformat(), "contributionCount": 0} for i in range(60)]
        m = {k: "—" for k in ("total", "commits", "prs", "issues", "repos", "stars", "cur", "long")}
        langs = [("SYNCING…", 1)]
        stamp = "awaiting first sync — refreshes automatically after push"
    else:
        u = fetch(login, token)
        cc = u["contributionsCollection"]
        days = [d for wk in cc["contributionCalendar"]["weeks"] for d in wk["contributionDays"]]
        cur, longest = streaks(days)
        repos = u["repositories"]["nodes"]
        agg = {}
        for r in repos:
            for e in r["languages"]["edges"]:
                agg[e["node"]["name"]] = agg.get(e["node"]["name"], 0) + e["size"]
        langs = sorted(agg.items(), key=lambda kv: -kv[1]) or [("—", 1)]
        m = {
            "total": cc["contributionCalendar"]["totalContributions"],
            "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
            "prs": u["pullRequests"]["totalCount"], "issues": u["issues"]["totalCount"],
            "repos": u["repositories"]["totalCount"],
            "stars": sum(r["stargazerCount"] for r in repos),
            "cur": f"{cur}d", "long": f"{longest}d",
        }
        stamp = f"updated {now}"

    for name, svg in (("stats.svg", stats_card(m, stamp)),
                      ("languages.svg", langs_card(langs, stamp)),
                      ("activity.svg", activity_card(days, stamp))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
    print("telemetry cards written to", os.path.normpath(OUT))


if __name__ == "__main__":
    main()
