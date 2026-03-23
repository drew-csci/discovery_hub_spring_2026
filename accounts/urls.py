from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView, ProfileUpdateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('settings/', ProfileUpdateView.as_view(), name='account_settings'),
]
