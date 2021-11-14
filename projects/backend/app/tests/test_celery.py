from typing import Dict

from app.config import Config
from fastapi.testclient import TestClient


def test_celery_worker_test(client: TestClient, superuser_token_headers: Dict[str, str]) -> None:
    data = {"msg": "test"}
    r = client.post(
        f"{Config.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
