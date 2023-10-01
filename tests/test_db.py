#!/usr/bin/env python3
import sqlite3
from _pytest import monkeypatch
from flask import Flask

import pytest
from backendProject.db import get_db


def test_get_close_db(app: Flask):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        # shall throw error since connection should be closed
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("backendProject.db.init_db", fake_init_db)
    result = runner.invoke(args=["init-db"])
    assert "Initialized Database" in result.output
    assert Recorder.called
