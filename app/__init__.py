from flask import Flask, render_template, redirect
from app.forms import NewPlayer, EditPlayer, NewTour, NewResult, NewOpponent, NewBattle, EditOpponent, NewHistory, Search, NewDual
from app.config import Configuration
from sqlalchemy import and_, or_

from flask_migrate import Migrate
from app.models import db, Player, Tour, Result, Opponent, Battle, Dual, Team, TourScore,  TourTeam, RankHistory


app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
Migrate(app,db)


@app.route('/')
def index():
    #pnt_leaders = Player.query.order_by(Player.points.desc(), Player.wins.desc(), Player.loss).all()
    players = Player.query.order_by(Player.name).all()
    entries = TourTeam.query.all()
    battles = Opponent.query.all()
    # teaam = TourScore.query.get(3)
    # teaam.corn -= 4
    # armin = Player.query.get(128)
    # armin.tour_points -= 1
    # gojo = Player.query.get(60)
    # gojo.img = 'https://wallpapers-clan.com/wp-content/uploads/2023/01/dragon-ball-vegeta-pfp-11.jpg'
    # anbukak = Player.query.get(13)
    # anbukak.points = 31
    # anbukak.medal += 1
    # for battle in battles:
    #     if battle.victory:
    #         player = Player.query.get(battle.player_id)
    #         if battle.score > 500:
    #            player.bonus += 1
    # for entry in entries:
    #     # entry.wins = 0
    #     # entry.loss = 0
    #     for battle in battles:
    #         if (battle.victory == False and entry.tourId == 1 and battle.tour_name == '1st Hunter Exam' and entry.playerId == battle.player_id):
    #             entry.loss += 1
    #             print (f'player #{entry.playerId} has {entry.loss} lozzes! tour id is { battle.tour_name }')
    # db.session.commit()
    ################### THIS IS WHERE I MADE RANKHISTORY ##############

    # for i in range(1,129):
    #     player = Player.query.get(i)
    #     tour_int = TourTeam.query.filter(and_(TourTeam.tourId == 3, TourTeam.playerId == i)).one() # CHANGE THIS the instance in the table.
    #     tour_pnt = tour_int.score # the total score for each player at tournament 1
    #     print(f'{player.name} scored {tour_pnt} points')
    #     # adding each score to the RankHistory table
    #     old_tour = RankHistory.query.filter(and_(RankHistory.tourId == 2, RankHistory.playerId == i)).one() #CHANGE THIS
    #     old_score = old_tour.total
    #     new_total = tour_pnt + old_score
    #     new_int = RankHistory(tourId = 3, playerId = i, score = tour_pnt, rank = 1, total = new_total) # CHANGE THIS
    #     db.session.add(new_int)

    # ##Set the proper rank for each player at tournament 1
    # all_scores_1 = RankHistory.query.filter(RankHistory.tourId == 3).order_by(RankHistory.total.desc()).all() # CHANGE THIS
    # for i, tscore in enumerate(all_scores_1, start=1):
    #     if i > 128:
    #         break
    #     print(f"{i}: {tscore}")
    #     tscore.rank = i

    #db.session.query(RankHistory).delete()
    db.session.commit()
    return render_template('main_page.html', players = players)

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
    return render_template('facts.html')

@app.route('/duals', methods=['GET', 'POST'])
def duals():
    form = NewDual()
    if form.validate_on_submit():
        params = {
            'home': form.data['home'],
            'away': form.data['away'],
            'hscore': form.data['hscore'],
            'ascore': form.data['ascore'],
            'week': form.data['week'],
        }
        new_dual = Dual(**params)
        db.session.add(new_dual)
        home_team = Team.query.filter(form.data['home'] == Team.name).one()
        away_team = Team.query.filter(form.data['away'] == Team.name).one()
        home_team.points += form.data['hscore']
        away_team.points += form.data['ascore']
        if form.data['hscore'] > form.data['ascore']:
            home_team.wins += 1
            away_team.loss += 1
            db.session.commit()
        elif form.data['ascore'] > form.data['hscore']:
            away_team.wins += 1
            home_team.loss += 1
            db.session.commit()
        db.session.commit()
        return redirect('/duals')
    duals = Dual.query.all()
    return render_template('duals.html', duals = duals, form=form)

