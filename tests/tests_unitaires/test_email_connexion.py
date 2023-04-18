from server import app

class TestEmail:

    client = app.test_client()

    def test_showSummary_valid_email(self):
        result = self.client.post("/showSummary", data=dict(email="john@simplylift.co"))
        assert result.status_code == 200

    def test_showSummary_invalide_email(self):
        result = self.client.post("/showSummary", data=dict(email="invalide@mail.com"))
        assert result.status_code == 403