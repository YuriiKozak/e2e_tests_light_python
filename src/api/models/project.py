from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ProjectAttributes(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str | None = None


class Project(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str
    type: str | None = None
    attributes: ProjectAttributes | None = None
    relationships: dict[str, Any] | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: list[Project]

    def __getitem__(self, item: int) -> Project:
        return self.data[item]
