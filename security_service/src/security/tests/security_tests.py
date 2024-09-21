from datetime import datetime, timezone, timedelta

import pytest
import requests
from starlette.testclient import TestClient

from src.common.database import DatabaseSessionManager, get_db_session
from src.common.serializer.auth_serializer import AuthPayload
from src.common.settings import settings
from src.main import app
from src.security.domain.models.entities import security_sql_model
import jwt

sessionmanager = DatabaseSessionManager(settings.TEST_DATABASE_URL, {"echo": True})


async def override_get_db_session():
    async with sessionmanager.connect() as connection:
        await connection.run_sync(security_sql_model.Base.metadata.create_all)
    async with sessionmanager.session() as session:
        yield session

    session.rollback()
    connection.close()


app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)


@pytest.fixture(scope="session")
def fake_token(
):
    auth = AuthPayload(sub=1,
                       permissions=["me", "security:read",
                                    "security:write",
                                    "security:delete",
                                    "security:read:all"],
                       exp=datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                       iat=datetime.now(timezone.utc)
                       )

    token = jwt.encode(auth.dict(), settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_list_securities_data(fake_token):
    response = client.get("/security/", headers=fake_token)
    assert response.status_code == 200


def test_get_security_data(fake_token):
    response = client.get("/security/1256", headers=fake_token)
    assert response.status_code == 404


def test_create_security_data(fake_token):
    response = client.post(
        "/security/",
        json={
            "title": "Test1",
        },
        headers=fake_token
    )
    assert response.status_code == 201


def test_update_security_data(fake_token):
    response = client.put(
        "/security/1000",
        json={
            "title": "Test",
        },
        headers=fake_token
    )
    assert response.status_code == 404


def test_delete_security_data(fake_token):
    response = client.delete("/security/1252"
                             , headers=fake_token)
    assert response.status_code == 404
