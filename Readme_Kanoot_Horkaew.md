# Discovery Hub Django App

## Project Description

Discovery Hub is a Django-based web application designed to facilitate connections between universities, companies, and investors. The app implements role-based authentication with three user types: University, Company, and Investor. Users can log in with their email and access role-specific dashboards and profiles. The application uses PostgreSQL for data storage and includes features like user registration, password reset, and an admin panel for management.

Key features include:
- Custom user model with email-based authentication
- Role-specific screens and profiles
- Bootstrap-styled templates for responsive design
- Environment variable configuration for security
- Automated setup via bootstrap script

The app is built with Django 5.x and follows standard Django project structure with separate apps for accounts (authentication) and pages (views).

## Project Structure

### Root-Level Files

- **manage.py**: Django's command-line utility for managing the project. Used to run migrations, start the development server, create superusers, and perform other administrative tasks.
- **requirements.txt**: Lists all Python dependencies required for the project. Install via `pip install -r requirements.txt`.
- **.env**: Environment configuration file containing sensitive settings like database credentials, secret keys, and debug mode. Loaded automatically by Django settings.
- **README.md**: Main project documentation with setup instructions, demo accounts, and usage notes.
- **bootstrap_discovery_hub.py**: Python script that sets up the entire project structure, including creating apps, templates, static files, and running initial migrations.
- **pack_dir_to_xml.py**: Utility script to convert the project directory structure into an XML file for packaging or analysis.
- **.gitignore**: Specifies files and directories to exclude from Git version control (e.g., virtual environments, cache files).
- **sample.txt**, **brenda_madrid.txt**, **David_Kvinikadze.txt**, **EmailerLogin.txt**, **Julia_Kolenda.txt**, **Paul_Greenleaf.txt**: Sample data files or contributor notes, not directly part of the Django application logic.
- **ReadMe_Adit.md**, **Readme_David.md**, **Readme_Julia.md**, **Readme_PaulGreenleaf.md**: Additional documentation or notes from project contributors.

### discovery_hub/ (Main Django Project Directory)

This directory contains the core Django project configuration.

- **settings.py**: Main configuration file defining installed apps, database settings, authentication backends, static/media file handling, and other Django settings.
- **urls.py**: Root URL configuration that routes incoming requests to appropriate views in the apps.
- **asgi.py**: ASGI configuration for asynchronous web servers.
- **wsgi.py**: WSGI configuration for traditional web servers.
- **__init__.py**: Marks the directory as a Python package.
- **__pycache__/**: Directory containing compiled Python bytecode files (auto-generated).

### accounts/ (Django App for User Management)

Handles user authentication, registration, and profile management.

- **models.py**: Defines the custom User model extending Django's AbstractUser, with additional fields like user_type for role-based access.
- **views.py**: Contains class-based views for login, registration, logout, and password reset functionality.
- **forms.py**: Custom forms for user registration and email-based authentication.
- **admin.py**: Configuration for Django admin interface, customizing how User models are displayed and managed.
- **urls.py**: URL patterns for authentication-related pages.
- **apps.py**: App configuration class.
- **migrations/**: Database migration files that track changes to the database schema.
- **__init__.py**: Package marker.
- **__pycache__/**: Compiled bytecode.

### pages/ (Django App for Page Views)

Manages the main application pages and user interfaces.

- **views.py**: Views for welcome page, role-specific screens, and profile pages.
- **urls.py**: URL patterns for page routing.
- **models.py**: Currently empty, but can be extended for page-specific data models.
- **admin.py**: Admin configuration (currently minimal).
- **apps.py**: App configuration.
- **tests.py**: Unit tests for the pages app.
- **__init__.py**: Package marker.
- **__pycache__/**: Compiled bytecode.

### static/ (Static Files)

Contains static assets served by Django.

- **css/styles.css**: Main stylesheet defining the visual appearance of the application.

### templates/ (HTML Templates)

Contains Django templates for rendering HTML pages.

- **base.html**: Base template with common layout elements like header, navigation, and footer.
- **welcome.html**: Public welcome page with role selection.
- **accounts/login.html**, **accounts/register.html**, **accounts/password_reset_*.html**: Authentication-related templates.
- **pages/screen1.html**, **pages/screen2.html**, **pages/screen3.html**: Role-specific dashboard screens.
- **pages/company_home.html**, **pages/company_profile.html**, etc.: Templates for different user roles and pages.
- **pages/partials/**: Reusable template fragments for different screens and roles.

### tests/ (Global Test Directory)

Contains test files for the project.

- **__init__.py**: Package marker.
- **email_test.py**, **test_company_home.py**, etc.: Individual test files for various components.

## How Files Interact

### Request Flow
1. A user accesses the application (e.g., http://127.0.0.1:8000/).
2. The request is routed through **discovery_hub/urls.py**, which delegates to app-specific URL configurations.
3. For authentication, **accounts/urls.py** and **accounts/views.py** handle login/registration, validating against the custom User model in **accounts/models.py**.
4. Successful authentication redirects to role-specific pages managed by **pages/urls.py** and **pages/views.py**.
5. Templates in **templates/** are rendered with data from views, using **base.html** for consistent layout.
6. Static files like **static/css/styles.css** are served to style the pages.

### Data Flow
- User data is stored in PostgreSQL, configured via **discovery_hub/settings.py** and environment variables in **.env**.
- Database schema changes are tracked via migrations in **accounts/migrations/**.
- The custom user model in **accounts/models.py** integrates with Django's authentication system.

### Development Workflow
- **bootstrap_discovery_hub.py** initializes the project structure and runs initial setup.
- **manage.py** is used for all Django management commands.
- **requirements.txt** ensures consistent dependency installation.
- Tests in **tests/** validate functionality.

### Security and Configuration
- Sensitive data is stored in **.env** and loaded by **discovery_hub/settings.py**.
- Role-based access is enforced in views by checking the user_type field from **accounts/models.py**.
- Admin functionality is provided through Django's admin interface, configured in **accounts/admin.py**.

The application follows Django's MTV (Model-Template-View) architecture, with clear separation of concerns between apps and reusable components.