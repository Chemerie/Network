
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("allpost", views.allpost, name="allpost"),
    path("<int:post_id>profile", views.profile, name="profile"),
	path("followers", views.followers, name= "followers"),


    path("follow", views.follow, name="follow"),
    path("unfollow/<int:follow_id>", views.unfollow, name="unfollow"),
    path("addfollow", views.addfollow, name="addfollow"),
    path("getpost", views.getpost, name="getpost"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like", views.like, name= "like"),
    path("deletelike/<int:like_id>", views.deletelike, name="deletelike"),
    path("addlike/<int:postid>", views.addlike, name="addlike"),
]
