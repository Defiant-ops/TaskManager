# Forge — Cloud Task Manager

`https://forge-8src.onrender.com`

A full-stack task management web application built with **Flask**, **MongoDB Atlas**, and **Google OAuth 2.0**, deployed on **Render**.

---

## Features

- **Google OAuth Authentication:** Secure single sign-on using Google accounts via Authlib.
- **Task Management (CRUD):** Create, search, filter, and track tasks (Pending, Completed, Overdue).
- **Persistent Storage:** Cloud-hosted MongoDB cluster for reliable document storage.
- **Dynamic Timezone & Reminders:** Handles local client deadlines, timestamps, and notification preferences.
- **Production-Ready WSGI:** Served via Gunicorn with dynamic HTTPS reverse-proxy support.

---

## Tech Stack

- **Backend:** Python 3, Flask, Werkzeug, Jinja2
- **Database:** MongoDB Atlas (via `Flask-PyMongo` & `pymongo`)
- **Authentication:** Authlib, Google OAuth 2.0
- **Server / Deployment:** Gunicorn, Render

---

## Project Structure

```text
├── static/              # CSS styles, client-side JS, images
├── templates/           # Jinja2 HTML templates
├── app.py               # Main Flask application and API routes
├── requirements.txt     # Python project dependencies
└── README.md            # Project documentation
```

---

## Getting Started Locally

### Prerequisites

- Python 3.10+ installed
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account and cluster
- A [Google Cloud Console](https://console.cloud.google.com/) project with OAuth 2.0 credentials

### 1. Clone the Repository

```bash
git clone https://github.com/Defiant-ops/Forge.git
cd Forge
```

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory (ensure it is added to `.gitignore`):

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/task_manager?retryWrites=true&w=majority
SECRET_KEY=your-super-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 5. Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your web browser.

---

## Deployment (Render)

### 1. Web Service Setup
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### 2. Environment Variables
Add the following keys in your Render service dashboard under **Environment**:
- `MONGO_URI`: Your MongoDB Atlas connection string
- `SECRET_KEY`: A cryptographically secure random key
- `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret

### 3. Google OAuth Redirects
In your Google Cloud Console OAuth 2.0 Client credentials, register:
- **Authorized JavaScript origins:** `https://forge-8src.onrender.com`
- **Authorized redirect URIs:** `https://forge-8src.onrender.com/authorize`

---

## License

This project is open-source and available under the [MIT License](LICENSE).
