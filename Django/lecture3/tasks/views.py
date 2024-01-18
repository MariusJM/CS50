from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New task")
    #priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)

#tasks = ["foo", "bar", "baz"]
tasks = []
# Create your views here.
def index(request):
    return render(request, "tasks/index.html",{
        "tasks": tasks
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            tasks.append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html",{
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })