# Discovery Hub - Comprehensive Project Documentation
**Author:** Dylan Tomza  
**Date:** March 22, 2026  
**Project Type:** Django-based Web Application

---

## 📋 Project Overview

**Discovery Hub** is a Django-based multi-role web application designed to facilitate connections between three distinct user types: Universities, Companies, and Investors. The application implements a custom authentication system using email-based login and provides role-specific user experiences through a progressive screen-based interface.

### Key Features:
- **Custom User Model**: Email-based authentication with three user roles (University, Company, Investor)
- **Role-Based Views**: Three progressive screens (Screen 1, 2, 3) accessible only after authentication
- **PostgreSQL Database**: Remote database connection for data persistence
- **Environment Configuration**: Secure credential management via `.env` file
- **Bootstrap Utility**: One-shot project setup script
- **File Packaging**: Utility to convert directory structures to XML format

---

## 📁 Project File Structure & Descriptions

### Core Project Configuration Files

#### `manage.py`
- **Purpose**: Django management command entry point
- **Usage**: Used to run Django commands (migrations, shell, runserver, etc.)
- **Interaction**: Called from the command line; manages all Django operations
- **Example**: `python manage.py runserver`, `python manage.py migrate`

#### `requirements.txt`
- **Purpose**: Lists Python package dependencies for the project
- **Dependencies**:
  - `Django>=5.0,<6.0` - Web framework
  - `psycopg2-binary` - PostgreSQL database adapter
  - `python-dotenv` - Environment variable management
- **Interaction**: Used with `pip install -r requirements.txt` to set up the Python environment
- **Current State**: Already populated with project dependencies

#### `.env` (Environment Configuration File)
- **Purpose**: Stores sensitive configuration and credentials
- **Key Variables**:
  - `DJANGO_SECRET_KEY` - Secret key for Django (security)
  - `DJANGO_DEBUG` - Debug mode toggle (True for development)
  - `DB_NAME` - PostgreSQL database name
  - `DB_USER` - PostgreSQL user
  - `DB_PASSWORD` - PostgreSQL password
  - `DB_HOST` - Remote database host (34.16.174.60)
  - `DB_PORT` - PostgreSQL port (5432)
  - `ALLOWED_HOSTS` - Permitted host names
- **Interaction**: Read by `settings.py` using `python-dotenv`
- **Status**: Already configured as noted in README

---

### Bootstrap & Utility Scripts

#### `bootstrap_discovery_hub.py`
- **Purpose**: One-shot setup script to initialize the entire Django project from scratch
- **What It Sets Up**:
  1. Virtual environment with required dependencies
  2. Django project structure (`discovery_hub` package)
  3. Two Django apps: `accounts` and `pages`
  4. Custom user model with email authentication
  5. Database migrations for initial schema
  6. Template directories and basic styling
- **Usage**: `python bootstrap_discovery_hub.py`
- **Interaction**: Runs independently to create project structure; subsequent runs by developers use this as reference
- **Status**: Completed; project structure already created

#### `pack_dir_to_xml.py`
- **Purpose**: Converts entire directory structure and file contents into a single XML file for easy distribution/analysis
- **Usage**: `python pack_dir_to_xml.py . combined_files.xml`
- **Flags**:
  - `--include-hidden` - Include hidden files like `.gitignore`
  - `--max-bytes 1000000` - Skip files larger than threshold
- **Features**:
  - Automatically detects text vs. binary files
  - Encodes binary files in base64
  - Preserves file structure in XML hierarchy
- **Interaction**: Used for backup, analysis, or code review by external parties
- **Typical Output**: XML file like `discovery_output_20260316.xml` stored in root
- **Current Output**: `discovery_output_20260316.xml` - likely generated snapshot of project files

---

### Django Project Package: `discovery_hub/`

The main Django configuration package containing project-level settings and routing.

#### `discovery_hub/settings.py`
- **Purpose**: Central Django configuration file
- **Key Configurations**:
  - Database settings pulled from `.env` (PostgreSQL)
  - Installed apps: `accounts`, `pages`, and Django built-ins
  - Middleware stack for security and session management
  - Template engine configuration pointing to `templates/` directory
  - Static files configuration
  - Custom user model: `AUTH_USER_MODEL = 'accounts.User'`
- **Interaction**: Loaded automatically when Django starts; provides all project settings
- **Environment Integration**: Uses `dotenv.load_dotenv()` to read `.env` file

#### `discovery_hub/urls.py`
- **Purpose**: Root URL router for the entire application
- **Routes**:
  - `/admin/` - Django admin interface
  - `/` and `/screen*/` - Pages app URLs (`pages.urls`)
  - `/accounts/` - Accounts app URLs (`accounts.urls`)
  - `/logout/` - Global logout view
