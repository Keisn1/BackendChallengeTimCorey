#!/usr/bin/env python3


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test product" in response.data
    # assert b"bought by test_name1 on 2018-01-01" in response.data
    # assert b"test\nbody" in response.data
    # assert b'href="/buy/1/return"' in response.data
