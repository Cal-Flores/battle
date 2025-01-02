from flask import Flask, render_template, redirect
from app.forms import NewPlayer, EditPlayer, NewTour, NewResult, NewOpponent, NewBattle, EditOpponent, NewHistory, Search
from app.config import Configuration
from sqlalchemy import and_, or_

from flask_migrate import Migrate
from app.models import db, Player, Tour, Result, Opponent, Battle


app = Flask(__name__)
app.config.from_object(Configuration)
db.init_app(app)
Migrate(app,db)


@app.route('/')
def index():
    players = Player.query.all()
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

@app.route('/tournament/<id>')
def single_tour(id):
    tour = Tour.query.get(id)
    return render_template('single_tournament.html', tour=tour)

############################## PLAYER  CARD ############!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/player/<id>')
def player_card(id):
    player = Player.query.get(id)

    player_img = player.img[17:]
    result = Result.query.filter(or_(Result.first == player_img, Result.second == player_img,Result.third == player_img, Result.fourth == player_img, Result.fifth == player_img, Result.sixth == player_img, Result.seventh == player_img, Result.eigth == player_img, Result.ninth == player_img, Result.tenth == player_img)).all()


    opponents_1 = Opponent.query.filter(Opponent.player_id == id).all()
    ops = []
    for opp in opponents_1:
        person = Player.query.get(opp.opponent_id)
        ops.append(person)
    all_opponents = list(reversed(ops))
    opponents = list(reversed(opponents_1))
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
    if opponent.victory == True:
        player.wins -= 1
        db.session.commit()
    else:
        player.loss -= 1
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
    players = Player.query.order_by(Player.points.desc(), Player.wins.desc(), Player.loss).all()
    return render_template('leader.html', players = players)


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
    tour = Tour.query.all()
    tournaments = list(reversed(tour))
    return render_template('tournaments.html', tournaments=tournaments)

@app.route('/new_tournament')
def tour_form():
    form = NewTour()
    return render_template('create_tour.html', form=form)

@app.route('/new_tournament', methods=['POST'])
def  new_tour():
    form = NewTour()
    if form.validate_on_submit():
        params = {
            'link': form.data['link'],
            'name': form.data['name'],
            'date': form.data['date'],
            'first': form.data['first'],
            'second': form.data['second'],
            'third': form.data['third'],
        }
        new_tourn = Tour(**params)
        db.session.add(new_tourn)
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


@app.route('/new_result', methods=['POST'])
def new_result():
    form = NewResult()
    if form.validate_on_submit():
        player_img = '../static/images/' + form.data['first']
        player_img2 = '../static/images/' + form.data['second']
        player_img3 = '../static/images/' + form.data['third']
        player_img4 = '../static/images/' + form.data['fourth']
        player_img5 = '../static/images/' + form.data['fifth']
        player_img6 = '../static/images/' + form.data['sixth']
        player_img7 = '../static/images/' + form.data['seventh']
        player_img8 = '../static/images/' + form.data['eigth']
        player_img9 = '../static/images/' + form.data['ninth']
        player_img10 = '../static/images/' + form.data['tenth']
        player_img11 = '../static/images/' + form.data['eleventh']
        player_img12 = '../static/images/' + form.data['twelfth']

        player1 = Player.query.filter(Player.img == player_img).one()
        player1.points += 16
        player1.gold += 1

        player2 = Player.query.filter(Player.img == player_img2).one()
        player2.points += 13
        player2.silver += 1

        player3 = Player.query.filter(Player.img == player_img3).one()
        player3.points += 11
        player3.bronze += 1

        player4 = Player.query.filter(Player.img == player_img4).one()
        player4.points += 9
        player4.medal += 1

        player5 = Player.query.filter(Player.img == player_img5).one()
        player5.points += 8
        player5.medal += 1

        player6 = Player.query.filter(Player.img == player_img6).one()
        player6.points += 7
        player6.medal += 1

        player7 = Player.query.filter(Player.img == player_img7).one()
        player7.points += 6
        player7.badge += 1

        player8 = Player.query.filter(Player.img == player_img8).one()
        player8.points += 5
        player8.badge += 1

        player9 = Player.query.filter(Player.img == player_img9).one()
        player9.points += 4
        player9.badge += 1

        player10 = Player.query.filter(Player.img == player_img10).one()
        player10.points += 3
        player10.badge += 1



        db.session.commit()

        params = {
            'first': form.data['first'],
            'second': form.data['second'],
            'third': form.data['third'],
            'fourth': form.data['fourth'],
            'fifth': form.data['fifth'],
            'sixth': form.data['sixth'],
            'seventh': form.data['seventh'],
            'eigth': form.data['eigth'],
            'ninth': form.data['ninth'],
            'tenth': form.data['tenth'],
            'eleventh': form.data['eleventh'],
            'twelfth': form.data['twelfth'],
        }
        new_result = Result(**params)
        db.session.add(new_result)
        db.session.commit()
        return redirect('/results')
    return 'Bad Data'


