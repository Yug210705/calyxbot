from locust import HttpUser, task, between
import uuid

class CalyxUser(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        # We assume the user has to signup and login, or we mock auth for the test
        self.email = f"loadtest_{uuid.uuid4()}@example.com"
        self.password = "password"
        
        # In a real test against staging, we would hit the Supabase / GoTrue endpoints
        # or use a test fixture token. For this verification script, we just hit the health endpoint
        # and simulate the domain flows.
        pass

    @task(3)
    def check_health(self):
        self.client.get("/api/v1/health")

    @task(1)
    def create_organization(self):
        # Requires auth token in reality
        self.client.post("/api/v1/organizations/", json={
            "name": f"Org {uuid.uuid4()}",
            "slug": f"org-{uuid.uuid4()}"
        }, headers={"Authorization": "Bearer MOCK_TOKEN"})
