import pytest

def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    response = client.post(
        '/authentication/register',
        data={'user_name': 'obama', 'password': 'unsafePassword123'}
    )
    assert response.headers['Location'] == '/authentication/login'

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
    ('', '', b'Username required'),
    ('ab', '', b'Username too short (minimum 3 characters)'),
    ('test', '', b'Your password is required'),
    ('test', 'test', b'Password too short (minimum 8 characters)'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'AWOL' in response.data

def test_login_required_to_review(client):
    response = client.post('/track/2/review')
    assert response.headers['Location'] == '/authentication/login'
