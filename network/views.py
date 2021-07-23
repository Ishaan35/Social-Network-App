from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required


from .models import Follower, Post, User, Like


def index(request):
    if request.method == "POST":
        user = request.user
        print("New Post:")
        post = request.POST["bodyText"]
        p = Post()
        p.user = user
        p.body = post
        p.date = timezone.now()
        print(p)
        p.save()

    allPosts = Post.objects.all().order_by('-date')

    for post in allPosts:
        post.numLikes = Like.objects.filter(post=post).count()
        post.save()

    LikesArr = Like.objects.all()
    likedByThisUser = []

    for p in allPosts:
        liked = False
        for l in LikesArr:
            if l.user == request.user and l.post == p:
                liked = True
                break
        likedByThisUser.append({
            "liked": liked,
            "post": p
        })

    paginator = Paginator(allPosts, 10)
    page = paginator.get_page(request.GET.get('page'))

    signedIn = request.user.is_authenticated

    return render(request, "network/index.html", {
        "page": page,
        "signedIn": signedIn,
        "homePage": True,
        "profile": False,
        "LikesArr": LikesArr,
        "user": request.user,
        "likedByThisUser": likedByThisUser
    })


def postsByFollowingPeople(request):

    peopleFollowing = Follower.objects.filter(
        user=request.user).values('following_id')
    print(peopleFollowing)

    allPosts = Post.objects.filter(user__in=peopleFollowing).order_by('-date')

    for post in allPosts:
        post.numLikes = Like.objects.filter(post=post).count()
        post.save()

    LikesArr = Like.objects.all()
    likedByThisUser = []

    for p in allPosts:
        liked = False
        for l in LikesArr:
            if l.user == request.user and l.post == p:
                liked = True
                break
        likedByThisUser.append({
            "liked": liked,
            "post": p
        })

    paginator = Paginator(allPosts, 10)
    page = paginator.get_page(request.GET.get('page'))

    signedIn = request.user.is_authenticated

    return render(request, "network/index.html", {
        "page": page,
        "signedIn": signedIn,
        "homePage": False,
        "followingPosts": True,
        "profile": False,
        "LikesArr": LikesArr,
        "user": request.user,
        "likedByThisUser": likedByThisUser
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


def viewProfile(request, id):
    user = User.objects.get(id=id)
    print(f'Profile: {user}')

    postsByUser = Post.objects.filter(user=user).order_by('-date')

    for p in postsByUser:
        p.numLikes = Like.objects.filter(post=p).count()
        p.save()

    paginator = Paginator(postsByUser, 10)
    page = paginator.get_page(request.GET.get('page'))

    # post likes
    LikesArr = Like.objects.all()

    likedByThisUser = []

    if request.user.is_authenticated:
        for p in postsByUser:
            liked = False
            for l in LikesArr:
                if l.user == request.user and l.post == p:
                    liked = True
                    break
            likedByThisUser.append({
                "liked": liked,
                "post": p
            })

    signedIn = request.user.is_authenticated

    print(request.user)
    # followers
    followerCount = Follower.objects.filter(following=user).count()
    followingCount = Follower.objects.filter(user=user).count()

    # are we following this user already
    areFollowing = False
    if signedIn:
        areFollowing = True if Follower.objects.filter(
            user=request.user, following=user).count() > 0 else False

    return render(request, "network/index.html", {
        "page": page,
        "signedIn": signedIn,
        "homePage": False,  # viewing profile, not all posts
        "profile": True,
        "signedInUser": request.user,
        "user": user,
        "likedByThisUser": likedByThisUser,
        "followerCount": followerCount,
        "followingCount": followingCount,
        "areFollowing": areFollowing
    })


def likePost(request, id):

    if request.method == "PUT":
        data = json.loads(request.body)
        if data["like"]:
            like = Like()
            like.user = request.user
            post = Post.objects.get(id=id)
            like.post = post
            like.save()
        else:
            post = Post.objects.get(id=id)
            Like.objects.filter(post=post, user=request.user).delete()
        return HttpResponse()

    else:
        post = Post.objects.get(id=id)

        return JsonResponse({
            'Likes': Like.objects.filter(post=post).count()
        })


def followUser(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data["following"]:
            follower = Follower()
            follower.user = request.user
            follower.following = User.objects.get(id=id)
            follower.save()
        else:
            Follower.objects.filter(
                user=request.user, following=User.objects.get(id=id)).delete()

    else:
        return JsonResponse({
            'followers': Follower.objects.filter(following=User.objects.get(id=id)).count()
        })

    return HttpResponse()


def edit(request, id):

    if request.method == "PUT":
        data = json.loads(request.body)
        body = data["newBody"]

        post = Post.objects.get(id=id)
        post.body = body
        post.save()
    else:
        return JsonResponse({
            'body': Post.objects.get(id=id).body
        })

    return HttpResponse()
