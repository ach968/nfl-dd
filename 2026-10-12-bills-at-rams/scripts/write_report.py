import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'data/baseline.json').read_text())
table=['| Metric, season / last three | Buffalo | Los Angeles |','|---|---:|---:|']
for label,role,k,pct in [('Offense EPA/play','posteam','epa',False),('Offense success','posteam','success',True),('Early-down offense EPA','posteam','early_epa',False),('Early-down offense success','posteam','early_success',True),('Defense EPA allowed/play','defteam','epa',False),('Early-down defense success allowed','defteam','early_success',True),('Dropback EPA allowed','defteam','pass_epa',False),('Rush success allowed','defteam','rush_success',True),('Offense explosive rate','posteam','explosive_rate',True),('Defense explosive rate allowed','defteam','explosive_rate',True),('Offense sack rate','posteam','sack_rate',True),('Defense sack rate','defteam','sack_rate',True),('Neutral early-down PROE (pp)','posteam','neutral_early_proe',False)]:
    vals=[]
    for t in ['BUF','LA']:
        v=[d[t][w][role][k] for w in ['season','last3']]
        vals.append(' / '.join(f'{100*x:.1f}%' if pct else f'{x:+.3f}' for x in v))
    table.append('| '+label+' | '+' | '.join(vals)+' |')
