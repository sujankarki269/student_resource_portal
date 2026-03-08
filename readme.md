# Student Resource Portal (Ongoing)

A fully functional, modern student resource portal built with Django, SQLite, Bootstrap 5, and vanilla JavaScript. It provides a centralized platform for students to access, download, and preview notes, assignments, programs, and tutorials – all with a sleek, responsive interface.

## ✨ Features

### 📚 Resource Management
- **Notes** – Upload/download PDF notes with metadata (title, subject, uploader, date). Preview PDFs directly in a modal.
- **Assignments** – Filter by subject, due date, status (draft, submitted, graded). Upload/download assignment files.
- **Programs** – Display code snippets with syntax highlighting (Prism.js). Full code modal, language icons, and file downloads.
- **Tutorials** – Categorized (Web, Python, Django, etc.), optional video links and PDF downloads.

### 🔍 Search & Filter
- Global search across all resources.
- Filter by subject, category, semester, or uploader.
- Pagination for large lists.

### 👤 Authentication
- **Google Sign-In only** – No email/password registration (powered by Django Allauth).
- User profiles with download/upload history (optional).
- Admin dashboard for managing resources.

### 🎨 Modern UI/UX
- Fully responsive – works on mobile, tablet, and desktop.
- Dark/Light mode toggle – persists via cookie.
- Smooth hover animations and card designs.
- Custom mouse cursor and Siyuan font (with fallback).

### 🎉 Fun Interactive Elements
- **Flying fish animation** at the bottom.
- **Particle explosion** on mouse click (colorful burst).

### 📊 Download Statistics
- Tracks downloads and views for each resource.
- Displayed on cards.

### 📢 Announcements
- Admin can post active announcements (displayed site-wide).

### 🏷️ Tagging System
- Resources can be tagged for better categorization.

### 🔧 Admin Dashboard
- Full Django admin interface for managing subjects, resources, tags, and announcements.

## 🛠 Tech Stack

| **Category**       | **Technologies**                                                                 |
|--------------------|----------------------------------------------------------------------------------|
| **Backend**        | Django 4.2, SQLite (default), Django Allauth (Google OAuth)                     |
| **Frontend**       | HTML5, CSS3, JavaScript, Bootstrap 5                                             |
| **Libraries**      | Prism.js (syntax highlighting), jQuery (fish animation), Live2D (mascot), Font Awesome |
| **Deployment**     | Ready for PythonAnywhere, Heroku, or any Django-compatible host                  |

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)
- Google OAuth credentials (for login)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/student-resource-portal.git
cd student-resource-portal
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, create one with:

```bash
pip freeze > requirements.txt
```

But for a fresh install, you can manually install:

```bash
pip install django django-allauth
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 🔐 Google OAuth Setup (To be done)

To enable Google Sign-In, follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Navigate to **APIs & Services** > **OAuth consent screen**.
   - Choose **External** (or Internal if within your organization).
   - Fill in the required fields (app name, support email, etc.).
   - Add the scope: `.../auth/userinfo.email` and `.../auth/userinfo.profile`.
   - Add test users if needed.
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client IDs**.
   - Application type: **Web application**.
   - Name: `Student Portal`.
   - **Authorized redirect URIs**: Add
     - `http://127.0.0.1:8000/accounts/google/login/callback/`
     - `http://localhost:8000/accounts/google/login/callback/`
     - (For production, add your domain)
5. Note your **Client ID** and **Client Secret**.
6. In Django admin (`/admin`), go to **Social Accounts** > **Social applications** and click **Add**.
   - Provider: Google
   - Name: `Google Login`
   - Client ID: (paste your client id)
   - Secret Key: (paste your secret)
   - Sites: Choose the default site (or create one). If no site exists, go to **Sites** and add one (e.g., `localhost:8000`).

Now the "Sign in with Google" button will work.

## 📁 Project Structure

```
student_resource_portal/
├── manage.py
├── portal/                  # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                     # Main app
│   ├── models.py             # Database models
│   ├── views.py              # All view logic
│   ├── urls.py               # App URLs
│   ├── admin.py              # Admin registrations
│   ├── forms.py              # User registration form
│   ├── context_processors.py # Global context (tags, announcements)
│   ├── templates/            # HTML templates
│   │   └── core/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── notes.html
│   │       ├── assignments.html
│   │       ├── programs.html
│   │       ├── tutorials.html
│   │       └── includes/
│   ├── static/               # CSS, JS, images
│   │   └── core/
│   │       ├── css/
│   │       ├── js/
│   │       └── images/
│   └── migrations/
├── media/                    # User-uploaded files (PDFs, etc.)
└── db.sqlite3                # SQLite database
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

For major changes, please open an issue first to discuss what you'd like to change.

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
