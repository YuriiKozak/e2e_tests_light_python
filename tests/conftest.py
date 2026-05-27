import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Configs:
    url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Configs(
        url=os.environ["URL"],
        email=os.environ["EMAIL"],
        password=os.environ["PASSWORD"]
    )
