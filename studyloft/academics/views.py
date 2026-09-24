from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import User, Subject, Teacher, Thesis, Project, Task, Note, Institution


class NewNoteForm(forms.Form):
    content = forms.CharField(
        label="Content",
        required=True,
        max_length=1000,
        widget=forms.Textarea(attrs={
            "rows": 2
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
        required=True,
        max_length=500
    )
    supervisor = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        empty_label="-Select Supervisor-"
    )
    degree = forms.ChoiceField(
        choices=Thesis.DEGREE_CHOICES,
        required=True
    )


class NewSubjectForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=200,
        required=True
        )
    description = forms.CharField(
        label="Description",
        max_length=500,
        required=False
    )
    credits = forms.IntegerField(
        label="Credits",
        min_value=0,
        required=True,
        max_value=50
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        required=True,
        empty_label="-Select Teacher-"
    )
    grade = forms.ChoiceField(
        choices=Subject.GRADE_CHOICES,
        required=True
    )


@login_required
def add_note(request, job_id):
    if request.method == "POST":
        content = request.POST["content"]
        job_type = request.POST["job-type"]

        # check if content empty
        if content == "":
            return JsonResponse({
                "success": False,
                "content": content
            })

        # get desired object
        match job_type:
            case "project":
                job = get_object_or_404(Project, id=job_id)
            case "task":
                job = get_object_or_404(Task, id=job_id)
            case "thesis":
                job = get_object_or_404(Thesis, id=job_id)

        # check if user is allowed to add note
        if not can_add_note(request.user, job):
            return JsonResponse({
                "success": False,
                "content": content
            })

        # create new note object
        new_note = Note(
            content=content,
            author=request.user
            )

        # add appropriate job type
        match job_type:
            case "project":
                new_note.project=job
            case "task":
                new_note.task=job
            case "thesis":
                new_note.thesis=job

        new_note.save()

        # convert note to html
        note_html = render_to_string(
            "academics/includes/note.html",
            {"note": new_note},
            request=request
        )

        return JsonResponse({
            "success": True,
            "note_html": note_html
        })


@login_required
def remove_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(
            Note,
            id=note_id,
            author=request.user
        )
    
        note.delete()
        return JsonResponse({
            "success": True
        })
    
    return JsonResponse({
        "success": False
    })


def index(request):
    if request.user.is_authenticated:
        return render(request, "academics/index.html", {
            "projects": request.user.contributing_projects.all().order_by("timestamp")[:3],
            "tasks": request.user.assigned_tasks.all().order_by("-deadline")[:3],
            "thesis": request.user.students_theses.all().order_by("-timestamp").first()
        })
    else:
        return render(request, "academics/login.html", {
            "message": "You need to login first."
        })


@login_required
def projects_list(request):
    return render(request, "academics/projects_list.html", {
        "projects": request.user.contributing_projects.all().order_by("-timestamp"),
    })


@login_required
def tasks_list(request):
    return render(request, "academics/tasks_list.html", {
        "tasks": request.user.assigned_tasks.all().order_by("deadline"),
        "created_tasks": request.user.created_tasks.all().order_by("deadline")
    })


@login_required
def theses_list(request):
    return render(request, "academics/theses_list.html", {
        "theses": request.user.students_theses.all().order_by("timestamp"),
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
                "message": "Invalid input(s).",
                "new_project_form": new_project_form
            })

        new_project = Project(
            title=title,
            description=description,
            author=request.user
        )
        new_project.save()
        new_project.members.add(request.user)
        new_project.members.add(*new_project_form.cleaned_data["members"])
        new_project.save()

        messages.success(request, f"Project \"{title}\" has been added.")
        return redirect("projects_list")

    else:
        new_project_form = NewProjectForm()
        new_project_form.fields["members"].queryset = User.objects.filter(
            institution=request.user.institution
        ).exclude(id=request.user.id)
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
                "message": "Invalid input(s).",
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

        messages.success(request, f"Task \"{title}\" has been added.")
        return redirect("tasks_list")

    else:
        return render(request, "academics/add_task.html", {
            "new_task_form": NewTaskForm()
        })


@login_required
def add_thesis(request):    
    if request.method == "POST":
        new_thesis_form = NewThesisForm(request.POST)
        if new_thesis_form.is_valid():
            title = new_thesis_form.cleaned_data["title"]
            description = new_thesis_form.cleaned_data["description"]
            degree = new_thesis_form.cleaned_data["degree"]
            supervisor = new_thesis_form.cleaned_data["supervisor"]
        else:
            return render(request, "academics/add_thesis.html", {
                "message": "Invalid input(s).",
                "new_thesis_form": new_thesis_form
            })

        new_thesis = Thesis(
            title=title,
            description=description,
            degree=degree,
            supervisor=supervisor,
            student=request.user
        )
        new_thesis.save()

        messages.success(request, f"Thesis \"{title}\" has been added.")
        return redirect("theses_list")

    else:
        new_thesis_form = NewThesisForm()
        new_thesis_form.fields["supervisor"].queryset = Teacher.objects.filter(
            institution=request.user.institution
        )
        return render(request, "academics/add_thesis.html", {
            "new_thesis_form": new_thesis_form
        })


