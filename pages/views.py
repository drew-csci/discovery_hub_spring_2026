from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Opportunity

def welcome(request):
    return render(request, 'pages/welcome.html')


def opportunity_search(request):
    q = request.GET.get('q', '').strip()

    opportunities = Opportunity.objects.all()

    if q:
        opportunities = opportunities.filter(name__icontains=q)

    context = {
        'query': q,
        'opportunities': opportunities,
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
