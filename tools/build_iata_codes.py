#!/usr/bin/env python3
"""Builds assets/iata-codes.json: every airport with an IATA code, from OurAirports.

OurAirports (https://ourairports.com/data/) publishes its data in the public domain.
Run from the repo root, then rebuild the airport pages:

    python3 tools/build_iata_codes.py            # downloads the latest data
    python3 tools/build_iata_codes.py DATA_DIR   # or uses airports.csv and countries.csv from DATA_DIR
    python3 tools/build_airports.py

The JSON is loaded only by the search on /airports/ and by /airports/all-codes, so
its size doesn't slow down any other page. Only standard-library Python is needed.
"""
import csv
import io
import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "iata-codes.json"
BASE = "https://raw.githubusercontent.com/davidmegginson/ourairports-data/main/"

# OurAirports airport types, shortened for the JSON. Closed airports are left out.
KINDS = {
    "large_airport": "L",
    "medium_airport": "M",
    "small_airport": "S",
    "seaplane_base": "W",
    "heliport": "H",
}

# Friendlier names for a few countries whose official names read oddly in a list.
COUNTRY_NAMES = {
    "KR": "South Korea",
    "KP": "North Korea",
    "RU": "Russia",
    "IR": "Iran",
    "SY": "Syria",
    "LA": "Laos",
    "VN": "Vietnam",
    "BO": "Bolivia",
    "VE": "Venezuela",
    "TZ": "Tanzania",
    "MD": "Moldova",
    "MK": "North Macedonia",
    "CZ": "Czech Republic",
    "FM": "Micronesia",
    "CD": "DR Congo",
    "CG": "Republic of the Congo",
    "TW": "Taiwan",
    "BN": "Brunei",
    "CV": "Cape Verde",
    "PS": "Palestine",
}


def read(data_dir, name):
    if data_dir:
        return (Path(data_dir) / name).read_text(encoding="utf-8")
    with urllib.request.urlopen(BASE + name, timeout=120) as r:
        return r.read().decode("utf-8")


def main():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else None
    countries = {row["code"]: row["name"] for row in csv.DictReader(io.StringIO(read(data_dir, "countries.csv")))}
    countries.update(COUNTRY_NAMES)

    rows = {}
    for row in csv.DictReader(io.StringIO(read(data_dir, "airports.csv"))):
        code = row["iata_code"].strip().upper()
        kind = KINDS.get(row["type"])
        if len(code) != 3 or not code.isalpha() or not kind:
            continue
        entry = [
            code,
            " ".join(row["name"].split()),
            " ".join(row["municipality"].split()),
            countries.get(row["iso_country"], row["iso_country"]),
            kind + ("" if row["scheduled_service"] == "yes" else "-"),
        ]
        # If two open airports share a code, keep the bigger one with airline service.
        old = rows.get(code)
        rank = lambda e: ("LMSWH".index(e[4][0]), e[4].endswith("-"))
        if old is None or rank(entry) < rank(old):
            rows[code] = entry

    codes = [rows[c] for c in sorted(rows)]
    data = {
        "source": "OurAirports (ourairports.com), public domain",
        "updated": date.today().isoformat(),
        "fields": ["code", "airport", "city", "country", "kind (L large, M medium, S small, W seaplane base, H heliport; - means no scheduled airline service)"],
        "codes": codes,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {len(codes)} IATA codes to {OUT.relative_to(ROOT)} ({OUT.stat().st_size // 1024} KB).")


if __name__ == "__main__":
    main()
