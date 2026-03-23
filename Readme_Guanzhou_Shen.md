# Discovery Hub - Project Documentation

## Table of Contents
1. [Project Description](#project-description)
2. [Project Structure Overview](#project-structure-overview)
3. [File Descriptions](#file-descriptions)
4. [How Files Interact](#how-files-interact)
5. [Architecture and Data Flow](#architecture-and-data-flow)

---

## Project Description

**Discovery Hub** is a Django-based web application designed as a multi-role platform connecting three distinct user types: Universities, Companies, and Investors. The application implements role-based access control, allowing each user type to view customized content across three different screens.

### Key Features
- **Custom User Model**: Email-based authentication with role-based user types (University, Company, Investor)
- **PostgreSQL Database**: Remote database connection for data persistence
- **Role-Based Content**: Dynamic template rendering that displays different information based on user role
- **Three-Screen Interface**: Sequential screens with navigation capabilities
- **Responsive Design**: CSS styling for professional presentation

### Technology Stack
- **Framework**: Django 5.x
- **Database**: PostgreSQL
- **Database Driver**: psycopg2-binary
- **Environment Management**: python-dotenv
- **Python Version**: 3.x compatible

---

## Project Structure Overview

```
discovery_hub_spring_2026/
├── Root Configuration Files
│   ├── manage.py
│   ├── bootstrap_discovery_hub.py
│   ├── pack_dir_to_xml.py
│   ├── requirements.txt
│   ├── README.md
│   └── .env
├── discovery_hub/              # Main Django project package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── __pycache__/
├── accounts/                   # Authentication & User Management App
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   └── __pycache__/
├── pages/                      # Main Content & Screen Views App
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   ├── tests.py
│   ├── migrations/
│   └── __pycache__/
├── static/
│   └── css/
│       └── styles.css
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── pages/
│       ├── welcome.html
│       ├── screen1.html
│       ├── screen2.html
│       ├── screen3.html
│       └── partials/
│           ├── s1_company.html
│           ├── s1_investor.html
│           ├── s1_university.html
│           ├── s2_company.html
│           ├── s2_investor.html
│           ├── s2_university.html
│           ├── s3_company.html
│           ├── s3_investor.html
│           └── s3_university.html
└── discovery_output_20260316.xml
```

---

## File Descriptions

### Root-Level Configuration Files

#### `manage.py`
- **Purpose**: Django's command-line utility for administrative tasks
- **Key Responsibilities**:
  - Runs the development server (`python manage.py runserver`)
  - Executes database migrations (`python manage.py makemigrations`, `migrate`)
  - Creates superusers, manages static files, and other admin tasks
- **Technology**: Standard Django utility; no custom modifications

#### `bootstrap_discovery_hub.py`
- **Purpose**: One-time initialization script for project setup
- **Key Responsibilities**:
  - Creates and configures the Python virtual environment
  - Installs Django and required dependencies
  - Generates the Django project structure
  - Creates the `accounts` app with custom user model
  - Creates the `pages` app with base templates and partials
  - Generates CSS styling
  - Outputs setup instructions to the console
- **Usage**: `python bootstrap_discovery_hub.py` (run once during initial setup)
- **Note**: Already executed; do not run again unless resetting the project

#### `pack_dir_to_xml.py`
- **Purpose**: Utility for exporting the entire project directory as an XML file
- **Key Responsibilities**:
  - Recursively scans the project directory
  - Identifies text vs. binary files
  - Encodes text files as readable content; binary files as base64
  - Outputs a combined XML file with all project contents
- **Usage**: `python pack_dir_to_xml.py . combined_files.xml [--include-hidden] [--max-bytes SIZE]`
- **Output**: `discovery_output_20260316.xml` (project snapshot for sharing/archiving)

#### `requirements.txt`
- **Purpose**: Specifies Python package dependencies
- **Contents**:
  - `Django>=5.0,<6.0` - Web framework
  - `psycopg2-binary` - PostgreSQL database adapter
  - `python-dotenv` - Environment variable loader
- **Usage**: `pip install -r requirements.txt` (install all dependencies)

#### `README.md`
- **Purpose**: End-user documentation and setup guide
- **Contents**:
  - Virtual environment setup instructions (Windows, macOS, Linux)
  - Dependency installation steps
  - Environment variable configuration
  - Database connection details
  - Notes on custom user model and role types

#### `.env`
- **Purpose**: Environment variables configuration file (not tracked in version control)
- **Key Variables**:
  - `DJANGO_SECRET_KEY` - Secret key for Django session encryption
  - `DJANGO_DEBUG` - Debug mode toggle (True for development)
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD` - PostgreSQL credentials
  - `DB_HOST`, `DB_PORT` - Remote database server details
  - `ALLOWED_HOSTS` - List of allowed hostnames for the application
- **Security**: Contains sensitive credentials; never commit to version control

### Django Project Configuration (`discovery_hub/`)

#### `discovery_hub/__init__.py`
- **Purpose**: Marks the directory as a Python package
- **Contents**: Typically empty; may contain package initialization code

#### `discovery_hub/settings.py`
- **Purpose**: Central Django configuration file
- **Key Responsibilities**:
  - Loads environment variables from `.env` using `python-dotenv`
  - Configures `INSTALLED_APPS` (includes `accounts`, `pages`, Django built-in apps)
  - Sets up middleware for security, sessions, CSRF protection, and authentication
  - Defines database connection (PostgreSQL with remote host)
  - Configures template engine with template directories
  - Sets up static file handling
  - Configures password validators and authentication backends
- **Critical Settings**:
  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': os.getenv('DB_NAME'),
          'USER': os.getenv('DB_USER'),
          'PASSWORD': os.getenv('DB_PASSWORD'),
          'HOST': os.getenv('DB_HOST'),
          'PORT': os.getenv('DB_PORT'),
      }
  }
  AUTH_USER_MODEL = 'accounts.User'  # Custom user model
  ```

#### `discovery_hub/urls.py`
- **Purpose**: Root URL configuration (routing for the entire application)
- **Key Routes**:
  - `/admin/` → Django admin interface
  - `/accounts/` → Include account-related URLs (login, register, logout)
  - `/` → Include page-related URLs (welcome, screens)
  - `/logout/` → Custom logout view
- **Pattern**: Uses `include()` to delegate routing to app-specific URL configurations

#### `discovery_hub/asgi.py`
- **Purpose**: ASGI (Asynchronous Server Gateway Interface) configuration
- **Use Case**: For production deployment with async-capable servers (e.g., Daphne, Hypercorn)
- **Note**: Less commonly used in development; more for advanced async deployments

#### `discovery_hub/wsgi.py`
- **Purpose**: WSGI (Web Server Gateway Interface) configuration
- **Use Case**: Standard for production deployment with sync servers (e.g., Gunicorn, uWSGI)
- **Note**: Typical entry point for containerized deployments

### Accounts App (`accounts/`)
Handles user authentication, registration, and custom user model management.

#### `accounts/models.py`
- **Purpose**: Defines the database schema for users
- **Key Model: `User`**
  - Extends Django's `AbstractUser` for custom user model
  - **Fields**:
    - `user_type` - CharField with choices: UNIVERSITY, COMPANY, INVESTOR (default: UNIVERSITY)
    - `email` - EmailField with unique constraint (primary login field)
  - **Custom Features**:
    - Uses `email` as the USERNAME_FIELD for login (instead of traditional username)
    - Auto-generates `username` from email if not provided (for admin compatibility)
    - `display_name` property returns user's full name or falls back to email
  - **Database**: Stored in PostgreSQL table `accounts_user`

#### `accounts/views.py`
- **Purpose**: Handles user authentication logic
- **Key Views**:
  - `CustomLoginView` - Class-based view for email-based login
    - Accepts email and password
    - Redirects authenticated users to welcome page
  - `RegisterView` - Class-based view for user registration
    - Allows new users to create accounts
    - Includes user_type selection during registration
    - Form validation for email uniqueness and password strength

#### `accounts/urls.py`
- **Purpose**: URL routing for account-related endpoints
- **Routes**:
  - `/accounts/login/` → CustomLoginView (GET: show form, POST: validate credentials)
  - `/accounts/register/` → RegisterView (GET: show form, POST: create user)
  - `/accounts/logout/` → Django's LogoutView (clears session, redirects to welcome)

#### `accounts/forms.py`
- **Purpose**: Django forms for login and registration
- **Likely Forms**:
  - Custom login form with email field instead of username
  - Registration form with email, password, and user_type selection
  - Form validation and error handling

#### `accounts/admin.py`
- **Purpose**: Registers models with Django admin interface
- **Functionality**: Allows superusers to manage users via `/admin/`
  - View, create, edit, delete users
  - Filter by user_type
  - Bulk actions

#### `accounts/apps.py`
- **Purpose**: App configuration class
- **Contains**: App name, label, and verbose name metadata

#### `accounts/tests.py`
- **Purpose**: Unit tests for the accounts app
- **Typical Tests**: User creation, login validation, form validation

#### `accounts/migrations/`
- **Purpose**: Database schema versioning and migration history
- **Files**:
  - `0001_initial.py` - Initial migration creating the User model and related tables
  - `__init__.py` - Marks the directory as a Python package
- **Auto-generated**: May expand as the model evolves (fields added, removed, modified)

### Pages App (`pages/`)
Handles the main content pages and role-based screen rendering.

#### `pages/models.py`
- **Purpose**: Database models for pages
- **Current State**: Empty (no custom models defined yet)
- **Future Use**: May contain models for storing dynamic content, user preferences, or screen data

#### `pages/views.py`
- **Purpose**: Handles rendering of the main screens and welcome page
- **Views**:
  - `welcome(request)` - Public view, no login required
    - Renders `pages/welcome.html`
    - Entry point to the application
  - `screen1(request)` - Login required (@login_required decorator)
    - Extracts user's role from `request.user.user_type`
    - Passes `role` to template for conditional content rendering
    - Renders `pages/screen1.html`
  - `screen2(request)` - Login required
    - Same functionality as screen1 with different template
    - Renders `pages/screen2.html`
  - `screen3(request)` - Login required
    - Same functionality as screen1 with different template
    - Renders `pages/screen3.html`
- **Key Logic**: Uses `@login_required` to enforce authentication; extracts role for template context

#### `pages/urls.py`
- **Purpose**: URL routing for page views
- **Routes**:
  - `/` → `welcome` view (name: 'welcome')
  - `/screen1/` → `screen1` view (name: 'screen1')
  - `/screen2/` → `screen2` view (name: 'screen2')
  - `/screen3/` → `screen3` view (name: 'screen3')
- **Pattern**: Simple direct routing to view functions

#### `pages/admin.py`
- **Purpose**: Admin interface configuration for pages app
- **Current State**: Likely empty (no custom models to register)

#### `pages/apps.py`
- **Purpose**: App configuration class for pages app

#### `pages/tests.py`
- **Purpose**: Unit tests for pages app
- **Typical Tests**: View access control, template rendering, role-based content

#### `pages/migrations/`
- **Purpose**: Migration history for pages app models
- **Current State**: Only `__init__.py` since no models exist yet

### Template Files (`templates/`)
HTML files rendered by views using Django's template engine.

#### `templates/base.html`
- **Purpose**: Base template providing common layout and structure
- **Contains**:
  - HTML document structure
  - Common header/navigation
  - CSS stylesheet links
  - `{% block content %}` for child templates
  - Common footer or scripts
- **Inheritance**: All other templates extend base.html using `{% extends "base.html" %}`

#### `templates/accounts/login.html`
- **Purpose**: Login form page
- **Contains**:
  - Email input field
  - Password input field
  - Submit button
  - Link to registration page
  - Error messages for invalid credentials

#### `templates/accounts/register.html`
- **Purpose**: User registration form page
- **Contains**:
  - Email input field
  - Password input fields (password and confirmation)
  - User type selector (dropdown or radio buttons for University, Company, Investor)
  - Submit button
  - Link to login page
  - Form validation error messages

#### `templates/pages/welcome.html`
- **Purpose**: Landing/welcome page (public, no login required)
- **Contains**:
  - Welcome message
  - Buttons for Login and Register
  - Project introduction or call-to-action

#### `templates/pages/screen1.html`, `screen2.html`, `screen3.html`
- **Purpose**: Main application screens (login required)
- **Common Structure**:
  - Extends `base.html`
  - Displays screen title with role: `<h1>Screen 1 {{ role }}</h1>`
  - Personalized greeting: `Hello {{ request.user.display_name }} ({{ role }})`
  - Conditional inclusion of role-specific partial template
  - Navigation buttons to other screens
- **Conditional Logic**:
  ```django
  {% if request.user.user_type == 'university' %}
      {% include "pages/partials/s1_university.html" %}
  {% elif request.user.user_type == 'company' %}
      {% include "pages/partials/s1_company.html" %}
  {% elif request.user.user_type == 'investor' %}
      {% include "pages/partials/s1_investor.html" %}
  {% endif %}
  ```

#### `templates/pages/partials/s*_*.html` (9 files total)
- **Purpose**: Reusable template fragments for role-specific content
- **Naming Convention**: `s[screen_number]_[role].html`
  - `s1_university.html`, `s1_company.html`, `s1_investor.html` - Screen 1 content by role
  - `s2_university.html`, `s2_company.html`, `s2_investor.html` - Screen 2 content by role
  - `s3_university.html`, `s3_company.html`, `s3_investor.html` - Screen 3 content by role
- **Contents**: Role-specific information, forms, or data displays
- **Usage**: Included via `{% include %}` tag in main screen templates

### Static Files (`static/`)

#### `static/css/styles.css`
- **Purpose**: Centralized styling for the application
- **Contains**:
  - CSS rules for layout, colors, fonts, spacing
  - Styling for dashboard cards (`.dash-card`)
  - Button styling (`.btn`, `.button-row`)
  - Responsive design rules
  - Component-specific styles (forms, navigation, etc.)
- **Served**: Django serves this automatically in development; in production, collected via `python manage.py collectstatic`

### Miscellaneous Files

#### `discovery_output_20260316.xml`
- **Purpose**: Project snapshot/export generated by `pack_dir_to_xml.py`
- **Contents**: XML structure with base64-encoded file contents
- **Use Cases**: Project archiving, sharing with others, backup
- **Note**: Auto-generated; should not be edited manually

---

## How Files Interact

### User Registration and Login Flow

```
1. User visits http://localhost:8000/
   ↓
2. Views welcome.html (public)
   ↓
3. User clicks "Register" or "Login"
   ↓
4. Request routed via discovery_hub/urls.py → accounts/urls.py
   ↓
5. accounts/views.py handles request:
   - RegisterView: Validates form using accounts/forms.py, creates User via accounts/models.py
   - CustomLoginView: Authenticates against User model
   ↓
6. User model saved to PostgreSQL (configured in discovery_hub/settings.py)
   ↓
7. Authenticated user redirected to screen1/welcome
```

### Screen Navigation Flow

```
1. Logged-in user at http://localhost:8000/screen1/
   ↓
2. Request routed via discovery_hub/urls.py → pages/urls.py
   ↓
3. pages/views.py checks @login_required:
   - If not logged in: redirect to login
   - If logged in: extract user.user_type
   ↓
4. Render pages/screen1.html with parameters:
   - role = user.user_type.title()
   - request.user for template context
   ↓
5. templates/pages/screen1.html:
   - Extends base.html (templates/base.html)
   - Includes CSS from static/css/styles.css
   - Conditionally includes partial based on user_type:
     templates/pages/partials/s1_[role].html
   ↓
6. Rendered HTML returned to user's browser
```

### Database Interaction

```
All user data:
  ↓
- Created via accounts/views.py (RegisterView)
- Stored in PostgreSQL (connection string from .env → settings.py)
- Retrieved for login via accounts/models.py (User model)
- Accessed in templates via request.user
  ↓
Schema managed by migrations:
  - accounts/migrations/0001_initial.py creates User table on first run
  - Run via: python manage.py migrate
```

### Configuration and Dependency Injection

```
Server Startup (python manage.py runserver):
  ↓
1. manage.py locates discovery_hub/settings.py
   ↓
2. settings.py loads environment variables from .env:
   - Database credentials (DB_NAME, DB_USER, etc.)
   - Secret key for encryption
   - Debug mode
   - Allowed hosts
   ↓
3. settings.py configured with app list:
   - Registers 'accounts' and 'pages' apps
   - Enables default Django apps (admin, auth, etc.)
   ↓
4. Server starts on http://localhost:8000/ with:
   - Template loader configured to templates/ directory
   - Static files configured to static/ directory
   - Database pointed to remote PostgreSQL
   ↓
5. Django's URL dispatcher ready to route requests:
   - discovery_hub/urls.py → app-specific urls
   - accounts/urls.py and pages/urls.py
```

### Template Rendering with Context

```
When screen1 view executes:
  ↓
1. pages/views.py extracts request.user (from accounts/models.py)
2. Computes role = request.user.user_type.title()
3. Renders pages/screen1.html with context:
   {
       'role': 'University',
       'request': request,  # includes user and CSRF token
   }
   ↓
4. Django template engine processes screen1.html:
   - {% extends "base.html" %} → Loads base.html
   - base.html includes static/css/styles.css
   - {% include "pages/partials/s1_university.html" %} → Includes role-specific content
   - {{ role }} → Renders 'University'
   - {{ request.user.display_name }} → Renders computed property from User model
   ↓
5. Final HTML served to browser with full layout, styling, and content
```

---

## Architecture and Data Flow

### High-Level Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ HTTP Request
         ↓
┌─────────────────────────────────────┐
│    Django Application (manage.py)    │
├─────────────────────────────────────┤
│  discovery_hub/               │ Root config
│  ├── settings.py              │ Database, apps, middleware
│  ├── urls.py                  │ URL routing
│  └── wsgi.py/asgi.py          │ Server gateway
├─────────────────────────────────────┤
│  App Layer                           │
│  ├── accounts/                │ Auth & users
│  │   ├── models.py            │ User model
│  │   ├── views.py             │ Login/Register
│  │   └── urls.py              │ /accounts/* routes
│  └── pages/                   │ Main content
│      ├── views.py             │ Screen views
│      └── urls.py              │ /screen* routes
├─────────────────────────────────────┤
│  Template Layer                      │
│  ├── templates/               │ HTML rendering
│  └── static/css/              │ Styling
├─────────────────────────────────────┤
│  Environment Config                  │
│  ├── .env                     │ Secrets & config
│  └── requirements.txt         │ Dependencies
└─────────────────────────────────────┘
         ↓ DB queries
┌───────────────────────────────────┐
│  PostgreSQL Database (Remote)     │
│  - accounts_user table            │
│  - Session/cache tables           │
└───────────────────────────────────┘
```

### Request Lifecycle

```
1. Request received by Django
2. Django middleware processes request (security, sessions, CSRF)
3. URL dispatcher (discovery_hub/urls.py) matches route
4. App-specific URL router invoked (accounts/urls.py or pages/urls.py)
5. View function/class executed:
   - Accesses database via models (accounts/models.py)
   - Checks authentication via @login_required
   - Computes context data
6. Template rendered with context:
   - Extends base.html
   - Includes static assets (css/styles.css)
   - Conditionally includes partials
   - Injects dynamic data
7. HTML response sent to browser
8. Browser renders page, user sees UI
```

### Role-Based Content Delivery

```
User Model (accounts/models.py)
  ↓ Contains user_type field
  ↓
Authentication (accounts/views.py)
  ↓ User logs in with email/password
  ↓ request.user.user_type set
  ↓
View Processing (pages/views.py)
  ↓ Extracts user_type → role variable
  ↓ Passes to template context
  ↓
Template Rendering (pages/screen*.html)
  ↓ {% if request.user.user_type == 'university' %}
  ↓ {% include "pages/partials/s*_[role].html" %}
  ↓
Role-Specific Content (partials/s*_*.html)
  ↓ Displayed to user
```

---

## Key Interaction Points Summary

| Interaction | Files Involved | Description |
|---|---|---|
| **Startup** | manage.py → settings.py → .env | Django loads config, connects to database, mounts apps |
| **User Registration** | forms.py → views.py → models.py → PostgreSQL | User submits form, validated, saved to database |
| **User Login** | forms.py → CustomLoginView → models.py → Session | User authenticated, session created |
| **Page Request** | urls.py → views.py → models.py | View extracts user data, renders template |
| **Template Rendering** | views.py → screen*.html → base.html → styles.css | Template engine combines layout, styling, content, and role-specific partials |
| **Static Files** | Django settings → static/ → CSS | CSS served to browser for page styling |
| **Data Persistence** | models.py → ORM → PostgreSQL | User data and session data stored and retrieved |

---

**Document Created**: March 22, 2026  
**Project**: Discovery Hub (Spring 2026)  
**Author**: Guanzhou Shen

