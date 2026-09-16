from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


# TODO: add institutions (groups to divide students and teachers)


class Subject(models.Model):
    title = models.CharField(max_length=200, blank=False)
    description = models.CharField(max_length=500, blank=True)
    credits = models.PositiveSmallIntegerField(blank=False)
    teachers = models.ManyToManyField(
        "Teacher",
        blank=False,
        related_name="teaching_subjects"
    )


class Grade(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="subject_grades"
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name="student_grades"
    )
    date = models.DateField(blank=False)
    grade = models.CharField(max_length=50, blank=False)


class Teacher(models.Model):
    first = models.CharField(max_length=50, blank=False)
    last = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f"{self.last} {self.first}"


class Thesis(models.Model):
    DEGREE_CHOICES = [
        ("", "-Select Degree-"),
        ("bachelor", "Bachelor's"),
        ("master", "Master's"),
        ("doctoral", "Doctoral")
    ]

    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES
    )
    supervisor = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name="supervised_theses",
        null=True,
        blank=True
    )
    student = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="students_theses"
    )


class Project(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(
        "User",
        blank=False,
        related_name="contributing_projects"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_projects"
    )


class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_tasks"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="related_tasks"
    )


class Note(models.Model):
    content = models.TextField(max_length=1000, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="project_notes"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="task_notes"
    )
    thesis = models.ForeignKey(
        Thesis,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="thesis_notes"
    )
