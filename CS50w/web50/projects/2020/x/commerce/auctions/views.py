from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages

from .models import User, Category, Listing, Comments, Bid


def index(request):
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.filter(is_closed=False)
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
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.values_list('category_name', flat=True)
        })
    else:
        add_listing = Listing(
            seller = request.user,
            category = Category.objects.get(category_name=request.POST["category"]),
            title = request.POST["title"],
            image = request.POST["image"],
            starting_bid = float(request.POST["starting_bid"]),
            description = request.POST["description"],
            isActive = bool(request.POST.get("is_active", False))
        )
        add_listing.save()
        return HttpResponseRedirect(reverse(index))


def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": Category.objects.all()
    })


def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category_listings = Listing.objects.filter(category=category, is_closed=False)
    return render(request, "auctions/category.html", {
        "category_listings": category_listings
    })

def watchlist(request):
    current_user = request.user
    watchlist_items = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": watchlist_items
    })


def off_watchlist(request, item_id):
    listing_data = Listing.objects.get(pk=item_id)
    listing_data.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse("watchlist"))


def on_watchlist(request, item_id):
    listing_data = Listing.objects.get(pk=item_id)
    listing_data.watchlist.add(request.user)
    return HttpResponseRedirect(reverse("watchlist"))

def listing_item(request, item_id):
    referring_url = request.META.get('HTTP_REFERER', '/')
    listing_item = Listing.objects.get(pk=item_id)
    is_seller = request.user == listing_item.seller
    is_winner = listing_item.is_closed and request.user == listing_item.winner
    if request.user.is_authenticated:
        on_watchlist = request.user in listing_item.watchlist.all()
    else:
        on_watchlist = False
    highest_bid = Bid.objects.filter(listing=listing_item).order_by('-bid_amount').first()
    return render(request, "auctions/listing_item.html", {
        "listing_item": listing_item,
        "referring_url": referring_url,
        "on_watchlist": on_watchlist,
        "comments": Comments.objects.filter(listing=listing_item),
        "highest_bid": highest_bid,
        "is_seller": is_seller,
        "is_winner": is_winner
    })


def add_comment(request, id):
    add_comment = Comments(
        commenter = request.user,
        listing = Listing.objects.get(pk=id),
        comment = request.POST['add_comment']
    )
    add_comment.save()
    return HttpResponseRedirect(reverse("listing_item", args=(id, )))

def place_bid(request, item_id):
    if request.method == "POST":
        bid_amount = float(request.POST.get('bid_amount', 0))
        listing = Listing.objects.get(pk=item_id)
        if bid_amount > listing.starting_bid:
            bid = Bid.objects.create(listing=listing, bidder=request.user, bid_amount=bid_amount)
            listing.highest_bid = bid
            listing.save()
        
    return HttpResponseRedirect(reverse("listing_item", args=(item_id,)))

def close_auction(request, item_id):
    listing_item = Listing.objects.get(pk=item_id)
    
    if request.method == "POST" and request.user == listing_item.seller:
        if not listing_item.is_closed:
            listing_item.is_closed = True
            highest_bidder = Bid.objects.filter(listing=listing_item).order_by('-bid_amount').first()
            if highest_bidder:
                listing_item.winner = highest_bidder.bidder
                listing_item.save()
                messages.success(request, f'The auction for "{listing_item.title}" has been closed. The winner will be notified.')
            else:
                messages.warning(request, f'The auction for "{listing_item.title}" cannot be closed as there are no bids.')
        else:
            messages.warning(request, f'The auction for "{listing_item.title}" is already closed.')
    return HttpResponseRedirect(reverse("listing_item", args=(item_id,)))

def my_listings(request):
    current_user = request.user
    return render(request, "auctions/my_listings.html", {
        "listings":Listing.objects.filter(seller=current_user),
        "listings_won":Listing.objects.filter(winner=current_user),
    })