@app.route('/duals/<id>')
def one_duals(id):
    dual = Dual.query.get(id)
    dualCode = f'{dual.away} vs {dual.home}'

    home_score = 0
    away_score = 0

    players = []
    records = Opponent.query.filter(and_(Opponent.tour_name == dualCode, Opponent.victory == True)).all()
    for rec in records:
        result = {}
        winner = Player.query.filter(rec.player_id == Player.id).one()
        loser = Player.query.filter(rec.opponent_id == Player.id).one()
        result['winner'] = winner
        result['loser'] = loser
        players.append(result)
        if winner.team == dual.home:
            if rec.score >= 1000:
                home_score += 7
            elif rec.score >= 700:
                home_score += 5
            if rec.score >= 400:
                home_score += 4
            else:
                home_score += 3
        elif winner.team == dual.away:
            if rec.score >= 1000:
                away_score += 7
            elif rec.score >= 700:
                away_score += 5
            elif rec.score >= 400:
                away_score += 4
            else:
                away_score += 3
    print(players)


    return render_template('one_dual.html', dual = dual,records = records, players  = players, home_score = home_score, away_score=away_score)

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

@app.route('/playerStat/<id>')
def player_stats(id):
    histories = RankHistory.query.filter(RankHistory.playerId == id).all()
    history = []
    rank = []
    total_score = 0

    for hist in histories:
        total_score += hist.score
        rank.append(hist.rank)
        history.append(hist.tourId)

    player = Player.query.get(id)
    rank.append(player.rank)

    all_wins = Opponent.query.filter(Opponent.player_id == id, Opponent.victory == True).all()
    all_losses = Opponent.query.filter(Opponent.opponent_id == id, Opponent.victory == True).all()

    # ---- Team beaten most ----
    beaten_teams = Counter()
    for win in all_wins:
        opponent = Player.query.get(win.opponent_id)
        if opponent:
          beaten_teams[opponent.team] += 1
    most_beaten_team = beaten_teams.most_common(1)[0][0] if beaten_teams else None
    wins_vs_beaten_team = 0
    losses_vs_beaten_team = 0

    if most_beaten_team:
        wins_vs_beaten_team = beaten_teams[most_beaten_team]
    for loss in all_losses:
        opponent = Player.query.get(loss.player_id)
        if opponent and opponent.team == most_beaten_team:
            losses_vs_beaten_team += 1
    beaten_team = Team.query.filter(Team.name == most_beaten_team).first()


    # ---- Team lost to most ----
    lost_to_teams = Counter()
    for loss in all_losses:
        opponent = Player.query.get(loss.player_id)  # they were the winner
        if opponent:
            lost_to_teams[opponent.team] += 1
    most_lost_team = lost_to_teams.most_common(1)[0][0] if lost_to_teams else None
    wins_vs_lost_team = 0
    losses_vs_lost_team = 0

    if most_lost_team:
        losses_vs_lost_team = lost_to_teams[most_lost_team]

        for win in all_wins:
            opponent = Player.query.get(win.opponent_id)
            if opponent and opponent.team == most_lost_team:
                wins_vs_lost_team += 1
    lost_team = Team.query.filter(Team.name == most_lost_team).first()

    # Find full fight object for biggest win
    biggest_win_fight = max(all_wins, key=lambda win: win.score, default=None)

    # Find full fight object for biggest loss
    all_losses = Opponent.query.filter(Opponent.opponent_id == id, Opponent.victory == True).all()
    biggest_loss_fight = max(all_losses, key=lambda loss: loss.score, default=None)

    # Get opponent info for biggest win
    if biggest_win_fight:
        win_opponent = Player.query.get(biggest_win_fight.opponent_id)
        biggest_win_info = {
        'score': biggest_win_fight.score,
        'round': biggest_win_fight.round,
        'tour_name': biggest_win_fight.tour_name,
        'opponent_name': win_opponent.name if win_opponent else 'Unknown',
        'opponent_team': win_opponent.team if win_opponent else 'Unknown',
        'image': win_opponent.img,
        'logo':win_opponent.logo,
        'rank': win_opponent.rank
        }
    else:
        biggest_win_info = None

    # Get opponent info for biggest loss
    if biggest_loss_fight:
        loss_opponent = Player.query.get(biggest_loss_fight.player_id)
        biggest_loss_info = {
        'score': biggest_loss_fight.score,
        'round': biggest_loss_fight.round,
        'tour_name': biggest_loss_fight.tour_name,
        'opponent_name': loss_opponent.name if loss_opponent else 'Unknown',
        'opponent_team': loss_opponent.team if loss_opponent else 'Unknown',
        'image': loss_opponent.img,
        'logo':loss_opponent.logo,
        'rank': loss_opponent.rank
        }
    else:
        biggest_loss_info = None
    # Find the biggest upset win (highest-ranked opponent defeated)
    biggest_upset_win_fight = min(
        all_wins,
        key=lambda win: Player.query.get(win.opponent_id).rank if Player.query.get(win.opponent_id) else float('inf'),
        default=None
    )

    # Find the biggest upset loss (lowest-ranked opponent who defeated this player)
    biggest_upset_loss_fight = max(
        all_losses,
        key=lambda loss: Player.query.get(loss.player_id).rank if Player.query.get(loss.player_id) else float('-inf'),
        default=None
    )

    # Get opponent info for biggest upset win
    if biggest_upset_win_fight:
        upset_win_opponent = Player.query.get(biggest_upset_win_fight.opponent_id)
        biggest_upset_win_info = {
        'score': biggest_upset_win_fight.score,
        'round': biggest_upset_win_fight.round,
        'tour_name': biggest_upset_win_fight.tour_name,
        'opponent_name': upset_win_opponent.name if upset_win_opponent else 'Unknown',
        'opponent_team': upset_win_opponent.team if upset_win_opponent else 'Unknown',
        'image': upset_win_opponent.img,
        'logo': upset_win_opponent.logo,
        'rank': upset_win_opponent.rank
        }
    else:
        biggest_upset_win_info = None

    # Get opponent info for biggest upset loss
    if biggest_upset_loss_fight:
        upset_loss_opponent = Player.query.get(biggest_upset_loss_fight.player_id)
        biggest_upset_loss_info = {
        'score': biggest_upset_loss_fight.score,
        'round': biggest_upset_loss_fight.round,
        'tour_name': biggest_upset_loss_fight.tour_name,
        'opponent_name': upset_loss_opponent.name if upset_loss_opponent else 'Unknown',
        'opponent_team': upset_loss_opponent.team if upset_loss_opponent else 'Unknown',
        'image': upset_loss_opponent.img,
        'logo': upset_loss_opponent.logo,
        'rank': upset_loss_opponent.rank
        }
    else:
        biggest_upset_loss_info = None



    # ---- Biggest rival ----
    all_fights = Opponent.query.filter(
        or_(Opponent.player_id == id, Opponent.opponent_id == id)
    ).all()
    rival_counter = Counter()
    for fight in all_fights:
        rival_id = fight.opponent_id if fight.player_id == int(id) else fight.player_id
        rival_counter[rival_id] += 1

    biggest_rival_id = rival_counter.most_common(1)[0][0] if rival_counter else None
    biggest_rival = Player.query.get(biggest_rival_id) if biggest_rival_id else None
        # Calculate win/loss vs biggest rival
    rival_fights = [
    fight for fight in all_fights
    if (fight.opponent_id == biggest_rival_id and fight.player_id == int(id)) or
       (fight.player_id == biggest_rival_id and fight.opponent_id == int(id))
    ]

    rival_wins = sum(1 for fight in rival_fights if fight.player_id == int(id) and fight.victory)
    rival_losses = sum(1 for fight in rival_fights if fight.opponent_id == int(id) and fight.victory)

    # Pack info to send to template
    biggest_rival_info = {
    'name': biggest_rival.name if biggest_rival else 'Unknown',
    'team': biggest_rival.team if biggest_rival else 'Unknown',
    'wins': rival_wins,
    'losses': rival_losses,
    'total_matches': rival_wins + rival_losses,
    }


    # ---- Win type breakdown ----
    pins, tfalls, mdec, dec = 0, 0, 0, 0
    for win in all_wins:
        if win.score > 1000:
            pins += 1
        elif win.score >= 750:
            tfalls += 1
        elif win.score >= 500:
            mdec += 1
        else:
            dec += 1
    wins = [pins, tfalls, mdec, dec]

    # ---- Team color ----
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
    wins=wins,
    color=color,
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
    player=player
    )



