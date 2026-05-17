# Robot Management System

Full-stack web application for managing a virtual robot via REST API and WebSocket telemetry.

## Tech Stack
- **Frontend:** React (Vite)
- **Backend:** Python — FastAPI
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Auth:** JWT (python-jose) + bcrypt
- **Robot Comms:** httpx (REST) + websockets
- **Containerisation:** Docker + docker-compose
- **CI/CD:** GitHub Actions

## Quick Start

```bash
# Start all 4 services
docker-compose up --build
```

| Service   | URL                        |
|-----------|----------------------------|
| Frontend  | http://localhost:5173       |
| Backend   | http://localhost:8000       |
| Robot     | http://localhost:5000       |
| API Docs  | http://localhost:8000/docs  |

## Project Structure

```
robot-management-system/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── auth/      # JWT auth, RBAC, User model
│   │   ├── robot/     # httpx client, WebSocket handler
│   │   ├── logs/      # Mission audit log
│   │   └── database.py
│   ├── tests/         # pytest test suite
│   └── Dockerfile
├── frontend/          # React (Vite) application
│   ├── src/
│   │   ├── pages/     # Login, Register, Dashboard
│   │   ├── components/# GridMap, StatusBar, CommandPanel, AuditLog
│   │   ├── context/   # AuthContext (JWT storage)
│   │   └── services/  # API calls, WebSocket client
│   └── Dockerfile
├── docker-compose.yml
└── .github/workflows/ci.yml
```

## Design Patterns
- **Observer** — WebSocket telemetry broadcasts to all subscribed frontend components
- **Singleton** — Single DB engine and httpx robot client instances
- **Factory** — Role-based permission objects (Viewer vs Commander)

## Roles
- **Viewer** — Can view robot status, map, and logs. Cannot send move commands.
- **Commander** — Full access including move commands.

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest -v
```
