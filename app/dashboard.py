from app.models import *
from datetime import datetime
import random
from sqlalchemy import and_, func


# ---------------------------------------------------
# Birthdays and player of the day
# ---------------------------------------------------

def get_player_of_day():

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

    return {
    "today_label": today_label,
    "birthdays": birthdays,
    "random_player": random_player,
    "player_of_day_history": player_of_day_history,
    "player_map": player_map
}



def get_spotlight_match(player_map):

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

    return {
        "spotlight_match": spotlight_match
    }

# ---------------------------------------------------
# Dual Meet Ticker
# ---------------------------------------------------

def get_dual_ticker():

    recent_duals = (
        Dual.query
        .filter(
            Dual.finalized == True,
            Dual.week != "0"
        )
        .order_by(Dual.date.desc(), Dual.id.desc())
        .limit(8)
        .all()
    )

    ticker_duals = []

    for dual in recent_duals:

        away = Team.query.filter_by(name=dual.away).first()
        home = Team.query.filter_by(name=dual.home).first()

        ticker_duals.append({
            "id": dual.id,
            "week": dual.week,
            "away": away,
            "home": home,
            "ascore": dual.ascore,
            "hscore": dual.hscore
        })

    latest_week = max(int(d.week) for d in recent_duals) if recent_duals else None

    featured_fights = build_featured_fights()

    return {
        "ticker_duals": ticker_duals,
        "latest_week": latest_week,
        "featured_fights": featured_fights
    }




# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def get_fight_method(score):
    score = score or 0

    if score >= 1000:
        return "Pin"

    if score >= 700:
        return "Tech Fall"

    if score >= 400:
        return "Major Decision"

    return "Decision"


def build_featured_fights():
    # ---------------------------------------------------------
    # FIND THE MOST RECENT TOURNAMENT
    # ---------------------------------------------------------
    players = Player.query.all()
    player_map = {p.id: p for p in players}
    latest_tour = (
        Tour.query
        .order_by(Tour.date.desc(), Tour.id.desc())
        .first()
    )

    latest_tour_name = latest_tour.name if latest_tour else None

    # ---------------------------------------------------------
    # FIND THE MOST RECENT COMPLETED DUAL WEEK
    # ---------------------------------------------------------

    finalized_duals = (
        Dual.query
        .filter(
            Dual.finalized == True,
            Dual.week != "0"
        )
        .all()
    )

    valid_duals = []

    for dual in finalized_duals:
        home_score = dual.hscore or 0
        away_score = dual.ascore or 0

        # Ignore unfinished duals
        if home_score == 0 and away_score == 0:
            continue

        if str(dual.week).strip().isdigit():
            valid_duals.append(dual)

    latest_dual_week = None
    latest_week_duals = []

    if valid_duals:
        latest_dual_week = max(
            int(str(dual.week).strip())
            for dual in valid_duals
        )

        latest_week_duals = [
            dual
            for dual in valid_duals
            if int(str(dual.week).strip()) == latest_dual_week
        ]

    # Your individual dual fights use:
    # "Away Team vs Home Team"
    latest_dual_codes = [
        f"{dual.away.strip()} vs {dual.home.strip()}"
        for dual in latest_week_duals
    ]

    # ---------------------------------------------------------
    # GET FIGHTS FROM THE LATEST TOURNAMENT OR DUAL WEEK
    # ---------------------------------------------------------

    context_names = []

    if latest_tour_name:
        context_names.append(latest_tour_name)

    context_names.extend(latest_dual_codes)

    if not context_names:
        return []

    records = (
        Opponent.query
        .filter(
            Opponent.victory == True,
            Opponent.tour_name.in_(context_names)
        )
        .order_by(Opponent.id.desc())
        .all()
    )

    fight_pool = []

    for record in records:
        winner = player_map.get(record.player_id)
        loser = player_map.get(record.opponent_id)
        if not winner or not loser:
            continue

        winner_rank = winner.rank or 999
        loser_rank = loser.rank or 999

        # A larger positive number means a bigger upset.
        # Example: rank 20 defeats rank 4 = upset score of 16.
        upset_score = max(0, winner_rank - loser_rank)

        raw_score = record.score or 0
        method = get_fight_method(raw_score)

        fight_pool.append({
            "id": record.id,
            "winner": winner,
            "loser": loser,
            "score": raw_score,
            "method": method,
            "event": record.tour_name,
            "date": record.date,
            "upset_score": upset_score,
            "is_pin": raw_score >= 1000,
            "is_dual": record.tour_name in latest_dual_codes
        })

    if not fight_pool:
        return []

    # ---------------------------------------------------------
    # BUILD A BALANCED 12-FIGHT FEATURE SET
    # ---------------------------------------------------------

    selected = []
    selected_ids = set()

    def add_fights(fights, limit):
        added = 0

        for fight in fights:
            if fight["id"] in selected_ids:
                continue

            selected.append(fight)
            selected_ids.add(fight["id"])
            added += 1

            if added >= limit or len(selected) >= 12:
                break

    # Biggest upsets
    biggest_upsets = sorted(
        fight_pool,
        key=lambda fight: (
            fight["upset_score"],
            fight["id"]
        ),
        reverse=True
    )

    add_fights(biggest_upsets, 3)

    # Pins
    pins = sorted(
        [fight for fight in fight_pool if fight["is_pin"]],
        key=lambda fight: fight["id"],
        reverse=True
    )

    add_fights(pins, 3)

    # Largest recorded performances
    biggest_scores = sorted(
        fight_pool,
        key=lambda fight: (
            fight["score"],
            fight["id"]
        ),
        reverse=True
    )

    add_fights(biggest_scores, 2)

    # Lowest nonzero recorded results
    lowest_scores = sorted(
        [
            fight
            for fight in fight_pool
            if fight["score"] > 0
        ],
        key=lambda fight: (
            fight["score"],
            -fight["id"]
        )
    )

    add_fights(lowest_scores, 2)

    # Fill remaining spots with the latest fights
    latest_fights = sorted(
        fight_pool,
        key=lambda fight: fight["id"],
        reverse=True
    )

    add_fights(latest_fights, 12)

    # Add a headline label to each selected fight
    for fight in selected:
        if fight["is_pin"]:
            fight["label"] = "PIN OF THE WEEK"

        elif fight["upset_score"] > 0:
            fight["label"] = "UPSET ALERT"

        elif fight["score"] >= 700:
            fight["label"] = "DOMINANT PERFORMANCE"

        elif fight["is_dual"]:
            fight["label"] = f"WEEK {latest_dual_week} SPOTLIGHT"

        else:
            fight["label"] = "TOURNAMENT SPOTLIGHT"

    return {
    "featured_fights": selected[:12]
}



