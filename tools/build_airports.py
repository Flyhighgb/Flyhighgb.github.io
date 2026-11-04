#!/usr/bin/env python3
"""Builds the airport code pages: /airports/ (A-Z index) and /airports/<code>.

Run from the repo root after editing assets/daily-airports.js or the STORIES below:

    python3 tools/build_airports.py

It rewrites everything in airports/ and the airport entries in sitemap.xml.
Only standard-library Python is needed.
"""
import html
import json
import random
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "airports"
TODAY = "2026-11-04"

REGIONS = {
    "eu": "Europe",
    "am": "Americas",
    "ap": "Asia & Pacific",
    "me": "Middle East & Africa",
}

CANADA = ("Most big Canadian airports have codes starting with Y. The usual explanation "
          "is that Canada's codes grew out of older two-letter weather and radio station "
          "identifiers, with a Y added in front.")
X_FILLER = ("Airports once used two-letter codes. When three letters became the standard, "
            "some cities kept their old code and added an X: {old} became {code}.")

# The story behind a code, where there is one worth telling.
# Keep these to facts you are sure of. Codes with no story here get an automatic
# note only if the letters appear in order in the airport's name.
STORIES = {
    "LHR": "It's the simple kind: L for London, HR for Heathrow. London's other airports follow the same pattern where they can, which is why they're easy to mix up.",
    "LGW": "L for London, GW for Gatwick, the same pattern as Heathrow's LHR.",
    "ORD": "ORD comes from Orchard Field, the airfield's name before it was renamed after the naval aviator Butch O'Hare in 1949. The old code stuck.",
    "MCO": "MCO comes from McCoy Air Force Base, the military airfield that became Orlando's main airport.",
    "MSY": "MSY comes from Moisant Stock Yards, the site of the airport's original field, named after the aviator John Moisant.",
    "IAH": "IAH stands for Intercontinental Airport of Houston, the airport's original name.",
    "IAD": "Dulles was first coded DIA, but on handwritten tags that looked too much like DCA, Washington's other airport. The letters were rearranged to IAD.",
    "EWR": "US codes starting with N are reserved for the US Navy, so NEW wasn't an option. Newark's code takes the next letters of the name: nEWaRk.",
    "DCA": "DCA is usually read as District of Columbia Airport, after Washington's official district.",
    "LAX": X_FILLER.format(old="LA", code="LAX"),
    "PDX": X_FILLER.format(old="PD", code="PDX"),
    "YYZ": CANADA,
    "YVR": CANADA,
    "YUL": CANADA,
    "YYC": CANADA,
    "YOW": CANADA,
    "PEK": "PEK comes from Peking, the older English spelling of Beijing.",
    "BOM": "BOM comes from Bombay, Mumbai's name until 1995.",
    "MAA": "MAA comes from Madras, Chennai's name until 1996.",
    "SGN": "SGN comes from Saigon, the city's name before it became Ho Chi Minh City. Locals still use the old name.",
    "CGK": "CGK comes from Cengkareng, the district west of Jakarta where the airport sits.",
    "DPS": "DPS comes from Denpasar, Bali's capital, near the airport.",
    "KIX": "KIX is Kansai International with an X on the end. Osaka's city code, OSA, covers both Kansai and Itami airports.",
    "OPO": "OPO comes from Oporto, the traditional English name for Porto.",
}

FAQ_ROUTE = {
    "LON": ["LHR", "LGW", "STN", "LTN", "LCY"],
}


def load_airports():
    src = (ROOT / "assets" / "daily-airports.js").read_text(encoding="utf-8")
    rows = re.findall(r'\["([A-Z]{3})",\s*"([^"]+)",\s*"([^"]+)",\s*"([a-z]{2})"\]', src)
    return [{"code": c, "name": n, "country": k, "region": r} for c, n, k, r in rows]


def plain(s):
    return "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch)).lower()


def letters_in_order(code, name):
    """True if the code's letters appear, in order, in the name."""
    rest = plain(name)
    for ch in code.lower():
        i = rest.find(ch)
        if i < 0:
            return False
        rest = rest[i + 1:]
    return True


def why(a):
    if a["code"] in STORIES:
        return STORIES[a["code"]]
    if letters_in_order(a["code"], a["name"]):
        spelled = ", ".join(a["code"][:-1]) + " and " + a["code"][-1]
        return f"The letters {spelled} all appear, in that order, in “{a['name']}”, which makes this one of the easier codes to remember."
    return None


