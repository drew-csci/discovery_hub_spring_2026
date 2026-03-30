# Integration Test Guide - Cadence

## Purpose
This document explains how the integration tests work for the invention disclosure submission flow.

Integration tests verify that multiple app layers work together in one request cycle:
- URL routing
- View permissions and request handling
- Form validation outcomes
- Database writes
- Email side effects
- User-facing response messages

## Where Integration Tests Live
The integration tests are in:
- pages/tests.py

The integration-focused class is:
- DisclosureSubmissionFlowTests

## Test Setup Strategy
DisclosureSubmissionFlowTests uses two important setup mechanisms:

1. Test fixture setup in setUp()
- Creates a valid researcher user (university role)
- Creates a non-researcher user (company role)
- Defines a valid disclosure payload used across tests

2. In-memory email backend
- Applied with @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
- Prevents real emails from being sent
- Stores sent emails in django.core.mail.outbox for assertions

Why this is important:
- Every test starts from a known state.
- Tests can safely verify email behavior without external dependencies.

## How Each Integration Test Works

### 1) test_login_required
What it does:
- Sends a GET request to the disclosure submission route without logging in.

What it checks:
- Response status is 302 (redirect to login).

Why it matters:
- Verifies the route is protected by authentication.

### 2) test_only_researchers_can_access_form
What it does:
- Logs in as a company user.
- Sends a GET request to disclosure submission.

What it checks:
- Response status is 403 Forbidden.

Why it matters:
- Verifies role-based access control is enforced.

### 3) test_successful_submission_creates_disclosure_pipeline_card_and_email
What it does:
- Logs in as researcher.
- POSTs valid disclosure payload.
- Follows redirect.

What it checks:
- Redirect happens after submit.
- Exactly one InventionDisclosure is created.
- Exactly one PipelineCard is created.
- Pipeline card is linked to the created disclosure.
- Pipeline stage defaults to NEW_DISCLOSURE.
- One confirmation email is captured.
- Email subject includes disclosure reference code.
- Success message is visible in response content.

Why it matters:
- Confirms complete happy path from request to side effects.

### 4) test_refresh_after_successful_submit_does_not_create_duplicate_pipeline_card
What it does:
- Logs in as researcher.
- Submits valid POST once.
- Performs a follow-up GET (simulating refresh after redirect).

What it checks:
- Response is valid after refresh.
- Disclosure count remains 1.
- PipelineCard count remains 1.
- The same pipeline card linkage still exists.

Why it matters:
- Verifies Post/Redirect/Get behavior does not duplicate records on refresh.

### 5) test_invalid_submission_renders_inline_errors_and_does_not_create_records
What it does:
- Logs in as researcher.
- Posts invalid payload (short summary + incomplete inventor name).

What it checks:
- Status is 200 (form re-render, not redirect).
- Inline error messages are present.
- No InventionDisclosure is created.
- No PipelineCard is created.
- No email is sent.

Why it matters:
- Confirms bad input is blocked and reported to the user without side effects.

## Request Flow Covered by These Tests
The current integration suite covers this lifecycle:

1. User access to disclosure route
2. Auth check
3. Role authorization
4. Form POST handling
5. Save disclosure record
6. Auto-create linked pipeline card
7. Send confirmation email
8. Return success or validation errors to UI

## Running Integration Tests
Run only the integration class:

python manage.py test pages.tests.DisclosureSubmissionFlowTests

Run all tests in pages app:

python manage.py test pages.tests

## Reading Integration Tests Quickly
Use this pattern for each method:
- Arrange: login state + payload
- Act: GET or POST request through Django test client
- Assert: status code, DB state, email outbox, and response text

This pattern makes it easy to confirm each acceptance criterion is exercised across real app layers.

## Suggested Next Integration Tests
If you want broader coverage later, add:
- Email failure path returns warning message but still saves disclosure
- CSRF rejection path
- Access verification for investor role
- End-to-end reference code format assertion across DB + UI + email
