#!/usr/bin/env python3
"""Setup script to apply migrations and seed data."""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discovery_hub.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.core.management import call_command
from pages.models import Opportunity

print("🔄 Applying migrations...")
try:
    call_command('migrate', 'pages', verbosity=1)
    print("✅ Migrations applied successfully")
except Exception as e:
    print(f"⚠️ Migration error: {e}")

print("\n🌱 Seeding sample companies...")

# Clear existing data
Opportunity.objects.all().delete()

companies_data = [
    {
        'name': 'FinFlow',
        'description': 'An innovative fintech platform using AI to automate personal finance management and investment portfolio optimization.',
        'industry': 'fintech',
        'stage': 'early',
        'founded_year': 2024,
        'patent_count': 2,
        'revenue_annual': 25000,
        'employee_count': 12,
        'funding_needed': 500000,
    },
    {
        'name': 'HealthTrack Pro',
        'description': 'IoT-enabled health monitoring devices with machine learning algorithms for early disease prediction.',
        'industry': 'healthcare',
        'stage': 'growth',
        'founded_year': 2022,
        'patent_count': 5,
        'revenue_annual': 450000,
        'employee_count': 28,
        'funding_needed': 2000000,
    },
    {
        'name': 'LogisticAI',
        'description': 'Intelligent logistics optimization platform reducing shipping costs by 40% using predictive algorithms.',
        'industry': 'logistics',
        'stage': 'growth',
        'founded_year': 2023,
        'patent_count': 3,
        'revenue_annual': 180000,
        'employee_count': 18,
        'funding_needed': 1500000,
    },
    {
        'name': 'NeuroSync',
        'description': 'Cutting-edge AI platform for analyzing neuroimaging data and assisting in diagnostic procedures.',
        'industry': 'ai',
        'stage': 'early',
        'founded_year': 2024,
        'patent_count': 1,
        'revenue_annual': 0,
        'employee_count': 7,
        'funding_needed': 750000,
    },
    {
        'name': 'ShopHub',
        'description': 'B2B e-commerce marketplace connecting manufacturers directly with retailers, eliminating middlemen.',
        'industry': 'ecommerce',
        'stage': 'expansion',
        'founded_year': 2021,
        'patent_count': 4,
        'revenue_annual': 2500000,
        'employee_count': 65,
        'funding_needed': 5000000,
    },
    {
        'name': 'GreenEnergy Solutions',
        'description': 'Solar panel manufacturer with proprietary thin-film technology achieving 35% efficiency gains.',
        'industry': 'energy',
        'stage': 'expansion',
        'founded_year': 2020,
        'patent_count': 8,
        'revenue_annual': 1800000,
        'employee_count': 45,
        'funding_needed': 3000000,
    },
    {
        'name': 'BioGen Therapeutics',
        'description': 'Biotech startup developing gene therapy treatments for rare genetic disorders.',
        'industry': 'biotech',
        'stage': 'early',
        'founded_year': 2023,
        'patent_count': 6,
        'revenue_annual': 0,
        'employee_count': 15,
        'funding_needed': 4000000,
    },
    {
        'name': 'CloudEdge Systems',
        'description': 'Enterprise software for edge computing and distributed data processing at the network edge.',
        'industry': 'software',
        'stage': 'growth',
        'founded_year': 2022,
        'patent_count': 7,
        'revenue_annual': 850000,
        'employee_count': 35,
        'funding_needed': 2500000,
    },
    {
        'name': 'PaymentPulse',
        'description': 'Real-time payment processing platform with blockchain verification for instant settlements.',
        'industry': 'fintech',
        'stage': 'mature',
        'founded_year': 2019,
        'patent_count': 12,
        'revenue_annual': 8500000,
        'employee_count': 120,
        'funding_needed': 10000000,
    },
    {
        'name': 'TeleMed Connect',
        'description': 'Telemedicine platform connecting patients with specialists worldwide, supporting 50+ languages.',
        'industry': 'healthcare',
        'stage': 'growth',
        'founded_year': 2021,
        'patent_count': 3,
        'revenue_annual': 600000,
        'employee_count': 42,
        'funding_needed': 1800000,
    },
    {
        'name': 'VisionAI Labs',
        'description': 'Computer vision AI for autonomous vehicle perception and real-time object detection.',
        'industry': 'ai',
        'stage': 'early',
        'founded_year': 2024,
        'patent_count': 0,
        'revenue_annual': 0,
        'employee_count': 9,
        'funding_needed': 2000000,
    },
    {
        'name': 'RouteOptimizer',
        'description': 'ML-powered route planning for delivery networks, reducing fuel costs and emissions.',
        'industry': 'logistics',
        'stage': 'growth',
        'founded_year': 2022,
        'patent_count': 2,
        'revenue_annual': 320000,
        'employee_count': 22,
        'funding_needed': 1200000,
    },
]

created_count = 0
for company_data in companies_data:
    opportunity = Opportunity.objects.create(**company_data)
    created_count += 1
    print(f'  ✓ Created: {opportunity.name}')

print(f'\n✅ Successfully seeded {created_count} companies!')
