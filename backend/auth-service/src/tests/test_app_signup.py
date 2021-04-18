
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import sys
import os
try:
    import main
except:
    sys.path.append(os.getcwd())
    import main
#client = TestClient(main.auth_service)


def test_signup():
    with TestClient(main.auth_service) as client:
        response = client.post("/api/users/signup", json={
            "username": "johndoe2",
            "email": "jdoe@example.com",
            "password": "123456",
            "full_name": "John Doe"
        })
        assert response.status_code == 201


def test_signup_bad_email():
    with TestClient(main.auth_service) as client:
        response = client.post("/api/users/signup", json={
            "username": "johndoe2",
            "email": "jdoeexample.com",
            "password": "123456",
            "full_name": "John Doe"
        })
        assert response.status_code == 422


def test_signup_bad_password():
    with TestClient(main.auth_service) as client:
        response = client.post("/api/users/signup", json={
        })
        assert response.status_code == 422