@app.route('/player/<id>')
def player_card(id):
    player = Player.query.get(id)

    player_img = player.img
    result = Result.query.filter(or_(Result.first == player_img, Result.second == player_img,Result.third == player_img, Result.fourth == player_img, Result.fifth == player_img, Result.sixth == player_img, Result.seventh == player_img, Result.eigth == player_img, Result.ninth == player_img, Result.tenth == player_img, Result.eleventh == player_img, Result.twelfth == player_img, Result.thirtenth == player_img, Result.fourtenth == player_img, Result.fifthtenth == player_img, Result.sixtenth == player_img)).all()


    opponents_1 = Opponent.query.filter(Opponent.player_id == id).all()
    ops = []
    for opp in opponents_1:
        person = Player.query.get(opp.opponent_id)
        ops.append(person)
    all_opponents = list(reversed(ops))
    opponents = list(reversed(opponents_1))
    print(player_img)
    print(result)
    print('-------------------')
    return render_template('player_card.html', player=player, opponents=opponents, all_opponents=all_opponents, result=result, player_img=player_img)

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

    team = 'sup' # THIS CAN STAY
    tid = 3# <---- Change this for the tournaments ID!!
    fixedPnts = 1  # <---- Change this for appropriate number!!
    if opponent.victory == True:
        player.wins -= 1
        player.tour_points -= fixedPnts
        tourData = TourScore.query.filter((TourScore.name == tourname)).one()
        tourData.okst -= fixedPnts # <---- Change this the .team to the winners team ex: tourData.mich!

        indvTeam = TourTeam.query.filter(and_(TourTeam.playerId == player.id, TourTeam.tourId == tid)).one()
        indvTeam.score -= fixedPnts
        indvTeam.wins -= 1

        db.session.commit()
    else:
        #loserId = 84
        player.loss -= 1
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


