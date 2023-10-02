#!/usr/bin/env python3


def test_index(client, auth):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test product" in response.data
    assert b"was bought on 2018-01-01" in response.data
    assert b"test\ndescription" in response.data

    assert b"13 of test product" in response.data
    assert b"Bought on 2018-01-01" in response.data
    assert b"Return test product" in response.data
    assert b'href="/1/return_product"' in response.data


def test_buy_product(client, auth, app):
    auth.login()
    assert client.get("/buy_product").status_code == 200