def build_player_movers():
    active_season = Season.query.filter_by(active=True).first()
    season_id = active_season.id if active_season else 1

    latest_week = (
        db.session.query(func.max(RankHistory.tourId))
        .filter(RankHistory.season_id == season_id)
        .scalar()
    )

    if latest_week is None or latest_week <= 1:
        return {
            "player_risers": [],
            "player_fallers": []
        }

    current_rows = RankHistory.query.filter_by(
        season_id=season_id,
        tourId=latest_week
    ).all()

    previous_rows = RankHistory.query.filter_by(
        season_id=season_id,
        tourId=latest_week - 1
    ).all()

    previous_lookup = {
        row.playerId: row
        for row in previous_rows
    }

    risers = []
    fallers = []

    for current in current_rows:

        previous = previous_lookup.get(current.playerId)

        if not previous:
            continue

        player = Player.query.get(current.playerId)

        if not player:
            continue

        movement = previous.rank - current.rank

        result = {
            "player": player,
            "previous_rank": previous.rank,
            "current_rank": current.rank,
            "movement": movement
        }

        if movement > 0:
            risers.append(result)

        elif movement < 0:
            fallers.append(result)

    risers.sort(
        key=lambda x: x["movement"],
        reverse=True
    )

    fallers.sort(
        key=lambda x: x["movement"]
    )

    return {
        "player_risers": risers[:10],
        "player_fallers": fallers[:10]
    }


def build_team_movers():
    active_season = Season.query.filter_by(active=True).first()
    season_id = active_season.id if active_season else 1

    latest_week = (
        db.session.query(func.max(TeamRankHistory.week))
        .filter(TeamRankHistory.season_id == season_id)
        .scalar()
    )

    if latest_week is None or latest_week <= 1:
        return {
            "team_risers": [],
            "team_fallers": []
        }

    current_rows = TeamRankHistory.query.filter_by(
        season_id=season_id,
        week=latest_week
    ).all()

    previous_rows = TeamRankHistory.query.filter_by(
        season_id=season_id,
        week=latest_week - 1
    ).all()

    previous_lookup = {
        row.teamId: row
        for row in previous_rows
    }

    risers = []
    fallers = []

    for current in current_rows:

        previous = previous_lookup.get(current.teamId)

        if not previous:
            continue

        team = Team.query.get(current.teamId)

        if not team:
            continue

        movement = previous.rank - current.rank

        result = {
            "team": team,
            "previous_rank": previous.rank,
            "current_rank": current.rank,
            "movement": movement
        }

        if movement > 0:
            risers.append(result)

        elif movement < 0:
            fallers.append(result)

    risers.sort(
        key=lambda x: x["movement"],
        reverse=True
    )

    fallers.sort(
        key=lambda x: x["movement"]
    )

    return {
        "team_risers": risers[:3],
        "team_fallers": fallers[:3]
    }




