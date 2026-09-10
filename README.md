Task Manager

A lightweight personal Task Manager built with Flask + MongoDB + Google OAuth, with a responsive dark/gunmetal dashboard.

The current UI uses a gunmetal grey + white + yellow visual theme.

Features

Authentication

Google OAuth 2.0 login using Authlib.

Login/logout session handling with Flask sessions.

/me endpoint to determine the current login state.

Tasks are isolated by the authenticated user's email address.

Task Management

Create tasks.

View all tasks.

View individual task details.

Edit tasks.

Mark tasks as completed.

Undo completion.

Delete tasks.

Task descriptions are hidden from the main card and shown in a details modal.

Task Status

Tasks display one primary status tag:

PENDING — deadline has not passed.

OVERDUE — deadline has passed and the task is not completed.

COMPLETED — task has been marked as done.

The frontend calculates OVERDUE dynamically from the due date.

Reminders

Supported reminder formats:

30M
2H
1D

Examples:

30M = 30 minutes before the due time.

2H = 2 hours before the due time.

1D = 1 day before the due time.

The browser checks reminders every 10 seconds.

Browser Notifications

Optional browser notifications.

Optional reminder sound.

Custom in-page reminder/overdue dialog.

Notification permission is controlled by the browser.

Browser-based reminders require the web application/browser to remain available. This project does not currently contain a server-side scheduler or push-notification service.

Dashboard

Total task count.

Pending count.

Completed count.

Overdue count.

All/Pending/Completed/Overdue filters.

Task search.

Local browser timezone display.

Responsive desktop/mobile layout.

Project Structure

task_manager/
│
├── app.py
│
├── static/
│   ├── index.html
│   └── style.css
│
├── requirements.txt
│
├── .env
│
├── .gitignore
│
└── README.md

Technology Stack

Component

Technology

Backend

Python / Flask

Database

MongoDB

MongoDB integration

Flask-PyMongo

Authentication

Google OAuth + Authlib

Frontend

HTML / CSS / JavaScript

Hosting

Google Cloud Run

Database hosting

MongoDB Atlas recommended

Environment configuration

.env locally / Secret Manager in production

Local Development

1. Clone or copy the project

git clone <YOUR_REPOSITORY_URL>
cd task_manager

If you are working from the local project folder instead:

cd task_manager

2. Create a virtual environment

Windows

python -m venv venv
venv\Scripts\activate

Linux/macOS

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

Create requirements.txt with:

Flask
Flask-PyMongo
Authlib
python-dotenv
gunicorn
pymongo

Then:

pip install -r requirements.txt

Environment Variables

Create a local .env file:

FLASK_SECRET_KEY=replace_with_a_long_random_secret
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/task_manager
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

Important

Never commit .env to Git.

Your .gitignore should contain:

.env
venv/
__pycache__/
*.pyc

MongoDB

This project expects MongoDB through:

MONGO_URI

The application uses the database selected by the MongoDB connection string and stores tasks in:

tasks

Each task contains approximately:

{
    "title": "Finish project",
    "description": "Complete the final report",
    "dueDate": "2026-09-12T18:30",
    "reminder": "30M",
    "status": "pending",
    "userEmail": "user@example.com"
}

The userEmail field is used to make sure users only access their own tasks.

Recommended production database

Use MongoDB Atlas rather than attempting to run MongoDB inside the Cloud Run container.

Make sure the Cloud Run service is allowed to connect to the Atlas cluster.

Google OAuth

The application currently uses Google OpenID Connect through Authlib.

Local development currently uses:

http://127.0.0.1:5000/authorize

This URI must be configured in the Google OAuth client's Authorized redirect URIs.

Production warning

The current app.py contains a hard-coded local redirect URI:

redirect_uri="http://127.0.0.1:5000/authorize"

This must be changed before deploying to Cloud Run.

For production, the redirect URI needs to use the deployed HTTPS service URL, for example:

https://YOUR-CLOUD-RUN-URL/authorize

The Google OAuth configuration must contain the exact same production redirect URI.

Recommended improvement before deployment

Change the application to use an environment variable:

GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

and:

return google.authorize_redirect(
    redirect_uri=GOOGLE_REDIRECT_URI
)

Then use:

Local .env

GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/authorize

Cloud Run

GOOGLE_REDIRECT_URI=https://YOUR-CLOUD-RUN-URL/authorize

This prevents the production deployment from depending on the local development URL.

Running Locally

Start Flask:

python app.py

Then open:

http://127.0.0.1:5000

Test the following:

Google login.

Logout.

Create a task.

Refresh the page.

Edit the task.

Click the task to open details.

Mark it completed.

Undo completion.

Delete the task.

Test an overdue task.

Test a reminder.

Test browser notifications.

API Endpoints

Authentication

Login

GET /login

Redirects the user to Google OAuth.

OAuth callback

GET /authorize

Handles the Google OAuth response and creates the Flask session.

Current user

GET /me

Unauthenticated:

{
    "authenticated": false
}

Authenticated:

{
    "authenticated": true,
    "user": {
        "email": "user@example.com",
        "name": "User Name"
    }
}

Logout

GET /logout

Clears the Flask session.

Task API

All task endpoints require authentication.

Create

POST /tasks

Example:

{
    "title": "Finish project",
    "description": "Complete the final report",
    "dueDate": "2026-09-12T18:30",
    "reminder": "30M",
    "status": "pending"
}

Get all tasks

GET /tasks

Returns only tasks belonging to the logged-in user.

Get one task

GET /tasks/<id>

Update

PUT /tasks/<id>

Example:

{
    "title": "Finish project",
    "description": "Updated description",
    "dueDate": "2026-09-12T18:30",
    "reminder": "1H",
    "status": "pending"
}

Valid backend statuses:

pending
done

The frontend converts these into:

PENDING
OVERDUE
COMPLETED

Delete

DELETE /tasks/<id>
