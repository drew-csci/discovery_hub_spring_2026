# Meeting Schedule #33 - Implementation Plan

## Goal
As a Business Development Analyst, schedule meetings directly from a match card so partnership discussions happen faster.

## Acceptance Criteria
- Integration with Google Calendar and Outlook
- Users can propose meeting times
- Confirmed meetings create calendar events
- Meeting notes logged in associated deal record

## Story Points
8

## Tasks
1. Implement authentication
2. Build scheduling interface
3. Create calendar event integration
4. Link meeting notes to deal record

## Scope & Goals
- New UI from existing match card (likely in `pages` templates/views).
- OAuth integration for Google Calendar + Outlook.
- Meeting proposals + confirm workflow.
- On confirm: create calendar event and link notes to related deal model.
- Persist meeting metadata as part of deal record (e.g., `Meeting` model or deal notes field).

## Data model design
- Add `Meeting` model:
  - `deal` (FK)
  - `scheduled_by` (FK user)
  - `status` (`proposed`, `confirmed`, `canceled`)
  - `start_time`, `end_time`, `location`, `agenda`
  - `calendar_event_id` + `provider` (`google|outlook`)
  - `notes`

## Authentication
- OAuth2 login flow for Google and Outlook:
  - Google: `https://developers.google.com/calendar/api/quickstart/python`
  - Outlook (MS Graph): calendar scope.
- Store OAuth tokens in `UserSocialCredential` model.
- Add settings for client IDs/secrets in `discovery_hub/settings.py`.
- Backend endpoints:
  - `/auth/connect/google/`
  - `/auth/connect/outlook/`
  - `/auth/callback/google/`, `/auth/callback/outlook/`

## UI
- In match card template (`templates/pages/partials/...`):
  - "Schedule Meeting" button.
  - Modal/form for propose times (`<input type=datetime-local>`), participants, medium.
  - Notes textarea.
  - Provider selection (Google/Outlook).
- New view in `pages/views.py`:
  - `propose_meeting(request, deal_id)` (POST)
  - `confirm_meeting(request, meeting_id)` (POST)
  - `cancel_meeting(...)`

## Calendar event integration
- Service module `services/calendar.py`:
  - `create_google_event(token, meeting)`
  - `create_outlook_event(token, meeting)`
- On confirmation:
  - call API and save `calendar_event_id`.
  - update meeting status to `confirmed`.
- Handle errors cleanly.

## Deal notes linkage
- Persist on `Meeting.notes` and display on deal page.
- Add relation with `Deal`: list recent meetings.
- Optional: append to `deal.notes` or `deal_activity`.

## Back-end wiring
- Models: `Meeting` and deal relation.
- URLs: add to `pages/urls.py`.
- Tests in `pages/tests.py`.
- Forms: `MeetingForm`.
- Validation: time windows and user auth.

## Testing
- Unit test auth endpoints (mock OAuth tokens).
- Integration meeting lifecycle tests.
- Manual sanity check with real calendars and deal log.

## Deployment
- Env vars:
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET`
- Update README docs.
- Refresh token support.

## Verification checklist
1. `models.Meeting` exists and migrated.
2. OAuth connection flows working.
3. Match card shows schedule modal.
4. Confirmed meeting triggers calendar event API.
5. Deal page shows meeting with notes and links.
