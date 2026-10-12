import json,csv,math,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
maths=runpy.run_path('/home/acheney/.agents/skills/nfl-deep-dd/scripts/market_math.py')
ap=maths['american_probability'];nv=maths['no_vig']
assert abs(ap(-170)-170/270)<1e-12
assert abs(sum(nv(ap(-170),ap(146)))-1)<1e-12
def fee(c,n=100): return math.ceil(.07*n*c*(1-c)*10000-1e-10)/10000/n
assert abs(fee(.62)-.016492)<1e-12
rows=[]
def add(contract,venue,side,c,low,mid,high,action,odds=None,bid=None,depth=None,note=''):
    f=fee(c) if venue=='Kalshi' else 0
    profit=lambda p: p*(1+100/abs(odds) if odds<0 else 1+odds/100)-1 if odds else p-c-f
    rows.append(dict(event='BUF at LAR 2026-10-12',contract=contract,venue=venue,side=side,observed_utc='2026-10-12T19:07:22Z' if venue=='Kalshi' else '2026-10-12T19:06:00Z',bid=bid,ask=c,depth=depth,fee=f,slippage='0 at displayed top size; unverified account access',market_break_even=c+f,model_low=low,model_mid=mid,model_high=high,ev_low=profit(low),ev_mid=profit(mid),ev_high=profit(high),max_entry=low-.02,action=action,source_url='https://api.elections.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT12BUFLAR' if venue=='Kalshi' else 'https://www.betus.com.pa/sportsbook/nfl/nfl-odds-week-5/',notes=note+'; model interval is judgmental stress range, not calibrated; max entry means total fee-inclusive cost for binary or break-even for sportsbook'))
add('Los Angeles R wins','Kalshi','Yes',.62,.55,.60,.65,'PASS',bid=.61,depth=7062911.37,note='100-contract taker fee basis; tie pays .50; fair-price settlement on delayed start beyond 48h')
add('Buffalo wins','Kalshi','Yes',.39,.35,.40,.45,'WATCH',bid=.38,depth=11566501.03,note='100-contract taker fee basis; ranges omit rare tie; no order placed')
add('Rams win','BetUS','Rams',ap(-170),.55,.60,.65,'PASS',odds=-170,note='public sportsbook display only; account eligibility, limits, house rules unverified')
add('Bills win','BetUS','Bills',ap(146),.35,.40,.45,'WATCH',odds=146)
add('Bills +3.5 full game','BetUS','Bills',ap(-115),.49,.535,.58,'WATCH',odds=-115)
add('Rams -3.5 full game','BetUS','Rams',ap(-105),.42,.465,.51,'PASS',odds=-105)
add('Full game total 54.5','BetUS','Under',ap(-110),.48,.535,.59,'WATCH',odds=-110)
add('Full game total 54.5','BetUS','Over',ap(-110),.41,.465,.52,'PASS',odds=-110)
with (ROOT/'markets.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
prior=nv(ap(-170),ap(146))
result={'market_no_vig_rams':prior[0],'market_no_vig_bills':prior[1],'rams_break_even_kalshi':.62+fee(.62),'bills_break_even_kalshi':.39+fee(.39),'ranges':'elicited sensitivity; no fitted probability model or simulation','rows':rows}
(ROOT/'models/price-analysis.json').write_text(json.dumps(result,indent=2))
print('No-vig Rams',prior[0],'Kalshi break-even Rams',result['rams_break_even_kalshi'],'Bills',result['bills_break_even_kalshi'])
for r in rows: print(r['contract'],r['side'],r['market_break_even'],r['ev_low'],r['ev_high'])
