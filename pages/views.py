from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from .forms import InventionDisclosureForm
from .services import create_disclosure_submission, send_disclosure_confirmation

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


@login_required
def disclosure_submit(request):
    if getattr(request.user, "user_type", None) != "university":
        return HttpResponseForbidden("Only researcher accounts can submit invention disclosures.")

    if request.method == "POST":
        form = InventionDisclosureForm(request.POST)
        if form.is_valid():
            disclosure = create_disclosure_submission(
                user=request.user,
                cleaned_data=form.cleaned_data,
            )
            email_sent = send_disclosure_confirmation(disclosure)
            if email_sent:
                messages.success(
                    request,
                    f"Disclosure {disclosure.reference_code} was submitted successfully.",
                )
            else:
                messages.warning(
                    request,
                    f"Disclosure {disclosure.reference_code} was submitted, but the confirmation email could not be sent.",
                )
            return redirect("disclosure_submit")
    else:
        form = InventionDisclosureForm()

    return render(
        request,
        "pages/disclosure_form.html",
        {
            "form": form,
        },
    )
