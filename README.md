# SafeHome AI — Smart Home Security Platform (Full-Stack)

SafeHome AI is a smart-home security and automation platform built with **React + Vite** on the frontend and **FastAPI + SQLAlchemy** on the backend.

It brings smart-device controls, camera status, security events, visitor management, automations, and notifications into a single dashboard.

![SafeHome AI Dashboard Preview](https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85)

> **Note:** Camera images and device actions may be simulated. Real camera feeds and physical device control require compatible integrations.

## Technology Stack

- **Frontend:** React 18, Vite 6, CSS3, Lucide React
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy ORM
- **Database:** SQLite, with potential PostgreSQL migration
- **Validation:** Pydantic
- **Authentication:** JWT access tokens and password hashing
- **Testing:** Pytest and FastAPI TestClient

## Features

- Smart-home dashboard and device status
- Smart lights, thermostat, blinds, and vacuum controls
- Security camera status and preview interface
- Security event history and alert acknowledgement
- Visitor access management
- Automation rules
- Notifications and unread counts
- API documentation through Swagger UI
- Automated backend tests

## Quick Start

Run the backend and frontend in separate terminals.

### 1. Backend — FastAPI

Open PowerShell in the project root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend — React + Vite

Open a second terminal in the frontend project root:

```powershell
npm install
npm run dev
```

### Local URLs

- Frontend: http://localhost:5173/
- API documentation: http://localhost:8000/docs
- Health endpoint: http://localhost:8000/health

## Demo Credentials

If the database seed script creates this account:

- **Email:** `alex@safehome.ai`
- **Password:** `SafeHome123!`

These credentials are for local demonstrations only. Never use them for a production deployment.

## API Endpoints

### Authentication

- `POST /api/auth/register` — Register a user
- `POST /api/auth/login` — Authenticate a user
- `GET /api/auth/me` — Retrieve the current user
- `POST /api/auth/logout` — Log out, if implemented

### Dashboard

- `GET /api/dashboard/summary` — Retrieve dashboard metrics

### Smart Devices

- `GET /api/devices` — List devices
- `GET /api/devices/{id}` — Get device details
- `POST /api/devices` — Register a device
- `PATCH /api/devices/{id}` — Update device details
- `DELETE /api/devices/{id}` — Remove a device
- `PATCH /api/devices/{id}/power` — Update power state
- `PATCH /api/devices/{id}/brightness` — Set brightness
- `PATCH /api/devices/{id}/temperature` — Set temperature
- `PATCH /api/devices/{id}/blinds` — Adjust blinds
- `PATCH /api/devices/{id}/vacuum` — Update vacuum state

### Cameras

- `GET /api/cameras` — List cameras
- `GET /api/cameras/{id}` — Get camera details
- `GET /api/cameras/{id}/status` — Retrieve camera status

### Security

- `GET /api/security/events` — Retrieve security events
- `POST /api/security/events/demo` — Generate a demo event
- `PATCH /api/security/events/{id}/acknowledge` — Acknowledge an event
- `GET /api/security/status` — Retrieve security status

### Visitors

- `GET /api/visitors` — List visitors
- `POST /api/visitors` — Create a visitor record
- `PATCH /api/visitors/{id}/approve` — Approve a request
- `PATCH /api/visitors/{id}/revoke` — Revoke access
- `DELETE /api/visitors/{id}` — Delete a visitor record

### Automations

- `GET /api/automations` — List automation rules
- `POST /api/automations` — Create a rule
- `PATCH /api/automations/{id}/toggle` — Enable or disable a rule
- `POST /api/automations/{id}/test` — Test a demo automation

### Notifications

- `GET /api/notifications` — List notifications
- `GET /api/notifications/unread-count` — Retrieve unread count
- `PATCH /api/notifications/{id}/read` — Mark a notification as read
- `PATCH /api/notifications/read-all` — Mark all notifications as read

> Check the running application at `/docs` to confirm which endpoints are implemented.

## Running Tests

```powershell
cd backend
python -m pytest
```

The supplied project description reports a previous run with nine passing tests. Run the command against your current code to verify the actual result.

## Environment Configuration

Configure the frontend API URL using an environment file when supported:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

Keep secrets in environment variables. Never commit production credentials, JWT secrets, passwords, or private device tokens.

## Security Considerations

- Use HTTPS in production.
- Replace development secrets before deployment.
- Restrict CORS to trusted frontend origins.
- Enforce household-level authorization.
- Hash passwords securely.
- Avoid logging sensitive credentials.
- Clearly distinguish simulated events from verified real-world events.

## Project Status

SafeHome AI is designed as a full-stack smart-home prototype. Real camera streams, physical device control, and hardware-based visitor access require additional integrations and testing.

## License

Add your chosen open-source license before publishing the project publicly.
# SafeHome-AI-