@login_required
def add_subject(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        credits = request.POST["credits"]
        grade = request.POST["grade"]
        teacher_id = request.POST["teacher"]

        # if required fields empty return unsuccessful
        if title == "" or credits == "" or grade == "" or teacher_id == "":
            return JsonResponse({
                "success": False
            })

        # create new subject object
        new_subject = Subject(
            title=title,
            description=description,
            credits=credits,
            grade=grade,
            teacher=get_object_or_404(Teacher, id=teacher_id),
            student=request.user
        )
        new_subject.save()

        # create subject html element
        subject_html = render_to_string(
            "academics/includes/subject.html",
            {"subject": new_subject},
            request=request
        )

        return JsonResponse({
            "success": True,
            "subject_html": subject_html
        })


@login_required
def subjects(request):
    if request.method == "POST":
        pass

    else:
        new_subject_form = NewSubjectForm()
        new_subject_form.fields["teacher"].queryset = Teacher.objects.filter(
            institution=request.user.institution
        )
        return render(request, "academics/subjects.html", {
            "subjects": request.user.subjects.all().order_by("-id"),
            "new_subject_form": new_subject_form
        })


@login_required
def project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        members=request.user
    )

    return render(request, "academics/project.html", {
        "project": project,
        "new_note_form": NewNoteForm(),
        "notes": project.project_notes.all().order_by("-timestamp")
    })


@login_required
def task(request, task_id):
    task = get_object_or_404(
        Task,
        Q(id=task_id) & (
            Q(assignee=request.user) |
            Q(author=request.user)
        )
    )

    return render(request, "academics/task.html", {
        "task": task,
        "new_note_form": NewNoteForm(),
        "notes": task.task_notes.all().order_by("-timestamp")
    })


@login_required
def thesis(request, thesis_id):
    thesis = get_object_or_404(
        Thesis,
        id=thesis_id,
        student=request.user
    )

    return render(request, "academics/thesis.html", {
        "thesis": thesis,
        "new_note_form": NewNoteForm(),
        "notes": thesis.thesis_notes.all().order_by("-timestamp")
    })


@login_required
def remove_project(request, project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        author=request.user
    )
    project_title = project.title

    # remove project from db
    project.delete()
    messages.success(request, f"Project \"{project_title}\" has been removed.")
    return redirect("projects_list")


@login_required
def remove_task(request, task_id):
    task = get_object_or_404(
            Task,
            id=task_id,
            author=request.user
        )
    task_title = task.title

    # remove task from db
    task.delete()
    messages.success(request, f"Task \"{task_title}\" has been removed.")
    return redirect("tasks_list")


@login_required
def remove_thesis(request, thesis_id):
    thesis = get_object_or_404(
        Thesis,
        id=thesis_id,
        student=request.user
    )
    thesis_title = thesis.title

    # remove thesis from db
    thesis.delete()
    messages.success(request, f"Thesis \"{thesis_title}\" has been removed.")
    return redirect("theses_list")


@login_required
def remove_subject(request, subject_id):
    if request.method == "POST":
        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        subject.delete()
        return JsonResponse({
            "success": True
        })

    return JsonResponse({
        "success": False
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        institution_id = request.POST["institution"]

        # password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "academics/register.html", {
                "message": "Passwords must match.",
                "institutions": Institution.objects.all().order_by("title")
            })

        if institution_id:
            # check if institution exists
            institution = Institution.objects.filter(id=institution_id ).first()
            if institution is None:
                return render(request, "academics/register.html", {
                    "message": "Invalid institution.",
                    "institutions": Institution.objects.all().order_by("title")
                })
        else:
            institution = None

        # try to create new user
        try:
            user = User.objects.create_user(
                username,
                email,
                password,
                institution=institution)
            user.save()
        except IntegrityError:
            return render(request, "academics/register.html",{
                "message": "Username or email already taken.",
                "institutions": Institution.objects.all().order_by("title")
            })

        login(request, user)
        messages.success(request, "Successfully registered.")
        return redirect("index")
    else:
        return render(request, "academics/register.html", {
            "institutions": Institution.objects.all().order_by("title")
        })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # check if authenticate successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "academics/login.html", {
                "message": "Invalid username and/or password."
            })

    else:
        return render(request, "academics/login.html")


def logout_view(request):
    logout(request)
    return redirect("login_view")


def can_add_note(user, obj):
    # returns True if user is allowed to add note to the job (project/task/thesis)
    if isinstance(obj, Project):
        return user in obj.members.all()

    if isinstance(obj, Task):
        return user == obj.assignee or user == obj.author

    if isinstance(obj, Thesis):
        return user == obj.student