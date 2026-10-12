import csv, gzip, json, statistics, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def num(r,k):
    try: return float(r[k])
    except (ValueError,KeyError): return 0.0
with gzip.open(ROOT/'data/pbp-2026.csv.gz','rt') as f:
    rows=[r for r in csv.DictReader(f) if r['season_type']=='REG' and num(r,'week')<=4 and r['game_date']<'2026-10-12']
def scrimmage(r):
    return r['play_type'] in ('pass','run') and not num(r,'qb_kneel') and not num(r,'qb_spike') and not num(r,'play_deleted') and r['epa']!=''
def summary(team,weeks,role):
    plays=[r for r in rows if num(r,'week') in weeks and r[role]==team and scrimmage(r)]
    early=[r for r in plays if num(r,'down') in (1,2)]
    drop=[r for r in plays if num(r,'qb_dropback')]
    rush=[r for r in plays if not num(r,'qb_dropback')]
    neutral=[r for r in early if num(r,'qtr')<=3 and abs(num(r,'score_differential'))<=7 and r['pass_oe']!='']
    return dict(n=len(plays),epa=statistics.mean(num(r,'epa') for r in plays),success=statistics.mean(num(r,'epa')>0 for r in plays),early_n=len(early),early_epa=statistics.mean(num(r,'epa') for r in early),early_success=statistics.mean(num(r,'epa')>0 for r in early),explosive_rate=statistics.mean(num(r,'yards_gained')>=(20 if num(r,'qb_dropback') else 10) for r in plays),dropbacks=len(drop),pass_epa=statistics.mean(num(r,'epa') for r in drop),sack_rate=sum(num(r,'sack') for r in drop)/len(drop),qb_hit_rate=sum(num(r,'qb_hit') for r in drop)/len(drop),rush_n=len(rush),rush_epa=statistics.mean(num(r,'epa') for r in rush),rush_success=statistics.mean(num(r,'epa')>0 for r in rush),neutral_early_n=len(neutral),neutral_early_proe=statistics.mean(num(r,'pass_oe') for r in neutral) if neutral else None)
out={}
for t in ['BUF','LA']:
    out[t]={}
    for window,weeks in [('season',[1,2,3,4]),('last3',[2,3,4])]:
        out[t][window]={role:summary(t,weeks,role) for role in ['posteam','defteam']}
    games={r['game_id']:r for r in rows if r['home_team']==t or r['away_team']==t}
    out[t]['scores']=[{'date':r['game_date'],'opponent':r['away_team'] if r['home_team']==t else r['home_team'],'for':num(r,'home_score') if r['home_team']==t else num(r,'away_score'),'against':num(r,'away_score') if r['home_team']==t else num(r,'home_score')} for r in games.values()]
    allp=[r for r in rows if r['posteam']==t and not num(r,'play_deleted')]
    out[t]['giveaways']=sum(num(r,'interception')+num(r,'fumble_lost') for r in allp)
    out[t]['takeaways']=sum(num(r,'interception')+num(r,'fumble_lost') for r in rows if r['defteam']==t and not num(r,'play_deleted'))
    out[t]['penalties']=sum(num(r,'penalty') for r in rows if r['penalty_team']==t)
    out[t]['situational']={}
    for role in ['posteam','defteam']:
        rp=[r for r in rows if r[role]==t and not num(r,'play_deleted')]
        drives={ (r['game_id'],r['fixed_drive']):r for r in rp if r['fixed_drive'] and r['fixed_drive_result'] and r['fixed_drive_result'] not in ['End of half','End of game'] }
        # Include clock-expiring red-zone possessions in the TD opportunity denominator.
        # Excluding these selectively inflates conversion efficiency.
        all_drives={(r['game_id'],r['fixed_drive']):r for r in rp if r['fixed_drive'] and r['fixed_drive_result']}
        rz=[r for r in all_drives.values() if num(r,'drive_inside20')]
        third=sum(num(r,'third_down_converted')+num(r,'third_down_failed') for r in rp)
        out[t]['situational'][role]={'drives_n':len(drives),'redzone_drives_n':len(rz),'redzone_td_rate':sum(r['fixed_drive_result']=='Touchdown' for r in rz)/len(rz) if rz else None,'third_down_n':third,'third_down_conversion':sum(num(r,'third_down_converted') for r in rp)/third if third else None,'fg_made':sum(r['field_goal_result']=='made' for r in rp),'fg_attempts':sum(num(r,'field_goal_attempt') for r in rp)}
    out[t]['usage']={}
    for name in ['D.Adams','P.Nacua','K.Shakir','D.Kincaid','D.Moore','J.Cook','K.Williams']:
        use=[r for r in allp if r['receiver_player_name']==name or r['rusher_player_name']==name]
        if use: out[t]['usage'][name]={'targets':sum(r['receiver_player_name']==name and num(r,'pass_attempt')==1 and num(r,'two_point_attempt')==0 for r in use),'receiving_yards':sum(num(r,'receiving_yards') for r in use),'rushes':sum(r['rusher_player_name']==name and num(r,'rush_attempt')==1 for r in use),'rushing_yards':sum(num(r,'rushing_yards') for r in use),'games':len(set(r['game_id'] for r in use))}
        if use:
            out[t]['usage'][name]['per_game']=[{'date':d,'targets':sum(r['receiver_player_name']==name and num(r,'pass_attempt')==1 and not num(r,'two_point_attempt') for r in use if r['game_date']==d),'catches':sum(num(r,'complete_pass') for r in use if r['game_date']==d and r['receiver_player_name']==name),'receiving_yards':sum(num(r,'receiving_yards') for r in use if r['game_date']==d)} for d in sorted(set(r['game_date'] for r in use))]
out['provenance']={'source':'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.csv.gz','sha256':hashlib.sha256((ROOT/'data/pbp-2026.csv.gz').read_bytes()).hexdigest(),'cutoff':'2026-10-12; weeks 1-4 only','excluded':'kneels, spikes, deleted plays; EPA requires nonmissing','pressure_warning':'QB hits are not pressure rate','adjustment':'unadjusted for opponent','last5':'unavailable: only 4 season games'}
(ROOT/'data/baseline.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
