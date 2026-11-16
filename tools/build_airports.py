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
TODAY = "2026-11-16"

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
    "YEG": CANADA,
    "YWG": CANADA,
    "YHZ": CANADA,
    "YQB": CANADA,
    "YYJ": CANADA,
    "CVG": "CVG comes from Covington, Kentucky. Cincinnati's main airport is actually across the river from Ohio, in northern Kentucky.",
    "PEK": "PEK comes from Peking, the older English spelling of Beijing.",
    "BOM": "BOM comes from Bombay, Mumbai's name until 1995.",
    "MAA": "MAA comes from Madras, Chennai's name until 1996.",
    "SGN": "SGN comes from Saigon, the city's name before it became Ho Chi Minh City. Locals still use the old name.",
    "CGK": "CGK comes from Cengkareng, the district west of Jakarta where the airport sits.",
    "DPS": "DPS comes from Denpasar, Bali's capital, near the airport.",
    "KIX": "KIX is Kansai International with an X on the end. Osaka's city code, OSA, covers both Kansai and Itami airports.",
    "OPO": "OPO comes from Oporto, the traditional English name for Porto.",
    # Added 2026-11-16. Same rule: only facts we are sure of.
    "JFK": "The airport opened in 1948 as Idlewild, with the code IDL. When it was renamed after President John F. Kennedy in December 1963, the code changed to JFK to match.",
    "LGA": "LGA takes the first letters of LaGuardia. The airport is named after Fiorello La Guardia, New York's mayor from 1934 to 1945, who pushed for an airport inside the city.",
    "CDG": "CDG is the initials of Charles de Gaulle, the French wartime leader and president. The airport opened in 1974 and took over most long-haul flights from Orly (ORY).",
    "ORY": "Orly is Paris's older airport, south of the city. Paris's city code, PAR, lets booking sites search Orly and Charles de Gaulle (CDG) together.",
    "BVA": "Beauvais is sold as Paris Beauvais, but it sits next to the town of Beauvais, around 80 km north of Paris. It's used mainly by low-cost airlines.",
    "HND": "Haneda is Tokyo's older airport, on Tokyo Bay and close to the city. Tokyo's city code, TYO, covers both Haneda and Narita (NRT).",
    "NRT": "Narita opened in 1978, about 60 km east of central Tokyo. For years it handled almost all of Tokyo's international flights, while Haneda (HND) handled domestic ones.",
    "ITM": "Itami is Osaka's original airport, named after the city of Itami. Since Kansai (KIX) opened in 1994, it has mostly handled domestic flights.",
    "ICN": "ICN comes from Incheon, the city west of Seoul where the airport opened in 2001. It took over Seoul's international flights from Gimpo (GMP). The city code SEL covers both.",
    "GMP": "GMP comes from Gimpo. It was Seoul's main airport until Incheon (ICN) opened in 2001, and now handles mostly domestic and short regional flights.",
    "PVG": "PVG comes from Pudong, the district east of the Huangpu River where the airport opened in 1999. Shanghai's older airport, Hongqiao, kept the code SHA.",
    "SHA": "SHA is short for Shanghai. It belonged to the city's original airport, Hongqiao, which kept it when the much bigger Pudong (PVG) opened in 1999.",
    "PKX": "Daxing opened in 2019 as Beijing's second major airport. Its code, PKX, echoes PEK, the code of Beijing Capital, which comes from the old spelling Peking.",
    "HKG": "Hong Kong's code moved with the airport. When Chek Lap Kok opened in 1998, it replaced the old Kai Tak airport overnight and took over HKG.",
    "BKK": "Suvarnabhumi opened in 2006 and took the code BKK from Don Mueang, Bangkok's old airport. Don Mueang later reopened with a new code, DMK.",
    "DMK": "Don Mueang was Bangkok's airport, coded BKK, until Suvarnabhumi opened in 2006 and took that code. It reopened as DMK and is now a hub for low-cost airlines.",
    "TPE": "Taoyuan is about 40 km west of Taipei, in Taoyuan city, but carries Taipei's code. It was called Chiang Kai-shek International until 2006.",
    "TSA": "Songshan is the airport inside Taipei itself, close to the centre. Most long-haul flights use Taoyuan (TPE) instead.",
    "MUC": "MUC comes from München, the city's German name. The current airport opened in 1992, replacing the old Munich-Riem airport, and kept the code.",
    "WAW": "WAW comes from Warszawa, the Polish name for Warsaw. The airport is named after the composer Frédéric Chopin.",
    "PRG": "PRG comes from Praha, the Czech name for Prague. Since 2012 the airport has been named after Václav Havel, the playwright who became president.",
    "BEG": "BEG comes from Beograd, the Serbian name for Belgrade. The airport is named after the inventor Nikola Tesla.",
    "CGN": "CGN comes from Cologne, the English name for Köln. The airport serves both Cologne and Bonn.",
    "KEF": "Keflavík is near the town of Keflavík, about 50 km from Reykjavík. Almost all international flights to Iceland land here, while Reykjavík's small city airport handles domestic flights.",
    "OSL": "Oslo's main airport moved to Gardermoen, north of the city, in 1998 and took the code OSL. The old airport at Fornebu closed the same year.",
    "ARN": "ARN comes from ARlaNda, the area north of Stockholm where the airport was built.",
    "IST": "IST moved in 2019. The new Istanbul Airport took it from Atatürk Airport, the city's old main airport, which closed to passenger flights. Istanbul's other airport is Sabiha Gökçen (SAW).",
    "SAW": "SAW is Sabiha Gökçen, on Istanbul's Asian side. It's named after Sabiha Gökçen, often called the world's first female fighter pilot.",
    "DEN": "Denver International opened in 1995 and took over the code DEN from Stapleton, the city's old airport, which closed the same year.",
    "BWI": "BWI stands for Baltimore/Washington International. It's one of three airports serving Washington, with Dulles (IAD) and Reagan National (DCA). The city code WAS covers all three.",
    "DTW": "DTW comes from DeTroit Wayne. The airport's full name is Detroit Metropolitan Wayne County Airport, and it sits in Wayne County, outside the city.",
    "MCI": "MCI comes from Mid-Continent International, the airport's name when it opened. Kansas City's older downtown airport has the code MKC.",
    "BNA": "BNA comes from Berry Field, NAshville, the airport's original name.",
    "SNA": "SNA comes from Santa Ana, the nearby city. The airport has been named after the actor John Wayne since 1979.",
    "MDW": "Midway is named after the Battle of Midway, the 1942 naval battle. Called Chicago Municipal Airport until 1949, it was the city's busiest airport before O'Hare (ORD) took over.",
    "DAL": "DAL is short for Dallas. Love Field is named after Moss Lee Love, an army aviator, not romance. The bigger airport, shared with Fort Worth, is DFW.",
    "DFW": "DFW stands for Dallas/Fort Worth. The airport sits between the two cities and opened in 1974.",
    "MSP": "MSP stands for Minneapolis-Saint Paul, the Twin Cities the airport serves.",
    "SEA": "SEA is for Seattle, though locals call the airport Sea-Tac because it serves both Seattle and Tacoma.",
    "HOU": "HOU is short for Houston. It belongs to Hobby, the city's older airport, named after William P. Hobby, a former Texas governor. The bigger airport is George Bush Intercontinental (IAH).",
    "LAS": "LAS is short for Las Vegas. The airport was called McCarran International until December 2021, when it was renamed after the Nevada senator Harry Reid.",
    "ATL": "ATL is short for Atlanta. The airport's name honours two of the city's mayors, William Hartsfield and Maynard Jackson.",
    "BOS": "BOS is short for Boston. The airport is named after General Edward Lawrence Logan.",
    "HNL": "HNL is short for Honolulu. Since 2017 the airport has been named after Daniel K. Inouye, Hawaii's long-serving senator.",
    "GRU": "GRU comes from Guarulhos, the city north-east of São Paulo where the airport sits. São Paulo's closer domestic airport, Congonhas, is CGH.",
    "EZE": "EZE comes from Ezeiza, the area south-west of Buenos Aires where the airport sits. Most domestic flights use the city airport, Aeroparque (AEP).",
    "AEP": "AEP comes from AEroParque, Buenos Aires's city airport beside the River Plate. It handles mostly domestic and short regional flights.",
    "DEL": "DEL is short for Delhi. The airport is named after Indira Gandhi, India's prime minister.",
    "CCU": "CCU comes from Calcutta. The city's name became Kolkata in 2001, but the code stayed.",
    "BLR": "BLR comes from Bangalore. The city's official name changed to Bengaluru in 2014, but the code didn't.",
    "COK": "COK comes from Cochin, the older English name for Kochi.",
    "RGN": "RGN comes from Rangoon, the old English name for Yangon.",
    "CMB": "CMB is short for Colombo. The main airport is Bandaranaike International, at Katunayake, north of the city.",
    "SIN": "SIN is short for Singapore. The airport sits at Changi, at the eastern end of the island.",
    "MNL": "MNL is short for Manila. The airport is named after Ninoy Aquino, the opposition politician who was shot there in 1983.",
    "SYD": "SYD is short for Sydney. The airport is named after Charles Kingsford Smith, who made the first flight across the Pacific from the United States to Australia in 1928.",
    "JNB": "JNB is short for Johannesburg. Once called Jan Smuts and then Johannesburg International, the airport was renamed in 2006 after Oliver Tambo, an anti-apartheid leader.",
    "NBO": "NBO is short for Nairobi. The airport is named after Jomo Kenyatta, Kenya's first president.",
    "TLV": "TLV is short for Tel Aviv. The airport is named after David Ben-Gurion, Israel's first prime minister, and is actually near the town of Lod.",
    "AMM": "AMM is short for Amman. The airport is named after Queen Alia of Jordan, who died in a helicopter crash in 1977.",
    "DWC": "DWC stands for Dubai World Central, the area south-west of Dubai where Al Maktoum International sits. Dubai's main airport is DXB.",
    "DOH": "Hamad International replaced Doha's old airport in 2014 and took over the code DOH.",
    "LPL": "LPL is short for LiverPooL. Since 2001 the airport has been named after John Lennon, with the motto 'Above us only sky'.",
    "BHD": "George Best Belfast City was renamed in 2006 after the footballer from Belfast. The city's other airport, Belfast International, is BFS.",
    "BFS": "Belfast International sits at Aldergrove, about 25 km north-west of Belfast. The city's closer airport is George Best Belfast City (BHD).",
    "CRL": "Charleroi is sold as Brussels South, but it's a different city, about 50 km south of Brussels. Brussels's main airport is BRU.",
    "BGY": "Bergamo is sold as Milan Bergamo, but it's about 45 km north-east of Milan. Milan's own airports are Malpensa (MXP) and Linate (LIN).",
    "LIN": "Linate is Milan's city airport, about 7 km from the centre. Long-haul flights use Malpensa (MXP).",
    "MXP": "MXP comes from Malpensa, the area north-west of Milan where the airport sits. The city's closer airport is Linate (LIN).",
    "FCO": "FCO comes from Fiumicino, the town on the coast west of Rome where the airport sits. Its official name is Leonardo da Vinci. Rome's smaller airport is Ciampino (CIA).",
    "CIA": "CIA is Rome Ciampino, the city's older airport, now used mostly by low-cost airlines. Nothing to do with the spy agency.",
    "VCE": "VCE is short for Venice. The airport is named after Marco Polo, the Venetian merchant and traveller.",
    "PSA": "PSA is short for Pisa. The airport is named after Galileo Galilei, who was born in the city.",
    "LIS": "LIS is short for Lisbon. The airport is named after Humberto Delgado, a general who stood against the Salazar dictatorship.",
    "MAD": "MAD is short for Madrid. Barajas is the district where the airport sits, and its full name honours Adolfo Suárez, Spain's first prime minister after Franco.",
    "BCN": "BCN is short for Barcelona. El Prat comes from El Prat de Llobregat, the town next to the airport. Since 2019 its full name also honours Josep Tarradellas.",
    "LYS": "LYS is short for Lyon. The airport is named after Antoine de Saint-Exupéry, the pilot and author of The Little Prince, who was born in Lyon.",
    "TFS": "Tenerife has two airports. TFS, in the south, handles most holiday flights. TFN, in the north near La Laguna, handles more inter-island and domestic flights.",
    "TFN": "Tenerife North, at Los Rodeos near La Laguna, was the scene of the 1977 Tenerife disaster, the deadliest accident in aviation history. Most holiday flights now use Tenerife South (TFS).",
    "JTR": "JTR comes from Thira, another name for Santorini.",
    "ESB": "ESB comes from Esenboğa, the area north-east of Ankara where the airport sits.",
    "MLE": "MLE is short for Malé. The airport, Velana International, sits on its own island, Hulhulé, next to the capital.",
    "JRO": "JRO is short for Kilimanjaro. The airport sits between the towns of Moshi and Arusha in Tanzania.",
    "DSS": "Dakar's new airport, Blaise Diagne, opened in 2017 about 45 km from the city and took the code DSS from the old Léopold Sédar Senghor airport.",
    "ADD": "ADD is short for Addis Ababa. The airport is Bole International, home of Ethiopian Airlines.",
    "SNN": "Shannon was a key refuelling stop for transatlantic flights, and the world's first airport duty-free shop opened there in 1947.",
    "KIN": "KIN is short for Kingston. The airport is named after Norman Manley, one of the founders of modern Jamaica.",
    "MBJ": "MBJ comes from Montego Bay, Jamaica. The airport is named after Sir Donald Sangster, a Jamaican prime minister.",
    "NAS": "NAS is short for Nassau. The airport is named after Lynden Pindling, the first prime minister of the Bahamas.",
    "HAV": "HAV is short for Havana. The airport is named after José Martí, the Cuban national hero.",
    "SJO": "SJO is San José, Costa Rica, though the airport is in nearby Alajuela. It's named after Juan Santamaría, a Costa Rican national hero.",
    "LIR": "Liberia here is the city in north-west Costa Rica, not the African country. Its airport serves the Guanacaste beaches.",
    "LPB": "LPB is short for La Paz. The airport, at El Alto, sits at about 4,060 m, one of the highest international airports in the world.",
    "CNF": "CNF comes from Confins, the town north of Belo Horizonte where the airport sits. The city's older airport, Pampulha, is PLU.",
    "MKE": "MKE is short for Milwaukee. The airport is named after Billy Mitchell, the US general who championed air power and grew up in Milwaukee.",
    "STL": "STL is short for St. Louis. The airport is named after Albert Bond Lambert, an aviation promoter who backed Charles Lindbergh's Spirit of St. Louis flight.",
    "BDL": "BDL comes from Bradley. The airport is named after Eugene Bradley, a US Army pilot killed in a training crash there in 1941.",
    "CLT": "CLT is short for Charlotte. The airport is named after Ben Elbert Douglas, the mayor who backed it.",
    "OKA": "OKA is short for Okinawa. The airport is at Naha, the prefecture's capital.",
    "CTS": "CTS comes from Chitose, the city south-east of Sapporo where New Chitose airport sits.",
    "NGO": "NGO is short for Nagoya. Chubu Centrair opened in 2005 on an artificial island and took over the code from Nagoya's old airport at Komaki.",
    "KTM": "KTM is short for Kathmandu. The airport is named after King Tribhuvan of Nepal.",
    "ISB": "Islamabad's new airport opened in 2018 and took over the code ISB from the old one.",
    "DMM": "DMM is short for Dammam. King Fahd International is often called the largest airport in the world by land area.",
    "JED": "JED is short for Jeddah. King Abdulaziz International has a separate Hajj Terminal for pilgrims travelling to Mecca.",
    "MRU": "MRU is short for Mauritius. The airport is named after Sir Seewoosagur Ramgoolam, the country's first prime minister.",
    "LOS": "LOS is short for Lagos. The airport is named after Murtala Mohammed, a former Nigerian head of state.",
    "ACC": "ACC is short for Accra. The airport is Kotoka International, named after Emmanuel Kotoka.",
    "DAR": "DAR is short for Dar es Salaam. The airport is named after Julius Nyerere, Tanzania's first president.",
    "LUN": "LUN is short for Lusaka. The airport is named after Kenneth Kaunda, Zambia's first president.",
    "EBB": "Entebbe is Uganda's international airport, serving the capital, Kampala, about 40 km away. It's famous for the 1976 hostage rescue.",
    "DUR": "King Shaka International opened in 2010, ahead of the football World Cup, and replaced Durban's old airport.",
    "CMN": "CMN is short for Casablanca. The airport is named after Mohammed V, King of Morocco.",
    "TUN": "TUN is short for Tunis. The airport's name, Tunis-Carthage, comes from the ancient city of Carthage nearby.",
    "ALG": "ALG is short for Algiers. The airport is named after Houari Boumediene, a former Algerian president.",
}

