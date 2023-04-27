from server import app


def test_purchasePlaces():
    client = app.test_client()
    result = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Big Competition",
            "places": "2",
        },
    )
    assert result.status_code == 200
    assert b"Great-booking complete!" in result.data


def test_purchasePlaces_invalid_places():
    client = app.test_client()
    result = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Big Competition",
            "places": "-1",
        },
    )
    assert result.status_code == 302


def test_purchasePlaces_invalid_places_exceed_club_points():
    client = app.test_client()
    result = client.post(
        "/purchasePlaces",
        data={
            "club": "Iron Temple",
            "competition": "Big Competition",
            "places": "100",
        },
    )
    assert result.status_code == 302


def test_purchasePlaces_invalid_max_places():
    client = app.test_client()
    result = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Big Competition",
            "places": "13",
        },
    )
    assert result.status_code == 200
    assert b"You can reserve a maximum of 12 places in a competition." in result.data


def test_purchasePlaces_invalid_not_enough_places():
    client = app.test_client()
    result = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Small Competition",
            "places": "10",
        },
    )
    assert result.status_code == 200
    assert b"There are not enough places available for this competition." in result.data
