# Midterm Plan - Innovation Feed Feature

## User Story
As a user on this site I want to be able to see videos of people displaying their patented ideas so that I could get inspired and potentially reach out to them.

## Roles
- Company
- University
- Investor

## Acceptance Criteria (AC)
1. Have a "Create Post" button visible for authorized roles.
2. View videos and pictures in the feed.
3. Underneath each post, the company or university profile is automatically inserted.
4. Only role-based users (Company/University) can post.

## Tasks
1. Design Innovation Feed UI
   - Add feed overview page and post cards.
   - Include media container for image/video preview.
   - Add profile snippet (organization name, logo, short summary) underneath.

2. Implement Create Post functionality
   - add action button in feed page.
   - modal/page for post form with title, text, role context.

3. Add media upload (video/image)
   - enable file picker (image/video) in create post form.
   - implement validation: max file size/type.
   - store references/URLs in database and UI.

4. Create Post database model
   - fields: author (FK to user/org), org profile, title, description, media_url, media_type, created_at, visibility.

5. Display posts in feed
   - query posts sorted by latest.
   - render post card with media (video tag/image tag), text, and author profile info.

6. Attach organization profile to posts
   - on post save, capture company/university profile metadata.
   - display profile summary below each post automatically.

7. Restrict posting by role
   - ensure only Company/University roles can access create post endpoint and button.
   - Investor role can only view, not create.

8. Test feature
   - unit tests for model, upload validation, permissions.
   - integration tests for create-post flow and feed rendering.
   - manual acceptance testing for UI behavior.

## Deliverables
- New branch: `Midterm_Guanzhou`
- Committed feature code in app module(s).
- README(s) for setup notes and usage.
- Tests and screenshots to validate AC.

---

## Schedule (suggested)
- Day 1: UI wireframe and feed page scaffolding.
- Day 2: Post model + create post backend.
- Day 3: Media upload + profile injection logic.
- Day 4: Role restriction and permission tests.
- Day 5: Final polish, documentation, and test coverage.
