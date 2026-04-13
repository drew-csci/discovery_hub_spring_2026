from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(
    recipient_email: str,
    subject: str,
    action_summary: str,
    action_details: list[str] | None = None,
    support_email: str | None = None,
    action_url: str | None = None,
) -> bool:
    """
    Send a reusable action confirmation email to a user.

    This function is generic and can support future confirmation email use cases.
    """
    support_email = support_email or getattr(settings, 'SUPPORT_EMAIL', settings.DEFAULT_FROM_EMAIL)

    email_subject = subject
    lines = [
        'Hello,',
        '',
        action_summary,
        '',
    ]

    if action_details:
        lines.extend(action_details)
        lines.append('')

    lines.extend([
        'If this was you, no action is needed.',
        '',
        'If this was NOT you, please contact our support team immediately.',
    ])

    if action_url:
        lines.extend([
            '',
            f'Review the activity here: {action_url}',
        ])

    lines.extend([
        f'Email: {support_email}',
        'Thank you,',
        'Discovery Hub Security Team',
    ])

    message = '\n'.join(lines)

    try:
        send_mail(
            email_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        return True
    except Exception:
        return False
