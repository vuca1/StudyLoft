from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


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


class Thesis(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=500, blank=True)
    supervisor = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        related_name="supervised_thesis",
        null=True
    )
    student = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="student_thesis"
    )


class Project(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=True)
    members = models.ManyToManyField(
        "User",
        blank=False,
        related_name="contributing_projects"
    )


class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=500, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_tasks"
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
