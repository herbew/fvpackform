from __future__ import unicode_literals, absolute_import

def test_welcome(app):
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert 'Welcome to PackForm' in resp.data.decode()