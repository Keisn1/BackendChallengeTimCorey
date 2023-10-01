#!/usr/bin/env python3

import pytest
from flask import g, session
from backendProject.db import get_db


def test_register(client, app):
    assert (
        client.get("/auth/register").status_code == 200
    )  # tests if page renders correctly (if rendering fails, Flask would return 500)
    response = client.post(
        "/auth/register",
        data={"client_name": "a", "client_email": "a", "password": "a"},
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert (
            get_db()
            .execute(
                "SELECT * FROM clients WHERE client_email = 'a'",
            )
            .fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("client_name", "client_email", "password", "message"),
    (
        ("", "a", "a", b"Client_name is required"),
        ("a", "", "a", b"Email is required"),
        ("a", "a", "", b"Password is required"),
        ("test_name1", "test_email1", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, client_name, client_email, password, message):
    response = client.post(
        "/auth/register",
        data={
            "client_name": client_name,
            "client_email": client_email,
            "password": password,
        },
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"
    with client:
        client.get("/")
        assert session["client_id"] == 1
        assert g.user["client_name"] == "test_name1"


@pytest.mark.parametrize(
    ("client_email", "password", "message"),
    (
        ("abc", "abc", b"Incorrect client_email"),
        ("test_email1", "a", b"Incorred password"),
    ),
)
def test_login_validate_input(auth, client_email, password, message):
    response = auth.login(client_email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
