from flask import Flask, render_template, redirect
from app.forms import NewPlayer, EditPlayer, NewTour, NewResult, NewOpponent, NewBattle, EditOpponent, NewHistory, Search, NewDual
from app.config import Configuration
from sqlalchemy import and_, or_,func
from collections import defaultdict
from sqlalchemy import desc
from datetime import datetime
from collections import Counter
import random


from flask_migrate import Migrate
from flask import request
from app.models import db, Player, Tour, Result, Opponent, Battle, Dual, Team, Tour,  TourTeam, RankHistory, TeamRank, TourScore, TeamRankHistory, PlayerOfDay, PositionRankHistory, PlayerSeasonStats, Season, TeamSeasonStats, TeamRosterSeason


app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
Migrate(app,db)
Cornell = "https://sportslogohistory.com/wp-content/uploads/2019/06/cornell_big_red_2002-pres.png"
Iowa = "https://storage.googleapis.com/hawkeyesports-com/2021/02/cf540990-logo-e1722875756178.png"
Iowa_State = "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/isuni.sidearmsports.com/images/responsive_2021/logo_nav.svg"
Lehigh =  "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/lehighsports.com/responsive_2020/images/svgs/logo_main2-new.svg"
Michigan ="https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/mgoblue.com/images/sng_2023/main_nav_logo.svg"
Minnesota = "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/gophersports.com/images/nextgen_2022/main_logo.svg"
Missouri= "https://loodibee.com/wp-content/uploads/Missouri_Tigers_logo.png"
Nebraska= "data:image/svg+xml,%3c?xml%20version=%271.0%27%20encoding=%27utf-8%27?%3e%3c!--%20Generator:%20Adobe%20Illustrator%2026.4.1,%20SVG%20Export%20Plug-In%20.%20SVG%20Version:%206.00%20Build%200)%20--%3e%3csvg%20version=%271.1%27%20id=%27Nebraska_N%27%20xmlns=%27http://www.w3.org/2000/svg%27%20xmlns:xlink=%27http://www.w3.org/1999/xlink%27%20x=%270px%27%20y=%270px%27%20viewBox=%270%200%20163%20152%27%20style=%27enable-background:new%200%200%20163%20152;%27%20xml:space=%27preserve%27%3e%3cstyle%20type=%27text/css%27%3e%20.st0{fill:%23FFFFFF;}%20%3c/style%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M159.1,144c-2.3,0-4.1,1.8-4.1,4s1.8,4,4,4s4-1.8,4-4S161.2,144,159.1,144z%20M159,151.2c-1.8,0-3.2-1.4-3.2-3.2%20s1.4-3.2,3.2-3.2c1.7,0,3.2,1.5,3.2,3.2C162.2,149.8,160.8,151.2,159,151.2z%27/%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M157.4,145.6h1.4c0.6,0,0.8,0,1.1,0.2c0.4,0.2,0.6,0.6,0.6,1.1c0,0.4-0.1,0.7-0.3,1c-0.1,0.2-0.3,0.2-0.6,0.4%20h-0.1l1.1,2.1h-0.8l-1-2h-0.6v2h-0.8L157.4,145.6L157.4,145.6z%20M158.6,147.7c0,0,0.3,0,0.4,0c0.4-0.1,0.6-0.3,0.6-0.8%20c0-0.3-0.1-0.5-0.4-0.6c-0.1,0-0.1,0-0.6,0h-0.4v1.4L158.6,147.7L158.6,147.7z%27/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M147,0H93h-5v5v35v5h5h5v24.8L55.2,2.3L53.7,0H51H5H0v5v35v5h5h5v62H5H0v5v35v5h5h54h5v-5v-35v-5h-5h-5V82.2%20l42.8,67.5l1.5,2.3h2.7h46h5v-5v-35v-5h-5h-5V45h5h5v-5V5V0H147z%20M150,5v35v3h-3h-7v66h7h3v3v35v3h-3h-46h-1.6l-0.9-1.4L52,75.3%20V109h7h3v3v35v3h-3H5H2v-3v-35v-3h3h7V43H5H2v-3V5V2h3h46h1.7l0.9,1.4L100,76.7V43h-7h-3v-3V5V2h3h54h3V5z%27/%3e%3c/g%3e%3cpath%20class=%27st0%27%20d=%27M103,87L103,87L51,5H5v35c0,0,7.8,0,10,0c0,3.3,0,68.7,0,72l0,0c-2.2,0-10,0-10,0v35h54v-35c0,0-7.8,0-10,0l0,0%20c0-2.6,0-47,0-47l52,82h46v-35c0,0-7.8,0-10,0l0,0c0-3.3,0-68.7,0-72c2.2,0,10,0,10,0V5H93v35c0,0,7.8,0,10,0%20C103,42.6,103,87,103,87z%27/%3e%3c/svg%3e"
NC_State= "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/unc.sidearmsports.com/images/sng_2023/main_nav_logo.svg"
Ohio_State= "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/ohiostatebuckeyes.com/images/nextgen_2023/logo_main.svg"
Oklahoma_State= "https://sportslogohistory.com/wp-content/uploads/2018/07/oklahoma_state_cowboys_2015-pres.png"
Penn_State= "https://gopsusports.com/_nuxt/logo.BDHEpLK6.svg"
Stanford= "https://gostanford.com/imgproxy/l6GXJbFV4z1yPuiCbXCePofeGNcKTlM78I9yNaTuiU4/rs:fit:1980:0:0/g:ce/q:90/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3N0YW5mb3JkLXByb2QvMjAyNC8wMy8yMC9hVXJvSkRQeEVBQzFBRE53M3M2YjBRQWNlcmd2WW9EOXRabHVsZHRrLnBuZw.png"
Virginia_Tech= "https://sportslogohistory.com/wp-content/uploads/2018/01/virginia_tech_hokies_1983-pres.png"
northern_iowa = 'https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/uni.sidearmsports.com/images/nextgen_2023/logo_main.svg'
wyoming = 'https://upload.wikimedia.org/wikipedia/commons/9/91/Wyoming_Athletics_logo.svg'
colorado = 'https://www.sdstate.edu/sites/default/files/2024-05/Jackrabbit-5%402x_1.png'
asu = 'https://logos-world.net/wp-content/uploads/2022/11/Arizona-State-Sun-Devils-Logo.png'
unc = 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Northern_Colorado_Bears_logo.svg/250px-Northern_Colorado_Bears_logo.svg.png'
rtc = 'https://sportslogohistory.com/wp-content/uploads/2022/05/north_carolina_state_wolfpack_2011-pres_a.png'
@app.route('/')
def index():
    # player1 = Player(name='',team='RTC',logo=rtc, wins=0, loss=0, points=0, img='', gold=0,silver=0,bronze=0,medal=0,badge=0, tour_points=0,rank=0,dual_points=0,d_wins=0,d_loss=0)
    players = Player.query.filter_by(active=True).order_by(Player.name.asc()).all()


    # player1 = Player.query.get()
    # player1.img = ''

    db.session.commit()
    return render_template('main_page.html', players = players)


from datetime import datetime
import random

from datetime import datetime
import random

@app.route('/dashboard')
def dashboard():
    today = datetime.now()
    today_label = today.strftime("%A, %B %d")
    pick_date = today.strftime("%Y-%m-%d")

    birthday_key = today.strftime("%B %-d")
    birthdays = Player.query.filter_by(birthday=birthday_key).all()

    all_players = Player.query.order_by(Player.id).all()
    player_map = {p.id: p for p in all_players}

    player_of_day_record = PlayerOfDay.query.filter_by(
        pick_date=pick_date
    ).first()

    if player_of_day_record:
        random_player = player_map.get(player_of_day_record.player_id)
    else:
        random_player = random.choice(all_players) if all_players else None

        if random_player:
            player_of_day_record = PlayerOfDay(
                pick_date=pick_date,
                player_id=random_player.id
            )
            db.session.add(player_of_day_record)
            db.session.commit()

    player_of_day_history_records = PlayerOfDay.query.order_by(
        PlayerOfDay.pick_date.desc()
    ).all()

    player_of_day_history = []

    for record in player_of_day_history_records:
        player = player_map.get(record.player_id)

        if player:
            player_of_day_history.append({
                "date": record.pick_date,
                "player": player
            })

    # grab only winning rows so the fight appears once
    all_matches = Opponent.query.filter_by(
        victory=True
    ).order_by(
        Opponent.id
    ).all()

    rendered_matches = []

    for match in all_matches:
        winner = player_map.get(match.player_id)
        loser = player_map.get(match.opponent_id)

        if not winner or not loser:
            continue

        rendered_matches.append({
            "winner": winner,
            "loser": loser,
            "score": match.score if match.score is not None else 0,
            "round": match.round,
            "tour_name": match.tour_name,
            "date": match.date
        })

    spotlight_match = random.choice(rendered_matches) if rendered_matches else None

    return render_template(
        "dashboard.html",
        today_label=today_label,
        birthdays=birthdays,
        random_player=random_player,
        spotlight_match=spotlight_match,
        player_of_day_history=player_of_day_history
    )

@app.route('/new_search',  methods=['GET', 'POST'])
def s_form():
    form = Search()
    search_data = form.data['name']
    if form.validate_on_submit():
        ###### search for a player
        players = []
        all_players = Player.query.all()
        for play in all_players:
            if search_data.lower() in play.name.lower():
                players.append(play)
        length = len(players)
        ###### search for a round
        history = []
        record_ids = Opponent.query.filter(and_(Opponent.round == form.data['round'], Opponent.victory == True)).all()
        for record in record_ids:
            winner = Player.query.get(record.player_id)
            loser = Player.query.get(record.opponent_id)
            history.append(
                {
                    "winner": winner,
                    "loser": loser,
                    "match": record.id,
                    'Tour_num': record.tour_name
                }
            )
        ######### organize players
        pnt_leaders = []
        if form.data['leaders'] == True:
            pnt_leaders = Player.query.order_by(Player.points.desc(), Player.wins.desc(), Player.loss).all()


        curr_leaders = []
        leaders = []
        if form.data['win_percent'] == True:
            all_players = Player.query.all()
            for player in all_players:
                bad_percent = (player.wins / (player.wins + player.loss)) * 100
                percent = round(bad_percent, 3)
                curr_leaders.append({
                    "name": player.name,
                    "img": player.img,
                    "wins": player.wins,
                    "loss": player.loss,
                    "percent": percent
                })
            leaders = sorted(curr_leaders, key=lambda x: x['percent'], reverse=True)
            print('zoooosh', leaders)


        return render_template('search_result.html', players=players, history=history, pnt_leaders=pnt_leaders, leaders=leaders)
    return render_template('search_form.html', form=form)

@app.route('/facts')
def facts():
    # CODE TO ADD NEW DUAL WEEK RESULTS
    # teams = Team.query.order_by(Team.wins.desc(), Team.points.desc(), Team.loss).all()
    # i = 1
    # week = 1
    # for team in teams:
    #     team.rank = i
    #     team_rank = TeamRank(week = week, teamId = team.id, score = team.points, rank = i)
    #     db.session.add(team_rank)
    #     i += 1
    return render_template('facts.html')


