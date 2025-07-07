import sys
import os
import pytest  


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Catalogue_Manager')))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

#  Helper to simulate login
def login(client, username='admin', password='admin123'):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

#  Valid login
def test_login_success(client):
    response = login(client)
    assert response.status_code == 200
    assert b'Catalogue' in response.data or b'Add New Catalogue' in response.data

#  Invalid login
def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'wronguser',
        'password': 'wrongpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data  


#  Get all catalogues
def test_get_all_catalogues(client):
    login(client)
    response = client.get('/api/catalogues')
    assert response.status_code == 200
    assert b'success' in response.data

#  Create a new catalogue
def test_create_catalogue(client):
    login(client)
    response = client.post('/api/catalogues', json={
        'catalogue_id': 999,
        'catalogue_name': 'Test Catalogue',
        'catalogue_version': 'v1.0',
        'is_cat_active': 1,
        'catalogue_start': '2025-09-01',
        'catalogue_end': '2025-12-31'
    })
    assert response.status_code == 201
    assert b'created successfully' in response.data

#  Get catalogue by ID
def test_get_catalogue_by_id(client):
    login(client)
    response = client.get('/api/catalogues/999')
    assert response.status_code in [200, 404]

#  Update catalogue
def test_update_catalogue(client):
    login(client)
    response = client.put('/api/catalogues/999', json={
        'catalogue_name': 'Updated Name',
        'catalogue_version': 'v2.0',
        'is_cat_active': 0,
        'catalogue_start': '2025-09-01',
        'catalogue_end': '2025-12-31'
    })
    assert response.status_code in [200, 404]

#  Delete catalogue
def test_delete_catalogue(client):
    login(client)
    response = client.delete('/api/catalogues/999')
    assert response.status_code in [200, 404]

#  Create catalogue with missing fields
def test_create_catalogue_missing_fields(client):
    login(client)
    response = client.post('/api/catalogues', json={
        'catalogue_id': 1000,
        'catalogue_name': 'Incomplete'
        
    })
    assert response.status_code == 400
    assert b'Invalid input' in response.data

#  Create catalogue with invalid date format
def test_create_catalogue_invalid_dates(client):
    login(client)
    response = client.post('/api/catalogues', json={
        'catalogue_id': 1001,
        'catalogue_name': 'Invalid Date Test',
        'catalogue_version': 'v1.0',
        'is_cat_active': 1,
        'catalogue_start': '31-12-2025',  # Invalid format
        'catalogue_end': '2025-12-31'
    })
    assert response.status_code == 400
    assert b'field types are incorrect' in response.data



#  Create catalogue with start date after end date
def test_create_catalogue_start_after_end(client):
    login(client)
    response = client.post('/api/catalogues', json={
        'catalogue_id': 1002,
        'catalogue_name': 'Date Order Test',
        'catalogue_version': 'v1.0',
        'is_cat_active': 1,
        'catalogue_start': '2025-12-31',
        'catalogue_end': '2025-01-01'
    })
    assert response.status_code == 400
    assert b'dates must be in the future' in response.data

