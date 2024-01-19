from django.urls import path
from . import views #imports from the same directory

urlpatterns =[
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("marius", views.marius, name="marius"),
    path("david", views.david, name="david")
]