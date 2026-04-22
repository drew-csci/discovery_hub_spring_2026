# 🚀 Discovery Page - Quick Start Guide

## Setup Instructions

### 1. **Local Development Setup** (Recommended for Testing)

Run the local setup script to seed sample companies:
```bash
cd /Users/tylerwerr/f25_Discovery
python3 setup_discovery_local.py
```

This creates `db_setup.sqlite3` with 12 sample companies ready to demo.

### 2. **Production Setup** (with PostgreSQL)

When ready to use the live PostgreSQL database:
```bash
# Apply migrations
python3 manage.py migrate pages

# Seed companies
python3 manage.py seed_companies

# Or use the comprehensive setup
python3 setup_discovery.py
```

## Quick Test

### Create Investor User Account
1. Navigate to http://localhost:8000/register
2. Create an account with:
   - Name: Your Name
   - Email: investor@example.com
   - User Type: **Investor** ⭐ (Important!)
   - Password: Your password

### Access Discovery Page
1. Log in with your investor account
2. Click **"💼 Discovery"** in the navigation menu
3. Explore the sample companies!

## Try the Features

### **Filters**
- Select **Industry**: Try "FinTech", "Healthcare", etc.
- Select **Stage**: Try "Early", "Growth", "Expansion"
- Set **Minimum Patents**: Try 5+ patents
- Click **"Apply Filters"** to see results

### **Risk Calculator**
- Click **"📊 Calculate Risk"** on any company card
- View the risk analysis modal showing:
  - 🟢 Low Risk (< 40 score)
  - 🟡 Medium Risk (40-70 score)
  - 🔴 High Risk (> 70 score)
- Read detailed analysis of why the company got that risk rating

## What's Included

✅ **12 Sample Companies** across 8 industries
- Real-world inspired company profiles
- Realistic financial data and team sizes
- Patent counts showing IP strength

✅ **Functional Filters**
- Filter by industry/field
- Filter by company stage
- Filter by patent count

✅ **Beautiful UI**
- Responsive grid layout
- Color-coded stage badges
- Hover effects and smooth interactions

✅ **Risk Calculator**
- Analyzes company metrics
- Shows risk level with recommendation
- Color-coded results (Low/Medium/High)

✅ **Investor-Only Access**
- Automatically checks user type
- Restricts to investors only

## File Structure

```
/discovery/ (Django URL)
├── Template: templates/pages/discovery.html
├── View: pages/views.py (discovery view & calculate_risk endpoint)
├── Model: pages/models.py (Opportunity model)
├── Helper: templates/pages/industry_emoji.html
└── Seeder: pages/management/commands/seed_companies.py
```

## Troubleshooting

### "Command not found: python"
Use `python3` instead:
```bash
python3 setup_discovery_local.py
```

### "Only investors can access this page"
Make sure your user account is set as **User Type: Investor** during registration.

###  Page shows "No companies found"
- Run the setup script: `python3 setup_discovery_local.py`
- Make sure filters aren't too restrictive
- Check that the database was seeded successfully

### Risk calculator won't show results
- Make sure JavaScript is enabled
- Check browser console for errors (F12)
- Verify CSRF token is sent with the POST request

## Sample Companies Quick Reference

| Company | Industry | Stage | Employees | Revenue |
|---------|----------|-------|-----------|---------|
| FinFlow | FinTech | Early | 12 | $25K |
| HealthTrack Pro | Healthcare | Growth | 28 | $450K |
| LogisticAI | Logistics | Growth | 18 | $180K |
| NeuroSync | AI | Early | 7 | Pre-revenue |
| ShopHub | E-Commerce | Expansion | 65 | $2.5M |
| GreenEnergy Solutions | Energy | Expansion | 45 | $1.8M |
| BioGen Therapeutics | Biotech | Early | 15 | Pre-revenue |
| CloudEdge Systems | Software| Growth | 35 | $850K |
| PaymentPulse | FinTech | Mature | 120 | $8.5M |
| TeleMed Connect | Healthcare | Growth | 42 | $600K |
| VisionAI Labs | AI | Early | 9 | Pre-revenue |
| RouteOptimizer | Logistics | Growth | 22 | $320K |

## Features Overview

### 🎯 Risk Calculation - What It Evaluates

- **Company Age**: Newer companies get higher risk
- **Stage**: Early stage = higher risk
- **Revenue**: More revenue = lower risk  
- **Team**: Larger teams = lower risk
- **Patents**: More patents = lower risk (IP strength)

### 📊 Results Interpretation

- **Low Risk (< 40)**: ✅ Solid fundamentals, good growth trajectory
- **Medium Risk (40-70)**: ⚠️ Promising but needs due diligence
- **High Risk (> 70)**: 🔴 Speculative, high growth potential but risky

## Next Steps

1. ✅ Set up local database with sample data
2. ✅ Create investor account
3. ✅ Explore the discovery page
4. ✅ Try all filters
5. ✅ Calculate risk for multiple companies
6. ✅ Compare risk profiles

---

**Ready to explore investment opportunities? Start with Step 1 above!** 🚀
