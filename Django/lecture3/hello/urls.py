from django.urls import path
from . import views #imports from the same directory

urlpatterns =[
    path("", views.index, name="index"),
    path("marius", views.marius, name="marius")
]