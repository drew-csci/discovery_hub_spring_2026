# Unit Test Explanation: Admin Dashboard

This document explains how the new unit tests for the admin dashboard work.

## Location
- File: `pages/tests.py`
- Class: `PageModelAndAdminDashboardTests`

## Tests added

### `test_admin_dashboard_redirects_non_superuser`
1. Log in as a normal non-superuser: `user@test.com`.
2. Request `reverse('admin_dashboard')` (i.e. `/admin-dashboard/`).
3. Expect response status `302` (redirect), since ordinary users cannot access this admin-only page.

### `test_admin_dashboard_shows_counts_for_superuser`
1. Log in as superuser: `admin@test.com`.
2. Request `reverse('admin_dashboard')`.
3. Expect response status `200`.
4. Assert page contains key UI text:
   - `Total users:`
   - `Companies: 1`
   - `Universities: 1`
   - `Patents: 1`
5. These checks verify that the view returns aggregated counts from the model data seeded in `setUp()`.

### `test_admin_dashboard_uses_correct_template`
1. Log in as superuser.
2. GET the admin dashboard.
3. Assert `response.template_name` includes `pages/admin_dashboard.html`.

## Data setup in `setUp()`
- Creates a superuser and a regular user.
- Creates `Company`, `University`, `Patent`, and `SystemSetting` objects.

## How to run
`./venv/bin/python manage.py test pages`