@app.route('/duals', methods=['GET', 'POST'])
def duals():
    form = NewDual()

    active_season = Season.query.filter_by(active=True).first()

    if form.validate_on_submit():
        params = {
            'home': form.data['home'].strip(),
            'away': form.data['away'].strip(),
            'hscore': form.data['hscore'],
            'ascore': form.data['ascore'],
            'week': form.data['week'],
            'winnerId': form.data['winner'],
            'season_id': active_season.id if active_season else 1
        }

        new_dual = Dual(**params)
        db.session.add(new_dual)
        db.session.commit()

        return redirect('/duals')

    selected_season = request.args.get('season', 'all')

    display_query = Dual.query
    streak_query = Dual.query

    if selected_season != 'all':
        season_id = int(selected_season)
        display_query = display_query.filter(Dual.season_id == season_id)
        streak_query = streak_query.filter(Dual.season_id == season_id)

    # For display, descending
    display_duals = display_query.order_by(Dual.id.desc()).all()

    # For streaks, chronological
    all_duals = streak_query.order_by(Dual.id.asc()).all()

    teams = Team.query.all()
    teams_by_name = {t.name.strip(): t for t in teams}

    # ---------------- STREAKS ----------------
    win_dir = {}
    win_len = {}

    for d in all_duals:
        home_name = d.home.strip()
        away_name = d.away.strip()

        if d.hscore > d.ascore:
            outcomes = [(home_name, True), (away_name, False)]
        elif d.ascore > d.hscore:
            outcomes = [(home_name, False), (away_name, True)]
        else:
            outcomes = [(home_name, None), (away_name, None)]

        for name, is_win in outcomes:
            if is_win is None:
                win_dir[name] = 0
                win_len[name] = 0
                continue

            prev_dir = win_dir.get(name, 0)
            prev_len = win_len.get(name, 0)
            current_dir = 1 if is_win else -1

            if prev_dir == current_dir:
                win_len[name] = prev_len + 1
            else:
                win_dir[name] = current_dir
                win_len[name] = 1

    win_streaks = {}

    for name, direction in win_dir.items():
        win_streaks[name] = win_len.get(name, 0) if direction == 1 else 0

    # ---------------- TEAM SEASON STATS MAP ----------------
    team_stats_by_id = {}

    if selected_season != 'all':
        season_id = int(selected_season)

        season_stats = TeamSeasonStats.query.filter_by(
            season_id=season_id
        ).all()

        team_stats_by_id = {
            stats.team_id: stats for stats in season_stats
        }

    # ---------------- BUILD ROWS ----------------
    dual_rows = []

    for d in display_duals:
        home_name = d.home.strip()
        away_name = d.away.strip()

        home_team = teams_by_name.get(home_name)
        away_team = teams_by_name.get(away_name)

        home_stats = home_team
        away_stats = away_team

        if selected_season != 'all':
            if home_team:
                home_stats = team_stats_by_id.get(home_team.id)
            if away_team:
                away_stats = team_stats_by_id.get(away_team.id)

        home_streak = win_streaks.get(home_name, 0)
        away_streak = win_streaks.get(away_name, 0)

        is_conf_game = (
            home_team is not None
            and away_team is not None
            and home_team.conf == away_team.conf
        )

        dual_rows.append({
            'dual': d,
            'home_team': home_team,
            'away_team': away_team,
            'home_stats': home_stats,
            'away_stats': away_stats,
            'home_streak': home_streak,
            'away_streak': away_streak,
            'is_conf_game': is_conf_game,
        })

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'duals.html',
        dual_rows=dual_rows,
        form=form,
        seasons=seasons,
        selected_season=selected_season
    )


@app.route('/finalize/<id>')
def finalize_dual(id):
    dual = Dual.query.get(id)
    home_team = Team.query.filter(dual.home.strip() == Team.name).one()
    away_team = Team.query.filter(dual.away.strip() == Team.name).one()
    home_team.points += dual.hscore
    away_team.points += dual.ascore
    awin = False
    hwin = False
    if dual.hscore > dual.ascore:
        home_team.wins += 1
        away_team.loss += 1
        awin = True
        db.session.commit()
    elif dual.ascore > dual.hscore:
        away_team.wins += 1
        home_team.loss += 1
        db.session.commit()
    elif dual.ascore == dual.hscore:
    # Custom-winner here
        # minn = Team.query.get(13)  # ID OF WINNER
        # isu = Team.query.get(14)   # ID OF LOSER
        # minn.wins += 1    # ADD WIN
        # isu.loss += 1     # ADD LOSS
        db.session.commit()
    return redirect('/duals')

@app.route('/finalize/week')
def finalize_week():
    week = 2 ######## BE SURE TO UPDATE EVERYTIME YOU HIT THIS ROUTE ########
    teams = Team.query.order_by(Team.wins.desc(), Team.loss, Team.points.desc()).all()
    for index, team in enumerate(teams, start=1):
        team.rank = index
    for index, team in enumerate(teams, start=1):
        new_rank = TeamRankHistory(week = week, teamId = team.id, points = 0, total = team.points, rank = index)
        db.session.add(new_rank)
    db.session.commit()
    return render_template('teams.html')




@app.route('/duals/<id>')
def one_duals(id):
    dual = Dual.query.get(id)
    dualCode = f'{dual.away.strip()} vs {dual.home.strip()}'
    away_Team = Team.query.filter(
    func.lower(func.trim(Team.name)) == dual.away.strip().lower()
).one()
    home_Team = Team.query.filter(Team.name == dual.home).one()

    home_score = dual.hscore
    away_score = dual.ascore
    hcurr = 0
    acurr = 0

    method = 'Dec'

    players = []
    records = Opponent.query.filter(and_(Opponent.tour_name == dualCode, Opponent.victory == True)).all()
    for rec in records:
        pts = 0
        if rec.score >= 1000:
            pts = 7
            method = 'Pin'
        elif rec.score >= 700:
            pts = 5
            method = 'Tech Fall'
        elif rec.score >= 400:
            pts = 4
            method = 'Major Dec'
        else:
            pts = 3
            method = 'Dec'

        result = {}
        winner = Player.query.filter(rec.player_id == Player.id).one()
        loser = Player.query.filter(rec.opponent_id == Player.id).one()

        if winner.team == dual.away:
            result['apts'] =  acurr
            result['apts'] += pts
            acurr += pts
        elif loser.team == dual.away:
            result['apts'] =  acurr

        if winner.team == dual.home:
            result['hpts'] =  hcurr
            result['hpts'] += pts
            hcurr += pts
        elif loser.team == dual.home:
            result['hpts'] =  hcurr

        result['winner'] = winner
        result['loser'] = loser
        result['score'] = rec.score
        result['method'] = method
        players.append(result)

    print(players)

    dual.ascore = acurr
    dual.hscore = hcurr
    db.session.commit()
    return render_template('one_dual.html', dual = dual,records = records, players  = players, home_score = home_score, away_score=away_score, away=away_Team, home=home_Team)



@app.route('/tournamentpage/<int:id>')
def tournamentpage(id):

    tour = TourScore.query.get_or_404(id)

    # Build player lookup
    players = Player.query.all()
    player_map = {p.id: p for p in players}

    # All tournament fights
    fights = Opponent.query.filter_by(
    tour_name=tour.name
    ).all()

    # Winner-side only so fights don't duplicate
    winning_fights = []

    for fight in fights:

        if fight.victory != True:
            continue

        winner = player_map.get(fight.player_id)
        loser = player_map.get(fight.opponent_id)

        if not winner or not loser:
            continue

        winning_fights.append({
            "winner": winner,
            "loser": loser,
            "round": fight.round,
            "score": fight.score if fight.score is not None else 0,
            "date": fight.date
        })

    # ----------------------------
    # OVERTIME MATCHES
    # ----------------------------

    overtime_fights = [
    fight for fight in winning_fights
    if fight["score"] < 0
    ]

    overtime_fights = sorted(
        overtime_fights,
        key=lambda fight: fight["score"]
    )

    # ----------------------------
    # BIGGEST / CLOSEST WIN
    # ----------------------------

    normal_wins = [
        fight for fight in winning_fights
        if fight["score"] >= 0
    ]

    biggest_win = None
    closest_win = None

    if normal_wins:
        biggest_win = max(
            normal_wins,
            key=lambda x: x["score"]
        )

        closest_win = min(
            normal_wins,
            key=lambda x: x["score"]
        )

    # ----------------------------
    # TOURNAMENT STANDINGS
    # ----------------------------

    tour_team_rows = TourTeam.query.filter_by(
        tourId=id
    ).all()

    fighter_standings = []

    for row in tour_team_rows:

        player = player_map.get(row.playerId)

        if not player:
            continue

        wins = row.wins or 0
        losses = row.loss or 0

    # skip players who did not participate
        if wins == 0 and losses == 0:
            continue

        fighter_standings.append({
        "player": player,
        "points": row.score or 0,
        "wins": wins,
        "losses": losses,
        "status": row.status
        })

    fighter_standings = sorted(
        fighter_standings,
        key=lambda x: x["points"],
        reverse=True
    )

    champion = fighter_standings[0] if fighter_standings else None

    # ----------------------------
    # BIGGEST UPSET
    # ----------------------------


    biggest_upset = None
    biggest_gap = -1

    for fight in winning_fights:
        winner_rank = fight["winner"].rank
        loser_rank = fight["loser"].rank

        if winner_rank is None or loser_rank is None:
            continue

        if winner_rank == 0 or loser_rank == 0:
            continue

        gap = winner_rank - loser_rank

        if gap <= 0:
            continue

        if gap > biggest_gap:
            biggest_gap = gap

            biggest_upset = {
            "winner": fight["winner"],
            "loser": fight["loser"],
            "winner_rank": winner_rank,
            "loser_rank": loser_rank,
            "rank_gap": gap,
            "score": fight["score"],
            "round": fight["round"]
            }

    return render_template(
        "tourpage.html",
        tour=tour,
        champion=champion,
        fighter_standings=fighter_standings,
        biggest_win=biggest_win,
        closest_win=closest_win,
        biggest_upset=biggest_upset,
        overtime_fights=overtime_fights,
        winning_fights=winning_fights
    )


@app.route('/tournament/<id>')
def single_tour(id):
    tour = Tour.query.get(id)
    return render_template('single_tournament.html', tour=tour)

############################## PLAYER  CARD ############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # away_fighters = []
    # winners = []

    # # all_records = Opponent.query.filter(and_(Opponent.player_id == player_1.id, Opponent.opponent_id == player_2.id )).all()
    # for record in records:
    #     fighter = Player.query.filter(Player.id == record.player_id).one()
    #     if fighter.team == dual.home:
    #         home_fighters.append(fighter)
    #     elif fighter.team == dual.away:
    #         away_fighters.append(fighter)
    #     if record.victory:
    #         winners.append(record)


