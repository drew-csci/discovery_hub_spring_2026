from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('search/', views.opportunity_search, name='opportunity_search'),
    path('discovery/', views.discovery, name='discovery'),
    path('api/calculate-risk/', views.calculate_risk, name='calculate_risk'),
    path('screen1/', views.screen1, name='screen1'),
    path('screen2/', views.screen2, name='screen2'),
    path('screen3/', views.screen3, name='screen3'),
]
