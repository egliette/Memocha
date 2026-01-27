import random

from locust import HttpUser, between, task


class MemochaUser(HttpUser):
    wait_time = between(1, 3)

    test_messages = [
        "Hello, how are you?",
        "What's the weather like today?",
        "Can you help me with a coding problem?",
        "Tell me a joke",
        "What is machine learning?",
        "How do I cook pasta?",
        "Explain quantum computing",
        "What are your capabilities?",
    ]

    def on_start(self):
        """Create a session on first request and store the UUID."""
        self.session_id = None
        message = random.choice(self.test_messages)
        payload = {"message": message}

        with self.client.post("/chat", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                data = response.json()
                self.session_id = data.get("session_id")
            else:
                response.failure(f"Status: {response.status_code}")

    @task(3)
    def chat_simple(self):
        """Non-streaming chat"""
        message = random.choice(self.test_messages)
        payload = {"message": message}
        if self.session_id:
            payload["session_id"] = self.session_id

        with self.client.post("/chat", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                if not self.session_id:
                    data = response.json()
                    self.session_id = data.get("session_id")
            else:
                response.failure(f"Status: {response.status_code}")

    @task(1)
    def chat_stream(self):
        """Streaming chat"""
        message = random.choice(self.test_messages)
        payload = {"message": message}
        if self.session_id:
            payload["session_id"] = self.session_id

        with self.client.post(
            "/chat/stream", json=payload, catch_response=True, stream=True
        ) as response:
            if response.status_code == 200:
                for __ in response.iter_content(chunk_size=1024):
                    pass
                response.success()
            else:
                response.failure(f"Status: {response.status_code}")
