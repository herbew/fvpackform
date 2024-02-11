from __future__ import unicode_literals, absolute_import
from backend.tests.run_test import app, db, config

def test_psycopg2_connection_string():
    assert app.config['SQLALCHEMY_DATABASE_URI'] == config['DATABASE_URL_TEST']