def lookalikes(a, airports):
    """Codes people are likely to confuse with this one."""
    c = a["code"]
    out = []
    for b in airports:
        d = b["code"]
        if d == c:
            continue
        same_letters = sorted(d) == sorted(c)
        one_off = sum(x != y for x, y in zip(c, d)) == 1
        if same_letters or one_off or d[:2] == c[:2]:
            out.append(b)
    return out[:6]


THE = {"United States", "United Kingdom", "United Arab Emirates", "Netherlands", "Philippines", "Maldives"}


def in_country(c):
    """'in the United States', 'in France'."""
    return ("the " + c) if c in THE else c


def e(s):
    return html.escape(s, quote=True)


HEAD = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://amateurgames1.com{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Amateurgames1">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://amateurgames1.com{path}">
  <meta property="og:image" content="https://amateurgames1.com/assets/og-airport-codes.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <meta name="theme-color" content="#0b1b33">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=JetBrains+Mono:wght@700;800&amp;family=Space+Grotesk:wght@500;700&amp;display=swap">
  <link rel="stylesheet" href="/assets/style.css">
  <!-- Google AdSense (Auto ads are placed by AdSense once the site is approved) -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3238867925400297" crossorigin="anonymous"></script>
{schema}</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/">
        <span class="brand-name">amateurgames</span><span class="brand-gate">1</span>
      </a>
      <nav class="site-nav" aria-label="Main">
        <a class="nav-link nav-keep" href="/daily">Daily</a>
        <a class="nav-link nav-keep" href="/play">Play</a>
        <a class="nav-link" href="/airports/" aria-current="page">Airports</a>
        <a class="nav-link" href="/airport-codes-quiz">Airport Codes</a>
        <a class="nav-link" href="/index1">Airline Tails</a>
        <a class="nav-cta" href="/#apps">Get the apps</a>
      </nav>
    </div>
  </header>
