from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:form>", views.authentication, name="authentication"),
    path("homepage", views.homepage, name="homepage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("test_view", views.test_view, name="test_view"),
    path("test", views.test, name="test"),
    path("projects_view", views.projects_view, name="projects_view"),
    path("images/<str:url>", views.image_view, name="images"),
    path("project/<int:id>", views.project, name="project"),
    path("project_view/<int:id>", views.project_view, name="project_view"),
    path("update_likes/<int:id>", views.update_likes, name="update_likes"),
    path("add_project/<int:id>", views.add_project, name="add_project"),
    path("user", views.user, name="user"),
    path("user_view", views.user_view, name="user_view"),
    path("create_project", views.create_project, name="create_project"),
    path("edit_project/<int:id>", views.edit_project, name="edit_project")
]