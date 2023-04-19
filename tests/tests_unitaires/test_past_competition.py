import server
from server import app

class TestPastCompetition:
    client = app.test_client()
    competitions = [
        {
            "name": "Closed",
            "date": "2019-09-21 15:00:00",
            "numberOfPlaces": "20",
            "numberOfPlacesTaken": "20"  
        },
        {
            "name": "Open",
            "date": "2023-09-27 09:00:00",
            "numberOfPlaces": "20",
            "numberOfPlacesTaken": "0" 
        }
    ]

    club = [
        {
            "name": "Test club",
            "email": "club@gmail.com",
            "points": "13"
        }
    ]


    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.club

   