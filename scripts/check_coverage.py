"""Download and assess a candidate sensor; do not assume station dates are coverage."""
import calendar
import argparse
import csv
from datetime import date
import json
import math
import os
from pathlib import Path
import sys

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
SENSOR = 1304222


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sensor', type=int, default=SENSOR)
    parser.add_argument('--location', type=int, default=5545)
    args = parser.parse_args()
    load_dotenv(ROOT / '.env')
    key = os.getenv('OPENAQ_API_KEY', '').strip()
    if not key or key == 'your_key_here':
        print('Configure OPENAQ_API_KEY in .env first.')
        return 1
    records = []
    raw = []
    output = ROOT / 'data' / 'coverage' / str(args.sensor)
    output.mkdir(parents=True, exist_ok=True)
    try:
        for year in (2024, 2025):
            response = requests.get(
                f'https://api.openaq.org/v3/sensors/{args.sensor}/days',
                headers={'X-API-Key': key},
                params={'date_from': f'{year}-01-01', 'date_to': f'{year}-12-31',
                        'limit': 1000, 'page': 1}, timeout=60)
            if response.status_code != 200:
                print(f'OpenAQ HTTP {response.status_code}; no complete report produced.')
                return 1
            payload = response.json()
            results = payload['results']
            if len(results) >= 1000:
                raise ValueError('Unexpected pagination; refusing partial data')
            raw.append({'year': year, 'response': payload})
            for item in results:
                period = item.get('period') or {}
                local = (period.get('datetimeFrom') or {}).get('local')
                if not local:
                    raise ValueError('Missing local period date')
                day = date.fromisoformat(local[:10])
                if day.year != year:
                    continue
                parameter = item['parameter']
                if parameter['name'] != 'pm25' or parameter['units'] != 'µg/m³':
                    raise ValueError('Unexpected parameter or units')
                value = item.get('value')
                coverage = (item.get('coverage') or {}).get('percentCoverage')
                flagged = (item.get('flagInfo') or {}).get('hasFlags')
                usable = (isinstance(value, (int, float)) and math.isfinite(value)
                          and value >= 0 and coverage is not None and coverage >= 75
                          and flagged is False)
                records.append({'date': day.isoformat(), 'pm25': value,
                                'coverage_percent': coverage, 'has_flags': flagged,
                                'usable': usable,
                                'period_start_utc': period['datetimeFrom']['utc'],
                                'period_end_utc': period['datetimeTo']['utc']})
    except (requests.RequestException, ValueError, KeyError, TypeError):
        print('Request or response validation failed; no complete report produced.')
        return 1
    if len({r['date'] for r in records}) != len(records):
        print('Duplicate dates found; inspect response before using data.')
        return 1
    (output / 'chula_daily_raw.json').write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding='utf-8')
    with (output / 'chula_daily.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'pm25', 'coverage_percent', 'has_flags', 'usable', 'period_start_utc', 'period_end_utc'])
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: r['date']))
    report = {'sensor_id': args.sensor, 'location_id': args.location,
              'selection_rule': 'finite nonnegative PM2.5; coverage >=75%; hasFlags=false',
              'note': 'Daily periods use OpenAQ local period start. Weather alignment still requires review.',
              'years': {}, 'months': {}}
    for year in (2024, 2025):
        rows = [r for r in records if r['date'].startswith(str(year))]
        usable = sum(r['usable'] for r in rows)
        expected = 366 if calendar.isleap(year) else 365
        report['years'][str(year)] = {'expected_days': expected, 'returned_days': len(rows),
                                      'usable_days': usable, 'usable_percent': round(100 * usable / expected, 2)}
        for month in range(1, 13):
            prefix = f'{year}-{month:02d}'
            monthly = [r for r in rows if r['date'].startswith(prefix)]
            report['months'][prefix] = {'returned': len(monthly), 'usable': sum(r['usable'] for r in monthly), 'expected': calendar.monthrange(year, month)[1]}
    (output / 'coverage_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())