##################### STATISTICAL DASHBOARD ############################################################
def get_most_wins(limit=10):
    return (
        Player.query
        .order_by(Player.wins.desc(), Player.points.desc())
        .limit(limit)
        .all()
    )
def get_most_pins(limit=10):

    pin_counts = {}

    pins = Opponent.query.filter(
        Opponent.victory == True,
        Opponent.score >= 1000
    ).all()

    for pin in pins:
        pin_counts[pin.player_id] = pin_counts.get(pin.player_id, 0) + 1

    leaders = []

    for player_id, total in pin_counts.items():
        player = Player.query.get(player_id)

        if player:
            leaders.append({
                "player": player,
                "total": total
            })

    leaders.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    return leaders[:limit]
def get_highest_win_pct(limit=10, minimum_matches=10):

    leaders = []

    for player in Player.query.all():

        matches = (player.wins or 0) + (player.loss or 0)

        if matches < minimum_matches:
            continue

        pct = player.wins / matches

        leaders.append({
            "player": player,
            "total": pct
        })

    leaders.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    return leaders[:limit]
def get_highest_bonus_pct(limit=10, minimum_wins=10):

    bonus_wins = {}

    for win in Opponent.query.filter(
        Opponent.victory == True,
        Opponent.score >= 500
    ).all():

        bonus_wins[win.player_id] = bonus_wins.get(win.player_id, 0) + 1

    leaders = []

    for player in Player.query.all():

        wins = player.wins or 0

        if wins < minimum_wins:
            continue

        bonus = bonus_wins.get(player.id, 0)

        pct = bonus / wins

        leaders.append({
            "player": player,
            "total": pct,
            "bonus_wins": bonus
        })

    leaders.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    return leaders[:limit]

def get_most_classics(limit=10):

    classic_counts = {}

    classics = Opponent.query.filter(
        Opponent.fotn == True
    ).all()

    for fight in classics:

        # Count both fighters
        classic_counts[fight.player_id] = classic_counts.get(fight.player_id, 0) + 1
        classic_counts[fight.opponent_id] = classic_counts.get(fight.opponent_id, 0) + 1

    leaders = []

    for player_id, total in classic_counts.items():

        player = Player.query.get(player_id)

        if player:
            leaders.append({
                "player": player,
                "total": round(total / 2)
            })

    leaders.sort(
        key=lambda x: (
            x["total"],
            x["player"].wins
        ),
        reverse=True
    )

    return leaders[:limit]

def get_biggest_rivalries(limit=300):

    rivalry_counts = {}

    fights = Opponent.query.all()

    for fight in fights:

        # Always store the smaller ID first
        pair = tuple(sorted([
            fight.player_id,
            fight.opponent_id
        ]))

        if pair not in rivalry_counts:
            rivalry_counts[pair] = {
                "total": 0,
                "p1_wins": 0,
                "p2_wins": 0
            }

        rivalry_counts[pair]["total"] += 1

        # Count wins (each victory only appears once)
        if fight.victory:

            if fight.player_id == pair[0]:
                rivalry_counts[pair]["p1_wins"] += 1
            else:
                rivalry_counts[pair]["p2_wins"] += 1

    leaders = []

    for (player1_id, player2_id), stats in rivalry_counts.items():

        player1 = Player.query.get(player1_id)
        player2 = Player.query.get(player2_id)

        if not player1 or not player2:
            continue

        leaders.append({
            "player1": player1,
            "player2": player2,
            "total": round(stats["total"] / 2),
            "p1_wins": stats["p1_wins"],
            "p2_wins": stats["p2_wins"]
        })

    leaders.sort(
        key=lambda x: x["total"],
        reverse=True
    )

    return leaders[:limit]
def get_most_ot_fights(limit=10):

    ot_counts = {}

    fights = Opponent.query.filter(
        Opponent.score < 0
    ).all()

    for fight in fights:

        # Count both competitors
        ot_counts[fight.player_id] = ot_counts.get(fight.player_id, 0) + 1
        ot_counts[fight.opponent_id] = ot_counts.get(fight.opponent_id, 0) + 1

    leaders = []

    for player_id, total in ot_counts.items():

        player = Player.query.get(player_id)

        if player:
            leaders.append({
                "player": player,
                "total": round(total / 2)
            })

    leaders.sort(
        key=lambda x: (
            x["total"],
            x["player"].wins
        ),
        reverse=True
    )

    return leaders[:limit]

def build_league_leaders():

    return {

        "most_wins": get_most_wins(),

        "most_pins": get_most_pins(),

        "highest_win_pct": get_highest_win_pct(),

        "highest_bonus_pct": get_highest_bonus_pct(),

        "most_classics": get_most_classics(),

        "biggest_rivalries": get_biggest_rivalries(),

        "most_ot_fights": get_most_ot_fights()

    }

def build_today_banner(today=None):

    if today is None:
        today = datetime.now()

    return {
        "today_label": today.strftime("%A, %B %d")
    }