- **Interaction**: Delegates routing to included URL patterns from `accounts.urls` and `pages.urls`
- **Request Flow**: All incoming requests matched against these patterns

#### `discovery_hub/asgi.py`
- **Purpose**: ASGI configuration for async web servers (e.g., Uvicorn, Daphne)
- **Usage**: Points to WSGI application for production deployment
- **Interaction**: Used by async web servers; not typically needed for development

#### `discovery_hub/wsgi.py`
- **Purpose**: WSGI configuration for standard web servers (e.g., Gunicorn, uWSGI)
- **Usage**: Entry point for production deployment
- **Interaction**: Used when running `python manage.py runserver` or in production

---

### Authentication App: `accounts/`

Handles user authentication, registration, and custom user model.

#### `accounts/models.py`
- **Purpose**: Defines the custom User model with email-based authentication
- **Custom User Model**:
  ```
  User (extends AbstractUser)
  ├── email (unique, required) - Primary login field
  ├── username (required for admin compatibility)
  ├── user_type (choices: university, company, investor)
  ├── first_name, last_name
  └── Methods:
      ├── save() - Auto-populates username from email if empty
      └── display_name (property) - Returns full name or email
  ```
- **Key Features**:
  - `USERNAME_FIELD = 'email'` - Uses email instead of username for login
  - `UserType` choices restrict valid roles
- **Interaction**: Database model; used by forms and views for user management
- **Database**: Stored in `auth_user` table (extended with `user_type` field)

#### `accounts/forms.py`
- **Purpose**: Django forms for user registration and login
- **Components**:
  1. **UserRegistrationForm** (extends UserCreationForm):
     - Fields: email, password1, password2, user_type (radio buttons)
     - Validates passwords and email uniqueness
  2. **EmailAuthenticationForm** (extends AuthenticationForm):
     - Relabels "username" field to "Email"
     - Adds placeholder text for better UX
- **Interaction**: Used by view forms in `accounts/views.py`; validates user input before saving

#### `accounts/views.py`
- **Purpose**: Handles registration and login logic
- **Views**:
  1. **RegisterView** (FormView):
     - Template: `templates/accounts/register.html`
     - Form: `UserRegistrationForm`
     - On success: Creates user, logs them in, redirects to `screen1`
     - Accepts `type` query parameter to pre-select user_type
  2. **CustomLoginView** (LoginView):
     - Template: `templates/accounts/login.html`
     - Form: `EmailAuthenticationForm`
     - Stores `selected_user_type` in session for context
     - Redirects authenticated users to `screen1`
- **Interaction**: Entry point for user authentication; called via URLs defined in `accounts/urls.py`

#### `accounts/urls.py`
- **Purpose**: URL routing for authentication endpoints
- **Routes**:
  - `/accounts/login/` → `CustomLoginView`
  - `/accounts/register/` → `RegisterView`
  - `/accounts/logout/` → Django's built-in LogoutView
- **Interaction**: Included in root `discovery_hub/urls.py`; maps requests to views

#### `accounts/admin.py`
- **Purpose**: Registers the User model with Django admin
- **Functionality**: Lists and manages users in `/admin/` interface
- **Interaction**: Used by administrators to manage user accounts

#### `accounts/apps.py` and `accounts/__init__.py`
- **Purpose**: Django app configuration and module initialization
- **Interaction**: Auto-discovered by Django for app setup

#### `accounts/migrations/`
- **Purpose**: Database migration files that define schema changes
- **Current Migrations**:
  - `0001_initial.py` - Creates initial User model with custom fields
- **Interaction**: Applied via `python manage.py migrate`; creates/updates database schema

---

### Pages App: `pages/`

Implements the main user interface screens and post-authentication views.

#### `pages/models.py`
- **Purpose**: Data models for the pages app
- **Current State**: Empty (placeholder for future models)
- **Intended Use**: Can store page content, user submissions, or discoveries

#### `pages/views.py`
- **Purpose**: Handles rendering of screens for authenticated users
- **Views** (all require `@login_required`):
  1. **welcome()** - Public welcome page with role selection buttons
  2. **screen1()** - First authenticated screen
  3. **screen2()** - Second authenticated screen
  4. **screen3()** - Third authenticated screen
- **Functionality**:
  - Extracts user's `user_type` role from request
  - Passes role to template for role-specific rendering
  - Enforces authentication with `@login_required` decorator
- **Interaction**: Renders role-specific templates from `templates/pages/`

