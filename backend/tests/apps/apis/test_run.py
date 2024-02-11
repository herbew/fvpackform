from __future__ import unicode_literals, absolute_import

import json

def test_api_welcome(app):
    client = app.test_client()
    resp = client.get('/api/')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Welcome' in data['title']
    assert 'PackForm' in data['desc']
    