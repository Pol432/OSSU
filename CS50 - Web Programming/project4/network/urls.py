
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts", views.posts, name="posts"),
    path("post_view/<int:id>", views.post_view, name="post_view"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("change_post/<int:id>", views.change_post, name="change_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("profile_view/<int:id>", views.profile_view, name="profile_view"),
    path("following", views.following, name="following"), 
    path("follow", views.follow, name="follow")
]
