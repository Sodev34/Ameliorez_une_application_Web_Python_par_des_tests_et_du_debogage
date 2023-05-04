from server import app, competitions, clubs


def test_purchase_places_with_valid_input():
    with app.test_client() as client:
        competition_name = competitions[1]["name"]
        club_name = clubs[1]["name"]
        response = client.post(
            "/purchasePlaces",
            data=dict(competition=competition_name, club=club_name, places=2),
        )
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data


def test_purchase_places_with_invalid_input():
    with app.test_client() as client:
        competition_name = competitions[0]["name"]
        club_name = clubs[0]["name"]
        response = client.post(
            "/purchasePlaces",
            data=dict(competition=competition_name, club=club_name, places=13),
        )
        assert response.status_code == 200
        assert (
            b"You can reserve a maximum of 12 places in a competition." in response.data
        )
