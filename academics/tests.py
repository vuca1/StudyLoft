from django.test import TestCase

from .models import User, Subject, Project, Task, Thesis, Note, Teacher, Institution

# Create your tests here.
class ProjectTestCase(TestCase):

    def setUp(self):

        # create institution
        institution = Institution.objects.create(title="institution")

        # create users
        u1 = User.objects.create(username="u1", institution=institution)
        u2 = User.objects.create(username="u2", institution=institution)
        u3 = User.objects.create(username="u3", institution=None)

        # create projects
        project01 = Project.objects.create(title="project01", author=u1)
        project01.members.add(u1, u2)

    def test_user_institution(self):
        u1 = User.objects.get(username="u1")
        inst = Institution.objects.get(title="institution")
        self.assertEqual(u1.institution, inst)

    def test_user_no_institution(self):
            u3 = User.objects.get(username="u3")
            self.assertIsNone(u3.institution)

    def test_users_in_institution_count(self):
         inst = Institution.objects.get(title="institution")
         self.assertEqual(inst.students.count(), 2)

    def test_project_author(self):
        project = Project.objects.get(title="project01")
        u1 = User.objects.get(username="u1")
        self.assertEqual(project.author, u1)

    def test_project_member(self):
        project = Project.objects.get(title="project01")
        u2 = User.objects.get(username="u2")
        self.assertIn(u2, project.members.all())

    def test_project_member_count(self):
         project = Project.objects.get(title="project01")
         self.assertEqual(project.members.count(), 2)
        
        