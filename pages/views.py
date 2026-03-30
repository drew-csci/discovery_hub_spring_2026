from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import CompanyProfile
from .risk_calculator import calculate_risk


def index(request):
    """Homepage"""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    return render(request, 'pages/index.html')


@login_required(login_url='accounts:login')
def dashboard(request):
    """Main user dashboard"""
    if request.user.user_type == 'company':
        return redirect('pages:company_dashboard')
    return render(request, 'pages/dashboard.html', {'user': request.user})


@login_required(login_url='accounts:login')
def company_dashboard(request):
    """Company-specific dashboard"""
    if request.user.user_type != 'company':
        return redirect('pages:dashboard')
    return render(request, 'pages/company_dashboard.html', {'user': request.user})


@login_required(login_url='accounts:login')
def screen1(request):
    """Onboarding screen 1"""
    return render(request, 'pages/screen1.html', {'user': request.user})


@login_required(login_url='accounts:login')
def university_dashboard(request):
    """University-specific dashboard"""
    if request.user.user_type != 'university':
        return redirect('pages:dashboard')
    return render(request, 'pages/university_dashboard.html', {'user': request.user})


@login_required(login_url='accounts:login')
def investor_dashboard(request):
    """Investor-specific dashboard"""
    if request.user.user_type != 'investor':
        return redirect('pages:dashboard')
    return render(request, 'pages/investor_dashboard.html', {'user': request.user})


def page_not_found(request, exception):
    """404 error handler"""
    return render(request, '404.html', status=404)


def server_error(request):
    """500 error handler"""
    return render(request, '500.html', status=500)


@login_required(login_url='accounts:login')
def discovery_list(request):
    """Company discovery list for investors"""
    if request.user.user_type != 'investor':
        return redirect('pages:dashboard')
    
    # Get all companies seeking funding
    companies = CompanyProfile.objects.filter(seeking_funding=True)
    
    # Apply filters
    industry = request.GET.get('industry', '')
    stage = request.GET.get('stage', '')
    min_patents = request.GET.get('min_patents', '')
    
    if industry:
        companies = companies.filter(industry__icontains=industry)
    if stage:
        companies = companies.filter(stage=stage)
    if min_patents:
        try:
            companies = companies.filter(patent_count__gte=int(min_patents))
        except ValueError:
            pass
    
    # Get unique industries for filter dropdown
    industries = CompanyProfile.objects.filter(seeking_funding=True).values_list('industry', flat=True).distinct()
    
    context = {
        'companies': companies,
        'industries': industries,
        'selected_industry': industry,
        'selected_stage': stage,
        'selected_min_patents': min_patents,
    }
    return render(request, 'pages/discovery_list.html', context)


@login_required(login_url='accounts:login')
def company_detail(request, company_id):
    """Company detail page for investors"""
    if request.user.user_type != 'investor':
        return redirect('pages:dashboard')
    
    company = get_object_or_404(CompanyProfile, id=company_id, seeking_funding=True)
    
    context = {
        'company': company,
    }
    return render(request, 'pages/company_detail.html', context)


@login_required(login_url='accounts:login')
def calculate_company_risk(request, company_id):
    """Calculate risk for a company and show result"""
    if request.user.user_type != 'investor':
        return redirect('pages:dashboard')
    
    company = get_object_or_404(CompanyProfile, id=company_id, seeking_funding=True)
    risk_level = calculate_risk(company)
    
    context = {
        'company': company,
        'risk_level': risk_level,
    }
    return render(request, 'pages/company_risk_result.html', context)
