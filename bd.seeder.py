from app.models import db, Player, Tour, Result, Opponent
from app import app
import datetime


# ../static/images/
with app.app_context():

    #Akatsuki Sasuke
    opp0 = Opponent(player_id=0, opponent_id=56,victory=True,tour_name=0,round='Round of 64')
    opp2 = Opponent(player_id=0, opponent_id=58,victory=True,tour_name=0,round='Round of 32')
    opp3 = Opponent(player_id=0, opponent_id=26,victory=True,tour_name=0,round='Round of 06')
    opp4 = Opponent(player_id=0, opponent_id=22,victory=False,tour_name=0, round='Quarter-Final')
    opp5 = Opponent(player_id=0, opponent_id=40,victory=False,tour_name=0, round='Round of 02')

    #Amaterasu Sasuke
    opp6 = Opponent(player_id=2, opponent_id=02,victory=False,tour_name=0, round='Round of 64')
    opp7 = Opponent(player_id=2, opponent_id=50,victory=True,tour_name=0, round='Consolation')





    db.session.add(opp0)
    db.session.add(opp2)
    db.session.add(opp3)
    db.session.add(opp4)

    db.session.commit()
    print('All Matches created!')
