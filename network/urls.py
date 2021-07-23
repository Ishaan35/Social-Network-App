
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewProfile/<int:id>", views.viewProfile, name="viewProfile"),
    path("likePost/<int:id>", views.likePost, name="likePost"),
    path("viewProfile/likePost/<int:id>",
         views.likePost, name="likePostProfile"),
    path("viewProfile/follow/<int:id>",
         views.followUser, name="followUser"),
    path("following", views.postsByFollowingPeople, name="postsByFollowingPeople"),

    path("editPost/<int:id>", views.edit, name="editPost"),
    path("viewProfile/editPost/<int:id>", views.edit, name="editPostProfile"),





]
