# StudyLoft

StudyLoft is a web application designed to help students organize their academic life in one place. It allows users to keep track of their subjects, grades, credits, teachers, theses, projects, tasks, deadlines, and notes. The application is built with Django on the back-end and JavaScript on the front-end, with Bootstrap used to create a responsive interface.

The main idea behind StudyLoft is to combine several parts of a student's academic life that would otherwise be managed separately. A student can maintain a list of their subjects and associated teachers and grades, create and manage academic projects, assign tasks to themselves or other students, and maintain information about their thesis. Projects, tasks, and theses can also contain notes, allowing additional information to be stored directly alongside the relevant work.

## Distinctiveness and Complexity

StudyLoft is distinct from the other CS50W projects because it is an academic management application rather than a social network, e-commerce site, or discussion-based website. Although users can work together on projects, collaboration is only one part of the application. The purpose of the application is to organize academic information and activities rather than to provide a platform for users to communicate socially. There are no posts, following relationships, likes, or other features whose primary purpose is social networking. Similarly, StudyLoft does not involve buying or selling products, shopping carts, payments, or any other e-commerce functionality.

The project is also more complex than a simple CRUD application because several different types of academic information are connected through Django model relationships. Users can belong to an institution, while teachers can also be associated with an institution. Subjects belong to individual students and are associated with teachers. Theses belong to students and can have a teacher as their supervisor. Projects can contain multiple student members and have an author, while tasks can be assigned to users and can optionally belong to a project. Notes can be associated with projects, tasks, or theses and also record their author and creation time.

The project therefore uses several types of Django relationships, including `ForeignKey` and `ManyToManyField`, as well as a custom user model based on Django's `AbstractUser`. These relationships are used throughout the application to determine what information should be displayed to a user and which users can access particular projects, tasks, theses, and notes.

JavaScript is also used for functionality beyond simply displaying a Django page. StudyLoft uses the Fetch API to add and remove notes and to add and remove subjects without requiring the entire page to reload. When a new note or subject is created, the Django view renders the corresponding HTML using `render_to_string()` and returns it as JSON. JavaScript then inserts the returned HTML into the existing page. This creates a more dynamic user experience while still allowing Django templates to generate the application's HTML.

The application also includes different access rules for different types of academic information. For example, project pages are restricted to project members, tasks can be accessed by their assignee or author, and thesis pages are restricted to the student who created the thesis. Notes also check whether the current user is allowed to add a note to the associated project, task, or thesis.

Finally, the application is designed to be mobile-responsive. Bootstrap is used throughout the templates to help the interface adapt to different screen sizes.

## Features

### User accounts

Users can register, log in, and log out. During registration, a user can select an institution. Django's authentication system is used for password handling and session management.

### Subjects

Users can create subjects containing a title, description, number of credits, grade, and teacher. Subjects are associated with the student who created them. Teachers are separate database objects and can be associated with multiple subjects.

Subjects can be added and removed using JavaScript and the Fetch API without reloading the page.

### Projects

Users can create academic projects and add other students from the same institution as project members. The user who creates a project is automatically added as a member and recorded as its author.

Projects have their own detail pages and can contain notes and related tasks. Project lists are ordered by their creation timestamp.

### Tasks

Users can create tasks with a title, description, deadline, and assignee. Tasks can optionally be associated with a project. Both the person who created a task and the person assigned to it can access the task.

### Theses

Users can create thesis entries containing a title, description, degree type, and supervisor. Thesis entries are associated with their student and can contain notes.

### Notes

Notes can be attached to projects, tasks, or theses. Each note records its author and creation time. JavaScript is used to add and remove notes dynamically without a full page reload.

## Technologies

* Python
* Django
* JavaScript
* HTML
* CSS
* Bootstrap
* SQLite
* Django Templates
* Fetch API

No additional third-party Python packages are currently required beyond Django and its dependencies.

## File Structure

### `manage.py`

The standard Django command-line utility used to run the development server, create migrations, apply migrations, and perform other Django management tasks.

### `studyloft/settings.py`

Contains the main Django configuration, including installed applications, middleware, templates, static files, database configuration, and the custom user model configuration.

### `studyloft/urls.py`

Contains the main URL configuration for the Django project and connects the project-level URLs with the `academics` application.

### `studyloft/asgi.py`

