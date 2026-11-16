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
from build_airports import FOOT, HEAD, ROOT, TODAY, e, load_airports, schema_block

AUTHOR = "Amateurgames1"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def nice_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def byline(g):
    pub = g["published"]
    if pub == TODAY:
        when = f"Published {nice_date(pub)}"
    else:
        when = f"Published {nice_date(pub)} &middot; Updated {nice_date(TODAY)}"
    return f'<p class="guide-byline">By <a href="/about">{AUTHOR}</a> &middot; {when}</p>'  # noqa: E402

OUT = ROOT / "guides"

WP = "https://en.wikipedia.org/wiki/"
IATA_SEARCH = ("IATA: Airline and Airport Code Search", "https://www.iata.org/en/publications/directories/code-search/")
IATA_CODES = ("IATA: Airline and Location Codes", "https://www.iata.org/en/services/codes/")
IATA_LOCATIONS = ("IATA: Airport & Location Identifier Database", "https://www.iata.org/en/publications/manuals/airline-airport-location-coding-databases/airport-location-identifier-database/")
IATA_CCD = ("IATA: City Code Directory", "https://www.iata.org/en/publications/manuals/mileage/city-code-directory-ccd/")


def wp(title, slug=None):
    return (f"Wikipedia: {title}", WP + (slug or title.replace(" ", "_")))


IATA_ARTICLE = wp("IATA airport code")

# Sources for each guide, shown at the end of the page. Add one whenever you add a fact.
SOURCES = {
    "why-canadian-airports-start-with-y": [IATA_ARTICLE, wp("Toronto Pearson International Airport"), wp("YYZ (song)", "YYZ_(song)"), wp("ICAO airport code")],
    "airport-codes-from-old-names": [IATA_ARTICLE, wp("O'Hare International Airport"), IATA_SEARCH],
    "london-airports-codes": [wp("Airports of London"), wp("Heathrow Airport"), wp("Gatwick Airport"), wp("London City Airport")],
    "why-lax-has-an-x": [IATA_ARTICLE, wp("History of Los Angeles International Airport"), wp("Theme Building")],
    "iata-and-icao-codes": [IATA_ARTICLE, wp("ICAO airport code"), wp("International Civil Aviation Organization"), IATA_CODES],
    "codes-that-dodged-a-clash": [IATA_ARTICLE, wp("Dulles International Airport"), wp("Sioux Gateway Airport")],
    "how-airport-codes-are-assigned": [IATA_CODES, IATA_LOCATIONS, IATA_ARTICLE, wp("Location identifier")],
    "why-us-airport-codes-avoid-n-k-w": [IATA_ARTICLE, wp("Location identifier"), wp("ICAO airport code")],
    "airports-that-moved-their-code": [wp("Istanbul Airport"), wp("Atatürk Airport", "Atat%C3%BCrk_Airport"), wp("Suvarnabhumi Airport"), wp("Don Mueang International Airport"), IATA_SEARCH],
    "city-codes-for-cities-with-several-airports": [IATA_CCD, wp("List of cities with more than one commercial airport"), IATA_ARTICLE],
    "airports-named-after-people": [wp("List of airports named after people"), IATA_SEARCH],
    "airline-codes-vs-airport-codes": [wp("Airline codes"), wp("Aviation call sign"), wp("Speedbird"), IATA_CODES],
    "reading-your-bag-tag-and-boarding-pass": [wp("Bag tag"), wp("Boarding pass"), wp("Baggage handling system")],
    "codes-from-local-names": [IATA_ARTICLE, IATA_SEARCH],
    "airports-named-for-a-city-they-are-not-in": [wp("Brussels South Charleroi Airport"), wp("Milan Bergamo Airport", "Bergamo_Airport"), wp("List of cities with more than one commercial airport")],
    "how-to-learn-airport-codes": [wp("Spacing effect"), IATA_SEARCH],
}


