# Readme Plan Tyler

## Feature Title
Investor Discovery Page

## Overview
This feature adds an investor-focused discovery experience to the project. The goal is to allow investor users to browse companies that are actively seeking funding, apply useful filters, open detailed company profiles, and evaluate company risk through a risk calculator.

The current Django project already supports role-based users through the custom `User` model in `accounts/models.py` and includes an investor dashboard route in `pages/views.py`. However, the application does not yet have a company discovery system, company profile data model, or risk-evaluation logic. This plan outlines how to build that functionality in a clean and organized way.

## GitHub Issue Summary
**User Role:** Investor

**User Story:**
As an investor, I want to find new companies that need funding so that I can potentially gain from their profits and success while funding them.

## Acceptance Criteria
- Investor can view a list of companies seeking funding.
- Investor can filter companies by industry or field.
- Investor can filter companies by patent count.
- Investor can filter companies by company stage such as new or experienced.
- Investor can open a company profile to view more details.
- Investor can press a Risk Calculator button to evaluate a company.
- The system displays a Low, Medium, or High risk result based on company information.

## Current Project State
The project already contains:
- A custom `User` model with a `user_type` field in `accounts/models.py`
- Role-based routing and redirects in `accounts/views.py`
- Existing dashboard views in `pages/views.py`
- A placeholder investor dashboard template in `templates/pages/investor_dashboard.html`

The project does **not** currently contain:
- A company profile model with discovery-related fields
- Discovery page list and filter logic
- Company detail pages for investors
- Risk calculator backend logic
- Automated tests for this feature

## Implementation Plan

### 1. Create company discovery data structure
A new data model should be added to support companies that want to be discovered by investors. This model should either extend the existing company user role through a linked profile or introduce a dedicated company profile model.

Suggested fields include:
- Linked `User`
- Company name
- Industry or field
- Patent count
- Company stage
- Funding status
- Short description
- Detailed profile content
- Optional website or contact information

This step is necessary because the current project does not have a data structure that supports the discovery requirements.

### 2. Generate and apply migrations
After the new company-related model is created, migrations should be generated and applied so the database includes the new table structure.

This ensures the discovery feature has persistent storage and can be managed properly through Django.

### 3. Register the model in the admin panel
The new company model should be added to `accounts/admin.py` or the most appropriate admin file so records can be created, edited, and reviewed through Django admin.

This will make it easier to seed company data and test the discovery page during development.

### 4. Add investor discovery routes
New routes should be added in `pages/urls.py` for:
- A discovery list page
- A company detail page
- A risk evaluation action if needed

These routes should be restricted to investor users when appropriate.

### 5. Build the discovery list view
A new view should be added in `pages/views.py` to display companies that are actively seeking funding. This view should support filtering based on:
- Industry or field
- Patent count
- Company stage

The filtering can be handled through query parameters so the page remains simple and easy to use.

### 6. Update the investor dashboard template
The current investor dashboard template should be expanded or replaced with a more complete discovery UI. The updated page should include:
- A page title and description
- Filter controls
- A results list of companies
- A link or button to open each company profile

This will turn the placeholder investor dashboard into a useful working page.

### 7. Create a company detail page
A dedicated detail template should be created so investors can click into a company and see more complete information. This page should show:
- Company name
- Industry or field
- Patent count
- Company stage
- Funding details
- Description and profile summary
- Risk calculator button

This step satisfies the acceptance criterion requiring investors to open company profiles and view details.

### 8. Implement risk calculator logic
A backend utility or service should be created to evaluate company risk. For the first version, a rule-based approach is the most practical option.

Example factors may include:
- Patent count
- Company stage
- Whether profile data is complete
- Funding readiness information

The result should return one of three values:
- Low
- Medium
- High

This logic can later be replaced or extended with AI-based scoring if the project evolves.

### 9. Connect the risk calculator to the UI
The company detail page should include a button that triggers risk evaluation and displays the result clearly to the investor.

This can initially be implemented with a standard Django form submission or view action.

### 10. Add tests
Tests should be added to confirm the feature works as expected. Test coverage should include:
- Investor-only access to discovery pages
- Company list rendering
- Filter behavior
- Company detail page loading
- Risk calculator result display

This will help prevent regressions and improve confidence in the final feature.

## Files Likely to Be Updated
- `accounts/models.py`
- `accounts/admin.py`
- `pages/views.py`
- `pages/urls.py`
- `templates/pages/investor_dashboard.html`
- `templates/pages/company_detail.html` (new)
- `tests/` files for feature coverage

## Risks and Considerations
- The project currently does not define a company profile model, so that decision must be made first.
- Some project files still reflect earlier migration and framework history, so implementation should be careful to stay consistent with the current Django structure.
- Risk calculation requirements are broad, so starting with a simple rules-based method is the safest and clearest approach.

## Deliverables
By the end of this feature, the application should provide:
- A working investor discovery page
- Filterable company listings
- Company detail pages
- A risk calculator with Low, Medium, or High output
- Supporting Django models, routes, templates, and tests

## Conclusion
This feature will make the investor experience much more useful by turning the current placeholder dashboard into a discovery tool. It builds directly on the existing Django structure while adding the domain models and logic needed to support real investor workflows.
