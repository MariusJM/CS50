from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("save", views.save, name="save"),
    path("random_page", views.random_page, name="random_page")
]