from collections import defaultdict, Counter
from sqlalchemy import or_
champ2 = [ # 3
    'Round of 128',
    'Round of 64',
    'Round of 32',
    'Round of 16',
    'Quarter-Final',
    'Semi-Final',
    ]
cons2 = [ #1
    'Consolation Round',
    'Consolation Round 2',
    'Consolation Round 3',
    'Blood Round',
    'Cons-24',
    'Cons-48',
    'Cons-64',
    'Cons-32',
    ]
medal_round2 = [ # 4
    'Bronze Medal Match',
    '5th Place Match',
    '7th Place Match',
    '9th Place Match',
    '11th Place Match',
    '13th Place Match',
    '15th Place Match',
    'Placement Round'
    'Cons-12',
    'Cons-16',
    'Cons-Semi',
    'Cons-Quarter',
    'Round of 12',
    ]
final2 = [ 'Gold Medal Match']

@app.route('/playerStat/<id>')
def player_stats(id):
    selected_season = request.args.get('season', 'all')
    player_id = int(id)

    player = Player.query.get_or_404(player_id)

    # ---------------- RANK HISTORY ONLY FILTERED BY SEASON ----------------
    histories_query = RankHistory.query.filter(RankHistory.playerId == player_id)

    if selected_season != 'all':
        histories_query = histories_query.filter(
            RankHistory.season_id == int(selected_season)
        )

    histories = histories_query.order_by(RankHistory.id.asc()).all()

    history = []
    rank = []
    rank_points = []

    for hist in histories:
        rank.append(hist.rank or 0)
        rank_points.append(hist.score or 0)
        history.append(hist.tourId)

    if selected_season == 'all':
        rank.append(player.rank or 0)

    # ---------------- ALL-TIME WINS / LOSSES ----------------
    all_wins = Opponent.query.filter(
        Opponent.player_id == player_id,
        Opponent.victory == True
    ).all()

    all_losses = Opponent.query.filter(
        Opponent.opponent_id == player_id,
        Opponent.victory == True
    ).all()

    # ---- Team beaten most ----
    beaten_teams = Counter()

    for win in all_wins:
        opponent = Player.query.get(win.opponent_id)
        if opponent:
            beaten_teams[opponent.team] += 1

    most_beaten_team = beaten_teams.most_common(1)[0][0] if beaten_teams else None
    wins_vs_beaten_team = beaten_teams[most_beaten_team] if most_beaten_team else 0
    losses_vs_beaten_team = 0

    for loss in all_losses:
        opponent = Player.query.get(loss.player_id)
        if opponent and opponent.team == most_beaten_team:
            losses_vs_beaten_team += 1

    beaten_team = Team.query.filter(Team.name == most_beaten_team).first() if most_beaten_team else None

    # ---- Team lost to most ----
    lost_to_teams = Counter()

    for loss in all_losses:
        opponent = Player.query.get(loss.player_id)
        if opponent:
            lost_to_teams[opponent.team] += 1

    most_lost_team = lost_to_teams.most_common(1)[0][0] if lost_to_teams else None
    losses_vs_lost_team = lost_to_teams[most_lost_team] if most_lost_team else 0
    wins_vs_lost_team = 0

    for win in all_wins:
        opponent = Player.query.get(win.opponent_id)
        if opponent and opponent.team == most_lost_team:
            wins_vs_lost_team += 1

    lost_team = Team.query.filter(Team.name == most_lost_team).first() if most_lost_team else None

    # ---------------- BIGGEST WIN / LOSS ALL-TIME ----------------
    biggest_win_fight = max(
        all_wins,
        key=lambda win: win.score or 0,
        default=None
    )

    biggest_loss_fight = max(
        all_losses,
        key=lambda loss: loss.score or 0,
        default=None
    )

    if biggest_win_fight:
        win_opponent = Player.query.get(biggest_win_fight.opponent_id)
        biggest_win_info = {
            'score': biggest_win_fight.score,
            'round': biggest_win_fight.round,
            'tour_name': biggest_win_fight.tour_name,
            'opponent_name': win_opponent.name if win_opponent else 'Unknown',
            'name': win_opponent.name if win_opponent else 'Unknown',
            'opponent_id': win_opponent.id if win_opponent else '#',
            'opponent_team': win_opponent.team if win_opponent else 'Unknown',
            'image': win_opponent.img if win_opponent else '',
            'logo': win_opponent.logo if win_opponent else '',
            'rank': win_opponent.rank if win_opponent else '?'
        }
    else:
        biggest_win_info = None

    if biggest_loss_fight:
        loss_opponent = Player.query.get(biggest_loss_fight.player_id)
        biggest_loss_info = {
            'score': biggest_loss_fight.score,
            'round': biggest_loss_fight.round,
            'tour_name': biggest_loss_fight.tour_name,
            'opponent_name': loss_opponent.name if loss_opponent else 'Unknown',
            'name': loss_opponent.name if loss_opponent else 'Unknown',
            'opponent_id': loss_opponent.id if loss_opponent else '#',
            'opponent_team': loss_opponent.team if loss_opponent else 'Unknown',
            'image': loss_opponent.img if loss_opponent else '',
            'logo': loss_opponent.logo if loss_opponent else '',
            'rank': loss_opponent.rank if loss_opponent else '?'
        }
    else:
        biggest_loss_info = None

    # ---------------- BIGGEST UPSETS ALL-TIME ----------------
    biggest_upset_win_fight = min(
        all_wins,
        key=lambda win: Player.query.get(win.opponent_id).rank
        if Player.query.get(win.opponent_id) and Player.query.get(win.opponent_id).rank
        else float('inf'),
        default=None
    )

    biggest_upset_loss_fight = max(
        all_losses,
        key=lambda loss: Player.query.get(loss.player_id).rank
        if Player.query.get(loss.player_id) and Player.query.get(loss.player_id).rank
        else float('-inf'),
        default=None
    )

    if biggest_upset_win_fight:
        upset_win_opponent = Player.query.get(biggest_upset_win_fight.opponent_id)
        biggest_upset_win_info = {
            'score': biggest_upset_win_fight.score,
            'round': biggest_upset_win_fight.round,
            'tour_name': biggest_upset_win_fight.tour_name,
            'opponent_name': upset_win_opponent.name if upset_win_opponent else 'Unknown',
            'name': upset_win_opponent.name if upset_win_opponent else 'Unknown',
            'opponent_id': upset_win_opponent.id if upset_win_opponent else '#',
            'opponent_team': upset_win_opponent.team if upset_win_opponent else 'Unknown',
            'image': upset_win_opponent.img if upset_win_opponent else '',
            'logo': upset_win_opponent.logo if upset_win_opponent else '',
            'rank': upset_win_opponent.rank if upset_win_opponent else '?'
        }
    else:
        biggest_upset_win_info = None

    if biggest_upset_loss_fight:
        upset_loss_opponent = Player.query.get(biggest_upset_loss_fight.player_id)
        biggest_upset_loss_info = {
            'score': biggest_upset_loss_fight.score,
            'round': biggest_upset_loss_fight.round,
            'tour_name': biggest_upset_loss_fight.tour_name,
            'opponent_name': upset_loss_opponent.name if upset_loss_opponent else 'Unknown',
            'name': upset_loss_opponent.name if upset_loss_opponent else 'Unknown',
            'opponent_id': upset_loss_opponent.id if upset_loss_opponent else '#',
            'opponent_team': upset_loss_opponent.team if upset_loss_opponent else 'Unknown',
            'image': upset_loss_opponent.img if upset_loss_opponent else '',
            'logo': upset_loss_opponent.logo if upset_loss_opponent else '',
            'rank': upset_loss_opponent.rank if upset_loss_opponent else '?'
        }
    else:
        biggest_upset_loss_info = None

    # ---------------- BIGGEST RIVAL ALL-TIME ----------------
    all_fights = Opponent.query.filter(
        or_(
            Opponent.player_id == player_id,
            Opponent.opponent_id == player_id
        )
    ).all()

    rival_counter = Counter()

    for fight in all_fights:
        rival_id = fight.opponent_id if fight.player_id == player_id else fight.player_id
        rival_counter[rival_id] += 1

    biggest_rival_id = rival_counter.most_common(1)[0][0] if rival_counter else None
    biggest_rival = Player.query.get(biggest_rival_id) if biggest_rival_id else None

    rival_fights = [
        fight for fight in all_fights
        if (
            fight.opponent_id == biggest_rival_id and fight.player_id == player_id
        ) or (
            fight.player_id == biggest_rival_id and fight.opponent_id == player_id
        )
    ]

    rival_wins = sum(
        1 for fight in rival_fights
        if fight.player_id == player_id and fight.victory
    )

    rival_losses = sum(
        1 for fight in rival_fights
        if fight.opponent_id == player_id and fight.victory
    )

    biggest_rival_info = {
        'name': biggest_rival.name if biggest_rival else 'Unknown',
        'id': biggest_rival.id if biggest_rival else '#',
        'team': biggest_rival.team if biggest_rival else 'Unknown',
        'wins': rival_wins,
        'losses': rival_losses,
        'total_matches': rival_wins + rival_losses,
    }

    # ---------------- WIN / LOSS TYPE BREAKDOWN ALL-TIME ----------------
    front, back, medalist, master = 0, 0, 0, 0

    pins, tfalls, mdec, dec = 0, 0, 0, 0

    for win in all_wins:
        score = win.score or 0

        if score >= 1000:
            pins += 1
        elif score >= 750:
            tfalls += 1
        elif score >= 500:
            mdec += 1
        else:
            dec += 1

        if win.round in champ2:
            front += 1
        elif win.round in cons2:
            back += 1
        elif win.round in medal_round2:
            medalist += 1
        elif win.round in final2:
            master += 1

    wins = [pins, tfalls, mdec, dec]

    lpins, ltfalls, lmdec, ldec = 0, 0, 0, 0

    for loss in all_losses:
        score = loss.score or 0

        if score >= 1000:
            lpins += 1
        elif score >= 750:
            ltfalls += 1
        elif score >= 500:
            lmdec += 1
        else:
            ldec += 1

        if loss.round in champ2:
            front += 1
        elif loss.round in cons2:
            back += 1
        elif loss.round in medal_round2:
            medalist += 1
        elif loss.round in final2:
            master += 1

    losss = [lpins, ltfalls, lmdec, ldec]
    battle_type = [master, medalist, front, back]

    # ---------------- POSITION RANK HISTORY ONLY FILTERED BY SEASON ----------------
    pos_query = PositionRankHistory.query.filter(
        PositionRankHistory.player_id == player_id
    )

    if selected_season != 'all':
        pos_query = pos_query.filter(
            PositionRankHistory.season_id == int(selected_season)
        )

    position_histories = pos_query.order_by(
        PositionRankHistory.week.asc()
    ).all()

    position_weeks = []
    position_ranks = []
    position_points = []

    for pos in position_histories:
        position_weeks.append(f"Week {pos.week}")
        position_ranks.append(pos.rank or 0)
        position_points.append(pos.points or 0)
    season_records = []

    season_records = []

    for season_id in [1, 2]:
        season_wins = Opponent.query.filter(
        Opponent.player_id == player_id,
        Opponent.victory.is_(True),
        Opponent.season_id == season_id
        ).count()

        season_losses = Opponent.query.filter(
        Opponent.opponent_id == player_id,
        Opponent.victory.is_(True),
        Opponent.season_id == season_id
        ).count()

        print(f"Season {season_id}: {season_wins}-{season_losses}")

        season_records.append({
        'season': season_id,
        'wins': season_wins,
        'losses': season_losses
        })

    # ---------------- TEAM COLOR CURRENT ----------------
    color = {
        'Cornell': '#B31B1B',
        'Iowa': '#FFCD00',
        'Iowa State': '#F1BE48',
        'Lehigh': '#653600',
        'Michigan': '#00274c',
        'Minnesota': '#7A0019',
        'Missouri': '#F1B82D',
        'Nebraska': '#E41C38',
        'NC State': '#4B9CD3',
        'Ohio State': '#BB0000',
        'Oklahoma State': '#Fe5c00',
        'Penn State': '#0E2B58',
        'Stanford': '#4D4F53',
        'Virginia Tech': '#630031'
    }.get(player.team, 'Black')

    return render_template(
        'advancedStats.html',
        rank=rank,
        history=history,
        rank_points=rank_points,
        wins=wins,
        losses=losss,
        battle=battle_type,
        color=color,
        season_records=season_records,
        beaten_team=beaten_team,
        wins_vs_beaten_team=wins_vs_beaten_team,
        losses_vs_beaten_team=losses_vs_beaten_team,
        lost_team=lost_team,
        wins_vs_lost_team=wins_vs_lost_team,
        losses_vs_lost_team=losses_vs_lost_team,
        biggest_win=biggest_win_info,
        biggest_loss=biggest_loss_info,
        biggest_rival=biggest_rival,
        biggest_rival_info=biggest_rival_info,
        biggest_upset_loss_info=biggest_upset_loss_info,
        biggest_upset_win_info=biggest_upset_win_info,
        player=player,
        selected_season=selected_season,
        position_weeks=position_weeks,
        position_ranks=position_ranks,
        position_points=position_points,
    )


