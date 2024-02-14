from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, PostContent, Follow
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def index(request):
    posts = PostContent.objects.all().order_by('-created_at')
    return render(request, "network/index.html",{
        "posts": posts
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

def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('newpost', '') 
        if content:
            post = PostContent(
                content=content, 
                author=request.user
                )
            post.save()
            return HttpResponseRedirect(reverse('index'))

    return render(request, 'network/index.html', {'message': 'Failed to create post.'})

def profile(request, author):
    user_profile = User.objects.get(username=author)
    posts = PostContent.objects.filter(author=user_profile).order_by('-created_at')
    is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()
    post_likes = {post.id: post.likes.count() for post in posts}
    return render(request, "network/profile.html",{
        "user": request.user,
        "author": author,
        "followers": user_profile.followers.count(),
        "following": user_profile.following.count(),
        "posts": posts,
        "is_following": is_following,
        "post_likes": post_likes,
    })


def follow(request, author):
    author = User.objects.get(username=author)
    
    if request.method == "POST":
        if not Follow.objects.filter(follower=request.user, following=author).exists():
            Follow.objects.create(follower=request.user, following=author)
            followed = True
        else:
            Follow.objects.filter(follower=request.user, following=author).delete()
            followed = False

        return JsonResponse({"followed": followed, "follower_count": author.followers.count()})
    else:
        return JsonResponse({"error": "Invalid request method"})