"""

FOOT = """
  <footer class="site-footer">
    <div class="wrap">
      <p>&copy; 2026 Amateurgames1. Free games for aviation fans.</p>
      <nav aria-label="Footer">
        <a href="/airports/">Airports A&ndash;Z</a>
        <a href="/privacy">Privacy policy</a>
        <a href="/support">Support</a>
        <a href="mailto:hello@amateurgames1.com">hello@amateurgames1.com</a>
      </nav>
    </div>
  </footer>
{scripts}</body>
</html>
"""

APP_URL = "https://apps.apple.com/gb/app/airport-codes-quiz/id6748875659"


def schema_block(obj):
    return ('  <script type="application/ld+json">\n  '
            + json.dumps(obj, ensure_ascii=False, indent=2).replace("\n", "\n  ")
            + "\n  </script>\n")


def chip(b):
    return (f'<a class="code-chip" href="/airports/{b["code"].lower()}">'
            f'<b>{b["code"]}</b><span>{e(b["name"])}</span></a>')


def quiz(a, airports, rng):
    """Three questions: this code, then two codes it gets confused with or shares a region with."""
    same_region = [b for b in airports if b["region"] == a["region"] and b["code"] != a["code"]]
    others = lookalikes(a, airports) + [b for b in airports if b["country"] == a["country"] and b["code"] != a["code"]]
    seen, picks = set(), []
    for b in others + rng.sample(same_region, len(same_region)):
        if b["code"] not in seen:
            seen.add(b["code"])
            picks.append(b)
        if len(picks) == 2:
            break

    qs = []
    # Q1: code -> airport
    wrong = rng.sample(same_region, 3)
    opts = [a["name"]] + [b["name"] for b in wrong]
    rng.shuffle(opts)
    qs.append((f"What airport is {a['code']}?", opts, a["name"]))
    # Q2 and Q3: airport -> code
    for b in picks:
        pool = [x for x in airports if x["region"] == b["region"] and x["code"] != b["code"]]
        wrong = rng.sample(pool, 3)
        opts = [b["code"]] + [x["code"] for x in wrong]
        rng.shuffle(opts)
        qs.append((f"Which code is {b['name']}?", opts, b["code"]))

    out = ['<section class="ap-quiz" data-ap-quiz aria-labelledby="quiz-title">',
           '<h2 id="quiz-title">Quick check</h2>']
    for n, (q, opts, right) in enumerate(qs, 1):
        mono = " is-code" if right.isupper() and len(right) == 3 else ""
        out.append(f'<div class="ap-q"><p class="ap-q-ask"><span>{n}/3</span> {e(q)}</p><div class="ap-q-opts{mono}">')
        for o in opts:
            r = ' data-right' if o == right else ''
            out.append(f'<button type="button" class="quiz-option"{r}>{e(o)}</button>')
        out.append('</div><p class="ap-q-result" aria-live="polite"></p></div>')
    out.append('<p class="ap-quiz-score" aria-live="polite"></p></section>')
    return "\n".join(out)


def airport_page(a, airports):
    rng = random.Random(a["code"])
    code, name, country = a["code"], a["name"], a["country"]
    region = REGIONS[a["region"]]
    path = f"/airports/{code.lower()}"
    story = why(a)
    looks = lookalikes(a, airports)
    same_country = [b for b in airports if b["country"] == country and b["code"] != code]
    title = f"{code} airport code: {name}, {country} | Amateurgames1"
    desc = f"{code} is the IATA airport code for {name} in {in_country(country)}. Why it's {code}, the codes people confuse it with, and a quick quiz."

    faqs = [
        (f"What airport is {code}?", f"{code} is the IATA code for {name} in {in_country(country)}."),
        (f"What is the airport code for {name}?", f"The three-letter IATA code for {name} is {code}."),
    ]
    if code in FAQ_ROUTE["LON"]:
        faqs.append(("What does LON mean on a ticket?",
                     "LON is a city code that covers all of London's airports. Booking sites use it to search Heathrow (LHR), Gatwick (LGW), Stansted (STN), Luton (LTN) and London City (LCY) at once."))

    schema = schema_block({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in faqs],
    }) + schema_block({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Airports A–Z", "item": "https://amateurgames1.com/airports/"},
            {"@type": "ListItem", "position": 2, "name": f"{code}: {name}", "item": "https://amateurgames1.com" + path},
        ],
    })

    flaps = "".join(f'<span class="flap" aria-hidden="true">{ch}</span>' for ch in code)
    parts = [HEAD.format(title=e(title), desc=e(desc), path=path, schema=schema)]
    parts.append(f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <nav class="ap-crumbs" aria-label="Breadcrumb"><a href="/airports/">Airports A&ndash;Z</a> / <a href="/airports/#{a['region']}">{e(region)}</a> / {code}</nav>
        <div class="ap-hero-row">
          <div class="flaps ap-flaps" role="img" aria-label="{' '.join(code)}">{flaps}</div>
          <div class="ap-hero-copy">
            <h1>{code} is {e(name)}</h1>
            <p class="lead">An airport in {e(in_country(country))}. {code} is its three-letter IATA code, the one on your boarding pass and bag tag.</p>
          </div>
        </div>
      </div>
    </section>

    <div class="wrap ap-layout">
      <div class="ap-main">
        <dl class="ap-facts">
          <div><dt>IATA code</dt><dd>{code}</dd></div>
          <div><dt>Airport</dt><dd>{e(name)}</dd></div>
          <div><dt>Country</dt><dd>{e(country)}</dd></div>
          <div><dt>Region</dt><dd>{e(region)}</dd></div>
        </dl>
""")
    if story:
        parts.append(f"""
        <section class="panel ap-panel">
          <h2>Why is it {code}?</h2>
          <p>{e(story)}</p>
        </section>
""")
    if looks:
        parts.append(f"""
        <section class="panel ap-panel">
          <h2>Don't mix it up with</h2>
          <p>These codes look or sound close to {code}.</p>
          <div class="code-chips">{''.join(chip(b) for b in looks)}</div>
        </section>
""")
    if same_country:
        parts.append(f"""
        <section class="panel ap-panel">
          <h2>Other airports in {e(in_country(country))}</h2>
          <div class="code-chips">{''.join(chip(b) for b in same_country[:8])}</div>
        </section>
""")
    parts.append(quiz(a, airports, rng))
    parts.append('\n        <section class="ap-faq">\n          <h2>Common questions</h2>\n')
    for q, ans in faqs:
        parts.append(f"          <details><summary>{e(q)}</summary><p>{e(ans)}</p></details>\n")
    parts.append(f"""        </section>
      </div>

      <aside class="ap-side">
        <div class="panel ap-cta accent-sky">
          <p class="ap-cta-kicker">Free on iPhone</p>
          <h2>Know {code}? Try 999 more.</h2>
          <p>Airport Codes Quiz has 50-question rounds, high scores and a study mode.</p>
          <a class="ap-cta-btn" href="{APP_URL}">Get Airport Codes Quiz</a>
        </div>
        <div class="panel ap-cta">
          <h2>Play in your browser</h2>
          <p><a href="/daily">Daily Departure</a>: five codes a day, the same for everyone.</p>
          <p><a href="/play">Quick Play</a>: unlimited ten-question rounds by region.</p>
        </div>
      </aside>
    </div>
  </main>
""")
    parts.append(FOOT.format(scripts='  <script src="/assets/airport-quiz.js" defer></script>\n'))
    return "".join(parts)


