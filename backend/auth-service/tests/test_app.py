import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import src.main

client = TestClient(src.main.auth_service)


def test_create_user():
    response = client.post("/signup", json={
        "username": "johndoe2",
        "email": "jdoe@example.com",
        "password": "123456",
        "full_name": "John Doe"
    })
    assert response.status_code == 201