@app.route('/leaderboards')
def leader():
    players = Player.query.order_by(
        Player.tour_points.desc(),
        Player.points.desc(),
        Player.wins.desc(),
        Player.loss.asc()
    ).all()
    for index, player in enumerate(players, start=1):
        player.rank = index
    db.session.commit()

    return render_template('leader.html', players=players)



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

@app.route('/tournaments')
def tournaments():
    tour_list = Tour.query.all()
    tournaments = list(reversed(tour_list))
    data = []

    for tour in tournaments:
        tour_score = TourScore.query.filter_by(name=tour.name).first()
        if not tour_score:
            continue
        team_scores = {
            "Penn State": tour_score.psu,
            "Ohio Sate": tour_score.osu,
            "Oklahoma State": tour_score.okst,
            "Cornell": tour_score.corn,
            "Lehigh": tour_score.leh,
            "NC State": tour_score.ncst,
            "Iowa": tour_score.iowa,
            "Iowa State": tour_score.isu,
            "Minnesota": tour_score.minn,
            "Virginia Tech": tour_score.vt,
            "Missouri": tour_score.mizz,
            "Nebraska": tour_score.neb,
            "Stanford": tour_score.stan,
            "Michigan": tour_score.mich,
        }

        sorted_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:3]

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

    return render_template('tournaments.html', tournaments=data)




@app.route('/new_tournament')
def tour_form():
    form = NewTour()
    return render_template('create_tour.html', form=form)

@app.route('/score/score/<int:id>/<team>')
def get_score(id, team):
    print(team)
    curr_team = Team.query.filter(Team.name == team).one()
    players = Player.query.filter(Player.team == curr_team.name).all()

    data = []
    for player in players:
        entry = TourTeam.query.filter(and_(TourTeam.tourId == id, TourTeam.playerId == player.id)).one()
        score = entry.score
        score_data = {
            'person': player,
            'score': score,
            'wins': entry.wins,
            'loss': entry.loss
        }
        data.append(score_data)
    data.sort(key=lambda x: x['score'], reverse=True)
    return render_template('team_scorepage.html', team = curr_team, score_data=data)

