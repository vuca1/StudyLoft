from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import IntegrityError

from .models import User

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "academics/index.html")
    else:
        return render(request, "academics/login.html", {
            "message": "You need to login first."
        })


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "academics/register.html", {
                "message": "Passwords must match."
            })

        # try to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "academics/register.html",{
                "message": "Username or email already taken."
            })

        login(request, user)
        return render(request, "academics/index.html", {
            "message": "Successfully registered."
        })
    else:
        return render(request, "academics/register.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authenticate successful
        if user is not None:
            login(request, user)
            return render(request, "academics/index.html", {
                "message": "Login successful."
            })
        else:
            return render(request, "academics/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "academics/login.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")