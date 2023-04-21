from locust import HttpUser, task, between
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def create_user(self):
        headers = {'Content-Type': 'application/json'}
        payload = {'username': 'John Doe', 'email': 'john.doe@example.com', 'password' : 'abobrinha', 'role': 'USER'}
        self.client.post('/user', headers=headers, json=payload)
