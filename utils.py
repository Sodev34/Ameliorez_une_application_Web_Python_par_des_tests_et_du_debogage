from datetime import datetime
import json


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


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


def update_comp_reserved_places(competition, club, places_required, places_reserved):
    for item in places_reserved:
        if item["competition"] == competition["name"]:
            if (
                item["reserved"][1] == club["name"]
                and item["reserved"][0] + places_required <= 12
            ):
                item["reserved"][0] += places_required
                return True
    return False
