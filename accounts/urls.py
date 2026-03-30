"""
Accounts URLs

Routes:
- accounts/register - User registration
- accounts/login - User login
- accounts/logout - User logout
- accounts/password_reset - Request password reset
- accounts/reset/<token> - Reset password with token
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<str:token>/', views.password_reset, name='password_reset'),
]
