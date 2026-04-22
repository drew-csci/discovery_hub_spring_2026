import time

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Opportunity

def welcome(request):
    return render(request, 'pages/welcome.html')


def opportunity_search(request):
    start = time.perf_counter()

    q = request.GET.get('q', '').strip()
    type_filter = request.GET.get('type', '').strip()
    category_filter = request.GET.get('category', '').strip()

    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10
    except (TypeError, ValueError):
        per_page = 10

    opportunities = Opportunity.objects.all()

    if q:
        opportunities = opportunities.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(type__icontains=q)
            | Q(category__icontains=q)
        )

    if type_filter:
        opportunities = opportunities.filter(type__iexact=type_filter)

    if category_filter:
        opportunities = opportunities.filter(category__iexact=category_filter)

    total_matches = opportunities.count()
    opportunities = opportunities.order_by('-created_at')

    paginator = Paginator(opportunities, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    elapsed = time.perf_counter() - start

    context = {
        'query': q,
        'type': type_filter,
        'category': category_filter,
        'opportunities': page_obj,
        'total_matches': total_matches,
        'load_time': f'{elapsed:.4f}',
    }

    return render(request, 'pages/search.html', context)


@login_required
def discovery(request):
    """Display companies seeking funding with filters - Investor view"""
    # Check if user is investor
    if hasattr(request.user, 'user_type') and request.user.user_type.lower() != 'investor':
        return render(request, 'pages/discovery.html', {'error': 'Only investors can access this page'})
    
    # Get filter parameters
    industry_filter = request.GET.get('industry', '').strip()
    stage_filter = request.GET.get('stage', '').strip()
    patent_filter = request.GET.get('patent_min', 0)
    
    try:
        patent_filter = int(patent_filter) if patent_filter else 0
    except (TypeError, ValueError):
        patent_filter = 0
    
    # Get all companies
    companies = Opportunity.objects.all()
    
    # Apply filters
    if industry_filter and industry_filter != 'all':
        companies = companies.filter(industry=industry_filter)
    
    if stage_filter and stage_filter != 'all':
        companies = companies.filter(stage=stage_filter)
    
    if patent_filter > 0:
        companies = companies.filter(patent_count__gte=patent_filter)
    
    total_companies = companies.count()
    
    # Get unique values for filter dropdowns
    industries = Opportunity.INDUSTRY_CHOICES
    stages = Opportunity.STAGE_CHOICES
    
    context = {
        'companies': companies,
        'total_companies': total_companies,
        'industries': industries,
        'stages': stages,
        'selected_industry': industry_filter,
        'selected_stage': stage_filter,
        'selected_patent_min': patent_filter,
    }
    
    return render(request, 'pages/discovery.html', context)


@require_http_methods(["POST"])
@login_required
def calculate_risk(request):
    """Calculate investment risk for a company"""
    import json
    
    try:
        data = json.loads(request.body)
        company_id = data.get('company_id')
        
        try:
            company = Opportunity.objects.get(id=company_id)
        except Opportunity.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)
        
        # Risk calculation algorithm
        risk_score = calculate_company_risk(company)
        risk_level = determine_risk_level(risk_score)
        
        return JsonResponse({
            'success': True,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'company_name': company.name,
            'analysis': generate_risk_analysis(company, risk_score, risk_level)
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


def calculate_company_risk(company):
    """
    Calculate risk score (0-100, where 100 is highest risk)
    Factors:
    - Newer companies = higher risk
    - Fewer employees = higher risk
    - Lower revenue = higher risk
    - Fewer patents = higher risk
    - Early stage = higher risk
    """
    from datetime import datetime
    
    risk_score = 50  # Base score
    
    # Age factor (newer = riskier)
    years_old = datetime.now().year - company.founded_year
    if years_old < 1:
        risk_score += 20
    elif years_old < 3:
        risk_score += 15
    elif years_old < 5:
        risk_score += 8
    elif years_old > 10:
        risk_score -= 10
    
    # Stage factor
    stage_risk = {
        'early': 25,
        'growth': 15,
        'expansion': 8,
        'mature': 0,
    }
    risk_score += stage_risk.get(company.stage, 0)
    
    # Revenue factor
    if company.revenue_annual == 0:
        risk_score += 15
    elif company.revenue_annual < 100000:
        risk_score += 10
    elif company.revenue_annual < 1000000:
        risk_score += 5
    elif company.revenue_annual > 10000000:
        risk_score -= 10
    
    # Employee count factor
    if company.employee_count == 0:
        risk_score += 10
    elif company.employee_count < 5:
        risk_score += 8
    elif company.employee_count < 20:
        risk_score += 3
    elif company.employee_count > 100:
        risk_score -= 5
    
    # Patent factor (innovation indicator)
    if company.patent_count == 0:
        risk_score += 5
    elif company.patent_count < 3:
        risk_score += 2
    elif company.patent_count > 5:
        risk_score -= 10
    
    # Normalize score to 0-100
    risk_score = max(0, min(100, risk_score))
    
    return round(risk_score, 1)


def determine_risk_level(risk_score):
    """Determine risk level based on score"""
    if risk_score < 40:
        return 'Low'
    elif risk_score < 70:
        return 'Medium'
    else:
        return 'High'


def generate_risk_analysis(company, risk_score, risk_level):
    """Generate detailed risk analysis text"""
    analysis = []
    
    from datetime import datetime
    years_old = datetime.now().year - company.founded_year
    
    # Age analysis
    if years_old < 1:
        analysis.append(f"⚠️ Very early stage company (founded {company.founded_year})")
    elif years_old < 3:
        analysis.append(f"📈 Relatively new company ({years_old} years old)")
    else:
        analysis.append(f"✓ Established company ({years_old} years old)")
    
    # Revenue analysis
    if company.revenue_annual > 0:
        analysis.append(f"💰 Annual revenue: ${company.revenue_annual:,.0f}")
    else:
        analysis.append("⚠️ No reported revenue yet")
    
    # Team analysis
    if company.employee_count > 0:
        analysis.append(f"👥 Team size: {company.employee_count} employees")
    else:
        analysis.append("⚠️ Team size not specified")
    
    # IP analysis
    if company.patent_count > 0:
        analysis.append(f"🔬 {company.patent_count} patent(s) - Strong IP")
    else:
        analysis.append("📋 No patents - New technology")
    
    # Stage analysis
    stage_text = dict(company.STAGE_CHOICES).get(company.stage, 'Unknown')
    analysis.append(f"📊 Stage: {stage_text}")
    
    return " | ".join(analysis)


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
