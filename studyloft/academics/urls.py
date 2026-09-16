from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login_view", views.login_view, name="login_view"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("register_view", views.register_view, name="register_view"),
    path("add_project", views.add_project, name="add_project"),
    path("projects_list", views.projects_list, name="projects_list"),
    path("project/<int:project_id>", views.project, name="project"),
    path("remove_project/<int:project_id>", views.remove_project, name="remove_project"),
    path("add_task", views.add_task, name="add_task"),
    path("tasks_list", views.tasks_list, name="tasks_list"),
    path("task/<int:task_id>", views.task, name="task"),
    path("remove_task/<int:task_id>", views.remove_task, name="remove_task"),
    path("add_note/<int:job_id>", views.add_note, name="add_note"),
    path("remove_note/<int:note_id>", views.remove_note, name="remove_note"),
    path("theses_list", views.theses_list, name="theses_list"),
    path("add_thesis", views.add_thesis, name="add_thesis"),
    path("thesis/<int:thesis_id>", views.thesis, name="thesis"),
    path("remove_thesis/<int:thesis_id>", views.remove_thesis, name="remove_thesis")
]