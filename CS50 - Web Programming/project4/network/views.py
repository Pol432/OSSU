from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from .models import User, Post

import time, json

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = { "content": "" }


@login_required
def following(request):
    return render(request, "network/following.html", {
        "posts": request.user.following.values("post")
    })


def profile(request, id):
    user = User.objects.get(id=id)
    
    return render(request, "network/profile.html", {
        "posts": Post.objects.filter(author=id).order_by("date"),
        "profile_user": user,
        "followers": User.objects.filter(following__in=[user]).annotate(count=Count("following"))["count"]
    })

def profile_view(request, id):
    posts = list(Post.objects.filter(author=id).values())
    profile_user = User.objects.get(id=id)
    following = profile_user in request.user.following.all()

    return JsonResponse({
        "posts": posts,
        "profile_user": model_to_dict(profile_user),
        "user": request.user.id,
        "following": following
    })


@login_required
def follow(request):
    user_id = int(request.GET.get("following") or 0)
    action = str(request.GET.get("action") or "")
    
    user = User.objects.get(id=user_id)
    if "Follow" in action and user not in request.user.following.all():
        request.user.following.add(user)
    elif "Unfollow" in action and user in request.user.following.all():
        request.user.following.remove(user)
    

def posts(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or start + 9)
    
    posts = list(Post.objects.order_by("date")[start:end].values())
    time.sleep(1)
    
    return JsonResponse({
        "posts": posts
    })

def post_view(request, id):
    post = Post.objects.get(id=id)
    author = User.objects.get(id=post.author_id)
    post_data = model_to_dict(post)
    post_data["date"] = post.date.isoformat()
    user = ""
    
    if request.user.is_authenticated: user = model_to_dict(request.user)
    

    data = {
        "post": post_data,
        "author": model_to_dict(author),
        "user": user
    }
    return JsonResponse(data)


@login_required
def edit_post(request):
    if request.method == "POST":
        form_data = json.loads(request.body)
        form = PostForm(form_data)
        return render(request, "network/edit_post.html", {
            "form": form,
            "id": form_data["id"]
        })
    return redirect("index")

@login_required
def change_post(request, id):
    if request.method == "POST":
        form = PostForm(request.POST)
        
        if form.is_valid():
            current_post = Post.objects.get(id=id)
            new_post = PostForm(request.POST, instance=current_post)
            new_post.save()
    return redirect("index")
    

def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
        else:
            return render(request, "network/index.html", {
                "form": PostForm(form),
                "message": "Invalid post format!"
            })

    return render(request, "network/index.html", {
        "form": PostForm()
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
