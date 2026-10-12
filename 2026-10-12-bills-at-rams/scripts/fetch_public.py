import json
import urllib.request
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
def fetch(item):
    name, url = item
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NFL public research'})
        raw = urllib.request.urlopen(req, timeout=45).read()
        (DATA / name).write_bytes(raw)
        return {'name': name, 'url': url, 'access_utc': datetime.now(timezone.utc).isoformat(), 'bytes': len(raw)}
    except Exception as exc:
        return {'name': name, 'url': url, 'error': str(exc)}

event = json.loads((DATA/'polymarket-event.json').read_text())[0]
chosen = [m for m in event['markets'] if m['question'] in ['Bills vs. Rams', 'Spread: Rams (-3.5)', 'Bills vs. Rams: O/U 54.5']]
urls = [('nws-hourly.json','https://api.weather.gov/gridpoints/LOX/151,41/forecast/hourly'),
        ('kalshi-matchup.json','https://api.elections.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT12BUFLAR'),
        ('pbp-2026.csv.gz','https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.csv.gz')]
for i, m in enumerate(chosen):
    for j, token in enumerate(json.loads(m['clobTokenIds'])):
        urls.append((f'poly-book-{i}-{j}.json', 'https://clob.polymarket.com/book?token_id='+token))
        urls.append((f'poly-fee-{i}-{j}.json', 'https://clob.polymarket.com/fee-rate?token_id='+token))
(DATA/'selected-markets.json').write_text(json.dumps(chosen, indent=2))
with ThreadPoolExecutor(max_workers=6) as pool:
    result=list(pool.map(fetch, urls))
(DATA/'fetch-manifest.json').write_text(json.dumps(result, indent=2))
for r in result: print(r)
