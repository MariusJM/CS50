from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import User, Posts


def index(request):
    posts = Posts.objects.all().order_by("-date_created");
    return render(request, "network/index.html",{
        "posts": posts
    })


def like_post(request, post_id):
    user = request.user
    post = Posts.objects.get(pk=post_id)

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return JsonResponse({"likes": post.likes.count()}, status=200)


def posts(request, post_filter):
    user = request.user
    if post_filter == "all":
        posts = Posts.objects.all().order_by("-date_created")
    elif post_filter == "following":
        following_users = user.followers.all()
        posts = Posts.objects.filter(author__in=following_users).order_by("-date_created")
    elif post_filter != "":
        posts = Posts.objects.filter(author__username=post_filter).order_by("-date_created")
    else:
        return JsonResponse({"error": "post_filter in get_posts doesn't exist."}, status=400)

    return JsonResponse([post.serialize() for post in posts], safe=False)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
