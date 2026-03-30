from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Company, University, Patent, SystemSetting


def welcome(request):
    return render(request, 'pages/welcome.html')


@login_required
def screen1(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen1.html', {'role': role})


@login_required
def screen2(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen2.html', {'role': role})


@login_required
def screen3(request):
    role = request.user.user_type.title() if hasattr(request.user, 'user_type') else 'User'
    return render(request, 'pages/screen3.html', {'role': role})


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    data = {
        'user_count': request.user.__class__.objects.count(),
        'company_count': Company.objects.count(),
        'university_count': University.objects.count(),
        'patent_count': Patent.objects.count(),
        'settings_count': SystemSetting.objects.count(),
        'settings': SystemSetting.objects.order_by('key').all(),
        'admin_urls': {
            'users': '/admin/accounts/user/',
            'companies': '/admin/pages/company/',
            'universities': '/admin/pages/university/',
            'patents': '/admin/pages/patent/',
            'settings': '/admin/pages/systemsetting/',
        },
    }
    return render(request, 'pages/admin_dashboard.html', data)

