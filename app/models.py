from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    wins = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    points = db.Column(db.Integer)
    img = db.Column(db.String(255))
    gold = db.Column(db.Integer)
    silver = db.Column(db.Integer)
    bronze = db.Column(db.Integer)
    medal = db.Column(db.Integer)
    badge = db.Column(db.Integer)
    team = db.Column(db.String(255))
    logo = db.Column(db.String)


# flask db_init
# flask db migrate
# flask db upgrade

class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date)
    first = db.Column(db.String(50), nullable=False)
    second = db.Column(db.String(50), nullable=False)
    third = db.Column(db.String(50), nullable=False)


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(255), nullable=False)
    second = db.Column(db.String(255), nullable=False)
    third = db.Column(db.String(255), nullable=False)
    fourth = db.Column(db.String(255), nullable=False)
    fifth = db.Column(db.String(255), nullable=False)
    sixth = db.Column(db.String(255), nullable=False)
    seventh = db.Column(db.String(255), nullable=False)
    eigth = db.Column(db.String(255), nullable=False)
    ninth = db.Column(db.String(255), nullable=False)
    tenth = db.Column(db.String(255), nullable=False)
    eleventh = db.Column(db.String(255), nullable=True)
    twelfth = db.Column(db.String(255), nullable=True)
    thirtenth = db.Column(db.String(255), nullable=True)
    fourtenth = db.Column(db.String(255), nullable=True)
    fifthtenth = db.Column(db.String(255), nullable=True)
    sixtenth = db.Column(db.String(255), nullable=True)


class Opponent(db.Model):
    __tablename = 'opponents'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    opponent_id = db.Column(db.Integer)
    victory = db.Column(db.Boolean)
    tour_name = db.Column(db.Integer)
    round = db.Column(db.String(255))
    score = db.Column(db.Integer)

class Battle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_1 = db.Column(db.String)
    victory_1 = db.Column(db.Boolean)
    player_2 = db.Column(db.Integer)
    victory_2 = db.Column(db.Boolean)
    tour_name = db.Column(db.Integer)
    round = db.Column(db.Integer)
    score = db.Column(db.Integer)


class Dual(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     home =  db.Column(db.String)
     away =  db.Column(db.String)
     week =  db.Column(db.String)

# flask db migrate -m "Updated Battle model"
# flask db upgrade