############$$$$$$$$$$$$ BATTLE #####$$$$$$$$$$$$$$$$$$$$$$

@app.route('/new_battle', methods=['GET', 'POST'])
def new_battle():
    form = NewBattle()
    names = [
    "Akatsuki Sasuke",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Asuma",
"Beat Naruto",
"Beat Sasuke",
"Chakra Naruto",
"Choji",
"Cursed Hidan",
"Dadara",
"Deidara",
"Gaara",
"Gamabunta",
"Gamakichi",
"Hashirama",
"Hiroku",
"Hidan",
"Hinata",
"Ino",
"Itachi",
"Jiraiya",
"Jutsu Naruto",
"Juubito",
"Kabuto",
"Kaguya",
"Kakashi",
"Kankuro",
"Karin",
"Kiba",
"Killer Bee",
"Konan",
"Kurama",
"Madara",
"Masked Man",
"Massacre Itachi",
"Might Guy",
"Minato",
"Neji",
"Obito",
"Orochimaru",
"Pain",
"Rage Tobi",
"Ramen Naruto",
"Rock Lee",
"Sage Naruto",
"Sai",
"Sakura",
"Sasori",
"Sasuke",
"Sharingan Kakashi",
"Shikamaru",
"Shino",
"Shukaku",
"Shuriken Naruto",
"Six Paths Naruto",
"Suigetsu",
"Sword Sasuke",
"Temari",
"Tobirama",
"Tsunade",
"War Sakura",
"Yamato",
"Zetsu",
]
    if form.validate_on_submit():
        player_1 = Player.query.filter(Player.name == form.data['player_1']).one()
        player_2 = Player.query.filter(Player.name == form.data['player_2']).one()

        if form.data['victory_1'] == True:
            player_1.wins += 1
            db.session.commit()
        else:
            player_1.loss += 1
            db.session.commit()

        if form.data['victory_2'] == True:
            player_2.wins += 1
            db.session.commit()
        else:
            player_2.loss += 1
            db.session.commit()

        params = {
            'player_id': player_1.id,
            'opponent_id': player_2.id,
            'victory': form.data['victory_1'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'],
            'round': form.data['round']
        }
        para = {
            'player_id': player_2.id,
            'opponent_id': player_1.id,
            'victory': form.data['victory_2'],
            'score': form.data['score'],
            'tour_name': form.data['tournamnet'],
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
    "Akatsuki Sasuke",
"Amaterasu Sasuke",
"Anbu Itachi",
"Anbu Kakashi",
"Asuma",
"Beat Naruto",
"Beat Sasuke",
"Chakra Naruto",
"Choji",
"Cursed Hidan",
"Dadara",
"Deidara",
"Gaara",
"Gamabunta",
"Gamakichi",
"Hashirama",
"Hiroku",
"Hidan",
"Hinata",
"Ino",
"Itachi",
"Jiraiya",
"Jutsu Naruto",
"Juubito",
"Kabuto",
"Kaguya",
"Kakashi",
"Kankuro",
"Karin",
"Kiba",
"Killer Bee",
"Konan",
"Kurama",
"Madara",
"Masked Man",
"Massacre Itachi",
"Might Guy",
"Minato",
"Neji",
"Obito",
"Orochimaru",
"Pain",
"Rage Tobi",
"Ramen Naruto",
"Rock Lee",
"Sage Naruto",
"Sai",
"Sakura",
"Sasori",
"Sasuke",
"Sharingan Kakashi",
"Shikamaru",
"Shino",
"Shukaku",
"Shuriken Naruto",
"Six Paths Naruto",
"Suigetsu",
"Sword Sasuke",
"Temari",
"Tobirama",
"Tsunade",
"War Sakura",
"Yamato",
"Zetsu",
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
