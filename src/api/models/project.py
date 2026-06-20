from pydantic import BaseModel, ConfigDict


class ProjectAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class Project(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: Project
