from server import app, clubs


def test_show_summary_with_valid_email():
    with app.test_client() as client:
        club_email = clubs[1]["email"]
        response = client.post("/showSummary", data=dict(email=club_email))
        assert response.status_code == 200