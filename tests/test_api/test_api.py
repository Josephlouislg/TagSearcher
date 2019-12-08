from tests.conftest import create_app


async def test_200(test_client):
    client = await test_client(create_app)
    resp = await client.post(
        '/text', 
        json={"text": "test1"},
        headers={'Content-Type': 'application/json'}
    )
    assert resp.status == 200
    data = await resp.json()
    assert 'tags' in data
    assert 'test1' in data['tags']


async def test_400(test_client):
    client = await test_client(create_app)
    resp = await client.post(
        '/text', 
        data={"text": "test1"},
        headers={'Content-Type': 'application/json'}
    )
    assert resp.status == 400


async def test_invalid_payload(test_client):
    client = await test_client(create_app)
    resp = await client.post(
        '/text', 
        json={"test": "test1"},
        headers={'Content-Type': 'application/json'}
    )
    assert resp.status == 400


async def test_empty_text(test_client):
    client = await test_client(create_app)
    resp = await client.post(
        '/text', 
        json={"text": ""},
        headers={'Content-Type': 'application/json'}
    )
    assert resp.status == 200
    data = await resp.json()
    assert 'tags' in data
    assert data['tags'] == []
