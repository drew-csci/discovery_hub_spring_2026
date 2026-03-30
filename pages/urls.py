"""
Pages URLs

Routes:
- pages/ - Homepage
- pages/dashboard - Main user dashboard
- pages/company_dashboard - Company-specific dashboard
- pages/screen1 - Onboarding screen 1
"""

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('screen1/', views.screen1, name='screen1'),
    path('university_dashboard/', views.university_dashboard, name='university_dashboard'),
    path('investor_dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('discovery/', views.discovery_list, name='discovery_list'),
    path('discovery/<int:company_id>/', views.company_detail, name='company_detail'),
    path('discovery/<int:company_id>/calculate-risk/', views.calculate_company_risk, name='calculate_risk'),
]