from flask import request
from sqlalchemy import or_

@app.route('/player/<id>')
def player_card(id):
    player = Player.query.get_or_404(id)

    selected_season = request.args.get('season', 'all')
    selected_type = request.args.get('fight_type', 'all')

    player_img = player.img

    result = Result.query.filter(or_(
        Result.first == player_img,
        Result.second == player_img,
        Result.third == player_img,
        Result.fourth == player_img,
        Result.fifth == player_img,
        Result.sixth == player_img,
        Result.seventh == player_img,
        Result.eigth == player_img,
        Result.ninth == player_img,
        Result.tenth == player_img,
        Result.eleventh == player_img,
        Result.twelfth == player_img,
        Result.thirtenth == player_img,
        Result.fourtenth == player_img,
        Result.fifthtenth == player_img,
        Result.sixtenth == player_img
    )).all()

    opponent_query = Opponent.query.filter(Opponent.player_id == id)

    if selected_season != 'all':
        opponent_query = opponent_query.filter(
        Opponent.season_id == int(selected_season)
    )

    if selected_type == 'dual':
        opponent_query = opponent_query.filter(
        Opponent.round == 'Dual'
    )

    elif selected_type == 'tournament':
        opponent_query = opponent_query.filter(
        Opponent.round != 'Dual'
    )

    opponents = opponent_query.order_by(Opponent.id.desc()).all()

    all_opponents = []

    for opp in opponents:
        person = Player.query.get(opp.opponent_id)
        all_opponents.append(person)

    return render_template(
        'player_card.html',
        player=player,
        opponents=opponents,
        all_opponents=all_opponents,
        result=result,
        player_img=player_img,
        selected_season=selected_season,
        selected_type=selected_type
    )

@app.route('/new_opponent/<int:id>',  methods=['GET', 'POST'])
def add_opponent(id):
    form = NewOpponent()
    player = Player.query.get(id)

    if form.validate_on_submit():
        opp = Player.query.filter(Player.name == form.data['name']).one()
        if form.data['victory'] == True:
            player.wins += 1
            db.session.commit()
        else:
            player.loss += 1
            db.session.commit()
        params = {
            'player_id': id,
            'opponent_id': opp.id,
            'victory': form.data['victory'],
            'tour_name': form.data['tournamnet'],
            'round': form.data['round']
        }
        new_record = Opponent(**params)
        db.session.add(new_record)
        db.session.commit()
        return render_template('redirect.html', player=player)
    return render_template('add_opponent.html',player=player, form=form)

########DELETE#########
@app.route('/delete/<id>')
def opp_delete(id):
    opponent = Opponent.query.get(id)
    player = Player.query.get(opponent.player_id)
    tourname = opponent.tour_name

    tid = 7  # <---- Change this for Current Tour!!
    fixedPnts = 1  # <---- Change this for appropriate number!!
    if opponent.victory == True:
        player.wins -= 1
        player.tour_points -= fixedPnts
        # tourData = TourScore.query.filter((TourScore.name == tourname)).one()
        # tourData.osu -= fixedPnts # <---- Change this the .team to the winners team ex: tourData.mich!
        # indvTeam = TourTeam.query.filter(and_(TourTeam.playerId == player.id, TourTeam.tourId == tid)).one()
        # indvTeam.score -= fixedPnts
        # indvTeam.wins -= 1


        # player.dual_points -= 1.5
        # player.d_wins -= 1
        # player.tour_points -= fixedPnts


        db.session.commit()
    else:
        #loserId = 84
        player.loss -= 1
        #player.d_loss -= 1
        #indvTeam = TourTeam.query.filter(and_(TourTeam.playerId == loserId, TourTeam.tourId == tid)).one()
        #indvTeam.loss -= 1
        db.session.commit()

    db.session.delete(opponent)
    db.session.commit()
    return render_template('redirect.html', player = player)



##########EDIT###########
@app.route('/record/edit/<id>', methods=['GET', 'POST'])
def edit_record(id):
    form = EditOpponent()
    opponent = Opponent.query.get(id)
    player = Player.query.get(opponent.player_id)
    if form.validate_on_submit():

        if form.data['victory'] == True and opponent.victory == False:
            player.wins += 1
            db.session.commit()
            player.loss -= 1
            db.session.commit()
        if form.data['victory'] == False and opponent.victory == True:
            player.wins -= 1
            db.session.commit()
            player.loss += 1
            db.session.commit()


        new_opp = Player.query.filter(Player.name == form.data['name']).one()
        opponent.opponent_id = new_opp.id
        opponent.victory = form.data['victory']
        opponent.tour_name = form.data['tournamnet']
        opponent.round = form.data['round']




        db.session.commit()
        return render_template('redirect.html', player=player)
    return render_template('edit_record.html',opponent=opponent, form=form)

@app.route('/success')
def success():
    return render_template('redirect.html')


from flask import request

@app.route('/leaderboards')
def leader():
    selected_season = request.args.get('season', 'all')

    if selected_season == 'all':
        players = Player.query.order_by(
            Player.tour_points.desc(),
            Player.points.desc(),
            Player.wins.desc(),
            Player.loss.asc()
        ).all()

        for index, player in enumerate(players, start=1):
            player.rank = index

        db.session.commit()

        return render_template(
            'leader.html',
            players=players,
            selected_season=selected_season
        )

    season_id = int(selected_season)

    players = db.session.query(Player, PlayerSeasonStats).join(
        PlayerSeasonStats,
        Player.id == PlayerSeasonStats.player_id
    ).filter(
        PlayerSeasonStats.season_id == season_id
    ).order_by(
        PlayerSeasonStats.tour_points.desc(),
        PlayerSeasonStats.points.desc(),
        PlayerSeasonStats.wins.desc(),
        PlayerSeasonStats.loss.asc()
    ).all()

    for index, item in enumerate(players, start=1):
        player, stats = item
        stats.rank = index

    db.session.commit()

    return render_template(
        'leader.html',
        players=players,
        selected_season=selected_season
    )



@app.route('/new_player')
def form():
    form = NewPlayer()
    return render_template('simple_form.html', form=form)



@app.route('/new_player', methods=['POST'])
def new_create():
    form = NewPlayer()
    if validate_on_submit():
        params = {
            'name': form.data['name'],
            'wins': form.data['wins'],
            'loss': form.data['loss'],
            'points': form.data['points'],
            'img': form.data['img'],
            'gold': form.data['gold'],
            'silver': form.data['silver'],
            'bronze': form.data['bronze'],
            'medal': form.data['medal'],
        }
        new_player = Player(**params)
        db.session.add(new_player)
        db.session.commit()
        return redirect('/')
    return 'Bad Data'



#################### EDIT ####################################
@app.route('/edit/medal/<id>', methods=['GET', 'POST'])
def medalform(id):
    # instantiate form
    form = EditPlayer()
    player = Player.query.get(id)
    if form.validate_on_submit():
    # send form into Jinja template (with form=form)
        player.points = form.data['points']
        player.gold = form.data['gold']
        player.silver = form.data['silver']
        player.bronze = form.data['bronze']
        player.medal = form.data['medal']
        player.badge = form.data['badge']

        db.session.commit()
        return redirect('/')
    return render_template('edit_medals.html', player=player, form=form)

#################### EDIT ####################################
@app.route('/edit/<id>', methods=['GET', 'POST'])
def eform(id):
    # instantiate form
    form = EditPlayer()
    player = Player.query.get(id)
    if form.validate_on_submit():
    # send form into Jinja template (with form=form)

        player.wins = form.data['wins']
        player.loss = form.data['loss']

        db.session.commit()
        return redirect('/')
    return render_template('edit_form.html', player=player, form=form)


#Tournamentss

from flask import request

