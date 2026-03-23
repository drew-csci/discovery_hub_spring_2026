# Discovery Hub - Setup & Running Guide

## Project Description

Discovery Hub is a Flask-based web application designed to help biopharma business development professionals, technology transfer offices (TTOs), and academic innovation teams discover, evaluate, and act on licensing and partnering opportunities. The platform consolidates multiple functionalities into a single, workflow-native environment, supporting three main user types: Universities, Companies, and Investors.

---

## Quick Start (5 Steps)

### Step 1: Activate Virtual Environment
```bash
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### Step 2: Install / Update Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials

```

### Step 4: Set Up Database
```bash
# Create database (if needed)
createdb discovery_hub

# Apply migrations
flask db upgrade
```

### Step 5: Run the Server
```bash
flask run
```

Visit: **http://localhost:5000**

---

## Detailed Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL (running locally or remote)
- pip and virtualenv

### Step 1: Create & Activate Virtual Environment

```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### Step 2: Install Dependencies

Create `requirements.txt` in project root with:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-Migrate==4.0.5
WTForms==3.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
email-validator==2.1.0
Werkzeug==3.0.1
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration

1. Copy template:
```bash
cp .env.example .env
```

2. Edit `.env` file with your settings:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

DATABASE_URL=postgresql://username:password@localhost:5432/discovery_hub

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Replace `username:password` with your PostgreSQL credentials.**

### Step 4: PostgreSQL Setup

1. **Start PostgreSQL:**
```bash
# macOS with Homebrew
brew services start postgresql

# Verify it's running
pg_isready
```

2. **Create database:**
```bash
createdb discovery_hub
```

3. **Initialize migrations:**
```bash
flask db init        # Create migrations folder
flask db migrate -m "Initial migration"
flask db upgrade     # Apply to database
```

### Step 5: Run Development Server

```bash
flask run
```

Expected output:
```
 * Serving Flask app 'app.py'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

---

## Using the Application

### Test URLs After Starting Server

| URL | Purpose |
|-----|---------|
| http://localhost:5000/ | Homepage |
| http://localhost:5000/accounts/register | Create account |
| http://localhost:5000/accounts/login | Login |
| http://localhost:5000/dashboard | Dashboard (requires login) |
| http://localhost:5000/accounts/logout | Logout |
| http://localhost:5000/accounts/password_reset | Forgot password |

### Try It Out

1. **Register**: Go to `/accounts/register`, fill form, submit
2. **Auto-login**: You'll be logged in automatically
3. **Dashboard**: See your user dashboard
4. **Logout**: Click logout to test login again

---

## Common Commands

### Flask Commands
```bash
# Run development server (http://localhost:5000)
flask run

# Run on different port
flask run --port 5001

# Interactive Python shell with database access
flask shell

# View all routes
flask routes
```

### Database Commands
```bash
# Check migration status
flask db current

# View all migrations
flask db history

# Create migration after model changes
flask db migrate -m "Description of change"

# Apply migrations
flask db upgrade

# Undo last migration
flask db downgrade
```

### Testing
```bash
# Run tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_accounts.py
```

### Database Access
```bash
flask shell
>>> from accounts.models import User
>>> users = User.query.all()
>>> user = User.query.filter_by(email='test@example.com').first()
>>> print(user.display_name)
>>> exit()
```

---

## Troubleshooting

### "No module named 'flask'"
```bash
# Verify venv is activated (should see (venv) in prompt)
source venv/bin/activate

# Install dependencies again
pip install -r requirements.txt
```

### "could not translate host name 'localhost'"
PostgreSQL not running:
```bash
brew services start postgresql    # Start it
pg_isready                        # Verify
```

### "database 'discovery_hub' does not exist"
```bash
createdb discovery_hub
```

### "No such table: users"
Migrations not applied:
```bash
flask db upgrade
```

### Port 5000 in use
```bash
flask run --port 5001
```

### "ImportError: cannot import name 'db'"
Check that `extensions.py` exists in project root and is not corrupted.

### Changes to models not in database
After editing `models.py`:
```bash
flask db migrate -m "Description"
flask db upgrade
```

---

## Project Structure

```
f25_discovery/
├── app.py                 ← Start here: Flask application factory
├── config.py              ← Configuration settings
├── extensions.py          ← Database setup
├── wsgi.py                ← Production entry point
├── requirements.txt       ← Python dependencies
├── .env                   ← Environment variables (keep secret!)
├── .env.example           ← Template for .env
│
├── accounts/              ← User auth & profiles
│   ├── __init__.py
│   ├── models.py          ← User, TTOProfile
│   ├── views.py           ← Routes
│   ├── forms.py           ← Forms
│   └── urls.py
│
├── pages/                 ← Pages & dashboards
│   ├── __init__.py
│   ├── models.py
│   ├── views.py           ← Routes
│   └── urls.py
│
├── templates/             ← HTML (Jinja2)
│   ├── base.html
│   ├── accounts/
│   └── pages/
│
├── static/                ← CSS, JS, images
├── migrations/            ← Database migrations
├── tests/                 ← Test suite
└── .git/                  ← Version control
```

---

## Key Files Explained

### `app.py`
Creates Flask app, initializes database, registers blueprints, sets up error handling.

### `config.py`
Development, Testing, Production configurations. Database URL, secret key, email settings.

### `extensions.py`
Initializes Flask extensions (SQLAlchemy, Flask-Login, Flask-Migrate).

### `accounts/models.py`
- **User**: Email login, password hashing, multiple user types (university, company, investor)
- **TTOProfile**: Optional profile for university users

### `accounts/forms.py`
Registration, login, password reset forms with WTForms validation.

### `accounts/views.py`
Routes: `/register`, `/login`, `/logout`, `/password_reset`

---

## Architecture

```
Flask App (app.py)
    ├── Accounts Blueprint
    │   ├── User model
    │   ├── Auth forms
    │   └── Routes
    └── Pages Blueprint
        ├── Page model
        └── Routes
```

---

## Next Steps

1. **Create Templates**: Build HTML in `templates/` directory
2. **Add Styling**: CSS/JS in `static/` directory
3. **Configure Email**: Set up SMTP for password reset
4. **Write Tests**: Add tests in `tests/` directory
5. **Deploy**: Use `wsgi.py` with Gunicorn or similar

---

## Support Resources

- Flask docs: https://flask.palletsprojects.com
- SQLAlchemy: https://docs.sqlalchemy.org
- PostgreSQL: https://www.postgresql.org/docs
- Flask-Login: https://flask-login.readthedocs.io

---

**Happy coding! 🚀**

