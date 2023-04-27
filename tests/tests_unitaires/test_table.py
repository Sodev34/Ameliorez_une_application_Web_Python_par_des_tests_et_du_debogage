from server import app


def test_clubs_table():
    client = app.test_client()
    result = client.get("/clubs_table")
    assert result.status_code == 200
    assert b"clubs" in result.data
