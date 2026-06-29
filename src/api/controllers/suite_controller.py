from src.api.controllers.base_controller import BaseController
from src.api.models.suite import Suite


class SuiteController(BaseController):
    def create(
        self,
        project_id: str,
        title: str,
        description: str | None = None,
    ) -> Suite:
        attributes = {"title": title, "description": description}
        data = self._post(
            endpoint=f"/api/{project_id}/suites",
            data={"data": {"type": "suites", "attributes": attributes}},
        )
        return Suite.model_validate(data["data"])

    def get_by_id(self, project_id: str, suite_id: str) -> Suite:
        data = self._get(f"/api/{project_id}/suites/{suite_id}")
        return Suite.model_validate(data["data"])

    def update(
        self,
        project_id: str,
        suite_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> Suite:
        attributes = {"title": title, "description": description}
        data = self._put(
            endpoint=f"/api/{project_id}/suites/{suite_id}",
            data={"data": {"type": "suites", "attributes": attributes}},
        )
        return Suite.model_validate(data["data"])

    def delete(self, project_id: str, suite_id: str) -> None:
        self._delete(f"/api/{project_id}/suites/{suite_id}")
