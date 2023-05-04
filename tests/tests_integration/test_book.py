from server import app, competitions, clubs


def test_book_with_valid_club_and_competition():
    with app.test_client() as client:
        club_name = clubs[1]["name"]
        competition_name = competitions[1]["name"]
        response = client.get(f"/book/{competition_name}/{club_name}")
        assert response.status_code == 200
