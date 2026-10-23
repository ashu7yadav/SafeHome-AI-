def test_register_user_success(client):
    payload = {
        "email": "newuser@safehome.ai",
        "full_name": "Jordan Lee",
        "password": "StrongPassword123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "newuser@safehome.ai"


def test_register_duplicate_email(client, test_user):
    payload = {
        "email": test_user.email,
        "full_name": "Duplicate User",
        "password": "AnotherPassword123!"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_success(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "SecretPassword123!"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == test_user.email


def test_login_invalid_password(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "WrongPassword999!"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user_me(client, auth_headers, test_user):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["email"] == test_user.email
