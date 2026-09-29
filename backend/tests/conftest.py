import os
import sys
from pathlib import Path

import pytest
import requests


BACKEND_DIR = Path('/app/backend')
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def _frontend_env_base_url() -> str | None:
    env_path = Path('/app/frontend/.env')
    if not env_path.exists():
        return None
    for line in env_path.read_text().splitlines():
        if line.startswith('REACT_APP_BACKEND_URL='):
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    return None


@pytest.fixture(scope='session')
def base_url() -> str:
    url = os.environ.get('REACT_APP_BACKEND_URL') or _frontend_env_base_url()
    if not url:
        pytest.skip('REACT_APP_BACKEND_URL is not configured')
    return url.rstrip('/')


@pytest.fixture(scope='session')
def api_url(base_url: str) -> str:
    return f'{base_url}/api'


@pytest.fixture
def api_client() -> requests.Session:
    session = requests.Session()
    session.headers.update({'Accept': 'application/json'})
    return session
