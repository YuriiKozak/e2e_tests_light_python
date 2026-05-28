from src.web.Application import Application


def test_project_search(login, app: Application):
    target_project = "Popopo"

    (app.projects_page
     .is_loaded()
     .search_project(target_project)
     .result_project(target_project))
