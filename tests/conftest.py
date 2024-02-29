# from src.shared.database import get_db
# https://fastapi.tiangolo.com/advanced/testing-dependencies/

import pytest
from fastapi.testclient import TestClient

from src.main import app

# https://testdriven.io/blog/fastapi-crud/


@pytest.fixture(scope="module")
def client():
    c = TestClient(app)
    yield c
