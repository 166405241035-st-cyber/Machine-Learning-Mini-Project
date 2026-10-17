"""Align NASA POWER UTC hours with OpenAQ daily period boundaries."""
import csv
from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import sys

import requests

ROOT = Path(__file__).resolve().parents[1]
LAT, LON = 13.729852, 100.536501
PARAMETERS = {'T2M': 'temperature_c', 'RH2M': 'humidity_percent', 'WS10M': 'wind_speed_ms'}


def main():
    raw_dir = ROOT / 'data' / 'weather'
    raw_dir.mkdir(parents=True, exist_ok=True)
    weather = {}
    for start, end in [('20231231', '20231231'), ('20240101', '20241231'), ('20250101', '20251231')]:
        cache = raw_dir / f'power_{start}_{end}.json'
        if cache.exists():
            payload = json.loads(cache.read_text(encoding='utf-8'))
        else:
            response = requests.get('https://power.larc.nasa.gov/api/temporal/hourly/point',
                params={'parameters': ','.join(PARAMETERS), 'community': 'AG',
                        'latitude': LAT, 'longitude': LON, 'start': start, 'end': end,
                        'format': 'JSON', 'time-standard': 'UTC'}, timeout=60)
            response.raise_for_status()
            payload = response.json()
            if 'parameter' not in payload.get('properties', {}):
                raise ValueError('Missing weather parameters')
            cache.write_text(json.dumps(payload), encoding='utf-8')
        if payload['header']['time_standard'] != 'UTC':
            raise ValueError('Weather timestamps must use UTC')
        units = {k: payload['parameters'][k]['units'] for k in PARAMETERS}
        if units != {'T2M': 'C', 'RH2M': '%', 'WS10M': 'm/s'}:
            raise ValueError(f'Unexpected weather units: {units}')
        fill = payload['header']['fill_value']
        params = payload['properties']['parameter']
        for timestamp in params['T2M']:
            dt = datetime.strptime(timestamp, '%Y%m%d%H').replace(tzinfo=timezone.utc)
            values = {name: params[key].get(timestamp) for key, name in PARAMETERS.items()}
            valid = all(isinstance(v, (int, float)) and math.isfinite(v) and v != fill for v in values.values())
            if valid and 0 <= values['humidity_percent'] <= 100 and values['wind_speed_ms'] >= 0:
                weather[dt] = values
        print(f'Weather loaded: {start} to {end}', flush=True)
    pm_path = ROOT / 'data' / 'coverage' / '1304222' / 'chula_daily.csv'
    rows = []
    rejected_weather = 0
    with pm_path.open(encoding='utf-8-sig') as f:
        for item in csv.DictReader(f):
            if item['usable'] != 'True':
                continue
            start = datetime.fromisoformat(item['period_start_utc'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(item['period_end_utc'].replace('Z', '+00:00'))
            if end - start != timedelta(hours=24):
                raise ValueError('Unexpected daily period length')
            hours = [weather.get(start + timedelta(hours=i)) for i in range(24)]
            if any(v is None for v in hours):
                rejected_weather += 1
                continue
            row = {'date': item['date'], 'pm25': float(item['pm25'])}
            row.update({name: round(sum(hour[name] for hour in hours) / 24, 6) for name in PARAMETERS.values()})
            row.update({'pm25_coverage_percent': item['coverage_percent'],
                        'period_start_utc': item['period_start_utc'], 'period_end_utc': item['period_end_utc']})
            rows.append(row)
    rows.sort(key=lambda r: r['date'])
    if not rows or len({r['date'] for r in rows}) != len(rows):
        raise ValueError('Empty or duplicated dataset')
    target = ROOT / 'data' / 'processed'
    target.mkdir(parents=True, exist_ok=True)
    with (target / 'airpredict_daily.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {'station': 'Chulalongkorn Hospital', 'location_id': 5545, 'sensor_id': 1304222,
               'latitude': LAT, 'longitude': LON, 'rows': len(rows),
               'first_date': rows[0]['date'], 'last_date': rows[-1]['date'],
               'rejected_for_incomplete_weather': rejected_weather,
               'features': PARAMETERS, 'wind_height_m': 10,
               'alignment': 'NASA hourly UTC timestamps in [OpenAQ period_start_utc, period_end_utc)',
               'weather_completeness': 'Require all 24 hours; no imputation',
               'limitation': 'Weather is gridded, not a co-located station measurement. Missing PM2.5 days are seasonal; not a validated forecast.'}
    (target / 'dataset_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (requests.RequestException, ValueError, KeyError, OSError) as exc:
        print(f'Dataset preparation failed: {type(exc).__name__}. Inspect data schema or connection.')
        sys.exit(1)

