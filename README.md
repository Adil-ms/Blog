# Django Blog

A blog application built with Django featuring post management, categories, rich text editing, image uploads, and pagination.

## Features

- Create and manage blog posts
- Categories and authors
- Rich text editor (CKEditor 5)
- Featured image uploads
- Pagination
- Search and filtering
- Django Admin integration

## Tech Stack

- Python
- Django 5
- CKEditor 5
- SQLite (default)
- HTML, CSS, JavaScript

## Installation

### Clone the repository

```bash
git clone https://github.com/Adil-ms/Blog.git
cd Blog
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
python manage.py migrate
```

### Start the development server

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000/
```

## Project Structure

```text
blog/
├── posts/
├── users/
├── web/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

## Notes

- Uploaded media files are not included in the repository.
- Configure your own database settings if using PostgreSQL.
- Generate a new Django SECRET_KEY before deployment.

## Author

Adil
