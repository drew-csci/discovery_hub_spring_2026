# Midterm Update: New Code Added

## Overview
This document lists all the files updated as part of the admin portal and data model feature set, with explanations of what each change does.

## Files Added/Updated

### 1. `pages/models.py`
- Added `Company`, `University`, `Patent`, `SystemSetting` models.
- Each model has fields for name/industry/domain and typical metadata (`created_at`, `updated_at`).
- `Patent` links to `Company` and `University` through optional foreign keys.
- `SystemSetting.get_value(key, default=None)` returns a config value.

### 2. `pages/admin.py`
- Registered models in Django admin.
- Added custom `ModelAdmin` classes for `CompanyAdmin`, `UniversityAdmin`, `PatentAdmin`, `SystemSettingAdmin`.
- Added `list_display`, `search_fields`, `list_filter` for admin usability.

### 3. `pages/views.py`
- Added `admin_dashboard` view restricted to superusers via `@user_passes_test(lambda u: u.is_superuser)`.
- Dashboard aggregates counts for users/companies/universities/patents/settings and renders `pages/admin_dashboard.html`.

### 4. `pages/urls.py`
- Added route `path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard')`.

### 5. `templates/pages/admin_dashboard.html`
- New template with stats and links to Django admin sections.
- Displays list of system settings.

### 6. `templates/base.html`
- Added an Admin Dashboard link in the top menu when `user.is_superuser`.

### 7. `pages/tests.py`
- Added tests for:
  - system setting lookup value
  - admin dashboard access control (superuser vs normal user)
  - data model persistence for `Company`, `University`, `Patent`, `SystemSetting`.

### 8. `accounts/tests.py`
- Added tests for creating user and superuser.

### 9. `static/css/styles.css` (reverted)
- Adjusted header/nav spacing (later reverted back to original as requested).

## Behavior implemented
- `admin-dashboard` page is now available to superusers with quick platform stats.
- New persistent domain models exist and can be managed via admin UI.
- Access control ensures only superadmin users can view admin dashboard.
- Through Django admin users can manage companies/universities/patents/system settings.

## Migration notes
- Run `./venv/bin/python manage.py makemigrations` and `migrate` to create tables in DB.
- If migration errors occur (e.g., `is_email_verified` already exists), run `./venv/bin/python manage.py migrate --fake accounts 0003` then `migrate`.

## File content update provenance
Most code was added to implement the admin user story described in `Readme_Plan_Dylan.md`.