report='''# Buffalo Bills at Los Angeles Rams — NFL Deep DD

Monday, October 12, 2026; SoFi Stadium, Inglewood. Kickoff 5:15 p.m. PDT / 8:15 p.m. EDT / October 13 00:15 UTC.
Pregame research window: 19:05–19:15 UTC (12:05–12:15 p.m. PDT). Exchange snapshots: 19:07:22–23 UTC. This is an early pregame report; final inactive lists are not yet verified. No bets placed.

## Executive decision

**Football lean: Rams. Betting decision: no BET; WATCH Bills +3.5 and under 54.5, PASS Rams at the current price.**

The Rams have the stronger defensive baseline and a favorable passing matchup. Buffalo has a substantially better offense than its last loss suggests, and Los Angeles has had execution and special-teams problems. A Rams win and a Bills cover can both be sensible football outcomes. These observations do not establish profitable wagers.

Direct BetUS display: Rams -3.5 (-105), Buffalo +3.5 (-115); total 54.5 (-110 each); moneylines Rams -170 / Bills +146. Limits, personal availability and house-rule details are unverified. Kalshi's public API shows Rams YES 61/62 cents and Bills YES 38/39 cents. Those moneylines imply roughly 60.8% Rams after removing sportsbook vig. The Kalshi Rams purchase needs roughly **63.65% expected winning payout probability after taker fees**, making a favorite lean insufficient. [BetUS](https://www.betus.com.pa/sportsbook/nfl/nfl-odds-week-5/), [Kalshi event API](https://api.elections.kalshi.com/trade-api/v2/events/KXNFLGAME-26OCT12BUFLAR), [fee schedule](https://kalshi.com/docs/kalshi-fee-schedule.pdf).

## Event and evidence controls

[Buffalo schedule](https://www.buffalobills.com/schedule/2026/) and [Rams schedule](https://www.therams.com/schedule/2026/) independently verify the game, venue and kickoff. Buffalo is 3-1; Los Angeles 2-2. Both last played October 4: eight calendar days to this matchup. Buffalo travels across three time zones; the Rams return from Philadelphia. The Rams' earlier Australia trip is context, not a separate automatic handicap after recovery time.

The current-looking [BettingLadies page](https://bettingladies.com/nfl/matchups/bills-vs-rams) shows Buffalo -4, an extreme Buffalo moneyline, and a 47.5 total. Those conflict with a direct sportsbook and both exchange feeds. Its inactive designation for Skyler Bell also conflicts with Buffalo's current announcement. Excluded from pricing and personnel decisions; no claim of an executable arbitrage. Local snapshots and access records are under data/.

## Quantitative baseline

Computed from a preserved [nflverse 2026 play-by-play release](https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2026.csv.gz) by scripts/baseline.py. Season means Weeks 1–4; last three means Weeks 2–4. No five-game 2026 window exists. Values are unadjusted for opponents and game state except the explicitly neutral PROE subset. Run/pass scrimmage plays exclude kneels, spikes, deleted plays and missing EPA. Dropbacks include scrambles and sacks; this is not necessarily the same denominator as PFF's EPA/pass metric.

'''+ '\n'.join(table)+'''

Success = EPA > 0. Explosive = at least 20 yards on a dropback or 10 on a designed run. Neutral early-down PROE uses first/second downs in quarters 1–3, score differential within seven, and available nflverse pass_oe; its units are percentage points. Season offensive samples: BUF 235 / LA 268 plays; defense BUF 271 / LA 239. Early-down offense: BUF 185 / LA 212. Last-three offensive samples: BUF 183 / LA 212. Neutral PROE samples are only 95 / 70 plays season and 66 / 51 last three: noisy.

Buffalo faced HOU, DET, LAC and NE. Los Angeles faced SF, NYG, DEN and PHI. The Rams' last-three improvement removes a poor opener and includes the Giants; it is not proof of a permanent elite level. The same warning applies to Buffalo's offensive decline.

Derived score baseline: BUF 31.75 scored / 26.75 allowed per game; LA 21.25 / 20.75. Last three: BUF 30.33 / 25.33; LA 26.00 / 18.67. A simple average of each offense and opposing defense gives a season total of 50.25 and last-three total of 50.17. This is an intentionally naive comparator, not a calibrated totals forecast: opponent quality, Nacua's missed games, scoring efficiency and home field matter.

Buffalo third-down offense: 24/45 (53.3%); LA 22/51 (43.1%). Third-down defense allowed BUF 22/54 (40.7%), LA 17/51 (33.3%). Red-zone offense: BUF 11/16 (68.8%), LA 8/15 (53.3%). The Rams denominator includes two possessions ending at halftime. Excluding them wrongly increases the rate to 61.5%. This was corrected and cross-checked against the official team preview. These short samples can regress substantially.

Turnovers: BUF seven giveaways / five takeaways; LA eight / three. Negative differentials may contain luck, but no fumble-recovery or turnover-worthy-play model was fitted. Penalties: BUF 30 / LA 31 flags charged in the data. FG results: BUF 6/6, LA 5/7. Four-game kicking samples are not kicker talent estimates.

Verified consistent neutral seconds/play, pressure rates, time-to-throw, CPOE analysis, exact blitz/coverage frequencies, run-block grades and yards-before-contact were not obtained. QB-hit and sack fields do not substitute for pressure rate. We do not fill those gaps with historical scheme assumptions.

## Personnel and scheme

**Buffalo:** Ed Oliver and Joshua Palmer are out. DJ Moore, Dee Alford and Landon Jackson are questionable. Benford reached full Saturday participation and is expected back opposite Maxwell Hairston; that is coach-indicated availability, not a final inactive confirmation. Skyler Bell is expected to make his debut. Palmer's absence and Moore's uncertainty broaden the WR usage distribution, rather than guaranteeing all missing targets go to one receiver. [Official injury report](https://www.buffalobills.com/news/buffalo-bills-injury-report-vs-rams-week-5).

The official [depth chart](https://www.buffalobills.com/team/depth-chart) lists DeWayne Carter behind Oliver and Bell behind Moore. Replacement snap shares and quality are unmeasured. Oliver's absence plausibly reduces interior disruption against Stafford; Alford uncertainty matters for nickel coverage. Returning Benford is a counterweight to a simple fade-the-secondary thesis.

**Rams:** Aaron Donald, Jaylen Watson and Colby Parkinson have no game designation; Quentin Lake is questionable. Donald's Saturday DNP is listed with rest/back, not an automatic absence. Terrance Ferguson remains an IR context item. [Current report](https://www.therams.com/news/rams-injury-report-week-5-2026-vs-bills-aaron-donald-colby-parkinson-and-jaylen-watson-good-to-go-for-monday-night-football). Myles Garrett is unavailable for this game under his minimum four-game IR period, which expressly includes Buffalo. This is already present in recent defensive performance and should not be deducted twice. [IR announcement](https://www.therams.com/news/mcvay-myles-garrett-knee-feeling-good-post-surgery-but-rams-not-going-to-rush-him-back-from-injured-reserve).

Projected Buffalo tackles Dawkins/Brown face Young/Stewart and a rotating interior of Turner, Fiske, Ford and Donald. Rams tackles Jackson/McClendon face Rousseau/Chubb; matchups vary with alignment and stunts, so these are not fixed one-on-one assignments. Stafford's protection has yielded a 3.5% sack rate versus Buffalo's 6.5%. Allen can scramble and create outside structure; aggressive rush lanes can open that escape route. [Rams depth chart](https://www.therams.com/team/depth-chart).

McDuffie's reported man-coverage sample is excellent but small: two catches for 14 yards on 62 snaps. Rousseau has six sacks, per the team preview. The Rams' ability to challenge outside targets raises the importance of Buffalo's quick answers, Cook and the middle of the field. Don't assume McDuffie shadows a specific receiver all night. [Rams matchup preview](https://www.therams.com/news/all-eyes-on-sofi-stadium-rams-bills-battle-week-5-monday-night-football-game-preview).

The key Rams offensive mechanism is distributing the ball among Nacua, Adams and receiving backs before Buffalo's rush arrives. Staff adjustments and personnel-group percentages remain unmeasured. New Buffalo coordinator Jim Leonhard's 2026 defense should not inherit an assumed old Buffalo zone frequency.

Buffalo's points/drive fell from 3.67 in its first two games to 2.27 in the last two. Los Angeles' average starting field position and coverage units have been weak; that creates a Buffalo path through hidden yards. These are matchup considerations, not independent guaranteed point bonuses. [Buffalo storylines](https://www.buffalobills.com/news/top-storylines-for-bills-vs-rams-week-5).

## Environment

Official NWS hourly forecast issued October 12 18:41 UTC, retrieved 19:07:22 UTC: 5 p.m. PDT **64°F, WSW 10 mph, 20% showers**; 8 p.m. **59°F, west 5 mph, 20% showers**. Gust estimate not recovered. This is an outdoor forecast at the stadium vicinity, not measured field conditions. JSON and provenance are saved. [NWS hourly API](https://api.weather.gov/gridpoints/LOX/151,41/forecast/hourly).

SoFi has a fixed roof and an indoor-outdoor design. The canopy substantially changes rain exposure; outdoor wind is not field-level wind. No weather-based under adjustment is justified from these conditions alone. [Stadium guide](https://www.sofistadium.com/plan-your-visit/a-z-guide), [stadium description](https://www.sofistadium.com/stadium/).

## Three competing scripts

| Script | Observable triggers | Usage implication | Counterargument |
|---|---|---|---|
| Rams control | Buffalo repeatedly faces long yardage; LA scores without turnovers | More Allen dropbacks/scrambles; LA can add Williams/Corum rushes later; Adams yardage may suffer from less second-half passing | Allen can convert difficult downs and erase a lead; Buffalo special teams can create short fields |
| Neutral | Buffalo early-down rushing/quick throws work; neither team gets separation | Both passing groups retain volume; Williams receiving and Buffalo middle-field targets matter | Rams red-zone stalls or penalties can keep points below a visually productive game |
| Bills control | Allen escapes pressure, Cook sustains drives, returning Benford limits explosives | More LA dropbacks; Nacua/Adams ceilings improve; BUF can reduce pace and passing volume | Oliver absence leaves a quick-response passing path; Buffalo's defense has allowed efficient dropbacks |

These scripts are conditional paths, not assigned simulated frequencies. No invented exact snap/route distributions.

## Models, fair ranges and sensitivities

No fitted regression, Monte Carlo or drive simulation was run. Therefore no seed, training set or validated out-of-sample model exists. Actual computations are descriptive play-by-play aggregation and checked market arithmetic. Opta independently published a 62.9% Rams forecast; it is a corroborating external model, not our calibration result. [Opta](https://theanalyst.com/articles/2026-week-5-nfl-predictions).

For price stress testing only, use **judgmental** ranges: Rams win 55–65% (working center 60%); Bills 35–45%; Bills +3.5 49–58%; under 54.5 48–59%. These are elicited uncertainty envelopes around the market anchor and opposing matchup cases, not statistical confidence intervals or empirically calibrated fair odds. They cannot by themselves support a BET label.

The Rams low case gives weight to Buffalo offensive talent, Benford's return, LA red-zone stalls and special teams. The high case emphasizes LA defense and Buffalo WR limitations. Removing Moore materially shifts the Bills' passing outlook but an exact percentage-point injury penalty is unsupported. Under's low case allows Rams efficiency against Buffalo's pass defense plus Allen-led scoring; its high case weights the defensive strength, recent drive trends and red-zone failures. No weather penalty is baked in.

## Market screen and decisions

EV below is profit per $1 staked for sportsbook odds; Kalshi EV is dollars per one $1-payout share. It is illustrative under the judgmental ranges. These units must not be compared directly as returns on capital.

| Candidate | Observed quote | Break-even | Stress probability | EV range | Action |
|---|---:|---:|---:|---:|---|
| Kalshi Rams YES | ask 62¢ / bid 61¢ | 63.65% | 55–65% | -8.65¢ to +1.35¢/share | PASS |
| Kalshi Bills YES | ask 39¢ / bid 38¢ | 40.67% | 35–45% | -5.67¢ to +4.33¢/share | WATCH |
| BetUS Rams ML | -170 | 62.96% | 55–65% | -12.6% to +3.2% | PASS |
| BetUS Bills ML | +146 | 40.65% | 35–45% | -13.9% to +10.7% | WATCH |
| BetUS Bills +3.5 | -115 | 53.49% | 49–58% | -8.4% to +8.4% | WATCH |
| BetUS Rams -3.5 | -105 | 51.22% | 42–51% | -18.0% to -0.4% | PASS |
| BetUS under 54.5 | -110 | 52.38% | 48–59% | -8.4% to +12.6% | WATCH |
| BetUS over 54.5 | -110 | 52.38% | 41–52% | -21.7% to -0.7% | PASS |

Kalshi displayed top-ask size: 7,062,911.37 Rams contracts; 11,566,501.03 Bills contracts. These are observed API quantities, not durable available fills. Fee calculation uses a 100-contract taker order, coefficient 0.07, multiplier 1 and centicent rounding; no settlement fee. Rams costs $63.6492 for 100 shares and Bills $40.6653. Third-party broker/funding charges are not included. Fee schedule lists NFL maker fees too, so a resting bid is not assumed free. Tie resolves at 50 cents; starts delayed beyond 48 hours resolve at fair price. Calculations approximate binary win/loss, omitting rare tie probability; that omission further argues against marginal edges.

Polymarket international books corroborate pricing: Rams 61/62¢, Bills 38/39¢; LA -3.5 47/48¢, BUF +3.5 52/53¢; over 54.5 51/52¢, under 48/49¢. Six full books are preserved. They are reference markets here: US availability is distinct from Polymarket US. Fee metadata says base_fee 1000 while the current fee page advertises an October NFL coefficient 0.03; that parameter/formula mapping was not resolved. Do not label the cheaper-looking under an executable net edge. [Market](https://polymarket.com/sports/nfl/nfl-buf-la-2026-10-13), [fees](https://polymarket.com/fees).

**Entry controls:** There is no authorized buy threshold today. For a conservative screening margin of two probability points, maximum all-in binary costs would be Rams 53¢, Bills 33¢, Bills +3.5 47¢, under 54.5 46¢. Equivalent sportsbook screening break-evens imply approximately Bills ML +204, Bills +3.5 +113, under +118. These are analytical reopen thresholds, not orders or claims such prices exist. Prices beyond them still require final lineup, rules, executable size and calibrated probabilities. A better point line (BUF +4.5 or total 55.5) requires recalculating its probability; do not reuse a +3.5/54.5 estimate.

Props and team totals:

- Adams 60+ yards at -126 (article quote): break-even 55.75%. His four-game receiving yards are 26, 195, 137, 32; targets 6, 10, 13, 9. Nacua returned last week with 12 targets, while Adams had nine but only 32 yards. Good opponent does not guarantee an over. WATCH for a verified main line and two-sided price, otherwise PASS.
- Kincaid over 3.5 catches at -215 (article quote): needs 68.25%. Season catches 5, 7, 2, 1; latest target counts 3 and 2. Absences could reverse that decline but confirmed routes/role are needed. PASS at this unverified execution quote.
- Stafford 3+ passing TDs +144 (article quote): needs 40.98%. Buffalo pass-defense weakness supports interest, but Rams red-zone conversion and rushing-TD substitution are serious counterarguments. PASS without a calibrated TD distribution. Geography-conditioned recent hit rates are selection-sensitive.
- BetUS BUF team total 24.5 O -125/U -105; LA 28.5 O/U -115. Displayed break-evens: 55.56/51.22%, 53.49/53.49%. No independent team-total distribution or house-rule verification: PASS. Alternates observed in the saved exchange metadata, but no fitted margin tails: PASS.

Article prices come from [PFF's October 12 preview](https://www.pff.com/news/bet-monday-night-football-same-game-parlay-bills-rams), not live order tickets. Props have no defensible numeric fair interval or EV here; blanks mean unavailable, not zero. Polymarket player markets may settle an inactive player's over to Under rather than voiding: venue rules cannot be imported from a sportsbook.

## Adversarial audit and catalysts

1. LA's improved defense faces a different quarterback challenge than prior opponents. Sack totals, pressure and effective coverage are separate mechanisms.
2. Buffalo's last loss is one outcome; season EPA remains strong. Conversely last-three trends are not opponent-adjusted.
3. Don't double count known Oliver/Palmer/Garrett status by applying another large penalty to market odds already reflecting it.
4. A 2024 shootout is historical context, not tonight's scoring distribution. Turnovers, return touchdowns and fourth-down swings matter.
5. Rams ML, Stafford TDs, Adams overs and LA team-total overs share exposure. Bills cover/under also interact with pace; no parlay edge was calculated.
6. Refresh Moore, Alford, Jackson and Lake at the final inactive release, usually around 3:45 p.m. PDT for this kickoff. Confirm starters and any restrictions. No unattended refresh is scheduled or promised.
7. Confirm the actual book's limits, overtime, void and inactive rules. The BetUS table is a public display, not a user-specific executable ticket.

## Reproduction and self-improvement audit

Run scripts/baseline.py, scripts/price_analysis.py, then scripts/validate_snapshot.py. Data cutoff excludes all Week 5 outcomes, even when the downloaded league file contains them. Hash and denominators are in data/baseline.json; API fetch timestamps in data/fetch-manifest.json. No previous matchup report was found, so no historical report diff is claimed. Postgame audit remains unfilled pending the result and closing market.

**Self-improvement audit:** improvement-log.md records ADOPT of primary cross-checking and of the corrected red-zone denominator in this workspace. All eight game scores matched team schedules; the corrected LA result is 8/15, consistent with its published 53% rate. Six books are uncrossed and market arithmetic checks passed. The tests establish data/process consistency, not predictive calibration. Skill source files were not modified or committed; no method deployment is claimed. Fee mapping and probability calibration remain PENDING.
'''
(ROOT/'report.md').write_text(report)
print(ROOT/'report.md')
