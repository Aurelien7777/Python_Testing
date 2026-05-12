from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def index(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        response = self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "2",
            },
        )

    @task(1)
    def load_public_points_board(self):
        self.client.get(
            "/points",
            name="Load public points board",
        )