GUIDES = [
    {
        "slug": "why-canadian-airports-start-with-y",
        "code": "YYZ",
        "published": "2026-11-05",
        "title": "Why do Canadian airports start with Y?",
        "blurb": "Toronto is YYZ, Vancouver is YVR, Montréal is YUL. Here's why nearly every big Canadian airport begins with a Y.",
        "body": """
<p>Look at a Canadian boarding pass and you'll almost always see a Y. Toronto Pearson is {{YYZ}}, Vancouver is {{YVR}}, Montréal is {{YUL}}, Calgary is {{YYC}} and Ottawa is {{YOW}}. Edmonton ({{YEG}}), Winnipeg ({{YWG}}), Halifax ({{YHZ}}), Québec City ({{YQB}}) and Victoria ({{YYJ}}) follow the same rule. No other country uses a single letter so consistently, which makes Canada one of the easiest places to spot on a departures board and one of the hardest to tell apart.</p>
<h2>Where the Y came from</h2>
<p>The usual explanation goes back to the early days of radio. Canada gave its weather and radio stations two-letter identifiers. When three-letter airport codes became the standard, Canada added a Y in front of the old two letters, and the habit stuck. One common account is that the Y marked a weather station that shared its site with an airport. Historians differ on the details, but the result is clear: Y now means Canada almost everywhere you look.</p>
<p>The same idea carries over to the four-letter codes pilots use. Those are set by ICAO, and Canada's all begin with C, so Toronto Pearson is CYYZ and Vancouver is CYVR. You can read more about the two systems in our guide to <a href="/guides/iata-and-icao-codes">IATA and ICAO codes</a>.</p>
<h2>Why the letters after the Y look random</h2>
<p>Because the last two letters came from those old station identifiers, many don't match the city's name at all. That's why Toronto is YYZ and not something like YTO. YTO does exist, but as a city code that covers all of Toronto's airports, including the small Billy Bishop airport on the Toronto Islands, which is YTZ. Montréal has a city code too, YMQ.</p>
<p>Some codes do line up with the name. In YVR you can see Vancouver's V and R, in YOW the W of Ottawa, and in YQB the Q and B of Québec. Others, like YYC for Calgary and YEG for Edmonton, have no obvious link, so they simply have to be learned.</p>
<h2>A code with a fan club</h2>
<p>YYZ might be the most famous airport code in music. The Canadian rock band Rush named an instrumental track "YYZ" on their 1981 album Moving Pictures, and its opening rhythm spells the letters out in Morse code, the way the airport's radio beacon did.</p>
<h2>Not every Y is Canadian</h2>
<p>Y isn't reserved for Canada worldwide. Australia's four-letter ICAO codes start with Y as well (Sydney is YSSY), but its three-letter codes, the ones on your ticket, don't: Sydney is {{SYD}} and Melbourne is {{MEL}}. If a three-letter code starts with Y, it is almost certainly in Canada.</p>
<h2>How to remember them</h2>
<ul>
<li>Ignore the Y and look at the last two letters: YV<b>R</b>, Vancouver; YO<b>W</b>, Ottawa; YQ<b>B</b>, Québec.</li>
<li>Group them by region. In the west: YVR, YYC, YEG and YYJ. In the middle: YWG. In the east: YYZ, YOW, YUL, YQB and YHZ.</li>
<li>Toronto, Calgary and Edmonton are the odd ones out, so learn YYZ, YYC and YEG by heart. Two of them have a double Y, which helps.</li>
<li>Montréal's YUL is easiest to remember as the "Yule" airport. Corny, but it works.</li>
</ul>
<p>Then test yourself. A round of <a href="/play">Quick Play</a> on the Americas will throw several Canadian codes at you at once, which is the best way to stop mixing them up.</p>
""",
    },
    {
        "slug": "airport-codes-from-old-names",
        "code": "ORD",
        "published": "2026-11-05",
        "title": "Airport codes that remember an old name",
        "blurb": "ORD for O'Hare, MCO for Orlando, BOM for Mumbai. These codes kept the name the airport or city had before.",
        "body": """
<p>Airport codes rarely change, even when an airport or city gets a new name. A new code would mean updating airline systems, timetables, signs and bag-tag printers all over the world, so the old letters usually stay. That turns some codes into little history lessons. Here are the best-known ones.</p>
<h2>Chicago O'Hare: {{ORD}}</h2>
<p>O'Hare started life as Orchard Field, next to an aircraft factory. It was renamed in 1949 after Butch O'Hare, a US Navy fighter pilot and Medal of Honor recipient, but the code ORD, from ORcharD, stayed. Chicago's other airport, {{MDW}}, is named after the Battle of Midway.</p>
<h2>Orlando: {{MCO}}</h2>
<p>Orlando's main airport was once McCoy Air Force Base. The base is long gone, but MCO lives on, and millions of theme-park visitors land on its letters every year.</p>
<h2>New Orleans: {{MSY}}</h2>
<p>MSY comes from Moisant Stock Yards, the site of the original airfield, named after the aviator John Moisant. Today the airport is named after the jazz musician Louis Armstrong, but the code still remembers the stockyards.</p>
<h2>Cincinnati: {{CVG}}</h2>
<p>Cincinnati's airport is actually in Kentucky, across the Ohio River near the town of Covington. Hence CVG.</p>
<h2>Kansas City and Nashville: {{MCI}} and {{BNA}}</h2>
<p>MCI comes from Mid-Continent International, Kansas City's airport's name when it opened. BNA comes from Berry Field, Nashville, the original name of the city's airport.</p>
<h2>New York JFK: {{JFK}}</h2>
<p>This one did change, which shows how unusual that is. The airport opened as Idlewild, with the code IDL. When it was renamed after President John F. Kennedy in December 1963, the code changed to JFK too.</p>
<h2>Cities that changed their names</h2>
<p>Asia has the most examples, because many cities moved from an older English spelling to a local one after the codes were set.</p>
<ul>
<li>{{PEK}}: Beijing, from Peking, the older English spelling. Beijing's newer airport, {{PKX}}, echoes it.</li>
<li>{{BOM}}: Mumbai, from Bombay. The city was renamed in 1995.</li>
<li>{{MAA}}: Chennai, from Madras. The city was renamed in 1996.</li>
<li>{{CCU}}: Kolkata, from Calcutta. The city was renamed in 2001.</li>
<li>{{BLR}}: Bengaluru, from Bangalore. The official name changed in 2014.</li>
<li>{{COK}}: Kochi, from Cochin.</li>
<li>{{RGN}}: Yangon, from Rangoon.</li>
<li>{{SGN}}: Ho Chi Minh City, from Saigon, a name locals still use.</li>
<li>{{OPO}}: Porto, from Oporto, its traditional English name.</li>
</ul>
<p>Russia has a famous one too. St Petersburg's airport is still LED, from Leningrad, the city's name from 1924 to 1991.</p>
<h2>How to use this when you're guessing</h2>
<p>If a code makes no sense for the city, try the old name. Indian and Southeast Asian codes very often follow it. In the US, try the name of the airfield or the town next door. And if neither works, it may be a code that had to dodge a clash, which is a story for <a href="/guides/codes-that-dodged-a-clash">another guide</a>.</p>
""",
    },
    {
        "slug": "london-airports-codes",
        "code": "LHR",
        "published": "2026-11-05",
        "title": "London has six airports. Can you name their codes?",
        "blurb": "LHR, LGW, STN, LTN, LCY and SEN, plus the LON code that covers them all, and how not to mix them up.",
        "body": """
<p>London is served by six airports, and their codes are a classic quiz trap because most start with L. Here they are, with a way to remember each, and how to get from each one into the city.</p>
<h2>The six codes</h2>
<ul>
<li>{{LHR}} <b>Heathrow</b>: L for London, HR for Heathrow. The UK's busiest airport, in west London. The Heathrow Express runs to Paddington, and the Elizabeth line and Piccadilly line also serve it.</li>
<li>{{LGW}} <b>Gatwick</b>: L for London, GW for Gatwick. South of London, in West Sussex, with one main runway. The Gatwick Express runs to Victoria.</li>
<li>{{STN}} <b>Stansted</b>: the letters come straight from STaNsted. North-east of London, in Essex, and a big base for low-cost airlines. The Stansted Express runs to Liverpool Street.</li>
<li>{{LTN}} <b>Luton</b>: LuToN. North of London, in Bedfordshire. Trains stop at Luton Airport Parkway, linked to the terminal by a short shuttle.</li>
<li>{{LCY}} <b>London City</b>: London CitY. The closest to central London, in the Docklands, with a short runway and a steep approach that only some aircraft can fly. It's on the DLR.</li>
<li>{{SEN}} <b>Southend</b>: SouthENd, out east in Essex. Its own station has trains to Liverpool Street.</li>
</ul>
<h2>What does LON mean?</h2>
<p>LON isn't an airport. It's a city code that covers all of London's airports, so booking sites can search them all at once. Other big cities have one too: NYC for New York, PAR for Paris and TYO for Tokyo. Our guide to <a href="/guides/city-codes-for-cities-with-several-airports">city codes</a> lists the rest.</p>
<p>Searching LON is a good way to find cheaper flights, but check which airport you land at. Getting from Southend to Heathrow for a connection can take longer than some short flights.</p>
<h2>The usual mix-ups</h2>
<p>People most often confuse LGW and LHR, because both start with L and end with a consonant pair. Remember that Gatwick has the G. The other trap is LCY: the Y comes from the end of "City", not from a place name.</p>
<p>STN and LTN are the next pair to watch. Both end in N, and both are north of London. Think STaNsted and LuToN, and say the letters as you read the name.</p>
<h2>A quick memory test</h2>
<p>Cover the list above and try to write all six codes from memory. Most people get LHR and LGW straight away, then stall on SEN and LCY. If you can do all six, try our <a href="/daily">Daily Departure</a> puzzle: London codes turn up often.</p>
""",
    },
    {
        "slug": "why-lax-has-an-x",
        "code": "LAX",
        "published": "2026-11-05",
        "title": "Why does LAX have an X?",
        "blurb": "Los Angeles is LAX and Portland is PDX. The X doesn't stand for anything, and here's why it's there.",
        "body": """
<p>Los Angeles is {{LAX}} and Portland, Oregon is {{PDX}}. In both cases, the X doesn't stand for anything. It's a placeholder, left over from the days when airport codes were shorter.</p>
<h2>From two letters to three</h2>
<p>In the early days of US aviation, many airports used two-letter codes, borrowed from the weather service, which had already given its stations short identifiers. Los Angeles was LA and Portland was PD. As the number of airports grew, two letters weren't enough to go round, and three-letter codes became the standard. Some airports simply kept their old two letters and added an X to fill the gap.</p>
<h2>A code that became a brand</h2>
<p>LAX is now so well known that people say it as a word. The airport opened in 1928 as Mines Field, and its space-age Theme Building, which looks like a flying saucer on four legs, has become a symbol of the city. Few people call it Los Angeles International. It's just LAX.</p>
<h2>Does X mean anything else?</h2>
<p>Not by itself. Plenty of codes contain an X for other reasons, such as {{KIX}} for Osaka's Kansai International, where the X helps it stand apart from Osaka's older airport, {{ITM}}. Phoenix is {{PHX}}, where the X is simply part of the name. If you're guessing, an X at the end of a US code is often a sign of the old two-letter history, but it's not a rule.</p>
<h2>Other codes that were stretched</h2>
<p>The X wasn't the only way to fill a gap. Some airports added a letter from elsewhere in the name, and others took a completely new code. That's part of why US codes feel less consistent than, say, Canada's, where nearly every code starts with a Y (see <a href="/guides/why-canadian-airports-start-with-y">why Canadian airports start with Y</a>).</p>
<h2>Try it yourself</h2>
<p>Next time you see a code ending in X, check whether the first two letters make sense on their own. For LA and PD, they do. It's a small trick, but it turns a random code into one you'll remember.</p>
<ul>
<li>{{LAX}}: Los Angeles, from LA.</li>
<li>{{PDX}}: Portland, Oregon, from PD.</li>
<li>{{KIX}}: Osaka Kansai, a different story.</li>
<li>{{PHX}}: Phoenix, where the X is in the name.</li>
</ul>
<p>Not to be confused with Portland, Maine, which is PWM. If you're flying to Oregon, make sure the tag says PDX.</p>
""",
    },
    {
        "slug": "iata-and-icao-codes",
        "code": "EGLL",
        "published": "2026-11-05",
        "title": "Three letters or four? IATA and ICAO codes explained",
        "blurb": "Heathrow is LHR on your boarding pass but EGLL to a pilot. What's the difference, and what are city codes like LON?",
        "body": """
<p>Every big airport has two codes. The one you know from your boarding pass is the three-letter <b>IATA</b> code. Pilots, air traffic control and flight-planning systems use a four-letter <b>ICAO</b> code instead. Heathrow is {{LHR}} to you and EGLL to the pilot flying you there.</p>
<h2>Who sets them</h2>
<p>IATA, the International Air Transport Association, is the airlines' trade body, founded in 1945. Its codes are for the commercial side of flying: tickets, timetables, baggage and booking systems. ICAO, the International Civil Aviation Organization, is a United Nations agency set up after the 1944 Chicago Convention. Its codes are for the operational side: flight plans, weather reports and air traffic control. Both organisations are based in Montréal.</p>
<h2>IATA codes: three letters, for passengers</h2>
<p>IATA codes like {{LHR}}, {{JFK}} and {{CDG}} appear on tickets, boarding passes and bag tags. They're short and easy to read, but there are only 17,576 possible three-letter combinations, and they were handed out roughly first come, first served. That's why some codes look odd, and why our guides spend so much time on the stories behind them. Small airfields often have no IATA code at all.</p>
<h2>ICAO codes: four letters, for pilots</h2>
<p>ICAO codes are organised by region, so they're much more logical. The first letter tells you roughly where in the world the airport is, and the second usually narrows it to a country:</p>
<ul>
<li><b>K</b> for the contiguous United States: KJFK, KLAX. Many US ICAO codes are just the IATA code with a K in front.</li>
<li><b>C</b> for Canada: CYYZ for Toronto.</li>
<li><b>E</b> for northern Europe: EG for the UK (EGLL Heathrow, EGKK Gatwick), ED for Germany (EDDF Frankfurt).</li>
<li><b>L</b> for southern Europe: LF for France (LFPG Charles de Gaulle), LE for Spain (LEMD Madrid), LI for Italy (LIRF Rome Fiumicino).</li>
<li><b>U</b> for Russia and some neighbours: UUEE for Moscow Sheremetyevo.</li>
<li><b>O</b> for the Middle East: OMDB for Dubai.</li>
<li><b>V</b> for South Asia and parts of East Asia: VIDP for Delhi, VHHH for Hong Kong.</li>
<li><b>R</b> for Japan, Korea and Taiwan: RJTT for Tokyo Haneda, RKSI for Seoul Incheon.</li>
<li><b>Z</b> for mainland China: ZBAA for Beijing Capital.</li>
<li><b>W</b> for maritime Southeast Asia: WSSS for Singapore Changi.</li>
<li><b>Y</b> for Australia: YSSY for Sydney.</li>
<li><b>N</b> for New Zealand and much of the South Pacific: NZAA for Auckland.</li>
<li><b>P</b> for Alaska, Hawaii and some Pacific islands: PANC for Anchorage, PHNL for Honolulu.</li>
<li><b>M</b> for Mexico and Central America: MMMX for Mexico City.</li>
<li><b>S</b> for South America: SBGR for São Paulo Guarulhos.</li>
<li><b>F</b> for southern and central Africa: FAOR for Johannesburg.</li>
</ul>
<h2>City codes</h2>
<p>Some cities have a third kind of code that covers all their airports at once. LON covers London's six airports, NYC covers JFK, LaGuardia and Newark, PAR covers Paris and TYO covers Tokyo. Booking sites use them to show every flight to a city in one search. See our guide to <a href="/guides/city-codes-for-cities-with-several-airports">city codes</a> for more.</p>
<h2>Which one should you learn?</h2>
<p>If you fly as a passenger, the IATA code is the one that matters. It's the one on your bag tag, and the one our games test. If you're into flight simulators, plane spotting or flight-tracking apps, you'll meet ICAO codes all the time, and knowing the region letters makes them easy to read.</p>
""",
    },
    {
        "slug": "codes-that-dodged-a-clash",
        "code": "EWR",
        "published": "2026-11-05",
        "title": "Why Newark is EWR, and other codes that dodged a clash",
        "blurb": "Newark couldn't be NEW, Washington Dulles swapped its letters, and Osaka needed a new code. The stories behind the odd ones.",
        "body": """
<p>Some codes look strange because the obvious choice was already taken, or not allowed. Once you know the rules they were dodging, they start to make sense.</p>
<h2>The letters the US keeps for itself</h2>
<p>In the United States, some first letters are off limits for airport codes. N is reserved for the US Navy. K and W are used for radio and TV station call signs. Q is used for international telecoms codes. That rules out a lot of obvious choices, and explains several of the codes below. We cover the rule in more depth in <a href="/guides/why-us-airport-codes-avoid-n-k-w">why US airport codes avoid N, K and W</a>.</p>
<h2>Newark: {{EWR}}</h2>
<p>Because N is reserved, Newark couldn't be NEW. It took the next letters of its name instead: nEWaRk. Norfolk, Nashville and New Orleans had the same problem, which is why their codes look unexpected too: Nashville is {{BNA}} and New Orleans is {{MSY}}.</p>
<h2>Washington Dulles: {{IAD}}</h2>
<p>Dulles first used the code DIA. On handwritten tags that looked too much like {{DCA}}, Washington's other airport, so the letters were rearranged to IAD. With {{BWI}} as well, Washington has three airports whose codes share no first letter.</p>
<h2>Osaka Kansai: {{KIX}}</h2>
<p>When Kansai International opened in 1994, Osaka already had an airport, {{ITM}} (Itami). The new one became KIX, and Osaka's city code OSA covers both. The K rule only applies in the US, so Japan could use it.</p>
<h2>Houston: {{IAH}}</h2>
<p>IAH stands for Intercontinental Airport of Houston, the airport's original name. Houston's older airport, Hobby, already had {{HOU}}, so the new airport needed something else.</p>
<h2>Kansas City: {{MCI}}</h2>
<p>Kansas City's downtown airport already had MKC. When the new airport opened, it took MCI, from Mid-Continent International.</p>
<h2>Codes people wish they could change</h2>
<p>Sometimes the clash is with good taste. Sioux City, Iowa, is SUX. The airport asked for a new code for years before deciding to embrace it, and now sells merchandise with the letters on. IATA rarely changes a code once it's in use, because so many systems rely on it.</p>
<h2>What to take from this</h2>
<p>If a US code seems to skip the first letter of its city, check whether that letter is N, K, W or Q. If a city has two airports, the newer one often got the odder code, because the obvious one was already taken.</p>
""",
    },
    {
        "slug": "how-airport-codes-are-assigned",
        "code": "IATA",
        "published": "2026-11-16",
        "title": "Who decides airport codes, and how?",
        "blurb": "There are 17,576 possible three-letter codes. Here's who hands them out, what they look for, and why a code almost never changes.",
        "body": """
<p>The three letters on your bag tag aren't chosen by the airport alone. They're assigned by IATA, the International Air Transport Association, the trade body for the world's airlines. IATA publishes the list of codes and makes sure no two locations share one.</p>
<h2>How many codes are there?</h2>
<p>With 26 letters in each of three places, there are 26 × 26 × 26 = 17,576 possible codes. That sounds like plenty, but thousands of airports, heliports, railway stations and bus terminals need one. Some codes are also kept back or avoided, and many good combinations were taken early. So the supply of sensible codes ran low a long time ago.</p>
<h2>How a code is chosen</h2>
<p>An airport, or the country's aviation authority, applies to IATA for a code. The ideal code spells out something obvious: the city, the airport's name or a well-known nickname. {{LHR}} for London Heathrow and {{DXB}} for Dubai are the easy kind. If that combination is already taken, the applicant tries another set of letters from the name, which is how you get codes like {{EWR}} for Newark.</p>
<p>In the United States, the Federal Aviation Administration also gives airports its own identifiers, and for airports with airline service these usually match the IATA code. The US avoids certain first letters altogether, which you can read about in <a href="/guides/why-us-airport-codes-avoid-n-k-w">why US airport codes avoid N, K and W</a>.</p>
<h2>Why codes almost never change</h2>
<p>An airport code is built into everything: airline reservation systems, timetables, fare tables, baggage sorting machines, printed signs and decades of records. Changing one is expensive and risky, because a bag tagged with the old code might end up somewhere else. So codes outlive airport names, city names and sometimes the airport itself. That's why Chicago O'Hare is still {{ORD}}, from Orchard Field, and Mumbai is still {{BOM}}, from Bombay.</p>
<p>The main exception is when a city opens a new airport and moves its main code across, as Istanbul did with {{IST}} in 2019. We cover those cases in <a href="/guides/airports-that-moved-their-code">airports that moved their code</a>.</p>
<h2>Codes for places that aren't airports</h2>
<p>Some railway stations and bus terminals have IATA codes so that a train or coach journey can be sold on the same ticket as a flight. To a booking system, they behave like airports. You'll rarely see them unless you book a combined air and rail trip.</p>
<h2>City codes and why they exist</h2>
<p>IATA also assigns codes to cities with more than one airport, such as LON for London and NYC for New York. These aren't places a plane can land. They exist so that one search can cover every airport in the city. Our guide to <a href="/guides/city-codes-for-cities-with-several-airports">city codes</a> lists the main ones.</p>
<h2>The four-letter codes</h2>
<p>A separate body, ICAO, gives airports four-letter codes for pilots and air traffic control. Those follow a regional system and are far more predictable. See <a href="/guides/iata-and-icao-codes">IATA and ICAO codes explained</a>.</p>
<h2>What this means for learning them</h2>
<p>Because codes were handed out over many decades, there's no single rule that explains them all. The best approach is to learn the patterns, such as old names, Canada's Y and the US letter rules, and then learn the exceptions one by one. Our <a href="/daily">Daily Departure</a> puzzle gives you five a day.</p>
""",
    },
    {
        "slug": "why-us-airport-codes-avoid-n-k-w",
        "code": "EWR",
        "published": "2026-11-16",
        "title": "Why US airport codes avoid N, K and W",
        "blurb": "Newark isn't NEW and Kansas City isn't KAN. A handful of letters are off limits for US airports, and it shows in the codes.",
        "body": """
<p>Look down a list of US airport codes and you'll notice something missing. Almost none begin with N, K or W, and very few with Q. That's not chance. Those letters were reserved for other uses long before most airports got their codes.</p>
<h2>N: kept for the Navy</h2>
<p>Codes beginning with N are reserved for the US Navy. That's why Newark couldn't be NEW and became {{EWR}}, taking the next letters of its name. Nashville is {{BNA}}, from Berry Field, Nashville. New Orleans is {{MSY}}, from Moisant Stock Yards. Norfolk, Virginia, is ORF.</p>
<h2>K and W: kept for radio and TV</h2>
<p>In the US, radio and TV stations have call signs that begin with K or W, roughly K west of the Mississippi and W to the east. To avoid confusion with those call signs, airport codes avoid both letters. That's why Kansas City is {{MCI}}, from Mid-Continent International, and why Washington's airports are {{DCA}}, {{IAD}} and {{BWI}}.</p>
<p>K does turn up in US aviation, but in a different place. The four-letter ICAO codes pilots use put a K in front of the US airport's code, so Los Angeles is KLAX. That's covered in <a href="/guides/iata-and-icao-codes">IATA and ICAO codes explained</a>.</p>
<h2>Q: kept for telecoms</h2>
<p>Q is used for international telecoms codes, the "Q codes" used in radio communication. US airports avoid it as a first letter for the same reason.</p>
<h2>Outside the US, the rule doesn't apply</h2>
<p>These restrictions are American. Elsewhere, codes starting with N, K and W are common:</p>
<ul>
<li>{{NRT}}: Tokyo Narita.</li>
<li>{{KIX}}: Osaka Kansai.</li>
<li>{{KUL}}: Kuala Lumpur.</li>
<li>{{NBO}}: Nairobi.</li>
<li>{{KEF}}: Reykjavík Keflavík.</li>
<li>{{WAW}}: Warsaw.</li>
<li>{{WLG}}: Wellington.</li>
<li>{{NCE}}: Nice.</li>
</ul>
<p>So if you see a code starting with N, K or W, you can be fairly sure it isn't in the United States. That's a handy shortcut in a quiz.</p>
<h2>Canada has a letter of its own</h2>
<p>Canada went the other way and put a Y at the front of nearly every major airport code. Toronto is {{YYZ}}, Vancouver {{YVR}}. Read the story in <a href="/guides/why-canadian-airports-start-with-y">why Canadian airports start with Y</a>.</p>
<h2>How to use this</h2>
<ul>
<li>A US city starting with N, K or W will almost always have a code that doesn't start with that letter.</li>
<li>Look for the next strong letters in the name, as with nEWaRk, or for an old airport name, as with BNA and MCI.</li>
<li>A code starting with N, K or W is a strong hint the airport is outside the US.</li>
</ul>
""",
    },
    {
        "slug": "airports-that-moved-their-code",
        "code": "IST",
        "published": "2026-11-16",
        "title": "Airports that moved their code to a new airport",
        "blurb": "When Istanbul, Bangkok and Denver opened new airports, the old code went with them. Here's how a city's code can move.",
        "body": """
<p>Airport codes rarely change. But when a city opens a big new airport to replace its old one, the city's best-known code often moves across too. Passengers keep booking the same three letters, and the old airport either closes or gets a new code.</p>
<h2>Istanbul: {{IST}}</h2>
<p>Istanbul's code belonged to Atatürk Airport for decades. In April 2019 the new Istanbul Airport, north of the city, took over IST in a single overnight move. Atatürk closed to scheduled passenger flights. Istanbul's other airport, on the Asian side, is {{SAW}}, Sabiha Gökçen.</p>
<h2>Bangkok: {{BKK}} and {{DMK}}</h2>
<p>Bangkok's old airport, Don Mueang, used BKK until Suvarnabhumi opened in 2006 and took the code. Don Mueang closed for a while, then reopened with a new code, DMK, and is now busy with low-cost airlines. Bangkok is one of the few cities where the older airport ended up with the newer code.</p>
<h2>Hong Kong: {{HKG}}</h2>
<p>Kai Tak, with its famous approach between apartment blocks, was HKG. When Chek Lap Kok opened in July 1998, flights moved across overnight and the code went with them.</p>
<h2>Denver: {{DEN}}</h2>
<p>Denver's old airport, Stapleton, was DEN. When Denver International opened in 1995, it took the code and Stapleton closed. The site is now a residential neighbourhood.</p>
<h2>Munich and Oslo: {{MUC}} and {{OSL}}</h2>
<p>Munich's new airport opened in 1992, replacing Munich-Riem overnight and keeping MUC. Oslo did the same in 1998: Gardermoen took OSL, and the old airport at Fornebu closed.</p>
<h2>Kuala Lumpur: {{KUL}}</h2>
<p>When Kuala Lumpur International opened in 1998, it took KUL from the older Subang airport, which got a new code and now handles mostly turboprop flights.</p>
<h2>And more</h2>
<ul>
<li>{{DOH}}: Hamad International replaced Doha's old airport in 2014.</li>
<li>{{NGO}}: Chubu Centrair took Nagoya's code in 2005.</li>
<li>{{ISB}}: Islamabad's new airport took ISB in 2018.</li>
<li>{{DSS}}: Dakar's Blaise Diagne airport took DSS in 2017.</li>
<li>{{ATH}}: Athens's new airport took ATH in 2001 when Ellinikon closed.</li>
</ul>
<h2>When the code doesn't move</h2>
<p>Sometimes a city keeps the old airport open and gives the new one a fresh code. Tokyo kept {{HND}} when {{NRT}} opened, Seoul kept {{GMP}} when {{ICN}} opened, and Shanghai kept {{SHA}} at Hongqiao when {{PVG}} opened at Pudong. In those cities you need to know both codes, which is exactly the kind of thing our <a href="/play">Quick Play</a> rounds test.</p>
<p>Berlin did something different again. When Berlin Brandenburg opened in 2020 with the code {{BER}}, the old Tegel and Schönefeld airports closed, and their codes went out of use.</p>
""",
    },
    {
        "slug": "city-codes-for-cities-with-several-airports",
        "code": "NYC",
        "published": "2026-11-16",
        "title": "City codes: LON, NYC, PAR and the cities with several airports",
        "blurb": "LON isn't an airport. Neither is NYC or TYO. Here's what city codes are, the main ones, and the airports behind them.",
        "body": """
<p>Type LON into a flight search and you'll get flights to six different airports. That's because LON is a <b>city code</b>: a three-letter code that stands for a whole city rather than one airport. Big cities with more than one airport usually have one.</p>
<h2>Why city codes exist</h2>
<p>If you want to fly to London and don't mind which airport, searching each one separately is slow. A city code lets a booking site search them all at once. You'll never see a city code on a bag tag, though. Your bag always goes to a specific airport.</p>
<h2>The main city codes</h2>
<ul>
<li><b>LON</b>, London: {{LHR}}, {{LGW}}, {{STN}}, {{LTN}}, {{LCY}} and {{SEN}}.</li>
<li><b>NYC</b>, New York: {{JFK}}, {{LGA}} and {{EWR}} (Newark, across the river in New Jersey).</li>
<li><b>PAR</b>, Paris: {{CDG}} and {{ORY}}.</li>
<li><b>TYO</b>, Tokyo: {{HND}} and {{NRT}}.</li>
<li><b>OSA</b>, Osaka: {{KIX}} and {{ITM}}.</li>
<li><b>SEL</b>, Seoul: {{ICN}} and {{GMP}}.</li>
<li><b>BJS</b>, Beijing: {{PEK}} and {{PKX}}.</li>
<li><b>MIL</b>, Milan: {{MXP}} and {{LIN}}.</li>
<li><b>ROM</b>, Rome: {{FCO}} and {{CIA}}.</li>
<li><b>STO</b>, Stockholm: {{ARN}} and the city's smaller airports.</li>
<li><b>CHI</b>, Chicago: {{ORD}} and {{MDW}}.</li>
<li><b>WAS</b>, Washington: {{IAD}}, {{DCA}} and {{BWI}}.</li>
<li><b>BUE</b>, Buenos Aires: {{EZE}} and {{AEP}}.</li>
<li><b>SAO</b>, São Paulo: {{GRU}} and Congonhas.</li>
<li><b>YTO</b>, Toronto: {{YYZ}} and Billy Bishop.</li>
<li><b>YMQ</b>, Montréal: {{YUL}} and the city's other airports.</li>
</ul>
<h2>When the city code is also an airport</h2>
<p>Not every city has a separate city code. In some places the main airport's code doubles as the city code. Shanghai is a good example of how this gets confusing: {{SHA}} is the code for Hongqiao airport, but Shanghai's bigger airport is {{PVG}}, Pudong. Always check the airport, not just the city.</p>
<h2>Watch out when connecting</h2>
<p>City codes are great for finding flights but can catch you out on connections. If you land at Gatwick and your next flight leaves from Heathrow, both are "LON", but they're about an hour apart by road. The same goes for JFK and Newark, Haneda and Narita, or Orly and Charles de Gaulle. Airlines usually won't move your bag between them for you.</p>
<h2>Airports that borrow a big city's name</h2>
<p>Some airports far outside a city are marketed under its name, such as Paris Beauvais ({{BVA}}) or Brussels South Charleroi ({{CRL}}). These usually aren't part of the city code. Our guide to <a href="/guides/airports-named-for-a-city-they-are-not-in">airports named for a city they're not in</a> covers them.</p>
<h2>Test yourself</h2>
<p>Can you name all three Washington airports, or both of Tokyo's? Try a round of <a href="/play">Quick Play</a> and see how many city pairs you know.</p>
""",
    },
    {
        "slug": "airports-named-after-people",
        "code": "CDG",
        "published": "2026-11-16",
        "title": "Airports named after people, and the codes that ignore them",
        "blurb": "Charles de Gaulle got his initials. John Lennon, Chopin and Galileo didn't. Who airports are named after, and why most codes don't show it.",
        "body": """
<p>Many airports are named after a famous person, but you'd rarely know it from the code. Usually the name came after the code was set, and the code stayed. Only a few airports carry their person's initials on every bag tag.</p>
<h2>The ones that kept the name in the code</h2>
<ul>
<li>{{CDG}}: Paris Charles de Gaulle, after the French wartime leader and president. The airport opened in 1974.</li>
<li>{{JFK}}: New York, after President John F. Kennedy. The airport was Idlewild (IDL) until it was renamed in 1963, one of the rare times a code was changed to match.</li>
<li>{{LGA}}: New York LaGuardia, after Fiorello La Guardia, the city's mayor from 1934 to 1945.</li>
</ul>
<h2>Named after leaders</h2>
<ul>
<li>{{DEL}}: Delhi, Indira Gandhi International.</li>
<li>{{JNB}}: Johannesburg, O.R. Tambo, after the anti-apartheid leader Oliver Tambo.</li>
<li>{{NBO}}: Nairobi, Jomo Kenyatta, Kenya's first president.</li>
<li>{{DAR}}: Dar es Salaam, Julius Nyerere, Tanzania's first president.</li>
<li>{{TLV}}: Tel Aviv, Ben Gurion, Israel's first prime minister.</li>
<li>{{DCA}}: Washington, Ronald Reagan Washington National.</li>
<li>{{IAD}}: Washington Dulles, after John Foster Dulles, US Secretary of State.</li>
<li>{{IAH}}: Houston, George Bush Intercontinental.</li>
<li>{{MNL}}: Manila, Ninoy Aquino, the opposition politician shot at the airport in 1983.</li>
<li>{{LIS}}: Lisbon, Humberto Delgado, a general who stood against the Salazar dictatorship.</li>
</ul>
<h2>Named after artists, scientists and writers</h2>
<ul>
<li>{{LPL}}: Liverpool John Lennon. Its motto is "Above us only sky".</li>
<li>{{WAW}}: Warsaw Chopin, after the composer.</li>
<li>{{PRG}}: Prague Václav Havel, the playwright who became president.</li>
<li>{{FCO}}: Rome Fiumicino, officially Leonardo da Vinci.</li>
<li>{{PSA}}: Pisa, Galileo Galilei, who was born in the city.</li>
<li>{{VCE}}: Venice Marco Polo, after the Venetian traveller.</li>
<li>{{LYS}}: Lyon Saint-Exupéry, after the pilot and author of The Little Prince.</li>
<li>{{BEG}}: Belgrade Nikola Tesla, after the inventor.</li>
<li>{{MSY}}: New Orleans Louis Armstrong, after the jazz musician.</li>
</ul>
<h2>Named after aviators</h2>
<ul>
<li>{{SYD}}: Sydney Kingsford Smith, after the pilot who first flew across the Pacific from the US to Australia in 1928.</li>
<li>{{ORD}}: Chicago O'Hare, after the naval aviator Butch O'Hare.</li>
<li>{{SAW}}: Istanbul Sabiha Gökçen, often called the world's first female fighter pilot.</li>
<li>{{MKE}}: Milwaukee Mitchell, after General Billy Mitchell, an early champion of air power.</li>
</ul>
<h2>And a few surprises</h2>
<ul>
<li>{{SNA}}: Orange County John Wayne, after the actor.</li>
<li>{{BHD}}: George Best Belfast City, after the footballer.</li>
<li>{{LAS}}: Las Vegas Harry Reid, renamed in 2021 after the Nevada senator.</li>
<li>{{HNL}}: Honolulu Daniel K. Inouye, after Hawaii's long-serving senator.</li>
</ul>
<h2>Why the codes don't follow</h2>
<p>An airport code is built into airline systems, timetables and baggage machines, so changing it is expensive and risky. Renaming an airport is just a new sign. That's why Las Vegas stayed LAS when McCarran became Harry Reid, and why Liverpool stayed LPL. JFK is the famous exception. Read more in <a href="/guides/how-airport-codes-are-assigned">who decides airport codes</a>.</p>
""",
    },
    {
        "slug": "airline-codes-vs-airport-codes",
        "code": "BA",
        "published": "2026-11-16",
        "title": "Airline codes vs airport codes: BA, BAW and LHR",
        "blurb": "Your flight is BA117 from LHR. Air traffic control calls it Speedbird. Here's how airline codes, airport codes and call signs fit together.",
        "body": """
<p>A boarding pass mixes two kinds of code that look alike. The three letters for where you're going are an <b>airport code</b>. The two characters at the front of your flight number are an <b>airline code</b>. And behind the scenes, there's a third code and a spoken call sign as well.</p>
<h2>Two-character airline codes</h2>
<p>IATA gives each airline a two-character designator, used in flight numbers, tickets and timetables. Some are obvious, others less so:</p>
<ul>
<li>BA: British Airways</li>
<li>AA: American Airlines</li>
<li>DL: Delta</li>
<li>UA: United</li>
<li>LH: Lufthansa</li>
<li>AF: Air France</li>
<li>KL: KLM</li>
<li>EK: Emirates</li>
<li>QF: Qantas</li>
<li>SQ: Singapore Airlines</li>
<li>FR: Ryanair</li>
<li>U2: easyJet</li>
</ul>
<p>A flight number is the airline code plus a number: BA117 is a British Airways flight, and the number identifies the route and time. The same number usually runs on the same route every day.</p>
<h2>Three-letter airline codes</h2>
<p>ICAO gives airlines a three-letter code too, used in flight plans and by air traffic control. It's the code you'll see on flight-tracking apps:</p>
<ul>
<li>BAW: British Airways</li>
<li>AAL: American Airlines</li>
<li>DAL: Delta</li>
<li>UAL: United</li>
<li>DLH: Lufthansa</li>
<li>AFR: Air France</li>
<li>UAE: Emirates</li>
<li>QFA: Qantas</li>
<li>SIA: Singapore Airlines</li>
<li>RYR: Ryanair</li>
<li>EZY: easyJet</li>
</ul>
<h2>Where they clash with airport codes</h2>
<p>Because airline and airport codes are separate lists, the same letters can mean different things. DAL is Delta's airline code, and it's also the airport code for Dallas Love Field ({{DAL}}). UAE is Emirates' airline code, but it's also short for the United Arab Emirates, whose airports are {{DXB}}, {{AUH}} and others. Context tells you which one you're looking at: on a bag tag or departures board, it's an airport.</p>
<h2>Call signs</h2>
<p>On the radio, controllers don't say "BAW117". Each airline has a spoken call sign. British Airways is "Speedbird", Aer Lingus is "Shamrock", easyJet is "Easy" and Ryanair is simply "Ryanair". So BA117 becomes "Speedbird one one seven".</p>
<h2>Putting it together</h2>
<p>Take a flight from London Heathrow to New York JFK on British Airways:</p>
<ul>
<li>On your boarding pass: BA117, {{LHR}} to {{JFK}}.</li>
<li>On a flight tracker: BAW117, EGLL to KJFK.</li>
<li>On the radio: "Speedbird one one seven".</li>
</ul>
<p>Our games focus on airport codes, the ones you'll see most as a passenger. To brush up on the four-letter versions, read <a href="/guides/iata-and-icao-codes">IATA and ICAO codes explained</a>.</p>
""",
    },
    {
        "slug": "reading-your-bag-tag-and-boarding-pass",
        "code": "TAG",
        "published": "2026-11-16",
        "title": "How to read your bag tag and boarding pass",
        "blurb": "The big three letters, the ten-digit number, the barcode and the odd abbreviations. What your bag tag and boarding pass are telling you.",
        "body": """
<p>Airport codes matter most at the moment you hand over your bag. The tag the agent prints decides where it goes, and a quick check can save you a lost suitcase. Here's what's on it, and on your boarding pass.</p>
<h2>The bag tag</h2>
<p>The biggest thing on a bag tag is the three-letter code of your final destination, printed large so baggage handlers can read it at a glance. If you're connecting, the tag also lists each stop, in order, often with the flight number for each leg.</p>
<p><b>Check it before the bag disappears.</b> If you're flying to Portland, Oregon, the tag should say {{PDX}}, not PWM (Portland, Maine). If you're going to Sydney, Australia, it should say {{SYD}}. Mix-ups between similar codes do happen, and the agent's screen is the last chance to catch one.</p>
<h2>The ten-digit number</h2>
<p>Each tag carries a ten-digit number, sometimes called the licence plate. The first digit is often 0, and the next three usually identify the airline that issued the tag, using its numeric airline code. British Airways is 125, for example. The last six digits identify your bag. You'll get a matching stub, often stuck to your boarding pass. Keep it: if your bag goes missing, that number is how the airline finds it.</p>
<h2>The barcode</h2>
<p>The barcode holds the same ten-digit number. Automated sorting systems scan it and look up where the bag should go, which is why the big printed code is mainly for people and the barcode does most of the work.</p>
<h2>Your boarding pass</h2>
<p>A boarding pass packs a lot into a small space:</p>
<ul>
<li><b>From and to</b>: the airport codes for this flight, such as {{LHR}} to {{JFK}}.</li>
<li><b>Flight number</b>: the two-character airline code plus a number, such as BA117. See <a href="/guides/airline-codes-vs-airport-codes">airline codes vs airport codes</a>.</li>
<li><b>Booking reference</b>: a six-character code, also called a PNR, used to find your booking.</li>
<li><b>Seat</b> and <b>boarding group</b> or zone.</li>
<li><b>Gate</b> and <b>boarding time</b>, though gates can change, so check the screens.</li>
<li><b>Sequence number</b>: the order in which passengers checked in.</li>
<li><b>Barcode</b>: holds your name, flight, seat and booking details, so it can be scanned at security and the gate.</li>
</ul>
<h2>Abbreviations you might see</h2>
<ul>
<li><b>SSSS</b> on a US boarding pass means you've been selected for extra security screening.</li>
<li><b>INF</b> means you're travelling with an infant on your lap.</li>
<li><b>Terminal</b> codes, such as T5 at Heathrow, tell you where to go before you even reach the airport.</li>
</ul>
<h2>Why it helps to know the codes</h2>
<p>Departures boards, bag tags, connecting-flight signs and booking sites all use the same three letters. Knowing the codes for the airports you use, and the ones they're easily confused with, makes travel noticeably less stressful. Each of our <a href="/airports/">airport pages</a> lists the codes most often mixed up with it.</p>
""",
    },
    {
        "slug": "codes-from-local-names",
        "code": "MUC",
        "published": "2026-11-16",
        "title": "Codes that come from the local name: MUC, WAW and PRG",
        "blurb": "Munich is MUC because of München, Warsaw is WAW because of Warszawa. When the code follows the local spelling, not the English one.",
        "body": """
<p>Most English speakers learn city names in English. But many airport codes were chosen by people who used the local name, so the letters only make sense once you know it. Here are the most common ones in Europe, and a few that went the other way.</p>
<h2>Codes from the local name</h2>
<ul>
<li>{{MUC}}: Munich, from München. The U and C are both there.</li>
<li>{{WAW}}: Warsaw, from Warszawa, the Polish name.</li>
<li>{{PRG}}: Prague, from Praha, the Czech name.</li>
<li>{{BEG}}: Belgrade, from Beograd, the Serbian name.</li>
</ul>
<h2>Codes from the English name</h2>
<p>Plenty of codes follow the English spelling instead, which can be just as confusing if you know the city by its local name:</p>
<ul>
<li>{{VIE}}: Vienna, not Wien.</li>
<li>{{CPH}}: Copenhagen, not København: CoPenHagen.</li>
<li>{{CGN}}: Cologne, not Köln.</li>
<li>{{FLR}}: Florence, not Firenze.</li>
<li>{{VCE}}: Venice, not Venezia.</li>
<li>{{ATH}}: Athens, not Athína.</li>
<li>{{LIS}}: Lisbon, which works for Lisboa too.</li>
</ul>
<h2>Codes from a nearby place</h2>
<p>Some codes follow the town or district where the airport sits rather than the city it serves:</p>
<ul>
<li>{{FCO}}: Rome, from Fiumicino, the town on the coast.</li>
<li>{{MXP}}: Milan, from Malpensa.</li>
<li>{{ARN}}: Stockholm, from Arlanda.</li>
<li>{{KEF}}: Reykjavík, from Keflavík.</li>
<li>{{ESB}}: Ankara, from Esenboğa.</li>
<li>{{GRU}}: São Paulo, from Guarulhos.</li>
<li>{{EZE}}: Buenos Aires, from Ezeiza.</li>
<li>{{CTS}}: Sapporo, from Chitose.</li>
</ul>
<h2>Codes from an older name</h2>
<p>Others come from a name the city no longer uses, such as BOM for Bombay and PEK for Peking. We've collected those in <a href="/guides/airport-codes-from-old-names">airport codes that remember an old name</a>.</p>
<h2>A quick way to crack them</h2>
<ol>
<li>Try the English name first.</li>
<li>If that fails, try the local spelling. Central and Eastern European codes often follow it.</li>
<li>Then try the town where the airport actually is.</li>
<li>Still nothing? It may be an old name, or a code that had to <a href="/guides/codes-that-dodged-a-clash">dodge a clash</a>.</li>
</ol>
<p>Put it into practice with a Europe round of <a href="/play">Quick Play</a>.</p>
""",
    },
    {
        "slug": "airports-named-for-a-city-they-are-not-in",
        "code": "BVA",
        "published": "2026-11-16",
        "title": "Airports named for a city they're not in",
        "blurb": "Paris Beauvais, Brussels South Charleroi, Milan Bergamo. Some airports borrow a big city's name from a long way away. Here's how far.",
        "body": """
<p>Low-cost airlines love a smaller airport: cheaper fees, quicker turnarounds, less congestion. To make those airports easier to sell, they're often marketed under the name of the nearest big city, even when that city is a long bus ride away. The code is the giveaway.</p>
<h2>Europe's best-known examples</h2>
<ul>
<li>{{BVA}} <b>Paris Beauvais</b>: next to the town of Beauvais, around 80 km north of Paris. Paris's main airports are {{CDG}} and {{ORY}}.</li>
<li>{{CRL}} <b>Brussels South Charleroi</b>: in Charleroi, a separate city about 50 km south of Brussels. Brussels's own airport is {{BRU}}.</li>
<li>{{BGY}} <b>Milan Bergamo</b>: in Bergamo, about 45 km north-east of Milan. Milan's own airports are {{MXP}} and {{LIN}}.</li>
<li><b>Frankfurt-Hahn</b> (HHN): over 100 km west of Frankfurt by road, nowhere near the main airport, {{FRA}}.</li>
<li><b>Stockholm Skavsta</b> (NYO): about 100 km south of Stockholm, near Nyköping, which is where the code comes from. Stockholm's main airport is {{ARN}}.</li>
<li><b>Barcelona Girona</b> (GRO): near Girona, about 90 km north of Barcelona. Barcelona's own airport is {{BCN}}.</li>
</ul>
<h2>Closer than they sound</h2>
<p>Some airports with a borrowed name are reasonably close. London Stansted ({{STN}}) and Luton ({{LTN}}) are outside London but have fast trains. Rome Ciampino ({{CIA}}) is actually closer to central Rome than Fiumicino. Tokyo Narita ({{NRT}}) is about 60 km from the city but well served by express trains.</p>
<h2>How to spot one</h2>
<ul>
<li>Look at the code. If it doesn't match the city, and you don't recognise it as the city's main airport, look it up.</li>
<li>Check whether the airport is included in the city code (PAR, MIL, STO and so on). Airports far outside the city usually aren't.</li>
<li>Look up the transfer. A cheap flight can lose its appeal if the coach into town costs nearly as much and takes over an hour.</li>
</ul>
<h2>Why it matters for connections</h2>
<p>Booking two separate cheap flights through different airports in the same "city" is risky. Getting from Beauvais to Charles de Gaulle, or from Bergamo to Malpensa, can take two hours or more. Leave plenty of time, or keep your journey to one airport.</p>
<p>Learning the real codes helps you spot these at a glance. Our guide to <a href="/guides/city-codes-for-cities-with-several-airports">city codes</a> covers which airports really belong to which city.</p>
""",
    },
    {
        "slug": "how-to-learn-airport-codes",
        "code": "TIP",
        "published": "2026-11-16",
        "title": "How to learn airport codes fast",
        "blurb": "A practical method for memorising airport codes: start with patterns, group by region, learn the look-alikes, and practise a little every day.",
        "body": """
<p>There are thousands of airport codes, but you don't need to know them all. Most frequent flyers and quiz fans get a long way with the busiest few hundred. Here's a method that works, whether you're preparing for a quiz, a job in travel, or just want to read a departures board without squinting.</p>
<h2>1. Start with the codes that spell the name</h2>
<p>A big share of codes are simply the first letters of the city or airport: {{DXB}} Dubai, {{SIN}} Singapore, {{AMS}} Amsterdam, {{MAD}} Madrid, {{BCN}} Barcelona. Learn these first. They build confidence and give you a base to compare the odd ones against.</p>
<h2>2. Learn the patterns</h2>
<p>Once the easy codes are in, learn the rules that explain whole groups at once:</p>
<ul>
<li>Canadian codes start with Y: {{YYZ}}, {{YVR}}, {{YUL}}. See <a href="/guides/why-canadian-airports-start-with-y">why</a>.</li>
<li>US codes avoid N, K and W at the start, so Newark is {{EWR}}. See <a href="/guides/why-us-airport-codes-avoid-n-k-w">why</a>.</li>
<li>Many codes keep an old name: {{BOM}} Bombay, {{PEK}} Peking, {{ORD}} Orchard Field. See <a href="/guides/airport-codes-from-old-names">the list</a>.</li>
<li>Some follow the local name or the town next door: {{MUC}} München, {{FCO}} Fiumicino. See <a href="/guides/codes-from-local-names">more</a>.</li>
</ul>
<h2>3. Group by region</h2>
<p>Your brain remembers things in groups better than in a long list. Learn London's six airports together, then Paris, then the big US hubs, then the Gulf. When you practise, stick to one region at a time until it's solid. Our <a href="/play">Quick Play</a> rounds are split by region for exactly this reason.</p>
<h2>4. Learn the look-alikes on purpose</h2>
<p>Most mistakes come from similar codes, not unknown ones. LHR and LGW, IAD and IAH, SJO and SJU, BNA and BNE. When you learn a code, look up the codes that are one letter away from it. Every one of our <a href="/airports/">airport pages</a> has a "Don't mix it up with" list for this.</p>
<h2>5. Attach a story</h2>
<p>A code with a story is far easier to remember than three random letters. "LAX has an X because Los Angeles used to be LA" sticks. "CDG is Charles de Gaulle's initials" sticks. Even a silly link works: YUL as the "Yule" airport.</p>
<h2>6. Little and often</h2>
<p>Memory research is clear that short, spaced practice beats long cramming sessions. Five minutes a day for a month will do more than an afternoon once. That's the idea behind our <a href="/daily">Daily Departure</a>: five codes a day, a streak to keep you coming back, and a mix of easy and tricky codes.</p>
<h2>7. Test yourself in both directions</h2>
<p>Knowing that {{CPT}} is Cape Town isn't the same as knowing Cape Town's code. Practise both ways: code to airport, and airport to code. Quick Play does both.</p>
<h2>How far to go</h2>
<p>For most people, the 100 busiest airports cover nearly every trip they'll take. Quiz fans can aim for a few hundred. If you want to go further, our <a href="/airport-codes-quiz">Airport Codes Quiz</a> app has 1,000 codes, a Learn section and a list of your mistakes to review.</p>
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
    h = HEAD.format(title=e(title), desc=e(desc), path=path, schema=schema, robots="")
    return h.replace('href="/airports/" aria-current="page"', 'href="/airports/"')


def sources_block(g):
    items = "".join(f'<li><a href="{e(u)}" rel="noopener">{e(t)}</a></li>' for t, u in SOURCES[g["slug"]])
    return (f'      <section class="guide-sources" aria-labelledby="sources-title">\n'
            f'        <h2 id="sources-title">Sources</h2>\n'
            f'        <ul>{items}</ul>\n'
            f'        <p>Found a mistake? See <a href="/about#corrections">how we handle corrections</a>.</p>\n'
            f'      </section>\n')


def guide_page(g, codes):
    path = f"/guides/{g['slug']}"
    schema = schema_block({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": g["title"],
        "description": g["blurb"],
        "datePublished": g["published"],
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": AUTHOR, "url": "https://amateurgames1.com/about"},
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
        {byline(g)}
      </div>
    </section>
    <article class="wrap prose guide-body">
{link_codes(g['body'], codes)}
{sources_block(g)}
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
                 "Why Canadian airports start with Y, why LAX has an X, London's six airports and more. Guides to airport codes and how to remember them.",
                 "/guides/", schema) + f"""
  <main id="main">
    <section class="hero ap-hero">
      <div class="wrap">
        <p class="eyebrow">Guides</p>
        <h1 class="guide-title">The stories behind the codes</h1>
        <p class="lead">Why airport codes are the way they are, and how to remember them. Written and checked by Amateurgames1.</p>
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
    slugs = {g["slug"] for g in GUIDES}
    assert set(SOURCES) == slugs, f"sources missing or extra: {set(SOURCES) ^ slugs}"
    for g in GUIDES:
        for link in re.findall(r'href="/guides/([^"]+)"', g["body"]):
            assert link in slugs, f"{g['slug']}: links to missing guide {link}"
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
