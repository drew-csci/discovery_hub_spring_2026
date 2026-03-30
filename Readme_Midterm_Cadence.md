# Midterm Cadence - Codex Code Summary

This document summarizes the new code currently present on branch Midterm_Cadence that appears to have been generated/assisted by Codex for the invention disclosure submission story.

## What Was Added

### 1) Disclosure data model and pipeline model
Files:
- pages/models.py
- pages/migrations/0001_initial.py

New code adds two core models:
- InventionDisclosure
  - Stores researcher submission data such as title, summary, inventors, department, technology area, novelty, applications, and funding source.
  - Auto-generates a unique reference code in the DISC-YYYYMMDDHHMMSS format.
- PipelineCard
  - One-to-one relationship with an invention disclosure.
  - Tracks triage stage with default stage New Disclosure.
  - Stores owner label and triage notes.

Why this matters:
- A successful submission now has a structured record in the system.
- Every disclosure can be tracked in a pipeline stage immediately.

### 2) Disclosure form with validation
File:
- pages/forms.py

New code adds InventionDisclosureForm with validation rules:
- Enforces required fields.
- Validates title, department, and funding source minimum quality.
- Validates inventor names include first and last names.
- Adds cross-field validation:
  - Summary length minimum
  - Novelty length minimum
  - Application length minimum
  - Prevents novelty text from being identical to summary
- Adds CSS classes for consistent UI rendering.

Why this matters:
- Meets the acceptance criterion for required fields and invalid input handling.
- Improves data quality at submission time.

### 3) Submission workflow service layer
File:
- pages/services.py

New code adds workflow services:
- create_disclosure_submission
  - Uses a database transaction.
  - Creates InventionDisclosure and PipelineCard together.
- send_disclosure_confirmation
  - Renders email subject/body templates.
  - Sends confirmation email to submitting researcher.
  - Logs exceptions and returns success/failure flag.

Why this matters:
- Centralizes business logic in one place.
- Connects submission to auto-pipeline creation and email confirmation.

### 4) New submission route and view
Files:
- pages/urls.py
- pages/views.py

New code adds endpoint:
- disclosures/new/ mapped to disclosure_submit

New view behavior:
- Requires login.
- Restricts access to university user type (researcher role).
- Validates form submission.
- On success:
  - Creates disclosure + pipeline card
  - Sends confirmation email
  - Shows success or warning message
  - Redirects after POST
- On failure:
  - Re-renders form with inline errors.

Why this matters:
- Implements the end-to-end submission flow from UI to persistence and notification.

### 5) Disclosure form UI and email templates
Files:
- templates/pages/disclosure_form.html
- templates/pages/emails/disclosure_confirmation_subject.txt
- templates/pages/emails/disclosure_confirmation_body.txt

New UI template includes:
- Structured form layout with required markers.
- Inline field-level error display.
- Non-field error banner.
- Explanation panel of next steps.

New email templates include:
- Subject with disclosure reference code.
- Body with title, reference, submit time, and next-step messaging.

Why this matters:
- Delivers user-facing experience for submission and confirmation communication.

### 6) Navigation and entry points to disclosure flow
Files:
- templates/base.html
- templates/pages/screen1.html

New code adds:
- New Disclosure nav item for university users.
- Submit Disclosure action on screen1 for university users.

Why this matters:
- Makes the new workflow discoverable from existing screens.

### 7) Styling support for the new form and alerts
File:
- static/css/styles.css

New styles include:
- Input, textarea, and select classes.
- Error-highlight states and banners.
- Success/warning flash message styles.
- Responsive disclosure form layout.

Why this matters:
- Supports readable inline validation and polished form UX.

### 8) Admin and test coverage
Files:
- pages/admin.py
- pages/tests.py

Admin additions:
- Registers InventionDisclosure and PipelineCard with list/filter/search setup.

Test additions:
- Form validation tests for required and invalid cases.
- Flow tests for:
  - login required
  - role authorization
  - successful submit creates disclosure and pipeline card
  - confirmation email send behavior
  - invalid submit returns inline errors and prevents record creation

Why this matters:
- Adds maintainability and verifies acceptance criteria behavior.

### 9) Settings and migration robustness updates
Files:
- discovery_hub/settings.py
- accounts/migrations/0002_user_is_email_verified.py

Updates include:
- Test database fallback to SQLite when running tests unless explicitly using Postgres.
- Safer migration logic for adding/removing is_email_verified via schema introspection.

Why this matters:
- Improves test reliability and migration portability.

## Additional Notes
- Readme_Plan_Cadence.md is a planning document created for the story, not runtime application code.
- templates/pages/screen3.html includes a small comment line used as a commit marker during branch publishing.

## How This Maps to the User Story
User story:
As a TTO Manager, I want researchers to submit structured invention disclosures so that new technologies automatically enter the pipeline.

Covered by this code:
- Structured disclosure capture: Implemented (model + form + template)
- Required field validation: Implemented (form validators + tests)
- Inline error messages: Implemented (template + validation feedback)
- Confirmation email: Implemented (service + templates + tests)
- Auto-create pipeline card: Implemented (service + model + tests)
