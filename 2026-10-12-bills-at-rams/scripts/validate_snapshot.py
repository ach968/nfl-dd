import json,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/baseline.json').read_text())
expected={'BUF':[(36,31),(41,31),(24,16),(26,29)],'LA':[(7,27),(28,6),(26,30),(24,20)]}
for team,scores in expected.items():
    assert [(g['for'],g['against']) for g in d[team]['scores']]==scores
    assert max(g['date'] for g in d[team]['scores'])<'2026-10-12'
rz=d['LA']['situational']['posteam']
assert rz['redzone_drives_n']==15
assert abs(rz['redzone_td_rate']-8/15)<1e-12
assert [g['catches'] for g in d['BUF']['usage']['D.Kincaid']['per_game']]==[5,7,2,1]
for i in range(3):
    for j in range(2):
        b=json.loads((ROOT/f'data/poly-book-{i}-{j}.json').read_text())
        assert max(float(x['price']) for x in b['bids'])<min(float(x['price']) for x in b['asks'])
runpy.run_path('/home/acheney/.agents/skills/nfl-deep-dd/scripts/market_math.py',run_name='__main__')
runpy.run_path(str(ROOT/'scripts/price_analysis.py'),run_name='__main__')
print('PASS: eight official-score matches; pregame cutoff; 8/15 RZ denominator; Kincaid chronology; six uncrossed books; market arithmetic.')
