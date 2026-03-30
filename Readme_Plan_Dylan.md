# Plan: Admin Portal + Data Models

**TL;DR:** Implement an admin portal (or enhanced admin tabs) to manage users, company/university/patent data, and system settings; align with the current Django accounts/pages structure and use existing admin role shortcuts.

## Steps

1. Flesh out requirements and finalized user story + acceptance criteria.
2. Add new models for Company, University, Patent, SystemSetting in `pages/models.py` (or a new `core` app).
3. Add migration files.
4. Register models in `pages/admin.py` with list display/search/filter and inline display as needed.
5. Add view-level admin pages (new `pages/views.py` functions plus templates) protected by superuser checks.
6. Update `pages/urls.py` and `discovery_hub/urls.py`.
7. Add feature tests in `pages/tests.py` and `accounts/tests.py`.
8. Add doc/README entry.

## Verification

- `python manage.py makemigrations` + `migrate` success
- `python manage.py test` pass
- manual superuser test in browser.

## Decisions

- Use Django admin for core model CRUD; add custom pages for complete story.
- Support role checks via `request.user.is_superuser`.