@app.route('/score/<id>')
def one_tourscore(id):
    tour = TourScore.query.get(id)
    teams = Team.query.all()
    scores = sorted(
    [
        {'team': 'Penn State', 'score': tour.psu, 'logo': "https://gopsusports.com/_nuxt/logo-BDHEpLK6.svg"},
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
        }
        new_tourn = Tour(**params)
        new_score = TourScore(**score)
        db.session.add(new_tourn)
        db.session.add(new_score)
        db.session.commit()
        for i in range(128):
            newPlayer = TourTeam(tourId = new_tourn.id, playerId = i + 1, score = 0)
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

@app.route('/teams')
def teams():
    score_final = 0
    teams = Team.query.order_by(Team.wins.desc(), Team.tour_points.desc()).all()
    return render_template('teams.html', teams=teams)

@app.route('/teams/<id>')
def one_team(id):
    team = Team.query.get(id)
    opponents = Dual.query.filter(or_(Dual.home == team.name, Dual.away == team.name)).all()
    all_players = Player.query.all()
    players = []
    for player in all_players:
        if player.team == team.name:
            players.append(player)
    players.sort(key=lambda p: p.tour_points, reverse=True)
    return render_template('single_team.html', team=team, opponents = opponents, players=players)


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
        RankHistory.query.filter(RankHistory.tourId == 3).delete()
        tour_id = 3 ## change this?
        for i in range(1,129):
            player = Player.query.get(i)
            new_int = RankHistory(tourId = 3, playerId = i, score = player.tour_points, rank = player.rank, total = player.tour_points)
            db.session.add(new_int)
        ######## LOGIC FOR TEAM TOUR POINTS ########
            teams = Team.query.all()
            tour = TourScore.query.get(tour_id).one()
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
    'Cons-Semi',
    'Cons-Quarter',
    'Blood Round',
    'Round of 12',
    'Cons-24',
    'Cons-48',
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
  "Adult Gon",
  "Akatsuki Sasuke",
  "Aki",
  "Amaterasu Sasuke",
  "Android 18",
  "Anbu Itachi",
  "Anbu Kakashi",
  "Armor Titan",
  "Asuma",
  "Attack Titan",
  "Beast Titan",
  "Bisky",
  "Bonolenov",
  "Cart Titan",
  "Chainsaw Man",
  "Choji",
  "Chrollo",
  "Colossal Titan",
  "Deidara",
  "Erza",
  "Feitan",
  "Female Titan",
  "Franklin",
  "Gaara",
  "Geto",
  "Ging",
  "Gohan",
  "Goku",
  "Godspeed Killua",
  "Gojo",
  "Gon",
  "Hashirama",
  "Hanzo",
  "Himeno",
  "Hidan",
  "Hinata",
  "Hisoka",
  "Hunter Killua",
  "Ikalgo",
  "Illumi",
  "Ino",
  "Itachi",
  "Jaw Titan",
  "Jiraiya",
  "Juubito",
  "Kabuto",
  "Kaguya",
  "Kakashi",
  "Kakuzu",
  "Kalluto",
  "Kankuro",
  "Karin",
  "Kasumi",
  "Katana Man",
  "Kenjaku",
  "Killer Bee",
  "Killua",
  "Kishibe",
  "Kisame",
  "Kite",
  "Knuckle",
  "Kobeni",
  "Koga",
  "Konan",
  "Kurama",
  "Kurapika",
  "Leorio",
  "Levi",
  "Madara",
  "Machi",
  "Maki",
  "Mai",
  "Mahito",
  "Makima",
  "Menthuthuyoupi",
  "Mechamaru",
  "Megumi",
  "Mei Mei",
  "Melody",
  "Meruem",
  "Might Guy",
  "Mikasa",
  "Minato",
  "Momo",
  "Nanami",
  "Naruto",
  "Natsu",
  "Neferpitou",
  "Neji",
  "Netero",
  "Nobara",
  "Nobunaga",
  "Noritoshi",
  "Obito",
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
  "Rock Lee",
  "Sai",
  "Sage Naruto",
  "Sakura",
  "Sasori",
  "Sasuke",
  "Shaiapouf",
  "Shalnark",
  "Shikamaru",
  "Shino",
  "Shizuku",
  "Shoko",
  "Shukaku",
  "Six Paths Naruto",
  "Suigetsu",
  "Sukuna",
  "Temari",
  "Todo",
  "Toji",
  "Tobe",
  "Tobirama",
  "Toge",
  "Trunks",
  "Tsunade",
  "Utahime",
  "Uvogin",
  "Vegeta",
  "Yamato",
  "Yuki",
  "Yuji",
  "Zetsu"
]

    if form.validate_on_submit():
        player_1 = Player.query.filter(Player.name == form.data['player_1']).one()
        player_2 = Player.query.filter(Player.name == form.data['player_2']).one()
        teampnts = 0

        if form.data['round'] in champ:
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
                ####### even more logic for tourteam ##########
                player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_1.id)).one()
                player_score.score += teampnts
                player_score.wins += 1
                db.session.commit()
        else:
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_1.id)).one()
            player_score.loss += 1
            player_1.loss += 1
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
                ####### even more logic for tourteam ##########
                player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_2.id)).one()
                player_score.score += teampnts
                player_score.wins += 1
                db.session.commit()

        else:
            tourn =  TourScore.query.filter(TourScore.name == form.data['tournamnet']).first()
            player_score = TourTeam.query.filter(and_(TourTeam.tourId == tourn.id, TourTeam.playerId == player_2.id)).one()
            player_score.loss += 1
            player_2.loss += 1
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

    names = [
  "Adult Gon",
  "Akatsuki Sasuke",
  "Aki",
  "Amaterasu Sasuke",
  "Android 18",
  "Anbu Itachi",
  "Anbu Kakashi",
  "Armor Titan",
  "Asuma",
  "Attack Titan",
  "Beast Titan",
  "Bisky",
  "Bonolenov",
  "Cart Titan",
  "Chainsaw Man",
  "Choji",
  "Chrollo",
  "Colossal Titan",
  "Deidara",
  "Erza",
  "Feitan",
  "Female Titan",
  "Franklin",
  "Gaara",
  "Geto",
  "Ging",
  "Gohan",
  "Goku",
  "Godspeed Killua",
  "Gojo",
  "Gon",
  "Hashirama",
  "Hanzo",
  "Himeno",
  "Hidan",
  "Hinata",
  "Hisoka",
  "Hunter Killua",
  "Ikalgo",
  "Illumi",
  "Ino",
  "Itachi",
  "Jaw Titan",
  "Jiraiya",
  "Juubito",
  "Kabuto",
  "Kaguya",
  "Kakashi",
  "Kakuzu",
  "Kalluto",
  "Kankuro",
  "Karin",
  "Kasumi",
  "Katana Man",
  "Kenjaku",
  "Killer Bee",
  "Killua",
  "Kishibe",
  "Kisame",
  "Kite",
  "Knuckle",
  "Kobeni",
  "Koga",
  "Konan",
  "Kurama",
  "Kurapika",
  "Leorio",
  "Levi",
  "Madara",
  "Machi",
  "Maki",
  "Mai",
  "Mahito",
  "Makima",
  "Menthuthuyoupi",
  "Mechamaru",
  "Megumi",
  "Mei Mei",
  "Melody",
  "Meruem",
  "Might Guy",
  "Mikasa",
  "Minato",
  "Momo",
  "Nanami",
  "Naruto",
  "Natsu",
  "Neferpitou",
  "Neji",
  "Netero",
  "Nobara",
  "Nobunaga",
  "Noritoshi",
  "Obito",
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
  "Rock Lee",
  "Sai",
  "Sage Naruto",
  "Sakura",
  "Sasori",
  "Sasuke",
  "Shaiapouf",
  "Shalnark",
  "Shikamaru",
  "Shino",
  "Shizuku",
  "Shoko",
  "Shukaku",
  "Six Paths Naruto",
  "Suigetsu",
  "Sukuna",
  "Temari",
  "Todo",
  "Toji",
  "Tobe",
  "Tobirama",
  "Toge",
  "Trunks",
  "Tsunade",
  "Utahime",
  "Uvogin",
  "Vegeta",
  "Yamato",
  "Yuki",
  "Yuji",
  "Zetsu"
]

    if form.validate_on_submit():
         player_1 = Player.query.filter(Player.name == form.data['player_1']).one()
         player_2 = Player.query.filter(Player.name == form.data['player_2']).one()
         all_records = Opponent.query.filter(and_(Opponent.player_id == player_1.id, Opponent.opponent_id == player_2.id )).all()
         records = list(reversed(all_records))
         return render_template('history_report.html', records=records, player_1=player_1, player_2=player_2)
    return render_template('history_form.html', form=form, names=names)

@app.route('/match-ups')
def match():
    return render_template('match-ups.html')
