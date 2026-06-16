# fix_null_seasons.py

from app import app
from app.models import db, Tour, Result, Opponent, Dual, Team, TourScore, TourTeam, TeamRank, TeamRankHistory, RankHistory

with app.app_context():
    models = [
        Tour,
        Result,
        Opponent,
        Dual,
        Team,
        TourScore,
        TourTeam,
        TeamRank,
        TeamRankHistory,
        RankHistory,
    ]

    for model in models:
        if hasattr(model, "season_id"):
            model.query.filter(model.season_id == None).update(
                {model.season_id: 1},
                synchronize_session=False
            )

    db.session.commit()
    print("All NULL season_id values changed to Season 1.")
