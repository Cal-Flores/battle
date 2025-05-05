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
    tour_points = db.Column(db.Integer, default=0)  # <-- New column
    rank = db.Column(db.Integer, default=0)  # <-- New column
    bonus = db.Column(db.Integer, default=0)  # <-- New column


# add new column to the model: ex: tour_points = db.Column(db.Integer, default=0)  # <-- New column
# flask db migrate -m "Added tour_points column"
# flask db upgrade
# done :)

class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    date = db.Column(db.Date)
    # first = db.Column(db.String(50), nullable=False)
    # second = db.Column(db.String(50), nullable=False)
    # third = db.Column(db.String(50), nullable=False)


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
     hscore = db.Column(db.Integer)
     ascore = db.Column(db.Integer)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    wins = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    points = db.Column(db.Integer)
    tour_points = db.Column(db.Integer)
    logo = db.Column(db.String)


class TourScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    psu = db.Column(db.Integer)
    osu = db.Column(db.Integer)
    okst = db.Column(db.Integer)
    corn = db.Column(db.Integer)
    leh = db.Column(db.Integer)
    ncst = db.Column(db.Integer)
    iowa = db.Column(db.Integer)
    isu = db.Column(db.Integer)
    minn = db.Column(db.Integer)
    vt = db.Column(db.Integer)
    mizz = db.Column(db.Integer)
    neb = db.Column(db.Integer)
    stan = db.Column(db.Integer)
    mich = db.Column(db.Integer)

class TourTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourId = db.Column(db.Integer)
    playerId = db.Column(db.Integer)
    score = db.Column(db.Integer)
    wins = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)

class RankHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourId = db.Column(db.Integer)
    playerId = db.Column(db.Integer)
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rank = db.Column(db.Integer, default=0)

# flask db migrate -m "Updated Battle model"
# flask db upgrade
