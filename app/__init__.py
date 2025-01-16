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
    #pnt_leaders = Player.query.order_by(Player.points.desc(), Player.wins.desc(), Player.loss).all()
    players = Player.query.order_by(Player.name).all()
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

@app.route('/duals')
def duals():
    return render_template('duals.html')

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
        # player_img = '../static/images/' + form.data['first']
        # player_img2 = '../static/images/' + form.data['second']
        # player_img3 = '../static/images/' + form.data['third']
        # player_img4 = '../static/images/' + form.data['fourth']
        # player_img5 = '../static/images/' + form.data['fifth']
        # player_img6 = '../static/images/' + form.data['sixth']
        # player_img7 = '../static/images/' + form.data['seventh']
        # player_img8 = '../static/images/' + form.data['eigth']
        # player_img9 = '../static/images/' + form.data['ninth']
        # player_img10 = '../static/images/' + form.data['tenth']
        # player_img11 = '../static/images/' + form.data['eleventh']
        # player_img12 = '../static/images/' + form.data['twelfth']
        # player_img13 = '../static/images/' + form.data['thirtenth']
        # player_img14 = '../static/images/' + form.data['fourtenth']
        # player_img15 = '../static/images/' + form.data['fifthtenth']
        # player_img16 = '../static/images/' + form.data['sixtenth']
        player1 = Player.query.filter(form.data['first'] == Player.name).one()
        player_img = player1.img
        player1.points += 20
        player1.gold += 1

        player2 = Player.query.filter(form.data['second'] == Player.name).one()
        player_img2 = player2.img
        player2.points += 17
        player2.silver += 1

        player3 = Player.query.filter(form.data['third'] == Player.name).one()
        player_img3 = player2.img
        player3.points += 15
        player3.bronze += 1

        player4 = Player.query.filter(form.data['fourth'] == Player.name).one()
        player_img4 = player4.img
        player2.points += 13
        player2.badge += 1

        player5 = Player.query.filter(form.data['fifth'] == Player.name).one()
        player_img5 = player5.img
        player5.points += 12
        player5.badge += 1

        player6 = Player.query.filter(form.data['sixth'] == Player.name).one()
        player_img6 = player6.img
        player6.points += 11
        player6.badge += 1

        player7 = Player.query.filter(form.data['seventh'] == Player.name).one()
        player_img7 = player7.img
        player7.points += 10
        player7.badge += 1

        player8 = Player.query.filter(form.data['eigth'] == Player.name).one()
        player_img8 = player8.img
        player8.points += 9
        player8.badge += 1

        player9 = Player.query.filter(form.data['ninth'] == Player.name).one()
        player_img9 = player9.img
        player9.points += 8
        player9.badge += 1

        player10 = Player.query.filter(form.data['tenth'] == Player.name).one()
        player_img10 = player10.img
        player10.points += 7
        player10.badge += 1

        player11 = Player.query.filter(form.data['eleventh'] == Player.name).one()
        player_img11 = player11.img
        player11.points += 6
        player11.badge += 1

        player12 = Player.query.filter(form.data['twelfth'] == Player.name).one()
        player_img12 = player12.img
        player12.points += 5
        player12.badge += 1

        player13 = Player.query.filter(form.data['thirtenth'] == Player.name).one()
        player_img13 = player13.img
        player13.points += 4
        player13.badge += 1

        player14 = Player.query.filter(form.data['fourtenth'] == Player.name).one()
        player_img14 = player14.img
        player14.points += 3
        player14.badge += 1

        player15 = Player.query.filter(form.data['fifthtenth'] == Player.name).one()
        player_img15 = player15.img
        player15.points += 2
        player15.badge += 1

        player16 = Player.query.filter(form.data['sixtenth'] == Player.name).one()
        player_img16 = player16.img
        player16.points += 1
        player16.badge += 1


        db.session.commit()

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
