"""Find candidate PM2.5 stations near Bangkok; no secret is printed."""
import csv
import os
from pathlib import Path
import sys

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]


def main():
    load_dotenv(ROOT / ".env")
    key = os.getenv("OPENAQ_API_KEY", "").strip()
    if not key or key == "your_key_here":
        print("Set OPENAQ_API_KEY in the project .env file first.")
        return 1
    rows = []
    page = 1
    try:
        while True:
            response = requests.get(
                "https://api.openaq.org/v3/locations",
                headers={"X-API-Key": key},
                params={"iso": "TH", "bbox": "100.3,13.5,100.95,14.0",
                        "limit": 100, "page": page, "order_by": "id",
                        "sort_order": "asc", "mobile": "false"},
                timeout=30,
            )
            if response.status_code != 200:
                print(f"OpenAQ HTTP {response.status_code}. "
                      "401/403: check key; 429: wait and retry.")
                return 1
            locations = response.json()["results"]
            for location in locations:
                for sensor in location.get("sensors") or []:
                    parameter = sensor.get("parameter") or {}
                    if parameter.get("name") != "pm25":
                        continue
                    coordinates = location.get("coordinates") or {}
                    first = location.get("datetimeFirst") or {}
                    last = location.get("datetimeLast") or {}
                    rows.append({
                        "location_id": location["id"],
                        "name": location.get("name"),
                        "locality": location.get("locality"),
                        "sensor_id": sensor["id"],
                        "unit": parameter.get("units"),
                        "latitude": coordinates.get("latitude"),
                        "longitude": coordinates.get("longitude"),
                        "first_utc": first.get("utc"),
                        "last_utc": last.get("utc"),
                    })
            if len(locations) < 100:
                break
            page += 1
    except (requests.RequestException, ValueError, KeyError, TypeError):
        print("Could not read OpenAQ response. Check internet and retry.")
        return 1
    if not rows:
        print("No PM2.5 stations found in this search area.")
        return 0
    output = ROOT / "data" / "station_candidates.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Found {len(rows)} PM2.5 sensors. Saved: {output}")
    for row in rows:
        print(f"{row['location_id']} | {row['name']} | sensor={row['sensor_id']}")
    print("Candidates include nearby provinces. Verify station location and "
          "sensor-level daily coverage before selecting dates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
