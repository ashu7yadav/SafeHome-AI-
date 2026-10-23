# SafeHome AI — FastAPI Backend

Modular, production-ready REST API for the **SafeHome AI** smart-home security and automation platform.

## Architecture

- **Framework:** FastAPI (Python 3.11+)
- **ORM & Database:** SQLAlchemy with SQLite for local development (PostgreSQL compatible)
- **Validation:** Pydantic v2
- **Authentication:** JWT Access Tokens with native bcrypt password hashing
- **Testing:** Pytest with TestClient & in-memory SQLite (`StaticPool`)

```
backend/
├── app/
│   ├── main.py              # FastAPI app setup, CORS, lifespan, exception handlers
│   ├── core/
│   │   ├── config.py        # Settings loaded via Pydantic & python-dotenv
│   │   ├── database.py      # SQLAlchemy engine, sessionmaker, get_db dependency
│   │   └── security.py      # Direct bcrypt hashing and JWT encoding/decoding
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py          # User & household isolation
│   │   ├── device.py        # Smart devices & JSON config
│   │   ├── security_event.py# Audit logs, detections, severity
│   │   ├── visitor.py       # Visitor passes & approval lifecycle
│   │   ├── automation.py    # Trigger rules & actions
│   │   └── notification.py  # User notifications & read flags
│   ├── schemas/             # Pydantic v2 request & response schemas
│   ├── api/                 # Modular API route controllers
│   │   ├── auth.py          # /api/auth (register, login, me, logout)
│   │   ├── dashboard.py     # /api/dashboard/summary
│   │   ├── devices.py       # /api/devices (CRUD & power/brightness/temp/blinds/vacuum)
│   │   ├── cameras.py       # /api/cameras (simulated preview metadata & status)
│   │   ├── security.py      # /api/security (events, demo triggers, acknowledge)
│   │   ├── visitors.py      # /api/visitors (passes, approve, revoke)
│   │   ├── automations.py   # /api/automations (routines, toggles, test run)
│   │   └── notifications.py # /api/notifications (list, read, count)
│   └── services/            # Clean business logic layer
├── tests/                   # Pytest test suite (9 automated tests)
├── seed.py                  # Idempotent demo database seeder
├── requirements.txt
├── .env.example
└── README.md
```

## Getting Started

### 1. Setup Virtual Environment
```bash
cd backend
python -m venv .venv
```

**Activate Virtual Environment (Windows PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Seed Demo Data
Populate the database with demo cameras, lights, thermostat, lock, vacuum, events, and automations:
```bash
python seed.py
```

### 4. Run the Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```

- API Base: [http://localhost:8000/api](http://localhost:8000/api)
- Interactive Swagger UI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)

### 5. Run Automated Tests
```bash
python -m pytest
```

---

## Default Demo Credentials
- **Email:** `alex@safehome.ai`
- **Password:** `SafeHome123!`
- **Household ID:** `00000000-0000-0000-0000-000000000001`
