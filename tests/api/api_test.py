import pytest
from faker import Faker

from src.api.controllers.suite_controller import SuiteController
from src.api.controllers.test_controller import TestController
from src.api.models.project import Project

fake = Faker()


# @pytest.mark.api
@pytest.mark.smoke
def test_create_suite(
    project: Project,
    suite_controller: SuiteController,
    test_controller: TestController,
):
    # Create suite
    suite_name = fake.sentence()
    suite_response = suite_controller.create(
        project_id=project.id, title=suite_name, description=fake.paragraph()
    )

    actual_test_suite = suite_controller.get_by_id(
        project_id=project.id, suite_id=suite_response.id
    )

    assert suite_response.id == actual_test_suite.id
    assert suite_response.attributes.title == actual_test_suite.attributes.title
    assert actual_test_suite.attributes.title == suite_name