@app.route('/tournaments')
def tournaments():
    selected_season = request.args.get('season', 'all')

    tour_query = Tour.query

    if selected_season != 'all':
        tour_query = tour_query.filter(
            Tour.season_id == int(selected_season)
        )

    tour_list = tour_query.order_by(Tour.id.desc()).all()

    data = []

    for tour in tour_list:
        tour_score_query = TourScore.query.filter_by(name=tour.name)

        if selected_season != 'all':
            tour_score_query = tour_score_query.filter_by(
                season_id=int(selected_season)
            )

        tour_score = tour_score_query.first()

        if not tour_score:
            continue

        team_scores = {
            "Penn State": tour_score.psu or 0,
            "Ohio State": tour_score.osu or 0,
            "Oklahoma State": tour_score.okst or 0,
            "Cornell": tour_score.corn or 0,
            "Lehigh": tour_score.leh or 0,
            "NC State": tour_score.ncst or 0,
            "Iowa": tour_score.iowa or 0,
            "Iowa State": tour_score.isu or 0,
            "Minnesota": tour_score.minn or 0,
            "Virginia Tech": tour_score.vt or 0,
            "Missouri": tour_score.mizz or 0,
            "Nebraska": tour_score.neb or 0,
            "Stanford": tour_score.stan or 0,
            "Michigan": tour_score.mich or 0,
            "Northern Iowa": tour_score.Northern_Iowa or 0,
            "Wyoming": tour_score.Wyoming or 0,
            "Arizona State": tour_score.Arizona_State or 0,
            "Colorado": tour_score.Colorado or 0,
            "Sacred Heart": tour_score.sh or 0
        }

        sorted_teams = sorted(
            team_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:4]

        top_teams = []

        for team_name, score in sorted_teams:
            team_instance = Team.query.filter_by(name=team_name).first()

            if team_instance:
                top_teams.append({
                    "team": team_instance.name,
                    "score": score,
                    "wins": team_instance.wins,
                    "loss": team_instance.loss,
                    "logo": team_instance.logo,
                })

        data.append({
            "tourn": tour,
            "top_teams": top_teams
        })

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'tournaments.html',
        tournaments=data,
        selected_season=selected_season,
        seasons=seasons
    )




@app.route('/new_tournament')
def tour_form():
    form = NewTour()
    return render_template('create_tour.html', form=form)

def sort_key(x):
    if x['status']:
        status = x['status'].lower()
        is_cons = 1 if status == 'cons' else 0
        return (
        is_cons,
        -x['score'],
        -x['wins'],
        x['loss']
        )

@app.route('/score/score/<int:id>/<team>')
def get_score(id, team):
    print(team)
    curr_team = Team.query.filter(Team.name == team).one()
    players = Player.query.filter(Player.team == curr_team.name).all()
    STATUS_ORDER = {"all-american": 0,"champ": 1, "cons": 2, "eliminated": 3}

    def team_sort_key(row):
        status_rank = STATUS_ORDER.get((row.get("status") or "").lower(), 99)
        points = row.get("score") or 0
        return (status_rank, -points)  # status first (asc), then points (desc)

    data = []
    for player in players:
        entry = TourTeam.query.filter(and_(TourTeam.tourId == id, TourTeam.playerId == player.id)).first()
        if entry:
            score = entry.score
            score_data = {
            'person': player,
            'score': score,
            'wins': entry.wins,
            'loss': entry.loss,
            'status': entry.status
            }
            data.append(score_data)

    data.sort(key=team_sort_key)
    return render_template('team_scorepage.html', team = curr_team, score_data=data)

