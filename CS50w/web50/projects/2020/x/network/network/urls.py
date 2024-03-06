
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_tweet", views.new_tweet, name="new_tweet"),
    path("profile/<int:user_id>", views.user_profile, name="user_profile"),
]
