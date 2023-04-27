from server import app

def test_book():
    client = app.test_client()
    competition = "Big Competition"
    club = "Simply Lift"
    result = client.get(f"/book/{competition}/{club}")
    assert result.status_code == 200
    assert b"club" in result.data
    assert b"competition" in result.data


