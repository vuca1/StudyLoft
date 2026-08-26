from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

# Create your views here.
def index(request):
    pass


def register(request):
    pass


def login(request):
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


def logout():
    pass