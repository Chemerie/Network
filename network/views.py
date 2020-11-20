from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.core import serializers
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import forms
from django.core.paginator import Paginator

class NewPOstForm(forms.Form):
    newpost = forms.CharField(widget=forms.Textarea(attrs={'rows':4, 'cols':60}))

def index(request):
    posts = Post.objects.all().order_by('-date')


    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "form": NewPOstForm(),
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
            return HttpResponseRedirect(reverse("allpost"))
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
        return HttpResponseRedirect(reverse("allpost"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def newpost(request):
    if request.method == "POST":
        form = NewPOstForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["newpost"]
            name = request.user.username
       

            f = Post(poster=name, content=content)
            f.save()
            return HttpResponseRedirect(reverse("allpost"))

def allpost(request):
    posts = Post.objects.all().order_by('-date')


    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    likes = Like.objects.all()
    return render(request, "network/allpost.html", {
        "page_obj": page_obj,
        "form": NewPOstForm(),
        "likes": likes,
        })

@login_required
def profile(request, post_id):
    post = Post.objects.get(id=post_id)

    name = post.poster
    posts = Post.objects.filter(poster=name).order_by('-date')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    profile = User.objects.get(username=name)
    return render(request, "network/profile.html", {
        "profile": profile,
        "page_obj": page_obj,
        })

@csrf_exempt
@login_required    
def follow(request):
    follows = Follow.objects.all()
    return JsonResponse([follow.serialize() for follow in follows], safe=False)

@csrf_exempt
@login_required
def unfollow(request, follow_id):
    item = Follow.objects.get(pk=follow_id)
    item.delete()

    follows = Follow.objects.all()
    return JsonResponse([follow.serialize() for follow in follows], safe=False)


@csrf_exempt
@login_required
def addfollow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    following = data.get("following")
    followed = data.get("followed")
    f = Follow(following=following, followed=followed)
    f.save()

    follows = Follow.objects.all()
    return JsonResponse([follow.serialize() for follow in follows], safe=False)

@login_required
def followers(request):
    user = request.user.username
    followers = Follow.objects.filter(followed=user)
    print(followers)

    followers_posts = []

    for follower in followers:
        folls = Post.objects.filter(poster=follower.following)
        for foll in folls:
            followers_posts.append(foll)

    paginator = Paginator(followers_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/followers.html", {
        "page_obj": page_obj,
        })

@csrf_exempt
@login_required
def getpost(request):
    posts = Post.objects.all()

    if request.method == "GET":
        return JsonResponse([post.serialize() for post in posts], safe=False)

        
@csrf_exempt
@login_required
def post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
        
@csrf_exempt
@login_required
def addlike(request, postid):
    post = Post.objects.get(pk=postid)
    user = request.user.username
    f = Like(liker=user, post_id =postid)
    f.save()

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)


        
@csrf_exempt
@login_required
def deletelike(request, postid):
    post = Post.objects.get(pk=postid)
    user = request.user.username
    f = Like.objects.filter(liker=user, post_id =postid)
    f.delete()

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("likes") is not None:
            post.likes = data["likes"]
        post.save()
        return HttpResponse(status=204)


@csrf_exempt
@login_required
def like(request):
   
    likes = Like.objects.all()
    return JsonResponse([like.serialize() for like in likes], safe=False)



