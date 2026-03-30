import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

from .models import InventionDisclosure, PipelineCard

logger = logging.getLogger(__name__)


def create_disclosure_submission(*, user, cleaned_data):
    with transaction.atomic():
        disclosure = InventionDisclosure.objects.create(researcher=user, **cleaned_data)
        PipelineCard.objects.get_or_create(
            disclosure=disclosure,
            defaults={
                "stage": PipelineCard.Stage.NEW_DISCLOSURE,
                "owner_label": "TTO Intake",
                "triage_notes": "Awaiting initial TTO review.",
            },
        )
    return disclosure


def send_disclosure_confirmation(disclosure):
    context = {
        "disclosure": disclosure,
        "researcher": disclosure.researcher,
        "submitted_at": timezone.localtime(disclosure.created_at),
    }
    subject = render_to_string("pages/emails/disclosure_confirmation_subject.txt", context).strip()
    message = render_to_string("pages/emails/disclosure_confirmation_body.txt", context)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@discoveryhub.local")
    try:
        send_mail(subject, message, from_email, [disclosure.researcher.email], fail_silently=False)
        return True
    except Exception:
        logger.exception(
            "Failed to send disclosure confirmation email for disclosure %s",
            disclosure.pk,
        )
        return False
