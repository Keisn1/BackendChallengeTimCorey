#!/usr/bin/env python3

from backendProject import create_app


def test_config():
    """
    Tests for default configuration
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    response = client.get("/hello")
    assert response.data == b"Hello World\n"
