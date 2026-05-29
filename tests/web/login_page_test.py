import pytest
from faker import Faker

from src.web.application import Application
from tests.fixtures.config import Configs

fake = Faker()


@pytest.mark.smoke
@pytest.mark.regression
def test_login(configs: Configs, clean_app: Application):
    (clean_app.home_page.open().is_loaded().click_login())

    (clean_app.login_page.is_loaded().login(configs.email, configs.password))

    (clean_app.projects_page.is_loaded())


INVALID_LOGIN_TEST_DATA = [
    # Email Equivalence Classes
    pytest.param(fake.email(), fake.password(length=10), id="unregistered_valid_email"),
    pytest.param(
        fake.user_name(), fake.password(length=10), id="email_missing_at_symbol"
    ),
    pytest.param("invalid@", fake.password(length=10), id="email_missing_domain"),
    pytest.param(
        "@domain.com", fake.password(length=10), id="email_missing_local_part"
    ),
    pytest.param("user@@domain.com", fake.password(length=10), id="email_double_at"),
    pytest.param(
        "user name@domain.com", fake.password(length=10), id="email_with_spaces"
    ),
    # Password Equivalence Classes
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param(fake.email(), "   ", id="password_only_spaces"),
    pytest.param(fake.email(), "a", id="password_1_char"),
    pytest.param(fake.email(), "a" * 256, id="password_2_256_chars"),
    # Boundary Value Analysis - Empty inputs
    pytest.param("", "", id="both_empty"),
    pytest.param("", fake.password(length=10), id="empty_email"),
    # Boundary Value Analysis - Min/Max lengths
    pytest.param("a@b.c", fake.password(length=10), id="min_valid_email_format"),
    pytest.param(
        f"{'a' * 64}@{'b' * 63}.com", fake.password(length=10), id="max_length_email"
    ),
    # Special Characters
    pytest.param(fake.email(), "pass<script>alert(1)</script>", id="xss_in_password"),
    pytest.param(
        fake.email(), "pass'; DROP TABLE users;--", id="sql_injection_password"
    ),
]


@pytest.mark.regression
@pytest.mark.parametrize("email, password", INVALID_LOGIN_TEST_DATA)
def test_login_invalid(
    email: str, password: str, configs: Configs, session_app: Application
):
    (
        session_app.login_page.open()
        .is_loaded()
        .login(email, password)
        .invalid_login_message_visible()
    )
