
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following/<str:val>", views.index, name="indexFol"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.load_profile, name="profile"),
    
    #API Routes
    path("follow", views.followUser, name='follow'),
    path("posts/get/follow/<int:num>", views.load_follow_posts, name='getFollowing'),
    path("posts/get/<str:name>/<int:page>", views.load_user_posts, name='getUserPost'),
    path("posts/page/<int:num>", views.load_posts, name='getAll'),
    path("posts", views.create, name='create')

]