FAQ_ROUTE = {
    "LON": ["LHR", "LGW", "STN", "LTN", "LCY", "SEN"],
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


NOINDEX = '  <meta name="robots" content="noindex, follow">\n'


# Airport pages that go in the sitemap and search results: the ones whose story
# is long and specific enough to stand as a page on its own. Every other page is
# still built so players can open it, but marked noindex. When a story gets
# longer and better, add its code here.
INDEXED = {
    "BCN", "BKK", "BOM", "BVA", "BWI", "CDG", "CVG", "DAL", "DEN", "DMK", "DSS",
    "DTW", "EWR", "EZE", "FCO", "GMP", "GRU", "HKG", "HOU", "IAD", "ICN", "IST",
    "ITM", "JFK", "JNB", "KEF", "KIX", "LAS", "LAX", "LGA", "LHR", "LYS", "MAD",
    "MCI", "MDW", "MSY", "MUC", "NRT", "ORD", "ORY", "OSL", "PEK", "PKX", "PRG",
    "PVG", "SAW", "SHA", "STL", "SYD", "TFN", "TFS", "TLV", "YYZ",
}


def indexable(a):
    return a["code"] in INDEXED


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
{robots}  <link rel="canonical" href="https://amateurgames1.com{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Amateurgames1">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://amateurgames1.com{path}">
  <meta property="og:image" content="https://amateurgames1.com/assets/og-home.jpg">
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
        <a class="nav-link nav-keep" href="/guides/">Guides</a>
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
        <a href="/guides/">Guides</a>
        <a href="/about">About</a>
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


def related_guides(code):
    """Guides that mention this code, as (slug, title)."""
    try:
        from build_guides import GUIDES
    except ImportError:
        return []
    tag = "{{" + code + "}}"
    return [(g["slug"], g["title"]) for g in GUIDES if tag in g["body"]][:3]


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
                     "LON is a city code that covers all of London's airports. Booking sites use it to search Heathrow (LHR), Gatwick (LGW), Stansted (STN), Luton (LTN), London City (LCY) and Southend (SEN) at once."))

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
    parts = [HEAD.format(title=e(title), desc=e(desc), path=path, schema=schema,
                         robots="" if indexable(a) else NOINDEX)]
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
          <h2>The story behind {code}</h2>
          <p>{e(story)}</p>
        </section>
