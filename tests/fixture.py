import pytest
from utils.docker import start_database_container


@pytest.fixture(scope="session", autouse=True)
def db_session():
    container = start_database_container()
