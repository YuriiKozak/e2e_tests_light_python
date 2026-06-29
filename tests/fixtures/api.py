import re
from pathlib import Path
from typing import Any, Generator, cast

import allure
import pytest
import requests
from playwright.sync_api import Page

from src.api.client import ApiClient
from src.api.controllers.project_controller import ProjectController
from src.api.controllers.suite_controller import SuiteController
from src.api.controllers.test_controller import TestController
from src.api.models.project import Project
from src.web.application import Application
from tests.fixtures.configs import Configs

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
TRACES_DIR = Path("test-result/traces")


@pytest.fixture(scope="session")
def auth_token(configs: Configs) -> str:
    """Single authentication token shared across all controllers."""
    response = requests.post(
        url=f"{configs.url}/api/login",
        json={"api_token": configs.token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_controller(configs: Configs, auth_token: str) -> ProjectController:
    controller = ProjectController(
        base_url=configs.url,
        api_token=configs.token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="session")
def suite_controller(configs: Configs, auth_token: str) -> SuiteController:
    controller = SuiteController(
        base_url=configs.url,
        api_token=configs.token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="session")
def test_controller(configs: Configs, auth_token: str) -> TestController:
    controller = TestController(
        base_url=configs.url,
        api_token=configs.token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="function")
def project(project_controller: ProjectController) -> Project:
    """Get the first available project as a precondition."""
    projects = project_controller.get_all()
    return projects[0]


@pytest.fixture(scope="function")
def api_client(configs: Configs) -> ApiClient:
    """Provides an ApiClient instance."""
    return ApiClient(configs.url)


@pytest.fixture(scope="function")
def api_login(
    configs: Configs, api_client: ApiClient, app: Application, request
) -> Generator[None, None, None]:
    """
    Fixture to perform user login via API.
    Saves authentication state upon successful login or bypasses if already logged in.
    Also records a Playwright trace saved to test-result/traces/{test_name}_trace.zip.
    """
    # Start tracing
    app.page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    try:
        if STORAGE_STATE_PATH.exists():
            app.page.goto("/projects")
        else:
            # 1. Login via API to get the JWT token (as requested)
            jwt_token = api_client.login(configs.email, configs.password)

            # 2. Get the session cookies to authenticate browser navigation
            cookies = api_client.get_session_cookies(configs.email, configs.password)

            # 3. Add cookies to the browser context
            app.page.context.add_cookies(cast(Any, cookies))

            # 4. Navigate to /projects
            app.page.goto("/projects")

            # 5. Set the JWT token in localStorage as well (so client-side JS has it)
            app.page.evaluate(f"window.localStorage.setItem('jwt', '{jwt_token}');")

            # 6. Save authentication state to storage state path
            STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            app.page.context.storage_state(path=STORAGE_STATE_PATH)

        yield
    finally:
        # Stop tracing and save it ONLY if the test failed
        failed = False
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            failed = True
        elif hasattr(request.node, "rep_setup") and request.node.rep_setup.failed:
            failed = True

        if failed:
            clean_name = re.sub(r'[\\/*?:"<>|]', "_", request.node.name)
            trace_path = Path("test-result/traces") / f"{clean_name}_trace.zip"
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            app.page.context.tracing.stop(path=str(trace_path))
        else:
            app.page.context.tracing.stop()


def stop_tracing_on_failure(page: Page, request: pytest.FixtureRequest) -> None:
    """Stop tracing and save only if test failed. Attaches screenshot and trace to Allure."""
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        allure.attach(
            page.screenshot(),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=trace_path)

        allure.attach.file(
            str(trace_path),
            name="trace",
            extension="zip",
            attachment_type="application/vnd.allure.playwright-trace",
        )
    else:
        page.context.tracing.stop()