#### `pages/urls.py`
- **Purpose**: URL routing for page views
- **Routes**:
  - `/` → `welcome` - Public landing page
  - `/screen1/` → `screen1` - First authenticated screen
  - `/screen2/` → `screen2` - Second authenticated screen
  - `/screen3/` → `screen3` - Third authenticated screen
- **Interaction**: Included in root URLs; directs to page views

#### `pages/admin.py`
- **Purpose**: Registers page-related models with admin interface
- **Current State**: Empty (no models registered yet)

#### `pages/apps.py` and `pages/__init__.py`
- **Purpose**: Django app configuration and module initialization

#### `pages/migrations/`
- **Purpose**: Database migration files for pages app models
- **Current State**: Contains only `__init__.py` (no active migrations)

---

## 🎨 Frontend Files

### Base Template: `templates/base.html`
- **Purpose**: Base template extended by all pages; provides HTML structure and navigation
- **Key Elements**:
  - Header with "Discovery Hub" branding
  - Navigation bar with conditional links (authenticated vs. anonymous)
  - If authenticated: Shows screens 1-3 links, user display name, logout button
  - If anonymous: Shows login and registration links
- **Used By**: All other templates via `{% extends "base.html" %}`

### Page Templates: `templates/pages/`

#### `pages/welcome.html`
- **Purpose**: Public welcome page (accessible without login)
- **Content**: 
  - Title and welcome message
  - Three buttons to choose user type (University, Company, Investor)
  - Links to login with selected type or to register
- **Interaction**: Entry point to application; user selects role before proceeding to login/register