@app.route('/score/<id>')
def one_tourscore(id):
    tour = TourScore.query.get(id)
    teams = Team.query.all()
    scores = sorted(
    [
        {'team': 'Penn State', 'score': tour.psu, 'logo': Penn_State, 'img':'../static/images/niah.jpeg'},
        {'team': 'Cornell', 'score': tour.corn, 'logo': "https://sportslogohistory.com/wp-content/uploads/2019/06/cornell_big_red_2002-pres.png"},
        {'team': 'Iowa', 'score': tour.iowa, 'logo': "https://storage.googleapis.com/hawkeyesports-com/2021/02/cf540990-logo-e1722875756178.png"},
        {'team': 'Iowa State', 'score': tour.isu, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/isuni.sidearmsports.com/images/responsive_2021/logo_nav.svg"},
        {'team': 'Lehigh', 'score': tour.leh, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/lehighsports.com/responsive_2020/images/svgs/logo_main2-new.svg"},
        {'team': 'Michigan', 'score': tour.mich, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/mgoblue.com/images/sng_2023/main_nav_logo.svg"},
        {'team': 'Minnesota', 'score': tour.minn, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/gophersports.com/images/nextgen_2022/main_logo.svg"},
        {'team': 'Missouri', 'score': tour.mizz, 'logo': "https://loodibee.com/wp-content/uploads/Missouri_Tigers_logo.png"},
        {'team': 'Nebraska', 'score': tour.neb, 'logo': "data:image/svg+xml,%3c?xml%20version=%271.0%27%20encoding=%27utf-8%27?%3e%3c!--%20Generator:%20Adobe%20Illustrator%2026.4.1,%20SVG%20Export%20Plug-In%20.%20SVG%20Version:%206.00%20Build%200)%20--%3e%3csvg%20version=%271.1%27%20id=%27Nebraska_N%27%20xmlns=%27http://www.w3.org/2000/svg%27%20xmlns:xlink=%27http://www.w3.org/1999/xlink%27%20x=%270px%27%20y=%270px%27%20viewBox=%270%200%20163%20152%27%20style=%27enable-background:new%200%200%20163%20152;%27%20xml:space=%27preserve%27%3e%3cstyle%20type=%27text/css%27%3e%20.st0{fill:%23FFFFFF;}%20%3c/style%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M159.1,144c-2.3,0-4.1,1.8-4.1,4s1.8,4,4,4s4-1.8,4-4S161.2,144,159.1,144z%20M159,151.2c-1.8,0-3.2-1.4-3.2-3.2%20s1.4-3.2,3.2-3.2c1.7,0,3.2,1.5,3.2,3.2C162.2,149.8,160.8,151.2,159,151.2z%27/%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M157.4,145.6h1.4c0.6,0,0.8,0,1.1,0.2c0.4,0.2,0.6,0.6,0.6,1.1c0,0.4-0.1,0.7-0.3,1c-0.1,0.2-0.3,0.2-0.6,0.4%20h-0.1l1.1,2.1h-0.8l-1-2h-0.6v2h-0.8L157.4,145.6L157.4,145.6z%20M158.6,147.7c0,0,0.3,0,0.4,0c0.4-0.1,0.6-0.3,0.6-0.8%20c0-0.3-0.1-0.5-0.4-0.6c-0.1,0-0.1,0-0.6,0h-0.4v1.4L158.6,147.7L158.6,147.7z%27/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cpath%20class=%27st0%27%20d=%27M147,0H93h-5v5v35v5h5h5v24.8L55.2,2.3L53.7,0H51H5H0v5v35v5h5h5v62H5H0v5v35v5h5h54h5v-5v-35v-5h-5h-5V82.2%20l42.8,67.5l1.5,2.3h2.7h46h5v-5v-35v-5h-5h-5V45h5h5v-5V5V0H147z%20M150,5v35v3h-3h-7v66h7h3v3v35v3h-3h-46h-1.6l-0.9-1.4L52,75.3%20V109h7h3v3v35v3h-3H5H2v-3v-35v-3h3h7V43H5H2v-3V5V2h3h46h1.7l0.9,1.4L100,76.7V43h-7h-3v-3V5V2h3h54h3V5z%27/%3e%3c/g%3e%3cpath%20class=%27st0%27%20d=%27M103,87L103,87L51,5H5v35c0,0,7.8,0,10,0c0,3.3,0,68.7,0,72l0,0c-2.2,0-10,0-10,0v35h54v-35c0,0-7.8,0-10,0l0,0%20c0-2.6,0-47,0-47l52,82h46v-35c0,0-7.8,0-10,0l0,0c0-3.3,0-68.7,0-72c2.2,0,10,0,10,0V5H93v35c0,0,7.8,0,10,0%20C103,42.6,103,87,103,87z%27/%3e%3c/svg%3e"},
        {'team': 'NC State', 'score': tour.ncst, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/unc.sidearmsports.com/images/sng_2023/main_nav_logo.svg"},
        {'team': 'Ohio State', 'score': tour.osu, 'logo': "https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/ohiostatebuckeyes.com/images/nextgen_2023/logo_main.svg"},
        {'team': 'Oklahoma State', 'score': tour.okst, 'logo': "https://sportslogohistory.com/wp-content/uploads/2018/07/oklahoma_state_cowboys_2015-pres.png"},
        {'team': 'Stanford', 'score': tour.stan, 'logo': "https://gostanford.com/imgproxy/l6GXJbFV4z1yPuiCbXCePofeGNcKTlM78I9yNaTuiU4/rs:fit:1980:0:0/g:ce/q:90/aHR0cHM6Ly9zdG9yYWdlLmdvb2dsZWFwaXMuY29tL3N0YW5mb3JkLXByb2QvMjAyNC8wMy8yMC9hVXJvSkRQeEVBQzFBRE53M3M2YjBRQWNlcmd2WW9EOXRabHVsZHRrLnBuZw.png"},
        {'team': 'Virginia Tech', 'score': tour.vt, 'logo': "https://sportslogohistory.com/wp-content/uploads/2018/01/virginia_tech_hokies_1983-pres.png"},
        {'team': 'Northern Iowa', 'score': tour.Northern_Iowa, 'logo':'https://dxbhsrqyrr690.cloudfront.net/sidearm.nextgen.sites/uni.sidearmsports.com/images/nextgen_2023/logo_main.svg'},
        {'team': 'Wyoming', 'score': tour.Wyoming, 'logo':'https://sportslogohistory.com/wp-content/uploads/2024/05/wyoming_cowboys_1986-2007.png'},
        {'team': 'Arizona State', 'score': tour.Arizona_State, 'logo':'https://storage.googleapis.com/statbroadcast-prod/2024/09/04/97c7abc1-17cc-47c6-8143-e4856a3eaf06.png'},
        {'team': 'Colorado', 'score': tour.Colorado, 'logo':'https://www.sdstate.edu/sites/default/files/2024-05/Jackrabbit-5%402x_1.png'},
        {'team': 'Sacred Heart', 'score': tour.sh, 'logo':'https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Northern_Colorado_Bears_logo.svg/250px-Northern_Colorado_Bears_logo.svg.png'}
    ],
    key=lambda x: x['score'],
    reverse=True
)

    return render_template('team_score.html', scores=scores, tour=tour, id=id)


@app.route('/new_tournament', methods=['POST'])
def  new_tour():
    form = NewTour()
    if form.validate_on_submit():
        params = {
            'link': form.data['link'],
            'name': form.data['name'],
            'date': form.data['date'],
        }
        score = {
             'name' : form.data['name'],
             'psu': 0,
             'osu': 0,
             'okst': 0,
             'corn': 0,
             'leh': 0,
             'ncst': 0,
             'iowa': 0,
             'isu': 0,
             'minn': 0,
             'vt': 0,
             'mizz': 0,
             'neb': 0,
             'stan': 0,
             'mich': 0,
             'Northern_Iowa': 0,
             'Wyoming': 0,
             'Arizona_State': 0,
             'Colorado':0,
             'sh': 0
        }
        new_tourn = Tour(**params)
        new_score = TourScore(**score)
        db.session.add(new_tourn)
        db.session.add(new_score)
        db.session.commit()
        for i in range(257):
            newPlayer = TourTeam(tourId = new_tourn.id, playerId = i + 1, score = 0, status='Champ')
            db.session.add(newPlayer)
            db.session.commit()
        return redirect('/tournaments')
    return 'Bad Data'


##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Results @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@app.route('/results')
def result():
    all_results = Result.query.all()
    results = list(reversed(all_results))
    return render_template('results.html', results = results)

@app.route('/new_result')
def rform():
    form = NewResult()
    return render_template('create_result.html', form=form)



from collections import defaultdict
from sqlalchemy import func

@app.route('/playoffs')
def playoffs():
    teams = Team.query.all()

    # Group teams by conference
    conferences = defaultdict(list)
    for t in teams:
        conferences[t.conf].append(t)

    # Sort: most wins, then most points, then name
    def sort_key(t):
        return (-(t.wins or 0), -(t.points or 0), (t.name or ""))

    # Fixed order for the columns
    conference_order = ['North', 'South', 'East', 'West']

    conf_standings = {}
    conference_winner_ids = set()
    division_winners = []

    for conf in conference_order:
        conf_teams = conferences.get(conf, [])
        sorted_teams = sorted(conf_teams, key=sort_key)
        conf_standings[conf] = sorted_teams

        if sorted_teams:
            winner = sorted_teams[0]
            conference_winner_ids.add(winner.id)
            division_winners.append(winner)

    # Wildcards: next 3 best teams overall (excluding conf winners)
    remaining_teams = [t for t in teams if t.id not in conference_winner_ids]
    remaining_sorted = sorted(remaining_teams, key=sort_key)
    wildcards = remaining_sorted[:3]
    wildcard_ids = {t.id for t in wildcards}

    # Seed division winners 1–4 (best overall = #1)
    seeded_division_winners = sorted(division_winners, key=sort_key)

    playoff_seeds = []
    seed_num = 1
    for team in seeded_division_winners:
        playoff_seeds.append({'seed': seed_num, 'team': team})
        seed_num += 1

    # Seed wildcards 5–7
    for team in wildcards:
        playoff_seeds.append({'seed': seed_num, 'team': team})
        seed_num += 1

    # Build matchups: 2 vs 7, 3 vs 6, 4 vs 5
    matchups = []
    if len(playoff_seeds) >= 7:
        matchups = [
            {'high': playoff_seeds[1], 'low': playoff_seeds[6]},  # 2 vs 7
            {'high': playoff_seeds[2], 'low': playoff_seeds[5]},  # 3 vs 6
            {'high': playoff_seeds[3], 'low': playoff_seeds[4]},  # 4 vs 5
        ]

    return render_template(
        'playoff.html',
        conf_standings=conf_standings,
        conference_order=conference_order,
        conference_winner_ids=conference_winner_ids,
        wildcard_ids=wildcard_ids,
        wildcards=wildcards,
        playoff_seeds=playoff_seeds,
        matchups=matchups,
    )


from flask import request

@app.route('/teams')
def teams():
    selected_season = request.args.get('season', 'all')

    if selected_season == 'all':
        teams = Team.query.order_by(
            Team.wins.desc(),
            Team.loss.asc(),
            Team.points.desc()
        ).all()

    else:
        season_id = int(selected_season)

        teams = db.session.query(Team, TeamSeasonStats).join(
            TeamSeasonStats,
            Team.id == TeamSeasonStats.team_id
        ).filter(
            TeamSeasonStats.season_id == season_id
        ).order_by(
            TeamSeasonStats.wins.desc(),
            TeamSeasonStats.loss.asc(),
            TeamSeasonStats.points.desc()
        ).all()

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'teams.html',
        teams=teams,
        selected_season=selected_season,
        seasons=seasons
    )


from flask import request
from sqlalchemy import or_

@app.route('/teams/<id>')
def one_team(id):
    selected_season = request.args.get('season', 'all')
    team = Team.query.get_or_404(id)

    # ---------------- TEAM STATS ----------------
    if selected_season == 'all':
        stats = team
    else:
        stats = TeamSeasonStats.query.filter_by(
            team_id=team.id,
            season_id=int(selected_season)
        ).first()

        if not stats:
            stats = {
                "wins": 0,
                "loss": 0,
                "points": 0,
                "tour_points": 0,
                "rank": 0
            }

    # ---------------- DUAL HISTORY ----------------
    opponents_query = Dual.query.filter(
        or_(
            Dual.home == team.name,
            Dual.away == team.name
        )
    )

    if selected_season != 'all':
        opponents_query = opponents_query.filter(
            Dual.season_id == int(selected_season)
        )

    opponents = opponents_query.all()

    # ---------------- TEAM RANK HISTORY ----------------
    rank_query = TeamRankHistory.query.filter_by(teamId=id)

    if selected_season != 'all':
        rank_query = rank_query.filter(
            TeamRankHistory.season_id == int(selected_season)
        )

    rank_objs = rank_query.order_by(
        TeamRankHistory.week.asc(),
        TeamRankHistory.id.asc()
    ).all()

    ranks = [{'week': r.week, 'rank': r.rank} for r in rank_objs]

    # ---------------- TEAM COLOR ----------------
    color = {
        'Cornell': '#B31B1B',
        'Iowa': '#FFCD00',
        'Iowa State': '#F1BE48',
        'Lehigh': '#653600',
        'Michigan': '#00274c',
        'Minnesota': '#7A0019',
        'Missouri': '#F1B82D',
        'Nebraska': '#E41C38',
        'NC State': '#4B9CD3',
        'Ohio State': '#BB0000',
        'Oklahoma State': '#Fe5c00',
        'Penn State': '#0E2B58',
        'Stanford': '#4D4F53',
        'Virginia Tech': '#630031'
    }.get(team.name, 'Black')

    # ---------------- ROSTER / RADAR PLAYERS ----------------
    if selected_season == 'all':
        players_raw = Player.query.filter(Player.team == team.name).all()

        players = [{
            'name': p.name,
            'points': p.dual_points or 0
        } for p in players_raw]

    else:
        roster_rows = TeamRosterSeason.query.filter_by(
            team_id=team.id,
            season_id=int(selected_season)
        ).all()

        players = []

        for row in roster_rows:
            player = Player.query.get(row.player_id)

            if player:
                season_stats = PlayerSeasonStats.query.filter_by(
                    player_id=player.id,
                    season_id=int(selected_season)
                ).first()

                players.append({
                    'name': player.name,
                    'points': season_stats.dual_points if season_stats else 0
                })

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'team_rec.html',
        team=team,
        stats=stats,
        opponents=opponents,
        ranks=ranks,
        color=color,
        players=players,
        seasons=seasons,
        selected_season=selected_season
    )



@app.route('/team_rec/<id>')
def one_team_rec(id):
    selected_season = request.args.get('season', 'all')

    team = Team.query.get_or_404(id)

    opponents_query = Dual.query.filter(
        or_(
            Dual.home == team.name,
            Dual.away == team.name
        )
    )

    if selected_season != 'all':
        opponents_query = opponents_query.filter(
            Dual.season_id == int(selected_season)
        )

    opponents = opponents_query.all()

    if selected_season == 'all':
        players = Player.query.filter(
            Player.team == team.name
        ).order_by(
            Player.tour_points.desc()
        ).all()

    else:
        roster_rows = TeamRosterSeason.query.filter_by(
            team_id=team.id,
            season_id=int(selected_season)
        ).all()

        players = []

        for row in roster_rows:
            player = Player.query.get(row.player_id)

            if not player:
                continue

            stats = PlayerSeasonStats.query.filter_by(
                player_id=player.id,
                season_id=int(selected_season)
            ).first()

            players.append({
                "player": player,
                "stats": stats,
                "position": row.position
            })

        players.sort(
            key=lambda row: row["stats"].tour_points if row["stats"] else 0,
            reverse=True
        )

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'single_team.html',
        team=team,
        opponents=opponents,
        players=players,
        selected_season=selected_season,
        seasons=seasons
    )


@app.route('/new_result', methods=['POST'])
def new_result():
    form = NewResult()
    if form.validate_on_submit():
        player1 = Player.query.filter(form.data['first'] == Player.name).one()
        player_img = player1.img
        player1.points += 25
        player1.gold += 1

        player2 = Player.query.filter(form.data['second'] == Player.name).one()
        player_img2 = player2.img
        player2.points += 21
        player2.silver += 1

        player3 = Player.query.filter(form.data['third'] == Player.name).one()
        player_img3 = player3.img
        player3.points += 18
        player3.bronze += 1

        player4 = Player.query.filter(form.data['fourth'] == Player.name).one()
        player_img4 = player4.img
        player4.points += 15
        player4.medal += 1

        player5 = Player.query.filter(form.data['fifth'] == Player.name).one()
        player_img5 = player5.img
        player5.points += 14
        player5.medal += 1

        player6 = Player.query.filter(form.data['sixth'] == Player.name).one()
        player_img6 = player6.img
        player6.points += 12
        player6.medal += 1

        player7 = Player.query.filter(form.data['seventh'] == Player.name).one()
        player_img7 = player7.img
        player7.points += 11
        player7.medal += 1

        player8 = Player.query.filter(form.data['eigth'] == Player.name).one()
        player_img8 = player8.img
        player8.points += 10
        player8.medal += 1

        player9 = Player.query.filter(form.data['ninth'] == Player.name).one()
        player_img9 = player9.img
        player9.points += 9
        player9.badge += 1

        player10 = Player.query.filter(form.data['tenth'] == Player.name).one()
        player_img10 = player10.img
        player10.points += 8
        player10.badge += 1

        player11 = Player.query.filter(form.data['eleventh'] == Player.name).one()
        player_img11 = player11.img
        player11.points += 7
        player11.badge += 1

        player12 = Player.query.filter(form.data['twelfth'] == Player.name).one()
        player_img12 = player12.img
        player12.points += 6
        player12.badge += 1

        player13 = Player.query.filter(form.data['thirtenth'] == Player.name).one()
        player_img13 = player13.img
        player13.points += 5
        player13.badge += 1

        player14 = Player.query.filter(form.data['fourtenth'] == Player.name).one()
        player_img14 = player14.img
        player14.points += 4
        player14.badge += 1

        player15 = Player.query.filter(form.data['fifthtenth'] == Player.name).one()
        player_img15 = player15.img
        player15.points += 3
        player15.badge += 1

        player16 = Player.query.filter(form.data['sixtenth'] == Player.name).one()
        player_img16 = player16.img
        player16.points += 2
        player16.badge += 1
        ####### LOGIC FOR RANKHISTORY ###########
        tour_id = 6 ## change this?
        RankHistory.query.filter(RankHistory.tourId == tour_id).delete()
        for i in range(1,209):
            if i != 132:
                player = Player.query.get(i)
                print(player.name)
                today_score = TourTeam.query.filter(and_(TourTeam.tourId == tour_id, TourTeam.playerId == i)).first()
                score = today_score.score
                new_int = RankHistory(tourId = tour_id, playerId = i, score = score, rank = player.rank, total = player.tour_points)
                db.session.add(new_int)
        ######## LOGIC FOR TEAM TOUR POINTS ########
                teams = Team.query.all()
                tour = TourScore.query.get(tour_id)
        for team in teams:
                if team.name == 'Virginia Tech':
                    team.tour_points += tour.vt
                if team == 'Penn State':
                    team.tour_points += tour.psu
                if team == 'Oklahoma State':
                    team.tour_points += tour.okst
                if team == 'Iowa':
                   team.tour_points += tour.iowa
                if team == 'Iowa State':
                    team.tour_points += tour.isu
                if team == 'Minnesota':
                    team.tour_points += tour.minn
                if team == 'Stanford':
                    team.tour_points += tour.stan
                if team == 'NC State':
                    team.tour_points += tour.ncst
                if team == 'Missouri':
                    team.tour_points += tour.mizz
                if team == 'Lehigh':
                    team.tour_points += tour.leh
                if team == 'Cornell':
                    team.tour_points += tour.corn
                if team == 'Michigan':
                    team.tour_points += tour.mich
                if team == 'Ohio State':
                    team.tour_points += tour.osu
                if team == 'Nebraska':
                    team.tour_points += tour.neb


        params = {
            'first': player_img,
            'second': player_img2,
            'third': player_img3,
            'fourth': player_img4,
            'fifth': player_img5,
            'sixth': player_img6,
            'seventh': player_img7,
            'eigth': player_img8,
            'ninth': player_img9,
            'tenth': player_img10,
            'eleventh': player_img11,
            'twelfth': player_img12,
            'thirtenth': player_img13,
            'fourtenth': player_img14,
            'fifthtenth': player_img15,
            'sixtenth': player_img16,
        }
        new_result = Result(**params)
        db.session.add(new_result)
        db.session.commit()
        return redirect('/results')
    return 'Bad Data'


############$$$$$$$$$$$$ BATTLE #####$$$$$$$$$$$$$$$$$$$$$$

@app.route('/new_battle', methods=['GET', 'POST'])
def new_battle():
    champ = [ # 3
    'Round of 128',
    'Round of 64',
    'Round of 32',
    'Round of 16',
    'Quarter-Final',
    ]
    cons = [ #1
    'Consolation Round',
    'Consolation Round 2',
    'Consolation Round 3',
    'Cons-Semi',
    'Cons-Quarter',
    'Blood Round',
    'Round of 12',
    'Cons-24',
    'Cons-48',
    'Cons-64',
    'Cons-32',
    'Cons-16',
    'Cons-12',
    'Placement Round'
    ]
    medal_round = [ # 4
    'Bronze Medal Match',
    '5th Place Match',
    '7th Place Match',
    'Semi-Final',
    ]
    badge_round = [ #3.5
    '9th Place Match',
    '11th Place Match',
    '13th Place Match',
    '15th Place Match',
    ]
    form = NewBattle()
    names = [
  "Abyss",
"Adult Gon",
"Akatsuki Sasuke",
"Aki",
"Alex Louis",
"Alphonse",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Android 18",
"Armor Titan",
"Asta",
"Asuma",
"Attack Titan",
"Beast Titan",
"Bisky",
"Bonolenov",
"Byakuya",
"Cammy",
"Cart Titan",
"Cell",
"Chainsaw Man",
"Chakra Naruto",
"Choji",
"Choso",
"Chrollo",
"Chun-Li",
"Colossal Titan",
"Deidara",
"Dot",
"Edward",
"Envy",
"Erwin",
"Erza",
"Feitan",
"Female Titan",
"Fern",
"Flamme",
"Franklin",
"Frieren",
"Frieza",
"Fubuki",
"Gaara",
"Geto",
"Ging",
"Godspeed Killua",
"Gohan",
"Gojo",
"Goku",
"Gon",
"Gotoh",
"Gray",
"Greed",
"Hanzo",
"Hashirama",
"Hidan",
"Himeno",
"Hinata",
"Hisoka",
"Hitsugaya",
"Ichigo",
"Ikalgo",
"Illumi",
"Ino",
"Inosuke",
"Itachi",
"Jaw Titan",
"Jellal",
"Jiraiya",
"Juubi",
"Juubito",
"Kaguya",
"Kaiju No. 8",
"Kakashi",
"Kakuzu",
"Kalluto",
"Kankuro",
"Kasumi",
"Katana Man",
"Kenjaku",
"Kiba",
"Kikoru",
"Killer Bee",
"Killua",
"Kisame",
"Kishibe",
"Kite",
"Knuckle",
"Kobeni",
"Konan",
"Kurama",
"Kurapika",
"Lance",
"Laxus",
"Leorio",
"Levi",
"Ling",
"Luffy",
"Lust",
"Machi",
"Madara",
"Mahito",
"Mai",
"Majin Buu",
"Maki",
"Makima",
"Mash",
"May",
"Mechamaru",
"Megumi",
"Mei Mei",
"Menthuthuyoupi",
"Meruem",
"Might Guy",
"Mikasa",
"Mina",
"Minato",
"Momo",
"Muzan",
"Nami",
"Nanami",
"Natsu",
"Neferpitou",
"Neji",
"Netero",
"Nezuko",
"Nobara",
"Nobunaga",
"Noelle",
"Noritoshi",
"Obito",
"Olivier",
"Orochimaru",
"Pain",
"Pakunoda",
"Panda",
"Phinks",
"Piccolo",
"Pokkle",
"Ponzu",
"Power",
"Rage Tobi",
"Rayne",
"Renji",
"Reno",
"Reze",
"Riza",
"Rock Lee",
"Roy",
"Rukia",
"Sage Naruto",
"Sai",
"Saitama",
"Sakura",
"Sasori",
"Sasuke",
"Scar",
"Shaiapouf",
"Shalnark",
"Shikamaru",
"Shino",
"Shisui",
"Shizuku",
"Shukaku",
"Silva",
"Six Paths Naruto",
"Soshiro",
"Stark",
"Suigetsu",
"Sukuna",
"Tanjiro",
"Tatsumaki",
"Temari",
"Tobirama",
"Todo",
"Toge",
"Toji",
"Trunks",
"Tsunade",
"Uryū",
"Utahime",
"Uvogin",
"Vegeta",
"Walker",
"Yamato",
"Yamamoto",
"Yoruichi",
"Yuji",
"Yuki",
"Yuno",
"Zenitsu",
"Zoro",
"Sheele",
"Bulat",
"Esdeath",
"Akame",
"Tatsumi",
"Mine",
"Leone",
"Kurome",
"Seryu",
"Toa & Ju Fa",
"Gabimaru",
"Sagiri",
"Chobei",
"Yuzuriha",
"Shion",
"Gantetsusai",
'Tao & Ju Fa',
'Mahoraga',
'Tengen',
'Zohakuten',
'Gyomei',
'Rengoku',
'Sanemi',
'Daki',
'Gluttony',
'Giyu',
'Obanai',
'Muichiro',
'Gyokko',
'Hohenheim',
'Nico Robin',
'Jogo',
'Shinobu',
'Mitsuri',
'All for One',
'Tsukoyomi',
'Uravity',
'Eraser Head',
'Deku',
'All Might',
'Lemillion',
'Mirko',
'Red Riot',
'Endeavor',
'Bakugo',
'Shoto',
'Dabi',
'Kurogiri',
'Nejire',
'Stain',
'Lady Nagant',
'Hawks',
'Yaoyorozu',
'Overhaul',
'Midnight',
'Himiko',
'Shigaraki',
'Pinky',
'Angel',
'Lucy',
'Viole',
'Khun',
'Rak',
'Yuri',
'Endorsi',
'Yihwa',
]

    if form.validate_on_submit():
        player_1 = Player.query.filter(Player.name == form.data['player_1']).one()
        player_2 = Player.query.filter(Player.name == form.data['player_2']).one()
        if form.data['round'] == 'Dual':
            print('Das a dual')
            ### CALCULATING DUAL POINT LOGIC
            dual_pts = 0
            if form.data['score'] >= 1000:
                dual_pts = 7
            elif form.data['score'] >= 700:
                dual_pts = 5
            elif form.data['score'] >= 400:
                dual_pts = 4
            else:
                dual_pts = 3

            # DETERMINING THE WINNER HERE
            if form.data['victory_1'] == True:
                player_1.wins += 1
                player_1.d_wins += 1
                player_1.dual_points += dual_pts
                player_1.tour_points += (dual_pts / 2)
                player_2.loss += 1
                player_2.d_loss += 1
            elif form.data['victory_2'] == True:
                player_2.wins += 1
                player_2.d_wins += 1
                player_2.dual_points += dual_pts
                player_2.tour_points += (dual_pts / 2)
                player_1.loss += 1
                player_1.d_loss += 1
            # ADDING IT TO OPPS
            params = {
            'player_id': player_1.id,
            'opponent_id': player_2.id,
            'victory': form.data['victory_1'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'] or 'Battle Royale 1',
            'round': form.data['round']
            }
            para = {
            'player_id': player_2.id,
            'opponent_id': player_1.id,
            'victory': form.data['victory_2'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'] or 'Battle Royal 1',
            'round': form.data['round']
             }

            player_1_record = Opponent(**params)
            db.session.add(player_1_record)
            player_2_record = Opponent(**para)
            db.session.add(player_2_record)
            db.session.commit()
            return redirect('/')

        teampnts = 0

        if form.data['round'] in champ:
            teampnts += 3
        if form.data['round'] == 'Round of 256':
            teampnts += 3
        if form.data['round'] in cons:
            teampnts += 1
        if form.data['round'] in badge_round:
            teampnts += 3.5
        if form.data['round'] in medal_round:
            teampnts += 4
        if form.data['round'] == 'Gold Medal Match':
            teampnts += 7

        if form.data['score'] >= 1000:
            teampnts += 2
        elif form.data['score'] >= 750:
            teampnts += 1.5
        elif form.data['score'] >= 500:
            teampnts += 1

        if form.data['victory_1'] == True:
            player_1.wins += 1
            player_1.tour_points += teampnts
            if form.data['score'] >= 500:
                player_1.bonus += 1
            db.session.commit()
            ##### NEW LOGIC FOR TEAM SCORES rudy#####
            team = player_1.team
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            print(tourn)
            if tourn:
                if team == 'Virginia Tech':
                    tourn.vt += teampnts
                    db.session.commit()
                if team == 'Penn State':
                    tourn.psu += teampnts
                    db.session.commit()
                if team == 'Oklahoma State':
                    tourn.okst += teampnts
                    db.session.commit()
                if team == 'Iowa':
                    tourn.iowa += teampnts
                    db.session.commit()
                if team == 'Iowa State':
                    tourn.isu += teampnts
                    db.session.commit()
                if team == 'Minnesota':
                    tourn.minn += teampnts
                    db.session.commit()
                if team == 'Stanford':
                    tourn.stan += teampnts
                    db.session.commit()
                if team == 'NC State':
                    tourn.ncst += teampnts
                    db.session.commit()
                if team == 'Missouri':
                    tourn.mizz += teampnts
                    db.session.commit()
                if team == 'Lehigh':
                    tourn.leh += teampnts
                    db.session.commit()
                if team == 'Cornell':
                    tourn.corn += teampnts
                    db.session.commit()
                if team == 'Michigan':
                    tourn.mich += teampnts
                    db.session.commit()
                if team == 'Ohio State':
                    tourn.osu += teampnts
                    db.session.commit()
                if team == 'Nebraska':
                    tourn.neb += teampnts
                    db.session.commit()
                if team == 'Wyoming':
                    tourn.Wyoming += teampnts
                    db.session.commit()
                if team == 'Northern Iowa':
                    tourn.Northern_Iowa += teampnts
                    db.session.commit()
                if team == 'Colorado':
                    tourn.Colorado += teampnts
                    db.session.commit()
                if team == 'Arizona State':
                    tourn.Arizona_State += teampnts
                    db.session.commit()
                if team == 'Sacred Heart':
                    tourn.sh += teampnts
                    db.session.commit()
                ####### even more logic for tourteam ##########
                player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_1.id)).one()
                player_score.score += teampnts
                player_score.wins += 1
                if form.data['round'] == 'Round of 16' or form.data['round'] == 'Blood Round':
                    player_score.status = 'All-American'
                db.session.commit()
        else:
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_1.id)).one()
            player_score.loss += 1
            player_1.loss += 1
            if player_score.status == 'All-American':
                pass
            elif player_score.status == 'Champ':
                player_score.status = 'Cons'
            elif player_score.status == 'Cons':
                player_score.status = 'Eliminated'
            db.session.commit()

        if form.data['victory_2'] == True:
            player_2.wins += 1
            player_2.tour_points += teampnts
            if form.data['score'] >= 500:
                player_2.bonus += 1
            db.session.commit()
             ##### NEW LOGIC FOR TEAM SCORES rudy#####
            team = player_2.team
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            if tourn:
                if team == 'Virginia Tech':
                    tourn.vt += teampnts
                    db.session.commit()
                if team == 'Penn State':
                    tourn.psu += teampnts
                    db.session.commit()
                if team == 'Oklahoma State':
                    tourn.okst += teampnts
                    db.session.commit()
                if team == 'Iowa':
                    tourn.iowa += teampnts
                    db.session.commit()
                if team == 'Iowa State':
                    tourn.isu += teampnts
                    db.session.commit()
                if team == 'Minnesota':
                    tourn.minn += teampnts
                    db.session.commit()
                if team == 'Stanford':
                    tourn.stan += teampnts
                    db.session.commit()
                if team == 'NC State':
                    tourn.ncst += teampnts
                    db.session.commit()
                if team == 'Missouri':
                    tourn.mizz += teampnts
                    db.session.commit()
                if team == 'Lehigh':
                    tourn.leh += teampnts
                    db.session.commit()
                if team == 'Cornell':
                    tourn.corn += teampnts
                    db.session.commit()
                if team == 'Michigan':
                    tourn.mich += teampnts
                    db.session.commit()
                if team == 'Ohio State':
                    tourn.osu += teampnts
                    db.session.commit()
                if team == 'Nebraska':
                    tourn.neb += teampnts
                    db.session.commit()
                if team == 'Wyoming':
                    tourn.Wyoming += teampnts
                    db.session.commit()
                if team == 'Northern Iowa':
                    tourn.Northern_Iowa += teampnts
                    db.session.commit()
                if team == 'Colorado':
                    tourn.Colorado += teampnts
                    db.session.commit()
                if team == 'Arizona State':
                    tourn.Arizona_State += teampnts
                    db.session.commit()
                if team == 'Sacred Heart':
                    tourn.sh += teampnts
                    db.session.commit()
                ####### even more logic for tourteam ##########
                player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_2.id)).one()
                player_score.score += teampnts
                player_score.wins += 1
                if form.data['round'] == 'Round of 16' or form.data['round'] == 'Blood Round':
                    player_score.status = 'All-American'
                db.session.commit()

        else:
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_2.id)).one()
            player_score.loss += 1
            player_2.loss += 1
            if player_score.status == 'All-American':
                pass
            elif player_score.status == 'Champ':
                player_score.status = 'Cons'
            elif player_score.status == 'Cons':
                player_score.status = 'Eliminated'
            db.session.commit()

        params = {
            'player_id': player_1.id,
            'opponent_id': player_2.id,
            'victory': form.data['victory_1'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'] or 'Battle Royale 1',
            'round': form.data['round']
        }
        para = {
            'player_id': player_2.id,
            'opponent_id': player_1.id,
            'victory': form.data['victory_2'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'] or 'Battle Royal 1',
            'round': form.data['round']
        }

        player_1_record = Opponent(**params)
        db.session.add(player_1_record)
        player_2_record = Opponent(**para)
        db.session.add(player_2_record)
        db.session.commit()
        return redirect('/')
    return render_template('new_battle.html', names=names, form=form)

#################### H I S T O R Y ####################

@app.route('/history_form', methods=['GET', 'POST'])
def new_history():
    form = NewHistory()

    names = []

    if form.validate_on_submit():
        teamz = True
        if form.data['player_1']:
         player_1 = Player.query.filter(Player.name == form.data['player_1']).one()
         player_2 = Player.query.filter(Player.name == form.data['player_2']).one()
         all_records = Opponent.query.filter(and_(Opponent.player_id == player_1.id, Opponent.opponent_id == player_2.id )).all()
         records = list(reversed(all_records))
         return render_template('history_report.html', records=records, player_1=player_1, player_2=player_2, teamz=teamz)
        else:
            teamz = False
            team_1 = Team.query.filter(Team.name == form.data['team_1']).one()
            team_2 = Team.query.filter(Team.name == form.data['team_2']).one()

# Step 2: Get all players on each team
            team1_players = Player.query.filter(Player.team == team_1.name).all()
            team2_players = Player.query.filter(Player.team == team_2.name).all()

# Step 3: Extract player IDs
            team1_ids = [p.id for p in team1_players]
            team2_ids = [p.id for p in team2_players]

# Step 4: Query Opponent records where team1 fought team2
            common_opp = Opponent.query.filter(
             or_(
                 and_(Opponent.player_id.in_(team1_ids), Opponent.opponent_id.in_(team2_ids)),
                 and_(Opponent.player_id.in_(team2_ids), Opponent.opponent_id.in_(team1_ids))
                )
            ).all()

            all_ids = set()
            for o in common_opp:
                all_ids.add(o.player_id)
                all_ids.add(o.opponent_id)

            players_dict = {p.id: p for p in Player.query.filter(Player.id.in_(all_ids)).all()}

            enriched_opp = []
            team_1_wins = 0
            team_2_wins = 0
            for rec in common_opp:
                 player_1 = players_dict.get(rec.player_id)
                 player_2 = players_dict.get(rec.opponent_id)
                 teams_involved = {player_1.team, player_2.team}
                 if team_1.name in teams_involved and team_2.name in teams_involved:
        # Count wins
                    if rec.victory:
                        if player_1.team == team_1.name:
                            team_1_wins += 1
                        elif player_1.team == team_2.name:
                            team_2_wins += 1
                    # else:
                    #      if player_2.team == team_1.name:
                    #         team_1_wins += 1
                    #      elif player_2.team == team_2.name:
                    #         team_2_wins += 1
                 enriched_opp.append({
                    'rec': rec,
                    'player_1': player_1,
                    'player_2': player_2,
                })

            return render_template(
            'history_report.html',
            team_1_wins=team_1_wins,
            team_2_wins=team_2_wins,
            team_1=team_1,
            team_2=team_2,
            teamz=teamz,
            common_opp=enriched_opp
            )

    return render_template('history_form.html', form=form, names=names)

@app.route('/match-ups')
def match():
    players = Player.query.all()
    players_serialized = [
        {"name": p.name, "img": p.img} for p in players
    ]
    print(players)
    return render_template('match-ups.html', players=players_serialized)

from flask import request

@app.route('/dualLeaders')
def dual_leaders():
    selected_season = request.args.get('season', 'all')
    selected_position = request.args.get('position', 'all')

    def matches_position(position, selected):
        if selected == 'all':
            return True

        if not position:
            return False

        pos = position.lower().strip()

        if selected == 'guards':
            return pos in ['guard', 'guards', 'center', 'left guard', 'right guard', 'lg', 'rg']

        if selected == 'vanguard':
            return pos == 'vanguard'

        if selected == 'defender':
            return pos in ['defender', 'defense']

        if selected == 'captain':
            return pos == 'captain'

        return True

    players = []

    if selected_season == 'all':
        raw_players = Player.query.order_by(
            Player.dual_points.desc(),
            Player.d_wins.desc(),
            Player.d_loss.asc()
        ).all()

        for player in raw_players:
            if matches_position(player.position, selected_position):
                players.append({
                    'player': player,
                    'stats': player,
                    'position': player.position
                })

    else:
        season_id = int(selected_season)

        roster_rows = TeamRosterSeason.query.filter_by(
            season_id=season_id
        ).all()

        for row in roster_rows:
            if not matches_position(row.position, selected_position):
                continue

            player = Player.query.get(row.player_id)

            if not player:
                continue

            stats = PlayerSeasonStats.query.filter_by(
                player_id=player.id,
                season_id=season_id
            ).first()

            if not stats:
                continue

            players.append({
                'player': player,
                'stats': stats,
                'position': row.position
            })

        players.sort(
            key=lambda row: (
                row['stats'].dual_points or 0,
                row['stats'].d_wins or 0,
                -1 * (row['stats'].d_loss or 0)
            ),
            reverse=True
        )

    # Update position rank for what you're currently viewing
    if selected_position != 'all':
        for index, row in enumerate(players, start=1):
            stats = row['stats']
            stats.pos_rank = index

        db.session.commit()

    seasons = Season.query.order_by(Season.id.asc()).all()

    return render_template(
        'dualleaders.html',
        players=players,
        seasons=seasons,
        selected_season=selected_season,
        selected_position=selected_position
    )

@app.route('/filter')
def filter_game():
    players = Player.query.order_by(Player.dual_points.desc()).all()

    players_data = [
        {
            "id": p.id,
            "name": p.name,
            "img": p.img,
            "rank": p.rank,
            "dual_points": p.dual_points
        }
        for p in players
    ]

    return render_template(
        'filter_game.html',
        players=players_data
    )


@app.route('/blind-rank')
def blind_rank():
    players = Player.query.order_by(Player.dual_points.desc()).all()

    players_data = [
        {
            "id": p.id,
            "name": p.name,
            "img": p.img,
            "rank": p.rank,
            "dual_points": p.dual_points
        }
        for p in players
    ]

    return render_template('blind_rank.html', players=players_data)

@app.route('/rank-puzzle')
def rank_puzzle():
    players = Player.query.order_by(Player.dual_points.desc()).all()

    players_data = [
        {
            "id": p.id,
            "name": p.name,
            "img": p.img,
            "rank": p.rank,
            "dual_points": p.dual_points
        }
        for p in players
    ]

    return render_template('rank_puzzle.html', players=players_data)
