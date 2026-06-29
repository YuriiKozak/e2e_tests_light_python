import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Configures browser launch parameters."""
    return {
        **browser_type_launch_args,
        "channel": "chromium",
        "headless": True,
        "slow_mo": 300,
        "timeout": 30000,
    }
