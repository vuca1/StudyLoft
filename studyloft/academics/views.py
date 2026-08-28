from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import IntegrityError

from .models import User


class NewNoteForm(forms.Form):
    content = forms.CharField(
        label="Content",
        required=True,
        max_length=1000,
        widget=forms.Textarea(attrs={
            "rows": 5
        })
    )


class NewTaskForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        max_length=50
        )
    description = forms.CharField(
        label="Description",
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 5
        })
    )
    deadline = forms.DateTimeField(
        label="Deadline",
        required=False
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        empty_label="-Select Assignee-"
    )


    class NewProjectForm(forms.Form):
        title = forms.CharField(
            label="Title",
            required=True,
            max_length=50
        )
        description = forms.CharField(
            label="Description",
            required=False,
            max_length=500,
            widget=forms.Textarea(attrs={
                "rows": 5
            })
        )
        members = forms.ModelChoiceField(
            queryset=User.objects.all(),
            #queryset=User.objects.exclude(id=user.id) # for all users except current user
            required=True,
            empty_label="-Select Members-"
        )


    # TODO: forms for Project and Thesis


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