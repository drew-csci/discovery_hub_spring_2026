# Discovery Hub - Django Backend Setup

This project has been converted from Flask to Django backend.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Update the following in `.env`:
- `SECRET_KEY`: Generate a new secret key
- `DEBUG`: Set to `False` in production
- Database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, etc.)
- Email settings for password reset

### 3. Database Migration

Create the initial database tables:

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

### 6. Access Django Admin

Visit `http://localhost:8000/admin/` and log in with your superuser credentials.

## Project Structure

- **accounts/**: User authentication and profile management
  - `models.py`: User model using Django's AbstractUser
  - `views.py`: Authentication views (login, register, logout, password reset)
  - `forms.py`: Django forms for authentication
  - `urls.py`: URL routing for accounts app
  - `admin.py`: Django admin configuration

- **pages/**: Main application pages
  - `models.py`: Page model for content management
  - `views.py`: Views for homepage, dashboards, and screens
  - `urls.py`: URL routing for pages app
  - `admin.py`: Django admin configuration

- **discovery_hub/**: Project configuration
  - `urls.py`: Root URL configuration
  - `__init__.py`: Package initialization

- **settings.py**: Django settings (database, authentication, installed apps, etc.)
- **manage.py**: Django management command utility
- **wsgi.py**: WSGI application for production deployment
- **requirements.txt**: Python package dependencies

## Key Differences from Flask

### Authentication
- **Flask**: Flask-Login + custom User model
- **Django**: Built-in Django authentication system with AbstractUser

### URL Routing
- **Flask**: @blueprint.route() decorators
- **Django**: urls.py with path() configuration

### Forms
- **Flask**: Flask-WTF with WTForms
- **Django**: Django Forms with ModelForms

### Database
- **Flask**: SQLAlchemy
- **Django**: Django ORM

### Configuration
- **Flask**: config.py with class-based configuration
- **Django**: settings.py module

## Common Django Commands

```bash
# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create a new app
python manage.py startapp app_name

# Run tests
python manage.py test

# Collect static files (for production)
python manage.py collectstatic

# Create a superuser account
python manage.py createsuperuser

# Access Django shell
python manage.py shell
```

## Notes

- User authentication now uses Django's built-in system
- Email-based authentication flows through Django's authentication backend
- Password reset tokens need to be implemented with Django's PasswordResetView or custom token system
- Static files should be collected using `collectstatic` for production
- CSRF protection is enabled by default in Django forms
