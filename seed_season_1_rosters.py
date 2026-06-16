from app import app
from app.models import db, Player, Team, TeamRosterSeason, Season

with app.app_context():
    season1 = Season.query.get(1)

    if not season1:
        print("Season 1 does not exist yet.")
        quit()

    players = Player.query.all()

    created = 0
    skipped = 0
    missing_team = []

    for player in players:
        if not player.team:
            skipped += 1
            print(f"SKIPPED: {player.name} has no team")
            continue

        team = Team.query.filter_by(name=player.team).first()

        if not team:
            missing_team.append((player.name, player.team))
            skipped += 1
            print(f"SKIPPED: {player.name} team not found: {player.team}")
            continue

        existing = TeamRosterSeason.query.filter_by(
            player_id=player.id,
            season_id=1
        ).first()

        if existing:
            skipped += 1
            continue

        roster_row = TeamRosterSeason(
            player_id=player.id,
            team_id=team.id,
            season_id=1,
            team_name=team.name,
            position=player.position
        )

        db.session.add(roster_row)
        created += 1

    db.session.commit()

    print("----------------------")
    print("Season 1 roster seed complete")
    print(f"Created rows: {created}")
    print(f"Skipped rows: {skipped}")

    if missing_team:
        print("----------------------")
        print("Players with team names that did not match Team table:")
        for player_name, team_name in missing_team:
            print(f"{player_name}: {team_name}")
