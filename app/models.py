from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Player(db.Model):
    __tablename__ = 'players'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    wins = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    d_wins = db.Column(db.Integer)
    d_loss = db.Column(db.Integer)
    points = db.Column(db.Integer)
    img = db.Column(db.String(255))
    gold = db.Column(db.Integer)
    silver = db.Column(db.Integer)
    bronze = db.Column(db.Integer)
    wood = db.Column(db.Integer)
    medal = db.Column(db.Integer)
    badge = db.Column(db.Integer)
    ribbon = db.Column(db.Integer)
    blood = db.Column(db.Integer)
    team = db.Column(db.String(255))
    logo = db.Column(db.String)
    birthday = db.Column(db.String)
    height = db.Column(db.String)
    position = db.Column(db.String)
    tour_points = db.Column(db.Integer, default=0)  # <-- New column
    dual_points = db.Column(db.Integer, default=0)  # <-- New column
    rank = db.Column(db.Integer, default=0)  # <-- New column
    pos_rank = db.Column(db.Integer, default=0)
    bonus = db.Column(db.Integer, default=0)  # <-- New column
    active = db.Column(db.Boolean, default=True)



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
    week = db.Column(db.Integer)
    finalized = db.Column(db.Boolean, default=False)
    season_id = db.Column(db.Integer, default=1)

class TournamentPlacement(db.Model):
    __tablename__ = 'tournament_placements'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'))
    place = db.Column(db.Integer)  # 1-16, or 17-20 for blood round
    award = db.Column(db.String(50))  # gold, silver, bronze, wood, medal, badge, ribbon, blood
    season_id = db.Column(db.Integer, default=1)


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(255), nullable=True)
    season_id = db.Column(db.Integer, default=1)
    date = db.Column(db.Date, default=date.today)


class Opponent(db.Model):
    __tablename = 'opponents'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    opponent_id = db.Column(db.Integer)
    victory = db.Column(db.Boolean)
    is_ressist = db.Column(db.Boolean)
    fotn = db.Column(db.Boolean)
    tour_name = db.Column(db.Integer)
    round = db.Column(db.String(255))
    score = db.Column(db.Integer)
    date = db.Column(db.Date, default=date.today)
    season_id = db.Column(db.Integer, default=1)

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
     winnerId =  db.Column(db.Integer)
     date = db.Column(db.Date, default=date.today)
     season_id = db.Column(db.Integer, default=1)



class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    wins = db.Column(db.Integer)
    loss = db.Column(db.Integer)
    points = db.Column(db.Integer)
    tour_points = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    logo = db.Column(db.String)
    conf = db.Column(db.String)
    divison = db.Column(db.String)
    season_id = db.Column(db.Integer, default=1)


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
    Northern_Iowa = db.Column(db.Integer)
    Wyoming = db.Column(db.Integer)
    Arizona_State = db.Column(db.Integer)
    Colorado = db.Column(db.Integer)
    sh = db.Column(db.Integer)
    season_id = db.Column(db.Integer, default=1)
## THIS WILL REPLACE TOUR SCORE IN THE NEAR FUTRURE ######
class TournamentTeamScore(db.Model):
    __tablename__ = 'tournament_team_scores'
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer)
    team_id = db.Column(db.Integer)
    score = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, default=1)


class TourTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourId = db.Column(db.Integer)
    playerId = db.Column(db.Integer)
    score = db.Column(db.Integer)
    wins = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)
    status = db.Column(db.String)
    season_id = db.Column(db.Integer, default=1)

class RankHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tourId = db.Column(db.Integer)
    playerId = db.Column(db.Integer)
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rank = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, default=1)

class TeamRank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    score = db.Column(db.Integer)
    rank = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, default=1)

class TeamRankHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    teamId = db.Column(db.Integer)
    points = db.Column(db.Integer)
    total = db.Column(db.Integer)
    rank = db.Column(db.Integer, default=0)
    season_id = db.Column(db.Integer, default=1)

class PlayerOfDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pick_date = db.Column(db.String(20), unique=True, nullable=False)
    player_id = db.Column(db.Integer, nullable=False)

class Season(db.Model):
    __tablename__ = 'seasons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date, nullable=True)

class PlayerSeasonStats(db.Model):
    __tablename__ = 'player_season_stats'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)

    team = db.Column(db.String(255))

    wins = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)
    d_wins = db.Column(db.Integer, default=0)
    d_loss = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    tour_points = db.Column(db.Integer, default=0)
    dual_points = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)
    pos_rank = db.Column(db.Integer, default=0)
    bonus = db.Column(db.Integer, default=0)

    gold = db.Column(db.Integer, default=0)
    silver = db.Column(db.Integer, default=0)
    bronze = db.Column(db.Integer, default=0)
    medal = db.Column(db.Integer, default=0)
    wood = db.Column(db.Integer, default=0)
    ribbon = db.Column(db.Integer, default=0)
    blood = db.Column(db.Integer, default=0)
    badge = db.Column(db.Integer, default=0)

class TeamSeasonStats(db.Model):
    __tablename__ = 'team_season_stats'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)

    wins = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    tour_points = db.Column(db.Integer, default=0)
    vanguard = db.Column(db.Integer, default=0)
    guard = db.Column(db.Integer, default=0)
    defense = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer, default=0)

class TeamRosterSeason(db.Model):
    __tablename__ = 'team_roster_season'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False)
    team_id = db.Column(db.Integer, nullable=False)
    season_id = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String)

    team_name = db.Column(db.String(255))

class PositionRankHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    week = db.Column(db.Integer)
    player_id = db.Column(db.Integer)
    season_id = db.Column(db.Integer)

    position = db.Column(db.String)

    points = db.Column(db.Integer)
    rank = db.Column(db.Integer)

class PositionSeasonFinish(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    player_id = db.Column(db.Integer)
    season_id = db.Column(db.Integer)

    position = db.Column(db.String)

    final_rank = db.Column(db.Integer)

# flask db migrate -m "Updated Battle model"
# flask db upgrade
