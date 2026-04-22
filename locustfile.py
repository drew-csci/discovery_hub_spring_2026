from locust import HttpUser, task, between


class DiscoveryHubUser(HttpUser):
    """Basic load-test user for public endpoints.

    Run locally (example):
      locust -H http://127.0.0.1:8000
    Then open http://127.0.0.1:8089

    Note: This is intentionally unauthenticated to avoid relying on seeded accounts.
    """

    wait_time = between(1, 3)

    @task(3)
    def welcome(self):
        self.client.get("/")

    @task(5)
    def search(self):
        self.client.get("/search/", params={"q": "Developer", "per_page": 10, "page": 1})

    @task(1)
    def login_page(self):
        self.client.get("/accounts/login/")

    @task(1)
    def register_page(self):
        self.client.get("/accounts/register/")
