#!/usr/bin/env python3
"""Builds the guides: /guides/ (index) and /guides/<slug>.

Run from the repo root after editing a guide below:

    python3 tools/build_guides.py

Guide bodies are simple HTML. Write {{LHR}} to link an airport code to its page.
Only add facts you are sure of.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_airports import FOOT, HEAD, ROOT, TODAY, e, load_airports, schema_block  # noqa: E402

OUT = ROOT / "guides"

GUIDES = [
    {
        "slug": "why-canadian-airports-start-with-y",
        "code": "YYZ",
        "title": "Why do Canadian airports start with Y?",
        "blurb": "Toronto is YYZ, Vancouver is YVR, Montréal is YUL. Here's why nearly every big Canadian airport begins with a Y.",
        "body": """
<p>Look at a Canadian boarding pass and you'll almost always see a Y. Toronto Pearson is {{YYZ}}, Vancouver is {{YVR}}, Montréal is {{YUL}}, Calgary is {{YYC}} and Ottawa is {{YOW}}. Edmonton ({{YEG}}), Winnipeg ({{YWG}}), Halifax ({{YHZ}}), Québec City ({{YQB}}) and Victoria ({{YYJ}}) follow the same rule.</p>
<h2>Where the Y came from</h2>
<p>The usual explanation goes back to the early days of radio. Canada gave its weather and radio stations two-letter identifiers. When three-letter airport codes became the standard, Canada added a Y in front of the old two letters, and the habit stuck. Historians differ on some of the details, but the result is clear: Y now means Canada almost everywhere you look.</p>
<h2>Why the letters after the Y look random</h2>
<p>Because the last two letters came from those old station identifiers, many don't match the city's name at all. That's why Toronto is YYZ and not something like YTO. (YTO does exist, but as a city code covering all of Toronto's airports.)</p>
<h2>A code with a fan club</h2>
<p>YYZ might be the most famous airport code in music. The Canadian rock band Rush named an instrumental track "YYZ" in 1981, and its opening rhythm spells the letters out in Morse code.</p>
<h2>How to remember them</h2>
<ul>
<li>Ignore the Y and look at the last two letters: YV<b>R</b>, Vancouver; YO<b>W</b>, Ottawa; YQ<b>B</b>, Québec.</li>
<li>Toronto, Calgary and Edmonton are the odd ones out, so learn YYZ, YYC and YEG by heart.</li>
</ul>
""",
    },
    {
        "slug": "airport-codes-from-old-names",
        "code": "ORD",
        "title": "Airport codes that remember an old name",
        "blurb": "ORD for O'Hare, MCO for Orlando, BOM for Mumbai. These codes kept the name the airport or city had before.",
        "body": """
<p>Airport codes rarely change, even when an airport or city gets a new name. So some codes are little history lessons. Here are the best-known ones.</p>
<h2>Chicago O'Hare: {{ORD}}</h2>
<p>O'Hare started life as Orchard Field. It was renamed after the naval aviator Butch O'Hare in 1949, but the code ORD, from ORcharD, stayed.</p>
<h2>Orlando: {{MCO}}</h2>
<p>Orlando's main airport was once McCoy Air Force Base. The base is long gone, but MCO lives on.</p>
<h2>New Orleans: {{MSY}}</h2>
<p>MSY comes from Moisant Stock Yards, the site of the original airfield, named after the aviator John Moisant.</p>
<h2>Cincinnati: {{CVG}}</h2>
<p>Cincinnati's airport is actually in Kentucky, near the town of Covington. Hence CVG.</p>
<h2>New York JFK: {{JFK}}</h2>
<p>This one did change. The airport opened as Idlewild, with the code IDL. When it was renamed after President John F. Kennedy in 1963, the code changed to JFK too.</p>
<h2>Cities that changed their names</h2>
<ul>
<li>{{PEK}}: Beijing, from Peking, the older English spelling.</li>
<li>{{BOM}}: Mumbai, from Bombay. The city was renamed in 1995.</li>
<li>{{MAA}}: Chennai, from Madras. The city was renamed in 1996.</li>
<li>{{SGN}}: Ho Chi Minh City, from Saigon, a name locals still use.</li>
<li>{{OPO}}: Porto, from Oporto, its traditional English name.</li>
</ul>
""",
    },
    {
        "slug": "london-airports-codes",
        "code": "LHR",
        "title": "London has six airports. Can you name their codes?",
        "blurb": "LHR, LGW, STN, LTN, LCY and SEN, plus the LON code that covers them all, and how not to mix them up.",
        "body": """
