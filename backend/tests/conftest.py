import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models  # Import all models so Base knows all tables!
from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.user import User
from app.main import app

# StaticPool ensures that all connections in the test process share the exact same in-memory SQLite database!
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session):
    user = User(
        id="test-user-id-001",
        household_id="test-household-001",
        full_name="Test Homeowner",
        email="test@safehome.ai",
        password_hash=get_password_hash("SecretPassword123!"),
        role="homeowner",
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(test_user):
    token = create_access_token(
        subject=test_user.id,
        household_id=test_user.household_id,
        role=test_user.role
    )
    return {"Authorization": f"Bearer {token}"}
