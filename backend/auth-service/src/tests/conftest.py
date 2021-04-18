import pytest
import mongomock
from pymongo_inmemory import MongoClient


@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch):

    monkeypatch.setenv(
        'JWT_SECRET_KEY', 'adfasdfasdfasdf')
    monkeypatch.setenv(
        'PYMONGOIM__MONGOD_PORT', '27020')
    monkeypatch.setenv(
        'DB_URL', 'mongodb://localhost:27020/?retryWrites=true&w=majority')
    client = MongoClient()
