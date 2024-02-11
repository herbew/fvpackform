from __future__ import unicode_literals, absolute_import

import os
import pytest

from backend.tests.run_test import db, app as app_test

@pytest.fixture()
def app():

    app_test.config.update({
        "TESTING": True,
    })
    
    with app_test.app_context():   
        db.create_all()
        yield app_test  
        db.session.remove()  # looks like db.session.close() would work as well
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()