def index_page(airports):
    title = "Airport codes A–Z: what airport is that code? | Amateurgames1"
    desc = f"Look up {len(airports)} major airport codes from LHR to JFK. Find the airport behind any three-letter IATA code, the story behind it and the codes people mix it up with."
    schema = schema_block({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Airport codes A–Z",
        "url": "https://amateurgames1.com/airports/",
    })
    parts = [HEAD.format(title=e(title), desc=e(desc), path="/airports/", schema=schema)]
    parts.append(f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <p class="eyebrow">Airports A&ndash;Z</p>
        <h1>What airport is that code?</h1>
        <p class="lead">{len(airports)} major airports, the story behind their codes, and the codes people mix them up with.</p>
        <form class="ap-search" role="search" action="#" onsubmit="return false">
          <label for="ap-filter">Search by code, airport or country</label>
          <input id="ap-filter" type="search" placeholder="e.g. ORD, Toronto or Japan" autocomplete="off">
        </form>
      </div>
    </section>
    <div class="wrap ap-index">
      <p class="ap-none" id="ap-none" hidden>No airports match that. Try a three-letter code or a city.</p>
""")
    for key, label in REGIONS.items():
        group = sorted([a for a in airports if a["region"] == key], key=lambda a: a["code"])
        parts.append(f'      <section class="ap-region" id="{key}">\n        <h2>{e(label)}</h2>\n        <ul class="ap-list">\n')
        for a in group:
            hay = e(f"{a['code']} {plain(a['name'])} {a['name']} {plain(a['country'])}".lower())
            parts.append(f'          <li data-search="{hay}"><a href="/airports/{a["code"].lower()}"><b>{a["code"]}</b><span>{e(a["name"])}<small>{e(a["country"])}</small></span></a></li>\n')
        parts.append("        </ul>\n      </section>\n")
    parts.append("""      <section class="prose ap-about">
        <h2>About airport codes</h2>
        <p>The three-letter codes on boarding passes and bag tags are IATA airport codes. Some spell out the name, like LHR for London Heathrow. Others come from an old name, like ORD for Chicago O'Hare, which was once Orchard Field. Each page explains the story where there is one.</p>
        <p>Want to test yourself? Try <a href="/daily">Daily Departure</a> or a round of <a href="/play">Quick Play</a>.</p>
      </section>
    </div>
  </main>
""")
    parts.append(FOOT.format(scripts='  <script src="/assets/airport-quiz.js" defer></script>\n'))
    return "".join(parts)


def update_sitemap(airports):
    path = ROOT / "sitemap.xml"
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"  <url><loc>https://amateurgames1\.com/airports/[^<]*</loc>[^\n]*\n", "", s)
    lines = [f"  <url><loc>https://amateurgames1.com/airports/</loc><lastmod>{TODAY}</lastmod></url>\n"]
    lines += [f"  <url><loc>https://amateurgames1.com/airports/{a['code'].lower()}</loc><lastmod>{TODAY}</lastmod></url>\n"
              for a in sorted(airports, key=lambda a: a["code"])]
    s = s.replace("</urlset>", "".join(lines) + "</urlset>")
    path.write_text(s, encoding="utf-8")


def main():
    airports = load_airports()
    codes = [a["code"] for a in airports]
    assert len(codes) == len(set(codes)), "duplicate airport code"
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    for a in airports:
        (OUT / f"{a['code'].lower()}.html").write_text(airport_page(a, airports), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(airports), encoding="utf-8")
    update_sitemap(airports)
    print(f"Built {len(airports)} airport pages and the A-Z index.")


if __name__ == "__main__":
    main()
