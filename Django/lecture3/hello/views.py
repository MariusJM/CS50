from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("Hello world!")

def marius(request):
    return HttpResponse("Hello, Marius!")

def david(request):
    return HttpResponse("Hello, David!")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")