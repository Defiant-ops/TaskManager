#Forge

## Task Management REST API

A lightweight task management application built with **Python**, **Flask**, **MongoDB Atlas**, and a simple **HTML/CSS/JavaScript frontend**.

The application provides a RESTful API for managing personal tasks and includes Google authentication, task filtering, reminders, and a responsive dashboard.

---

## Features

### Task Management

- **Create Task (`POST`)**: Add a new task with title, description, due date, reminder, and status.
- **Read All Tasks (`GET`)**: Retrieve all tasks belonging to the logged-in user.
- **Read Task by ID (`GET`)**: Retrieve a single task by its MongoDB `ObjectId`.
- **Update Task (`PUT`)**: Modify an existing task.
- **Delete Task (`DELETE`)**: Remove a task by its ID.
- **Task Status**: Tasks can be marked as pending or completed.
- **Overdue Detection**: Pending tasks automatically appear as overdue after their due date.

### Authentication

- Google OAuth 2.0 login.
- User sessions using Flask sessions.
- Each user's tasks are isolated using their Google account email.
- Logout functionality.

### Dashboard

- Total task count.
- Pending task count.
- Completed task count.
- Overdue task count.
- Search tasks by title or description.
- Filter tasks by:
  - All
  - Pending
  - Completed
  - Overdue
- Click a task to view its details.
- Edit and delete tasks directly from the dashboard.

### Reminders & Notifications

- Task reminder date and time.
- Browser notification support.
- Custom task reminder alerts.
- Sound notification support.
- Automatic overdue alerts.
- Reminder checking while the application is open.

---

## Tech Stack

- **Backend**: Python
- **Framework**: Flask
- **Database**: MongoDB Atlas
- **Database Driver**: Flask-PyMongo / PyMongo
- **Authentication**: Google OAuth 2.0 using Authlib
- **Environment Management**: python-dotenv
- **Frontend**: HTML, CSS, JavaScript
- **Server**: Flask development server / Gunicorn for later deployment

---

## Prerequisites

Before running the application, make sure you have:

- [Python 3.10+](https://www.python.org/downloads/)
- A free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) cluster
- A MongoDB Atlas database user
- A Google Cloud project with Google OAuth credentials

---

## Project Structure

```text
Task-Manager/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
└── static/
    ├── index.html
    └── style.css
