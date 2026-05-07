import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from booking_rules import (
    is_valid_place_number,
    has_enough_competition_places,
    is_within_booking_limit,
    has_enough_points,
    calculate_remaining_places,
    calculate_remaining_points,
)


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    
    if not club:
        flash("Sorry, that email was not found")
        return redirect(url_for("index"))
    
    return render_template('welcome.html',
                        club=club[0],
                        competitions=competitions,
                        clubs=clubs)



@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club_list = [
        c for c in clubs
        if c['name'] == club
    ]

    found_competition_list = [
        c for c in competitions
        if c['name'] == competition
    ]

    if not found_club_list or not found_competition_list:
        flash("Something went wrong-please try again")
        return redirect(url_for("index"))

    foundClub = found_club_list[0]
    foundCompetition = found_competition_list[0]

    competition_date = datetime.strptime(
        foundCompetition["date"],
        "%Y-%m-%d %H:%M:%S"
    )

    now = datetime.now()

    if competition_date < now:
        flash("You cannot book places for a past competition")
        return render_template(
            'welcome.html',
            club=foundClub,
            competitions=competitions,
            clubs=clubs
        )

    return render_template(
        'booking.html',
        club=foundClub,
        competition=foundCompetition
    )


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition_name = request.form.get('competition')
    club_name = request.form.get('club')
    places = request.form.get('places')

    competition_list = [
        c for c in competitions
        if c['name'] == competition_name
    ]

    if not competition_list:
        flash("Sorry, competition was not found")
        return redirect(url_for("index"))

    club_list = [
        c for c in clubs
        if c['name'] == club_name
    ]

    if not club_list:
        flash("Sorry, that club was not found")
        return redirect(url_for("index"))

    competition = competition_list[0]
    club = club_list[0]

    try:
        placesRequired = int(places)
    except (TypeError, ValueError):
        flash("Please enter a valid number of places")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            clubs=clubs
        )

    point_club = int(club['points'])
    places_competition = int(competition['numberOfPlaces'])

    if not is_valid_place_number(placesRequired):
        flash("You must book at least 1 place")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            clubs=clubs
        )

    if not has_enough_competition_places(
        placesRequired,
        places_competition
    ):
        flash('You are not authorized to book more than available places!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            clubs=clubs
        )

    if not is_within_booking_limit(placesRequired):
        flash('You are not authorized to book more than 12 places per competition!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            clubs=clubs
        )

    if not has_enough_points(point_club, placesRequired):
        flash('You are not authorized to book this number of places!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions,
            clubs=clubs
        )

    flash('Great-booking complete!')

    competition['numberOfPlaces'] = calculate_remaining_places(
        places_competition,
        placesRequired
    )

    club['points'] = calculate_remaining_points(
        point_club,
        placesRequired
    )

    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        clubs=clubs
    )


@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))