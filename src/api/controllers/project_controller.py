from src.api.controllers.base_controller import BaseController
from src.api.models import Project, ProjectResponse


class ProjectController(BaseController):
    def get_all(self) -> ProjectResponse:
        data = self._get("/api/projects")
        return ProjectResponse.model_validate(data)

    def get_by_id(self, project_id: str) -> Project:
        data = self._get(f"/api/project/{project_id}")
        return Project.model_validate(data["data"])
