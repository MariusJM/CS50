from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(isActive=True)
    })


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
        add_listing = Listing(
            seller = request.user,
            category = Category.objects.get(category_name=request.POST["category"]),
            title = request.POST["title"],
            image = request.POST["image"],
            starting_bid = int(request.POST["starting_bid"]),
            description = request.POST["description"],
            isActive = bool(request.POST.get("is_active", False))
        )
        add_listing.save()
        return HttpResponseRedirect(reverse(index))
    

def watchlist(request):
    return render(request, "auctions/watchlist.html")

def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": Category.objects.all()
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category_listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category_listings": category_listings
    })

def listing_item(request, item_id):
    referring_url = request.META.get('HTTP_REFERER', '/')
    listing_data = Listing.objects.get(pk=item_id)
    if request.user in listing_data.watchlist.all():
        on_watchlist = True
    else:
        on_watchlist = False
    return render(request, "auctions/listing_item.html",{
        "listing_item": Listing.objects.get(pk=item_id),
        "referring_url": referring_url,
        "on_watchlist": on_watchlist
    })

def off_watchlist(request, item_id):
    listing_data = Listing.objects.get(pk=item_id)
    listing_data.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing_item", args=(item_id, )))

def on_watchlist(request, item_id):
    listing_data = Listing.objects.get(pk=item_id)
    listing_data.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("listing_item", args=(item_id, )))