""")
    guides = related_guides(code)
    if guides:
        links = "".join(f'<li><a href="/guides/{slug}">{e(t)}</a></li>' for slug, t in guides)
        parts.append(f"""
        <section class="panel ap-panel">
          <h2>Read more about {code}</h2>
          <ul class="ap-guides">{links}</ul>
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
    parts = [HEAD.format(title=e(title), desc=e(desc), path="/airports/", schema=schema, robots="")]
    parts.append(f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <p class="eyebrow">Airports A&ndash;Z</p>
        <h1>What airport is that code?</h1>
        <p class="lead">{len(airports)} airports, the story behind their codes, and the codes people mix them up with.</p>
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
        <p>For the stories behind the strangest codes, read our <a href="/guides/">guides</a>. Want to test yourself? Try <a href="/daily">Daily Departure</a> or a round of <a href="/play">Quick Play</a>.</p>
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
              for a in sorted(airports, key=lambda a: a["code"]) if indexable(a)]
    s = s.replace("</urlset>", "".join(lines) + "</urlset>")
    path.write_text(s, encoding="utf-8")


def main():
    airports = load_airports()
    assert INDEXED <= set(STORIES), f"indexed without a story: {INDEXED - set(STORIES)}"
    codes = [a["code"] for a in airports]
    assert len(codes) == len(set(codes)), "duplicate airport code"
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    for a in airports:
        (OUT / f"{a['code'].lower()}.html").write_text(airport_page(a, airports), encoding="utf-8")
    (OUT / "index.html").write_text(index_page(airports), encoding="utf-8")
    update_sitemap(airports)
    n = sum(indexable(a) for a in airports)
    print(f"Built {len(airports)} airport pages and the A-Z index ({n} indexable, {len(airports) - n} noindex).")


if __name__ == "__main__":
    main()
