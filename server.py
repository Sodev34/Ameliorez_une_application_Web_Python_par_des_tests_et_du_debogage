from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for

def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def comp_reserved_places(comps, clubs_list):
    places = []
    for comp in comps:
        for club in clubs_list:
            places.append({"competition": comp["name"], "reserved": [0, club["name"]]})

    return places


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()
places_reserved = comp_reserved_places(competitions, clubs)


def update_comp_reserved_places(competition, club, placesRequired):
    for item in places_reserved:
        if item["competition"] == competition["name"]:
            if (
                item["reserved"][1] == club["name"]
                and item["reserved"][0] + placesRequired <= 12
            ):
                item["reserved"][0] += placesRequired
                return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    except IndexError:
        return render_template('index.html', error="Unknown Email"), 403


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    if placesRequired < 0 or placesRequired > int(club["points"]):
        flash("enter a valid number")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )
    elif placesRequired > 12:
        flash("You can reserve a maximum of 12 places in a competition.")
        return render_template("booking.html", club=club, competition=competition)
    elif int(competition["numberOfPlaces"]) < placesRequired:
        flash("There are not enough places available for this competition.")
        return render_template("booking.html", club=club, competition=competition)
    else:
        try:
            update_comp_reserved_places(competition, club, placesRequired)
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = int(club["points"]) - placesRequired
            flash("Great-booking complete!")
            return render_template("welcome.html", club=club, competitions=competitions)

        except ValueError:
            flash("unknown error")
            return render_template("booking.html", club=club, competition=competition)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
