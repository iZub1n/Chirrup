
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("chirpPost", views.chirpPost, name="chirpPost"), 
    path("allPosts", views.allPosts, name="allPosts"),
    path("<int:userID>/userPage", views.userPage, name="userPage"),
    path("<int:userID>/follow", views.follow, name="follow"),
    path("<int:userID>/unfollow", views.unfollow, name="unfollow"),
     path("<int:userID>/following", views.following, name="following"),
    path("<int:userID>/followingList", views.followingList, name="followingList"),
    path("<int:userID>/followersList", views.followersList, name="followersList"),
    path("comments/<int:userID>/<int:postID>", views.commentsPage, name="commentsPage"),
    path("editPost", views.editPost, name="editPost"),
    path("react", views.react, name="react"),
]
