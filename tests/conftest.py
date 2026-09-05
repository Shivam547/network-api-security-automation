from pathlib import Path

import pytest
import yaml

from automation.clients.api_client import APIClient
from automation.utils.auth_utils import login


CONFIG_PATH = (
    Path(__file__).parent.parent
    / "automation"
    / "config"
    / "config.yaml"
)


with open(CONFIG_PATH, "r") as file:
    CONFIG = yaml.safe_load(file)


@pytest.fixture(scope="session")
def base_url():

    return CONFIG["base_url"]


@pytest.fixture(scope="session")
def timeout():

    return CONFIG["timeout"]


def create_authenticated_client(
    base_url,
    timeout,
    username,
    password
):

    token = login(
        base_url=base_url,
        username=username,
        password=password,
        timeout=timeout
    )

    return APIClient(
        base_url=base_url,
        token=token,
        timeout=timeout
    )


@pytest.fixture
def admin_client(base_url, timeout):

    credentials = CONFIG["users"]["admin"]

    return create_authenticated_client(
        base_url,
        timeout,
        credentials["username"],
        credentials["password"]
    )


@pytest.fixture
def manager_client(base_url, timeout):

    credentials = CONFIG["users"]["manager"]

    return create_authenticated_client(
        base_url,
        timeout,
        credentials["username"],
        credentials["password"]
    )


@pytest.fixture
def user_client(base_url, timeout):

    credentials = CONFIG["users"]["user"]

    return create_authenticated_client(
        base_url,
        timeout,
        credentials["username"],
        credentials["password"]
    )


@pytest.fixture
def readonly_client(base_url, timeout):

    credentials = CONFIG["users"]["readonly"]

    return create_authenticated_client(
        base_url,
        timeout,
        credentials["username"],
        credentials["password"]
    )


@pytest.fixture
def unauthenticated_client(base_url, timeout):

    return APIClient(
        base_url=base_url,
        timeout=timeout
    )