import json
from logging import PlaceHolder
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Post, User

class NewPostForm(forms.Form):
    tweet = forms.CharField(label='',widget=forms.Textarea(
        attrs={'placeholder': 'Whats going on?', 'id':'post-content'}))

def index(request, val = ''):
    main = True
    if(val != ''):
        print(val)
        main = False

    return render(request, "network/index.html", {
        'form': NewPostForm(),
        'main': main
    })

@csrf_exempt
def create(request):
    # Post must be via POST
    if(request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)

    #Load data
    data = json.loads(request.body)
    content = data.get('content', '')
    
    #CreatePost
    post = Post(
        user = request.user,
        username = request.user.username,
        content = content,
    )
    post.save()

    return JsonResponse({'message': 'Post Created successfully'}, status = 201)

def load_posts(request, num):
    objects = list(Post.objects.order_by('-id').all().values()) 
    pages = Paginator(objects, 10)
    posts = pages.page(num)
    post_info = {'data': posts.object_list,
                'num_pages': pages.num_pages
    }
    print(pages.count)
    return JsonResponse(post_info, safe = False, status = 200)

def load_user_posts(request, name, page): 
    objects = list(Post.objects.order_by('-id').filter(username = name).values())
    pages = Paginator(objects, 3)
    posts = pages.page(page)
    post_info = {'data': posts.object_list,
                'num_pages': pages.num_pages
    }
    print(pages.count)
    return JsonResponse(post_info, safe = False, status = 200)

def load_follow_posts(request, num):
    user = request.user
    following = [User for User in user.following.all()]
    objects = list(Post.objects.order_by('-id').filter(user__in = following).values())
    pages = Paginator(objects, 10)
    posts = pages.page(num)
    post_info = {'data': posts.object_list,
                'num_pages': pages.num_pages
    }
    return JsonResponse(post_info, safe = False, status = 200)

def load_profile(request, name):
    user = User.objects.get(username = str(name))
    viewer = request.user
    return render(request, 'network/profile.html', {
        'puser': user.username,
        'following': 0,
        'followers': user.following.count,
        'is_followed': viewer.following.filter(username = str(name)).exists()
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

@csrf_exempt
def followUser(request):
    if(request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)
    
    user = request.user
    data = json.loads(request.body)
    follow = data.get('follow', '')

    #Follow
    if(user.following.filter(username = follow).exists()):
        user.following.remove(User.objects.get(username = follow))
    else:
        user.following.add(User.objects.get(username = follow))
    return JsonResponse({'message': 'All done'}, status = 201)

@csrf_exempt
def LikePost(request, content):
    if(request.method != 'POST'):
        return JsonResponse({"error": "POST request required."}, status=400)
    
    post = Post.objects.get(content = content)
    data = json.loads(request.body)
    follow = data.get('like', '')

    #Follow
    if(post.likes.filter(username = request.user.username).exists()):
        post.likes.remove(User.objects.get(username = request.user.username))
    else:
        post.likes.add(User.objects.get(username = ))
    return JsonResponse({'message': 'All done'}, status = 201)


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
