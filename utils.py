from datetime import datetime
import json


def load_clubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def competition_date(competitions: list):
    for comp in competitions:
        try:
            comp["past"] = datetime.now() > datetime.strptime(
                comp["date"][2:], "%y-%m-%d %H:%M:%S"
            )
        except ValueError:
            pass
    return competitions


def comp_reserved_places(comps, clubs_list):
    places = []
    for comp in comps:
        for club in clubs_list:
            places.append({"competition": comp["name"], "reserved": [0, club["name"]]})

    return places


def update_comp_reserved_places(competition, club, placesRequired, places_reserved):
    for item in places_reserved:
        if item["competition"] == competition["name"]:
            if (
                item["reserved"][1] == club["name"]
                and item["reserved"][0] + placesRequired <= 12
            ):
                item["reserved"][0] += placesRequired
                return True
    return False


