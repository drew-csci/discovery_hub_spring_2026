# Readme Plan Cadence

## User Story
As a TTO Manager, I want researchers to submit structured invention disclosures so that new technologies automatically enter the pipeline.

## Story Metadata
- Story Points: 8
- Wireframe: Invention Disclosure Submission Form

## Acceptance Criteria
1. Required fields are validated before submission.
2. Confirmation email is sent upon successful submission.
3. Inline error messages are displayed for invalid fields.
4. A pipeline card is automatically created after successful submission.

## Scope and Assumptions
- Form is available to authenticated researcher users.
- Django forms are used for server-side validation.
- HTML templates render field-level inline errors.
- Email delivery uses configured Django email backend.
- Pipeline card is created in the same transaction boundary as disclosure save when possible.

## Implementation Plan

### 1. Build Disclosure Form UI
- Create a new disclosure form page using the wireframe structure.
- Add fields for structured disclosure data (title, abstract/summary, inventors, department, technology area, novelty, potential applications, funding source, and attachments if in scope).
- Add required-field indicators and accessible labels/help text.
- Add submit and cancel actions and success/failure user feedback regions.

Deliverables:
- Django template for disclosure submission form.
- Route and view to render the form.
- Basic styling consistent with existing site design.

### 2. Implement Form Validation
- Define a Django Form (or ModelForm) with explicit required fields.
- Add field-level validation methods for format/content rules.
- Add cross-field validation in clean() for dependent rules (if any).
- Return errors to template and render inline field errors near each input.
- Prevent record creation when validation fails.

Deliverables:
- Form class with required constraints and validation logic.
- Template updates for inline error rendering and user-friendly messages.
- Unit tests for valid and invalid submissions.

### 3. Trigger Confirmation Email
- On successful save, trigger a confirmation email to the submitting researcher.
- Include key submission details (disclosure ID/reference, title, timestamp, next steps).
- Add retry-safe behavior so duplicate emails are not sent on refresh/repost.
- Handle email exceptions gracefully without exposing stack traces to users.

Deliverables:
- Email utility/service function.
- Email template (subject/body).
- Tests that verify email is queued/sent for successful submissions.

### 4. Auto-Create Pipeline Card
- After successful disclosure creation, create a linked pipeline card record.
- Set initial status/stage (for example: "New Disclosure").
- Persist metadata needed for TTO triage dashboard.
- Guard against duplicate pipeline cards for the same disclosure.

Deliverables:
- Pipeline creation logic in service layer or post-save workflow.
- Data relationship between disclosure and pipeline card.
- Tests for automatic card creation and duplicate prevention.

## Task Breakdown with Suggested Effort (8 Points)
- Build disclosure form UI: 2 points
- Implement form validation: 3 points
- Trigger confirmation email: 1 point
- Auto-create pipeline card: 2 points

## Definition of Done
- All acceptance criteria are met and demo-able.
- Automated tests cover happy path and key validation failures.
- No unhandled exceptions in submission flow.
- Submission creates both disclosure record and pipeline card.
- Confirmation email verified in configured environment.

## Testing Plan
- Unit tests for form validation (required fields, invalid data, cross-field checks).
- Integration test for end-to-end submission success.
- Integration test for inline error rendering on invalid submission.
- Email test using Django test outbox.
- Pipeline card creation test linked to disclosure.

## Risks and Mitigations
- Risk: Email backend misconfiguration.
  - Mitigation: Add environment checks and fallback logging in non-production.
- Risk: Duplicate submissions from browser refresh.
  - Mitigation: Use POST/Redirect/GET pattern and idempotent creation guards.
- Risk: Validation gaps causing poor data quality.
  - Mitigation: Add strict server-side validators and targeted tests.

## Suggested Implementation Sequence
1. Add models/form structures needed for disclosure and pipeline linkage.
2. Build UI template and view route.
3. Implement validation and inline error rendering.
4. Add successful submission save flow.
5. Add confirmation email step.
6. Add automatic pipeline card creation.
7. Write and run tests; fix edge cases.
