"""Unit tests for auth: registration, login, JWT, RBAC."""

from app.auth.service import hash_password, verify_password, create_access_token, decode_token, permissions_factory


class TestPasswordHashing:
    def test_hash_and_verify(self):
        hashed = hash_password("securepass123")
        assert verify_password("securepass123", hashed)

    def test_wrong_password_fails(self):
        hashed = hash_password("securepass123")
        assert not verify_password("wrongpassword", hashed)


class TestJWT:
    def test_create_and_decode(self):
        token = create_access_token({"sub": "alice", "role": "commander"})
        payload = decode_token(token)
        assert payload["sub"] == "alice"
        assert payload["role"] == "commander"

    def test_invalid_token_raises(self):
        import pytest
        with pytest.raises(Exception):
            decode_token("not.a.valid.token")


class TestRBAC:
    def test_viewer_cannot_move(self):
        perms = permissions_factory("viewer")
        assert perms.can_move is False
        assert perms.can_view_status is True
        assert perms.can_view_logs is True

    def test_commander_can_move(self):
        perms = permissions_factory("commander")
        assert perms.can_move is True
        assert perms.can_view_status is True
        assert perms.can_view_logs is True


class TestRegisterEndpoint:
    def test_register_success(self, client):
        res = client.post("/api/auth/register", json={
            "username": "testuser",
            "password": "password123",
            "role": "viewer",
        })
        assert res.status_code == 201
        data = res.json()
        assert data["username"] == "testuser"
        assert data["role"] == "viewer"

    def test_register_duplicate_user(self, client):
        client.post("/api/auth/register", json={
            "username": "dup",
            "password": "password123",
            "role": "viewer",
        })
        res = client.post("/api/auth/register", json={
            "username": "dup",
            "password": "password123",
            "role": "viewer",
        })
        assert res.status_code == 400


class TestLoginEndpoint:
    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "username": "loginuser",
            "password": "mypassword",
            "role": "commander",
        })
        res = client.post("/api/auth/login", json={
            "username": "loginuser",
            "password": "mypassword",
        })
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["role"] == "commander"

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "username": "loginuser2",
            "password": "correctpass",
            "role": "viewer",
        })
        res = client.post("/api/auth/login", json={
            "username": "loginuser2",
            "password": "wrongpass",
        })
        assert res.status_code == 401