The ASGI configuration used when serving the Django project through an ASGI-compatible server.

### `studyloft/wsgi.py`

The WSGI configuration used when serving the Django project through a WSGI-compatible server.

### `academics/models.py`

Defines the application's database models. These include `Institution`, `User`, `Teacher`, `Subject`, `Thesis`, `Project`, `Task`, and `Note`.

The custom `User` model extends Django's `AbstractUser` and adds an optional relationship to an institution. Subjects belong to a student and have a teacher. Projects use a many-to-many relationship for their members, while tasks can optionally belong to projects. Notes can belong to a project, task, or thesis.

### `academics/views.py`

Contains the application's views, forms, authentication logic, object creation and deletion, access checks, and JSON endpoints used by JavaScript.

It also contains the `NewNoteForm`, `NewTaskForm`, `NewProjectForm`, `NewThesisForm`, and `NewSubjectForm` forms.

The note and subject endpoints return rendered HTML inside JSON responses so that JavaScript can insert newly created elements into the page without reloading it.

### `academics/urls.py`

Maps application URLs to the appropriate views, including authentication pages, lists and detail pages for projects, tasks, and theses, and endpoints used to add and remove notes and subjects.

### `academics/admin.py`

Contains the Django administration configuration for the `academics` application.

### `academics/apps.py`

Contains the Django application configuration for the `academics` application.

### `academics/tests.py`

Contains the test module for the `academics` Django application.

### `academics/static/academics/script.js`

Contains the JavaScript used for dynamic functionality. Event listeners handle adding and removing notes and subjects. The Fetch API sends asynchronous POST requests to Django views and processes the JSON responses.

When a note or subject is successfully created, the returned HTML is inserted into the existing page. Forms can also be reset without refreshing the page.

### `academics/static/academics/images/icon.png`

Contains the application's icon used by the website.

### `academics/templates/academics/layout.html`

The main layout template shared by the application's pages.

### `academics/templates/academics/index.html`

The main page displayed to authenticated users, providing an overview of relevant academic information.

### `academics/templates/academics/login.html`

Provides the user login interface.

### `academics/templates/academics/register.html`

Provides the registration interface, including institution selection.

### `academics/templates/academics/subjects.html`

Displays the user's subjects and provides the interface for adding and removing subjects.

### `academics/templates/academics/projects_list.html`

Displays projects available to the current user.

### `academics/templates/academics/project.html`

Displays the details of an individual project, including its members and notes.

### `academics/templates/academics/add_project.html`

Contains the form for creating a new project.

### `academics/templates/academics/tasks_list.html`

Displays tasks associated with the current user.

### `academics/templates/academics/task.html`

Displays the details of an individual task and its associated notes.

### `academics/templates/academics/add_task.html`

Contains the form for creating a new task.

### `academics/templates/academics/theses_list.html`

Displays the user's theses.

### `academics/templates/academics/thesis.html`

Displays the details of an individual thesis and its associated notes.

### `academics/templates/academics/add_thesis.html`

Contains the form for creating a new thesis.

### `academics/templates/academics/includes/card.html`

A reusable template for displaying project, task, or thesis information in a card format.

### `academics/templates/academics/includes/note.html`

A reusable template for displaying an individual note.

### `academics/templates/academics/includes/subject.html`

A reusable template for displaying an individual subject.

## How to Run

1. Make sure Python and Django are installed.

2. Clone or download the project and navigate to the project directory:

```bash
cd studyloft
```

3. Apply the existing database migrations:

```bash
python manage.py migrate
```

4. Start the Django development server:

```bash
python manage.py runserver
```

5. Open the development server address shown by Django in a web browser, normally:

```text
http://127.0.0.1:8000/
```

A user can then register a new account or log in with an existing account.

## Additional Information

StudyLoft uses SQLite as its database during development. The database file is included in the project directory. Django migrations are included in the application so that the database structure can be recreated with `python manage.py migrate`.

The application currently focuses on providing a centralized academic workspace rather than attempting to replace a university's official information system. Its purpose is to give students a convenient personal overview of their subjects, academic projects, tasks, thesis work, and notes.

The application was developed as the CS50W final project and builds upon concepts covered throughout the course, including Django models and relationships, authentication, Django forms, templates, URL routing, static files, JavaScript, asynchronous requests, and responsive web design.
