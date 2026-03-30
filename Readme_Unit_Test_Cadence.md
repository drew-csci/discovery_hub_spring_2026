# Unit Test Guide - Cadence

## Purpose
This document explains how the current unit tests work for the invention disclosure feature.

The tests live in pages/tests.py and verify three major areas:
- Form validation behavior
- Submission workflow behavior
- Email and pipeline side effects

## Test File Structure
The test file is organized into two test classes:

1. InventionDisclosureFormTests
- Tests validation logic in InventionDisclosureForm.
- These are fast unit-level tests that instantiate the form directly.

2. DisclosureSubmissionFlowTests
- Tests the disclosure submission view end-to-end through Django test client.
- Includes auth checks, permissions, database writes, and confirmation email behavior.

## How the Form Tests Work
Class: InventionDisclosureFormTests

### test_invalid_when_required_fields_missing
- Creates a form with empty data.
- Calls form.is_valid().
- Asserts validation fails.
- Asserts required field errors include title and summary.

What this proves:
- Required fields are enforced before submission.

### test_invalid_when_title_is_fewer_than_ten_characters
- Creates a form with a short title and otherwise valid payload.
- Calls form.is_valid().
- Asserts title has an error with the specific expected message.

What this proves:
- Custom title-length validation is active and user-facing error text is correct.

### test_invalid_when_inventor_name_is_incomplete
- Submits inventors as a single-name entry (for example, "Cher").
- Calls form.is_valid().
- Asserts inventors field has an error.

What this proves:
- Inventor formatting rule (first + last name) is enforced.

### test_invalid_when_summary_and_novelty_match
- Uses the same text for summary and novelty.
- Calls form.is_valid().
- Asserts novelty field has an error.

What this proves:
- Cross-field validation is working and prevents duplicated summary/novelty content.

## How the Submission Flow Tests Work
Class: DisclosureSubmissionFlowTests
Decorator: @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")

Why the decorator matters:
- Email sends are captured in memory (mail.outbox).
- No real emails are sent during tests.
- Tests can assert email count, subject, and recipient behavior safely.

### setUp
Before each flow test:
- Creates a university researcher user.
- Creates a company user.
- Prepares one valid payload used by multiple tests.

What this provides:
- Consistent and isolated fixtures for every test.

### test_login_required
- Performs GET on disclosure_submit without logging in.
- Asserts HTTP 302 redirect.

What this proves:
- The view is protected by login requirements.

### test_only_researchers_can_access_form
- Logs in as company user.
- Performs GET on disclosure_submit.
- Asserts HTTP 403 forbidden.

What this proves:
- Role-based access control is enforced (researchers only).

### test_successful_submission_creates_disclosure_pipeline_card_and_email
- Logs in as researcher.
- POSTs valid payload.
- Asserts redirect after submit.
- Asserts one InventionDisclosure and one PipelineCard were created.
- Asserts the disclosure is linked to the logged-in researcher.
- Asserts pipeline stage defaults to NEW_DISCLOSURE.
- Asserts exactly one email exists in mail.outbox.
- Asserts reference code appears in subject.
- Asserts success message appears in response.

What this proves:
- Happy path is complete: save disclosure, create pipeline card, send confirmation, and show success feedback.

### test_invalid_submission_renders_inline_errors_and_does_not_create_records
- Logs in as researcher.
- POSTs invalid payload (too short summary + invalid inventor format).
- Asserts response returns HTTP 200 (form re-render).
- Asserts inline validation messages are present.
- Asserts no disclosure, no pipeline card, and no email were created.

What this proves:
- Invalid submissions do not persist data and return meaningful inline errors.

## Why These Tests Are Valuable
The suite protects the most important product behaviors:
- Data quality before save
- Access control and authentication
- Business side effects (pipeline card + email)
- User-visible feedback on both success and error paths

## How to Run the Tests
From the project root:

python manage.py test pages.tests

To run a single class:

python manage.py test pages.tests.InventionDisclosureFormTests

python manage.py test pages.tests.DisclosureSubmissionFlowTests

## Practical Reading Tip
When reading a test, use this pattern:
- Arrange: setup data and user state
- Act: submit form or request endpoint
- Assert: check status code, messages, DB records, and email outbox

This makes it easier to map each test directly to acceptance criteria.