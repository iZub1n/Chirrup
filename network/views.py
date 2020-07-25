from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import datetime, date

from .models import User, Post, Follow, Comment, Reaction
import pytz

def index(request):
    return render(request, "network/index.html")


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

def chirpPost(request):
    if request.method == "POST":
        chirp = request.POST["chirp"]

        Post.objects.create(content=chirp, poster_id=request.user.id )
    return HttpResponseRedirect(reverse('allPosts'))

def allPosts(request):
    posts = Post.objects.all().order_by('-dTEdited') 
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "posts":  posts,
        "page_obj": page_obj
    }
    return render(request, "network/allPosts.html", context)

def userPage(request, userID):
    try:
        user = User.objects.get(pk=userID)
    except:
        raise Http404("User does not exist")

    followers = Follow.objects.filter(target_id=userID).count()

    following = Follow.objects.filter(user_id=userID).count()

    context = {
        "userSearched": user,
        "posts": user.posts.all().order_by('-dTEdited'),
        "followerCount":  followers,
        "followingCount": following,
        "following": Follow.objects.filter(user_id=request.user.id, target_id=userID).count() < 1
    }
    return render(request, "network/userPage.html", context)

def follow(request, userID):
    Follow.objects.create(user_id=request.user.id, target_id=userID)
    return HttpResponseRedirect(reverse('userPage', kwargs={'userID':userID}))

def unfollow(request, userID):
    Follow.objects.filter(user_id=request.user.id, target_id=userID).delete()
    return HttpResponseRedirect(reverse('userPage', kwargs={'userID':userID}))

class followType():
    def __init__(self, userID, type):
        self.userID = userID
        self.type = type

    def factoryDecider(self):
        if self.type == "following":
            return (Follow.objects.filter(user_id=self.userID))
        elif self.type == "follower":
            return (Follow.objects.filter(target_id=self.userID))
        return None


def followingList(request, userID):
    uIDList =  followType(userID,"following").factoryDecider()
    usersList = []
    for u in uIDList:
        result = User.objects.get(pk=u.target_id)
        usersList.append(result)
    context = {
        "users":  usersList,
        "requestType": "Following:"
    }
    return render(request, "network/analytics.html", context)

def followersList(request, userID):
    uIDList =  followType(userID,"follower").factoryDecider()
    usersList = []
    for u in uIDList:
        result = User.objects.get(pk=u.user_id)
        usersList.append(result)
    context = {
        "users":  usersList,
        "requestType": "Followers:"
    }
    return render(request, "network/analytics.html", context)

def following(request, userID):
    follows = Follow.objects.filter(user_id=request.user.id)
    followsList = []
    for f in follows:
        followsList.append(f.target_id)
    posts = Post.objects.filter(poster_id__in=followsList).order_by('-dTEdited')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "posts":  posts,
        "page_obj": page_obj
    }
    return render(request, "network/following.html", context)

def commentsPage(request, userID, postID):
    try:
       user = User.objects.get(pk=userID)
       post = Post.objects.get(pk=postID)
       comments = Comment.objects.filter(post_id=postID).order_by('-dTCreated')
    except:
       raise Http404("ERROR 404")
    context = {
        "post": post,
        "comments": comments,
    }
    return render(request, "network/comments.html", context)

def editPost(request):
    if request.method == 'POST':
        content=request.POST['content']
        postID=(request.POST['postID'])[2:]
        p = Post.objects.get(pk=postID)

        if content==p.content:
            return HttpResponse(status=304)
        p.content= content
        p.Edited = True
        p.dTEdited = datetime.now(pytz.utc)
        p.save()
        #print(p.dTEdited)

    return HttpResponse(status=201)

def react(request):
    reaction=request.POST['reaction']
    reaction = int(reaction)
    postID=(request.POST['postID'])[2:]
    reactionsObj = Reaction.objects.filter(post_id=postID)
    
    userID = request.user.id

    if reactionsObj is None or reactionsObj.count()<1:
         reactionsObj = None
    else:
        try:
            reactionsObj = reactionsObj.get(user_id=userID)
        except:
            reactionsObj = None

    reactBehaviour(reaction, reactionsObj, postID, userID)

    postObj = Post.objects.get(pk=postID)
    
    response = {}
    response['likes'] = postObj.likes
    response['dislikes'] = postObj.dislikes

    return JsonResponse(response)

def reactBehaviour(reaction, reactionsObj, postID, userID):
    postObj = Post.objects.get(pk=postID)
    
    if reactionsObj is None:
        Reaction.objects.create(post_id=postID, user_id=userID, type=reaction)
        if reaction==1:
            postObj.likes = postObj.likes+1
        elif reaction==2:
            postObj.dislikes = postObj.dislikes-1
        postObj.save()
        return

    elif reaction == 1:
        if reactionsObj.type==1:
            reactionsObj.delete()
            postObj.likes = postObj.likes - 1
            postObj.save()
            return
        elif reactionsObj.type==2:
            reactionsObj.type = 1
            postObj.likes = postObj.likes+1
            postObj.dislikes = postObj.dislikes+1
            postObj.save()
            reactionsObj.save()
            return
    elif reaction == 2:
        if reactionsObj.type==2:
            reactionsObj.delete()
            postObj.dislikes = postObj.dislikes +1
            postObj.save()
            return
        elif reactionsObj.type==1:
            reactionsObj.type = 2
            postObj.likes = postObj.likes-1
            postObj.dislikes = postObj.dislikes-1
            postObj.save()
            reactionsObj.save()
            return
        return

    



