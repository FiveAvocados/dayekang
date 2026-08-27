#!/usr/bin/env python3
"""Build the compact COVID-19 data asset used by the ToonNote study replicas."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


TARGET_DATES = (
    "2020-01-22",
    "2020-03-31",
    "2020-04-30",
    "2020-06-30",
    "2020-08-12",
)
FINAL_DATE = "2020-08-12"

COUNTRY_ALIASES = {
    "Mainland China": "China",
    "US": "United States",
    "UK": "United Kingdom",
    "Republic of Ireland": "Ireland",
    "Korea, South": "South Korea",
    "Republic of Korea": "South Korea",
    "Taipei and environs": "Taiwan",
    "Taiwan*": "Taiwan",
    "Congo (Brazzaville)": "Congo",
    "Congo (Kinshasa)": "Dem. Rep. Congo",
    "Republic of the Congo": "Congo",
    "Democratic Republic of the Congo": "Dem. Rep. Congo",
    "Central African Republic": "Central African Rep.",
    "Dominican Republic": "Dominican Rep.",
    "Equatorial Guinea": "Eq. Guinea",
    "Bosnia and Herzegovina": "Bosnia and Herz.",
    "North Macedonia": "Macedonia",
    "Czech Republic": "Czechia",
    "Ivory Coast": "Côte d'Ivoire",
    "Cote d'Ivoire": "Côte d'Ivoire",
    "Burma": "Myanmar",
    "West Bank and Gaza": "Palestine",
    "Eswatini": "eSwatini",
    "Vietnam": "Vietnam",
    "Viet Nam": "Vietnam",
    "East Timor": "Timor-Leste",
    "The Bahamas": "Bahamas",
    "The Gambia": "Gambia",
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "Iran (Islamic Republic of)": "Iran",
    "United Republic of Tanzania": "Tanzania",
    "South Sudan": "S. Sudan",
}

SKIP_COUNTRIES = {
    "Diamond Princess",
    "MS Zaandam",
    "Others",
    "Cruise Ship",
    "Summer Olympics 2020",
    "Winter Olympics 2022",
}


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def iso_date(raw: str) -> str:
    return datetime.strptime(raw, "%m/%d/%Y").strftime("%Y-%m-%d")


def number(raw: str) -> float:
    try:
        return float(raw or 0)
    except ValueError:
        return 0.0


def compact_number(value: float) -> int | float:
    rounded = round(value)
    return int(rounded) if abs(value - rounded) < 1e-9 else round(value, 2)


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: build_toonnote_covid_study_data.py CSV WORLD_TOPOJSON OUTPUT_JSON")

    csv_path = Path(sys.argv[1])
    world_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    world = json.loads(world_path.read_text())
    geometries = world["objects"]["countries"]["geometries"]
    by_normalized_name = {
        normalized(g["properties"]["name"]): str(g["id"]).zfill(3)
        for g in geometries
        if g.get("id") is not None
    }
    canonical_by_normalized = {
        normalized(g["properties"]["name"]): g["properties"]["name"]
        for g in geometries
        if g.get("id") is not None
    }

    daily = defaultdict(lambda: {"confirmed": 0.0, "deaths": 0.0, "recovered": 0.0})
    snapshots_by_country = {
        date: defaultdict(float) for date in TARGET_DATES
    }
    us_states = defaultdict(float)
    unmatched = set()
    rows_through_final = 0

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            date = iso_date(row["ObservationDate"])
            if date > FINAL_DATE:
                continue
            rows_through_final += 1
            confirmed = number(row["Confirmed"])
            deaths = number(row["Deaths"])
            recovered = number(row["Recovered"])
            daily[date]["confirmed"] += confirmed
            daily[date]["deaths"] += deaths
            daily[date]["recovered"] += recovered

            source_country = row["Country/Region"].strip()
            if date in snapshots_by_country and source_country not in SKIP_COUNTRIES:
                canonical = COUNTRY_ALIASES.get(source_country, source_country)
                key = normalized(canonical)
                if key in by_normalized_name:
                    snapshots_by_country[date][key] += confirmed
                else:
                    unmatched.add(source_country)

            if date == FINAL_DATE and source_country == "US":
                state = row["Province/State"].strip()
                if state:
                    us_states[state] += confirmed

    snapshots = {}
    for date, values in snapshots_by_country.items():
        snapshots[date] = {
            by_normalized_name[key]: compact_number(value)
            for key, value in sorted(values.items(), key=lambda item: by_normalized_name[item[0]])
        }

    daily_rows = []
    previous = None
    for date in sorted(daily):
        values = daily[date]
        active = max(0.0, values["confirmed"] - values["deaths"] - values["recovered"])
        row = {
            "date": date,
            "confirmed": compact_number(values["confirmed"]),
            "deaths": compact_number(values["deaths"]),
            "recovered": compact_number(values["recovered"]),
            "active": compact_number(active),
        }
        if previous is None:
            row.update({"newCases": 0, "newDeaths": 0, "newRecovered": 0})
        else:
            row.update({
                "newCases": compact_number(values["confirmed"] - previous["confirmed"]),
                "newDeaths": compact_number(values["deaths"] - previous["deaths"]),
                "newRecovered": compact_number(values["recovered"] - previous["recovered"]),
            })
        daily_rows.append(row)
        previous = values.copy()

    state_name_to_fips = {
        "Alabama": "01", "Alaska": "02", "Arizona": "04", "Arkansas": "05",
        "California": "06", "Colorado": "08", "Connecticut": "09", "Delaware": "10",
        "District of Columbia": "11", "Florida": "12", "Georgia": "13", "Hawaii": "15",
        "Idaho": "16", "Illinois": "17", "Indiana": "18", "Iowa": "19",
        "Kansas": "20", "Kentucky": "21", "Louisiana": "22", "Maine": "23",
        "Maryland": "24", "Massachusetts": "25", "Michigan": "26", "Minnesota": "27",
        "Mississippi": "28", "Missouri": "29", "Montana": "30", "Nebraska": "31",
        "Nevada": "32", "New Hampshire": "33", "New Jersey": "34", "New Mexico": "35",
        "New York": "36", "North Carolina": "37", "North Dakota": "38", "Ohio": "39",
        "Oklahoma": "40", "Oregon": "41", "Pennsylvania": "42", "Rhode Island": "44",
        "South Carolina": "45", "South Dakota": "46", "Tennessee": "47", "Texas": "48",
        "Utah": "49", "Vermont": "50", "Virginia": "51", "Washington": "53",
        "West Virginia": "54", "Wisconsin": "55", "Wyoming": "56",
        "Puerto Rico": "72",
    }
    state_values = {
        state_name_to_fips[name]: compact_number(value)
        for name, value in us_states.items()
        if name in state_name_to_fips
    }
    top_states = [
        {"name": name, "fips": state_name_to_fips[name], "confirmed": compact_number(value)}
        for name, value in sorted(us_states.items(), key=lambda item: item[1], reverse=True)
        if name in state_name_to_fips
    ][:10]

    payload = {
        "_meta": {
            "source": "Novel Corona Virus 2019 Dataset (covid_19_data.csv), derived from JHU CSSE",
            "period": [daily_rows[0]["date"], daily_rows[-1]["date"]],
            "snapshotDates": list(TARGET_DATES),
            "rowsThrough2020-08-12": rows_through_final,
            "aggregation": "Daily country and state totals are sums of the source province/state records.",
        },
        "snapshots": snapshots,
        "daily": daily_rows,
        "usStates2020-08-12": state_values,
        "topStates2020-08-12": top_states,
        "unmatchedCountries": sorted(unmatched),
        "naturalEarthNames": canonical_by_normalized,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {output_path} ({output_path.stat().st_size:,} bytes)")
    print(f"rows through {FINAL_DATE}: {rows_through_final:,}")
    print(f"unmatched country labels: {len(unmatched)}")


if __name__ == "__main__":
    main()
