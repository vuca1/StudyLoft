from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import IntegrityError

from .models import User, Subject, Grade, Teacher, Thesis, Project, Task, Note


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
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
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
    members = forms.ModelMultipleChoiceField(
        label="Members",
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )


class NewThesisForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        max_length=150
    )
    description = forms.CharField(
        label="Description",
        required=False,
        max_length=500
    )
    sepervisor = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        empty_label="-Select Supervisor-"
    )


def index(request):
    if request.user.is_authenticated:
        return render(request, "academics/index.html")
    else:
        return render(request, "academics/login.html", {
            "message": "You need to login first."
        })


@login_required
def projects_list(request):
    return render(request, "academics/projects_list.html", {
        "projects": request.user.contributing_projects.all(),
    })

@login_required
def tasks_list(request):
    return render(request, "academics/tasks_list.html", {
        "tasks": request.user.assigned_tasks.all()
    })


@login_required
def add_project(request):
    if request.method == "POST":
        new_project_form = NewProjectForm(request.POST)
        if new_project_form.is_valid():
            title = new_project_form.cleaned_data["title"]
            description = new_project_form.cleaned_data["description"]
        else:
            return render(request, "academics/add_project.html", {
                "message": "Invalid inputs.",
                "new_project_form": new_project_form
            })

        new_project = Project(
            title=title,
            description=description
        )
        new_project.save()
        new_project.members.add(request.user)
        new_project.members.add(*new_project_form.cleaned_data["members"])
        new_project.save()

        return render(request, "academics/projects_list.html", {
            "message": f"Successfully added project \"{title}\".",
            "projects": request.user.contributing_projects.all()
        })

    else:
        new_project_form = NewProjectForm()
        new_project_form.fields["members"].queryset = User.objects.exclude(id=request.user.id)
        return render(request, "academics/add_project.html", {
            "new_project_form": new_project_form
        })


@login_required
def add_task(request):
    if request.method == "POST":
        new_task_form = NewTaskForm(request.POST)
        if new_task_form.is_valid():
            title = new_task_form.cleaned_data["title"]
            description = new_task_form.cleaned_data["description"]
            deadline = new_task_form.cleaned_data["deadline"]
            assignee = new_task_form.cleaned_data["assignee"]
        else:
            return render(request, "academics/add_task.html", {
                "message": "Invalid inputs",
                "new_task_form": new_task_form
            })

        new_task = Task(
            title=title,
            description=description,
            deadline=deadline,
            assignee=assignee,
            author=request.user,
        )
        new_task.save()

        return render(request, "academics/tasks_list.html", {
            "message": f"Successfully added task \"{title}\".",
            "tasks": request.user.assigned_tasks.all()
        })

    else:
        return render(request, "academics/add_task.html", {
            "new_task_form": NewTaskForm()
        })

@login_required
def project(request, project_id):
    # TODO: check if user in members
    return render(request, "academics/project.html", {
        "project": get_object_or_404(Project, id=project_id)
    })

@login_required
def task(request, task_id):
    # TODO: check if user author or assignee
    return render(request, "academics/task.html", {
        "task": get_object_or_404(Task, id=task_id)
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