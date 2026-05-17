"""Tests for robot endpoint access control — Commander vs Viewer."""


class TestRobotRBAC:
    def _register_and_login(self, client, username, role):
        client.post("/api/auth/register", json={
            "username": username,
            "password": "password123",
            "role": role,
        })
        res = client.post("/api/auth/login", json={
            "username": username,
            "password": "password123",
        })
        return res.json()["access_token"]

    def test_viewer_cannot_move(self, client):
        token = self._register_and_login(client, "viewer1", "viewer")
        res = client.post(
            "/api/robot/move",
            json={"x": 1, "y": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert res.status_code == 403

    def test_move_requires_auth(self, client):
        res = client.post("/api/robot/move", json={"x": 1, "y": 1})
        assert res.status_code == 401

    def test_status_requires_auth(self, client):
        res = client.get("/api/robot/status")
        assert res.status_code == 401
