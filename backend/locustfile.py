from locust import HttpUser, task, between

class CalyxUser(HttpUser):
    wait_time = between(0.1, 0.2)
    
    @task(3)
    def check_health(self):
        self.client.get("/api/v1/health", name="/api/v1/health")

    @task(1)
    def try_unauthorized_access(self):
        with self.client.get("/api/v1/auth/me", catch_response=True, name="/api/v1/auth/me") as response:
            if response.status_code == 401:
                response.success()
            else:
                response.failure(f"Got status {response.status_code}")
