# Readme Midterm Tyler

## Overview
This document describes the midterm implementation of the Discovery Hub investor discovery feature. The codebase now supports role-based user authentication, company profile management, and a functional investor discovery experience.

## What's New

### 1. **Enhanced User Model** (`accounts/models.py`)
- Custom `User` model with three user types: `university`, `company`, and `investor`
- convenience properties: `is_university`, `is_company`, `is_investor` for easy role checking
- `display_name` property returns full name or email fallback
- timestamps for tracking user creation and updates

### 2. **TTOProfile Model** (`accounts/models.py`)
- Stores Technology Transfer Office details for university users
- Tracks institution name, office name, country, and therapeutic focus areas
- Supports TRL (Technology Readiness Level) range preferences
- One-to-one relationship with `User`

### 3. **CompanyProfile Model** (`accounts/models.py`)
- New model for company users seeking investment
- Stores company name, industry, patent count, and funding stage (new/experienced)
- Tracks seeking_funding status, description, and funding details
- One-to-one relationship with `User`
- Sortable and filterable by industry, patent count, and stage

### 4. **Discovery System** (views, URLs, templates)
- **Discovery List View** (`/discovery/`) - displays all companies seeking funding
- **Company Detail View** (`/discovery/<id>/`) - shows full company profile
- **Risk Calculator** - evaluates company risk as Low, Medium, or High based on:
  - Patent count (patents → lower risk)
  - Company stage (experienced → lower risk)
  - Funding history (seeking funding → medium to high risk)
- **Filtering** - investors can filter by industry, patent count, and company stage

### 5. **Templates**
- `discovery_list.html` - clean list of companies with filter controls
- `company_detail.html` - full company profile with Risk Calculator button
- `company_risk_result.html` - displays calculated risk level
- `investor_dashboard.html` - entry point for investor users

## How to Use

### As an Investor
1. Register or log in as an investor user
2. Navigate to `/discovery/` from your dashboard
3. View all companies seeking funding
4. Use filters to narrow by industry, patent count, or stage
5. Click a company to see full details
6. Press "Calculate Risk" to see a risk assessment (Low/Medium/High)

### As an Admin
1. Go to Django admin at `/admin/`
2. Add companies under "Company Profiles"
3. Set seeking_funding to True for investors to see them
4. Fill in industry, patent count, stage, and description

## Feature Checklist ✅
- ✅ Investor discovery list with company data
- ✅ Filter by industry, patent count, company stage
- ✅ Company detail pages
- ✅ Risk calculator (rules-based)
- ✅ Role-based access control
- ✅ Database migrations applied
- ✅ Simple, functional UI

## Technical Details
- **Framework:** Django 5.2.8
- **Database:** SQLite (default)
- **Auth:** Custom User model with email-based login
- **Templates:** Django template language with Bootstrap styling

## Next Steps (Future Work)
- AI-enhanced risk scoring
- Investor messaging system
- Company dashboard to view investor interest
- Patent integration API
- Advanced analytics for investors