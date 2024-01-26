from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method=="GET":
        return render(request, "auctions/create_listing.html",{
            "categories": Category.objects.values_list('category_name', flat=True)
        })
    else:
        # request.method== "POST":
        user = request.user
        category = request.POST["category"]
        category_d = Category.objects.get(category_name=category)
        title = request.POST["title"]
        image = request.POST["image"]
        starting_bid = request.POST["starting_bid"]
        description = request.POST["description"]
        is_active = request.POST["is_active"]
        add_listing = Listing(
            seller = user,
            category = category_d,
            title = title,
            image = image,
            starting_bid = int(starting_bid),
            description = description,
            isActive = bool(is_active)
        )
        add_listing.save()
        return HttpResponseRedirect(reverse(index))
    

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": Category.objects.all()
    })
