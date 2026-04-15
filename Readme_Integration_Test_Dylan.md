# Integration Test Explanation: Admin Dashboard Flow

This document explains the integration test for superuser workflow through the protected admin dashboard.

## Location
- File: `pages/tests.py`
- Test method: `test_superuser_workflow_protected_admin_dashboard`

## Purpose
Verify that authentication and authorization work end-to-end for the superuser path, and that the admin dashboard shows correct aggregated data.

## Setup
`setUp()` creates:
- Superuser: `admin@test.com` (password `adminpass`)
- Regular user: `user@test.com`
- `Company` record
- `University` record
- `Patent` record
- `SystemSetting` record

## Test steps
1. Submit login form to `/accounts/login/` via `POST reverse('login')` with superuser credentials.
   - This simulates the real login flow and sets session cookie.
2. Assert login response has `status_code == 200` and user in response context is superuser.
3. GET `/admin-dashboard/` using the same client session.
4. Assert response code `200` (success for superuser).

## Assertions
- `Total users:` is present in response body.
- `Companies: 1` is present in response body.
- `Universities: 1` is present in response body.
- `Patents: 1` is present in response body.

## Why this is useful
- Confirms the auth cookie/session is persisted between login and dashboard request.
- Confirms UIs are rendered for a superuser.
- Confirms database values are shown in the admin dashboard metrics.

## Run
`./venv/bin/python manage.py test pages`
