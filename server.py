from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, url_for

from utils import (
    load_clubs,
    load_competitions,
    competition_date,
    comp_reserved_places,
    update_comp_reserved_places,
)


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()
places_reserved = comp_reserved_places(competitions, clubs)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clubs_table")
def clubs_table():
    return render_template("clubs_table.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        d_competitions = competition_date(competitions)
        return render_template("welcome.html", club=club, competitions=d_competitions)
    except IndexError:
        flash("Unknown Email")
        return render_template("index.html"), 403


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    places_required = int(request.form["places"])
    if places_required < 0 or places_required > int(club["points"]):
        flash("enter a valid number")
        return redirect(
            url_for("book", club=club["name"], competition=competition["name"])
        )
    elif places_required > 12:
        flash("You can reserve a maximum of 12 places in a competition.")
        return render_template("booking.html", club=club, competition=competition)
    elif int(competition["numberOfPlaces"]) < places_required:
        flash("There are not enough places available for this competition.")
        return render_template("booking.html", club=club, competition=competition)
    else:
        try:
            update_comp_reserved_places(
                competition, club, places_required, places_reserved
            )
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - places_required
            )
            club["points"] = int(club["points"]) - places_required
            flash(
                "Great-booking complete! You have reserved {} seats.".format(
                    places_required
                )
            )
            return render_template("welcome.html", club=club, competitions=competitions)

        except ValueError:
            flash("unknown error")
            return render_template("booking.html", club=club, competition=competition)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