<p>London is served by six airports, and their codes are a classic quiz trap because most start with L. Here they are, with a way to remember each.</p>
<ul>
<li>{{LHR}} <b>Heathrow</b>: L for London, HR for Heathrow. The big one, in west London.</li>
<li>{{LGW}} <b>Gatwick</b>: L for London, GW for Gatwick. South of London, in West Sussex.</li>
<li>{{STN}} <b>Stansted</b>: the letters come straight from STaNsted. North-east of London, in Essex.</li>
<li>{{LTN}} <b>Luton</b>: LuToN. North of London, in Bedfordshire.</li>
<li>{{LCY}} <b>London City</b>: London CitY. The closest to central London, in the Docklands.</li>
<li>{{SEN}} <b>Southend</b>: SouthENd, out east in Essex.</li>
</ul>
<h2>What does LON mean?</h2>
<p>LON isn't an airport. It's a city code that covers all of London's airports, so booking sites can search them all at once. Other big cities have one too: NYC for New York, PAR for Paris and TYO for Tokyo.</p>
<h2>The usual mix-ups</h2>
<p>People most often confuse LGW and LHR, because both start with L and end with a consonant pair. Remember that Gatwick has the G. The other trap is LCY: the Y comes from the end of "City".</p>
""",
    },
    {
        "slug": "why-lax-has-an-x",
        "code": "LAX",
        "title": "Why does LAX have an X?",
        "blurb": "Los Angeles is LAX and Portland is PDX. The X doesn't stand for anything, and here's why it's there.",
        "body": """
<p>Los Angeles is {{LAX}} and Portland, Oregon is {{PDX}}. In both cases, the X doesn't stand for anything.</p>
<h2>From two letters to three</h2>
<p>In the early days of US aviation, many airports used two-letter codes, borrowed from the weather service. Los Angeles was LA and Portland was PD. When three-letter codes became the standard, some airports simply kept their old two letters and added an X to fill the gap.</p>
<h2>Does X mean anything else?</h2>
<p>Not by itself. Plenty of codes contain an X for other reasons, such as {{KIX}} for Osaka's Kansai International. If you're guessing, an X at the end of a US code is often a sign of this old two-letter history.</p>
<h2>Try it yourself</h2>
<p>Next time you see a code ending in X, check whether the first two letters make sense on their own. For LA and PD, they do.</p>
""",
    },
    {
        "slug": "iata-and-icao-codes",
        "code": "EGLL",
        "title": "Three letters or four? IATA and ICAO codes explained",
        "blurb": "Heathrow is LHR on your boarding pass but EGLL to a pilot. What's the difference, and what are city codes like LON?",
        "body": """
<p>Every big airport has two codes. The one you know from your boarding pass is the three-letter <b>IATA</b> code. Pilots and air traffic control use a four-letter <b>ICAO</b> code instead.</p>
<h2>IATA codes: three letters, for passengers</h2>
<p>IATA codes like {{LHR}}, {{JFK}} and {{CDG}} appear on tickets, boarding passes and bag tags. They're short and easy to read, but there are only so many three-letter combinations, which is why some codes look odd.</p>
<h2>ICAO codes: four letters, for pilots</h2>
<p>ICAO codes are organised by region. The first letter tells you roughly where in the world the airport is:</p>
<ul>
<li><b>K</b> for the contiguous United States: KJFK, KLAX.</li>
<li><b>C</b> for Canada: CYYZ for Toronto.</li>
<li><b>E</b> for northern Europe: EGLL for Heathrow, EGKK for Gatwick.</li>
<li><b>L</b> for southern Europe: LFPG for Paris Charles de Gaulle, LEMD for Madrid.</li>
<li><b>Y</b> for Australia: YSSY for Sydney.</li>
</ul>
<h2>City codes</h2>
<p>Some cities have a third kind of code that covers all their airports at once. LON covers London's six airports, NYC covers JFK, LaGuardia and Newark, PAR covers Paris and TYO covers Tokyo. Booking sites use them to show every flight to a city in one search.</p>
""",
    },
    {
        "slug": "codes-that-dodged-a-clash",
        "code": "EWR",
        "title": "Why Newark is EWR, and other codes that dodged a clash",
        "blurb": "Newark couldn't be NEW, Washington Dulles swapped its letters, and Osaka needed a new code. The stories behind the odd ones.",
        "body": """
