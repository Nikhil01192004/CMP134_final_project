"""Unit tests for mission log service."""

from app.logs.service import write_log, get_logs


class TestLogService:
    def test_write_log(self, db_session):
        log = write_log(db_session, username="alice", command="MOVE x=1 y=2", response="ok")
        assert log.id is not None
        assert log.username == "alice"
        assert log.command == "MOVE x=1 y=2"

    def test_get_logs_ordered(self, db_session):
        write_log(db_session, username="alice", command="CMD1", response="r1")
        write_log(db_session, username="bob", command="CMD2", response="r2")
        logs = get_logs(db_session)
        assert len(logs) == 2
        # Most recent first
        assert logs[0].command == "CMD2"

    def test_get_logs_limit(self, db_session):
        for i in range(5):
            write_log(db_session, username="u", command=f"CMD{i}", response="r")
        logs = get_logs(db_session, limit=3)
        assert len(logs) == 3


class TestLogsEndpoint:
    def _get_token(self, client, username="logviewer", role="viewer"):
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

    def test_logs_requires_auth(self, client):
        res = client.get("/api/logs/")
        assert res.status_code == 401

    def test_logs_returns_empty(self, client):
        token = self._get_token(client)
        res = client.get("/api/logs/", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json() == []
