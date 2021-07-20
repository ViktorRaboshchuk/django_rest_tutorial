from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def check_snippets(self):
        self.client.get("snippets")
        self.client.get("snippets/2/")