<p>Some codes look strange because the obvious choice was already taken, or not allowed.</p>
<h2>Newark: {{EWR}}</h2>
<p>In the US, codes starting with N are reserved for the US Navy. So Newark couldn't be NEW. It took the next letters of its name instead: nEWaRk.</p>
<h2>Washington Dulles: {{IAD}}</h2>
<p>Dulles first used the code DIA. On handwritten tags that looked too much like {{DCA}}, Washington's other airport, so the letters were rearranged to IAD.</p>
<h2>Osaka Kansai: {{KIX}}</h2>
<p>When Kansai International opened, Osaka already had an airport, {{ITM}} (Itami). The new one became KIX, and Osaka's city code OSA covers both.</p>
<h2>Houston: {{IAH}}</h2>
<p>IAH stands for Intercontinental Airport of Houston, the airport's original name. Houston's older airport, Hobby, is {{HOU}}.</p>
""",
    },
]


def link_codes(html, codes):
    def repl(m):
        c = m.group(1)
        if c in codes:
            return f'<a class="code-inline" href="/airports/{c.lower()}">{c}</a>'
        return c
    return re.sub(r"\{\{([A-Z]{3})\}\}", repl, html)


def head(title, desc, path, schema):
    h = HEAD.format(title=e(title), desc=e(desc), path=path, schema=schema)
    return h.replace('href="/airports/" aria-current="page"', 'href="/airports/"')


def guide_page(g, codes):
    path = f"/guides/{g['slug']}"
    schema = schema_block({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": g["title"],
        "description": g["blurb"],
        "datePublished": TODAY,
        "author": {"@type": "Organization", "name": "Amateurgames1"},
        "publisher": {"@type": "Organization", "name": "Amateurgames1", "url": "https://amateurgames1.com/"},
        "mainEntityOfPage": "https://amateurgames1.com" + path,
    })
    others = [o for o in GUIDES if o["slug"] != g["slug"]][:3]
    more = "".join(
        f'<a class="guide-card" href="/guides/{o["slug"]}"><span class="guide-code">{o["code"]}</span>'
        f'<h3>{e(o["title"])}</h3><p>{e(o["blurb"])}</p></a>' for o in others)
    return (head(f"{g['title']} | Amateurgames1", g["blurb"], path, schema) + f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <nav class="ap-crumbs" aria-label="Breadcrumb"><a href="/guides/">Guides</a> / {e(g['code'])}</nav>
        <h1 class="guide-title">{e(g['title'])}</h1>
        <p class="lead">{e(g['blurb'])}</p>
      </div>
    </section>
    <article class="wrap prose guide-body">
{link_codes(g['body'], codes)}
      <div class="panel guide-cta">
        <h2>Test yourself</h2>
        <p>Play today's <a href="/daily">Daily Departure</a>, or a round of <a href="/play">Quick Play</a>. Want all 1,000 codes? Get <a href="/airport-codes-quiz">Airport Codes Quiz</a>, free on iPhone.</p>
      </div>
    </article>
    <section class="wrap guide-more" aria-labelledby="more-title">
      <h2 id="more-title">More guides</h2>
      <div class="guide-cards">{more}</div>
    </section>
  </main>
""" + FOOT.format(scripts=""))


def index_page():
    schema = schema_block({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Airport code guides",
        "url": "https://amateurgames1.com/guides/",
    })
    cards = "".join(
        f'<a class="guide-card" href="/guides/{g["slug"]}"><span class="guide-code">{g["code"]}</span>'
        f'<h3>{e(g["title"])}</h3><p>{e(g["blurb"])}</p></a>' for g in GUIDES)
    return (head("Airport code guides: the stories behind the codes | Amateurgames1",
                 "Why Canadian airports start with Y, why LAX has an X, London's six airports and more. Short guides to airport codes.",
                 "/guides/", schema) + f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <p class="eyebrow">Guides</p>
        <h1 class="guide-title">The stories behind the codes</h1>
        <p class="lead">Short reads on why airport codes are the way they are, and how to remember them.</p>
      </div>
    </section>
    <div class="wrap guide-more">
      <div class="guide-cards">{cards}</div>
    </div>
  </main>
""" + FOOT.format(scripts=""))


def update_sitemap():
    path = ROOT / "sitemap.xml"
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"  <url><loc>https://amateurgames1\.com/guides/[^<]*</loc>[^\n]*\n", "", s)
    lines = [f"  <url><loc>https://amateurgames1.com/guides/</loc><lastmod>{TODAY}</lastmod></url>\n"]
    lines += [f"  <url><loc>https://amateurgames1.com/guides/{g['slug']}</loc><lastmod>{TODAY}</lastmod></url>\n" for g in GUIDES]
    s = s.replace("</urlset>", "".join(lines) + "</urlset>")
    path.write_text(s, encoding="utf-8")


def main():
    codes = {a["code"] for a in load_airports()}
    for g in GUIDES:
        for c in re.findall(r"\{\{([A-Z]{3})\}\}", g["body"]):
            assert c in codes, f"{g['slug']}: {c} has no airport page"
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    for g in GUIDES:
        (OUT / f"{g['slug']}.html").write_text(guide_page(g, codes), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(), encoding="utf-8")
    update_sitemap()
    print(f"Built {len(GUIDES)} guides and the guides index.")


if __name__ == "__main__":
    main()
