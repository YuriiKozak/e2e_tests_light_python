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
    token: str


@pytest.fixture(scope="session")
def configs() -> Configs:
    """
    Loads and validates configuration from the .env file.
    Raises ValueError with descriptive instructions if any required variable is missing.
    """
    try:
        return Configs(
            url=os.environ["URL"],
            email=os.environ["EMAIL"],
            password=os.environ["PASSWORD"],
            token=os.environ["TOKEN"],
        )
    except KeyError as e:
        raise ValueError(
            f"Missing required environment variable in .env: {e.args[0]}. "
            f"Please verify your .env file configurations."
        )
