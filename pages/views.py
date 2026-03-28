import time

from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
