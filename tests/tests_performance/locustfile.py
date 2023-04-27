from locust import HttpUser, between, task

class PerformanceTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_index(self):
        self.client.get("/")

    @task
    def test_clubs_list(self):
        self.client.get("/clubs_table")

    @task
    def show_summary(self):
        email = "john@simplylift.co"  
        self.client.post("/showSummary", data={"email": email})

    @task
    def book(self):
        competition = "Big Competition"  
        club = "Simply Lift" 
        self.client.get(f"/book/{competition}/{club}")


    @task
    def purchase_places(self):
        club = "Simply Lift"  
        competition = "Big Competition"  
        places = "2"  
        response = self.client.post("/purchasePlaces", data={
            "club": club,
            "competition": competition,
            "places": places
        })
        assert response.elapsed.total_seconds() < 2, f"Response took too long: {response.elapsed.total_seconds()}"
    

   
   

  


   