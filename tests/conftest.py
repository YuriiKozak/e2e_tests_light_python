import pytest

pytest_plugins = [
    "tests.fixtures.api",
    "tests.fixtures.app",
    "tests.fixtures.configs",
    "tests.fixtures.playwright",
    "tests.fixtures.selenium",
]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """Exposes test outcome (success/failure) to fixtures via item.rep_call, item.rep_setup, etc."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
