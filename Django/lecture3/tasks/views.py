from django.shortcuts import render

tasks = ["foo", "bar", "baz"]
# Create your views here.
def index(requests):
    return render(requests, "tasks/index.html",{
        "tasks": tasks
    })