#### `pages/screen1.html` through `pages/screen3.html`
- **Purpose**: Role-specific user interface screens (protected)
- **Interaction**: Rendered by corresponding views in `pages/views.py`
- **Context Variables**: `role` (User's role in title case)
- **Design**: Likely contains role-specific content for each of the three user types

### Authentication Templates: `templates/accounts/`

#### `accounts/login.html`
- **Purpose**: Email/password login form
- **Form**: `EmailAuthenticationForm` with email and password fields
- **Context**: `selected_user_type` (if coming from welcome page)
- **Interaction**: Submits to `CustomLoginView`

#### `accounts/register.html`
- **Purpose**: User registration form with role selection
- **Form**: `UserRegistrationForm` with email, passwords, and user_type radio buttons
- **Interaction**: Submits to `RegisterView`; creates new user

### Partial Templates: `templates/pages/partials/`
- **Purpose**: Reusable components for role-specific content
- **Files** (pattern: `s{screen}_{role}.html`):
  - `s1_company.html`, `s1_investor.html`, `s1_university.html`
  - `s2_company.html`, `s2_investor.html`, `s2_university.html`
  - `s3_company.html`, `s3_investor.html`, `s3_university.html`
- **Likely Usage**: Included in screen templates via `{% include %}` for role-specific content

### Static Files: `static/css/styles.css`
- **Purpose**: Global CSS styling for the application
- **Linked From**: `base.html` via `{% static 'css/styles.css' %}`
- **Scope**: All templates inherit these styles

---

## 🔄 Application Data Flow & Interactions

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser / User                            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Django Development Server                      │
│  (runserver via manage.py or gunicorn/uWSGI in production)  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────┐
         │  discovery_hub/urls.py (router)   │
         └───┬──────────────────────────┬───────┬───────────┐
             │                          │       │           │
             ▼                          ▼       ▼           ▼
         pages/urls.py          accounts/urls.py admin  logout
         (/, /screen*/)         (/login,/register)
             │                          │
             ▼                          ▼
      pages/views.py          accounts/views.py
      (welcome, screen1-3)  (RegisterView, LoginView)
             │                          │
             ├──────────┬───────────────┤
             │          │               │
             ▼          ▼               ▼
         Templates    Forms         Models
         (HTML)      (Validation)   (Database)
             │          │               │
             └──────────┴───────────────┘
                         │
                         ▼
         ┌───────────────────────────────────┐
         │      PostgreSQL Database          │
         │  (Remote: 34.16.174.60:5432)     │
         │  Tables: auth_user, etc.         │
         └───────────────────────────────────┘
```

### Authentication Flow

```
User arrives at welcome page
         │
         ├─── (Not logged in)
         │
         ▼
Selects role (University/Company/Investor)
         │
         ▼
Authenticates (Login or Register)
         │
         ├─── Existing User (Login):
         │    └─ CustomLoginView validates email + password
         │      └─ EmailAuthenticationForm.clean_username() checks credentials
         │      └─ Session created
         │
         └─── New User (Register):
             └─ RegisterView renders registration form
             └─ UserRegistrationForm validates email, passwords, role
             └─ User.save() creates new record in auth_user table
             └─ auth_login() creates session
         │
         ▼
Redirect to screen1
         │
         ├─ @login_required checks session
         └─ pages/views.py calls render() with role context
             │
             ▼
         HTML rendered with role-specific partials
         (screen1.html includes s1_{role}.html)
             │
             ▼
         User views Screen 1 content
         (Can navigate to Screen 2, 3, or logout)
```

### User Journey by Role Type

**Step 1: Welcome**
- User lands on `welcome.html`
- Selects their role (University/Company/Investor)
- Redirected to login with `?type={role}` parameter

**Step 2: Authentication**
- If existing user: Logs in with email/password
- If new user: Registers with email/password/role
- Session created; user authenticated

**Step 3: Screen Navigation**
- Redirected to Screen 1 (after login/register)
- User sees role-specific content from partials
- Can navigate between Screen 1, 2, 3
- Sessions maintained across requests
- Display name shown in header
- Logout available at any time

---

## 🗄️ Database Schema (Key Tables)

### `auth_user` (PostgreSQL)
- Stores all user accounts
- **Fields**:
  - `id` (PK)
  - `email` (UNIQUE) - Login credential
  - `password` (hashed)
  - `username` - Auto-populated from email
  - `user_type` - university, company, investor
  - `first_name`, `last_name`
  - `is_active`, `is_staff`, `is_superuser`
  - `date_joined`, `last_login`

### `django_session`
- Stores session data for authentication persistence
- Automatically managed by Django

---

## 🚀 Deployment & Environment Configuration

### Development Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env` with database credentials
5. Run migrations: `python manage.py migrate`
6. Start server: `python manage.py runserver`
7. Access at: `http://localhost:8000`

### Production Deployment
1. Set `DJANGO_DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with domain names
3. Use production WSGI server (e.g., Gunicorn)
4. Use permanent database (PostgreSQL on cloud/server)
5. Collect static files: `python manage.py collectstatic`

---

## 📊 File Interaction Map

| File | Reads From | Writes To | Triggers |
|------|-----------|-----------|----------|
| `manage.py` | - | - | All other operations |
| `settings.py` | `.env` | - | Returns config to Django |
| `.env` | - | `settings.py` | Used at startup |
| `bootstrap_discovery_hub.py` | `requirements.txt` | Project structure | One-time setup |
| `pack_dir_to_xml.py` | Source code | XML output | Manual XML generation |
| `discovery_hub/urls.py` | - | Route matching | Directs to apps |
| `accounts/models.py` | - | PostgreSQL | User storage |
| `accounts/forms.py` | `accounts/models.py` | Form validation | Used by views |
| `accounts/views.py` | Forms, Models | Session, Templates | Authentication logic |
| `pages/views.py` | Session (request.user) | Templates | Screen rendering |
| `templates/*.html` | Context data | Browser HTML | User interface |

---

## 🔐 Security Features

1. **Custom User Model**: Email-based login prevents username enumeration
2. **Password Hashing**: Django's PBKDF2 hashing for all passwords
3. **CSRF Protection**: Middleware prevents cross-site request forgery
4. **Session Security**: Secure session cookies for authenticated users
5. **Environment Variables**: Credentials stored in `.env`, not in code
6. **Login Required**: `@login_required` decorator protects screens
7. **Encrypted Remote DB**: PostgreSQL connection to secure host

---

## 🐛 Common Development Tasks

### Create a New User
```bash
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_user(email='user@example.com', password='SecurePass123!', user_type='company')
```

### Access Django Admin
- URL: `http://localhost:8000/admin/`
- Login with superuser credentials (email: `admin_disco@drew.edu`)

### Run Migrations
```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply to database
```

### View Database Content
```bash
python manage.py dbshell
SELECT * FROM auth_user;
```

### Generate Project XML Backup
```bash
python pack_dir_to_xml.py . discovery_backup.xml
```

---

## 📝 Summary

Discovery Hub is a well-structured Django application that implements:
- **Custom Authentication**: Email-based multi-role user system
- **Progressive UI**: Three screens with role-specific content via partials
- **Scalable Architecture**: Modular apps (accounts, pages) for clean separation
- **Database Integration**: PostgreSQL backend for persistence
- **Security**: Environment-based configuration and session management
- **Development Tools**: Bootstrap script for setup and XML packer for distribution

The application facilitates role-based matchmaking between Universities, Companies, and Investors through a user-friendly web interface.
