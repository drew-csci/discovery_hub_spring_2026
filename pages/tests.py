from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User

from .forms import InventionDisclosureForm
from .models import InventionDisclosure, PipelineCard


class InventionDisclosureFormTests(TestCase):
    def test_invalid_when_required_fields_missing(self):
        form = InventionDisclosureForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("summary", form.errors)

    def test_invalid_when_title_is_fewer_than_ten_characters(self):
        form = InventionDisclosureForm(
            data={
                "title": "Too short",
                "summary": "This platform improves signal capture in remote monitoring environments." * 2,
                "inventors": "Ada Lovelace",
                "department": "Biomedical Engineering",
                "technology_area": "medical_device",
                "novelty": "Uses a flexible architecture to reduce calibration drift.",
                "potential_applications": "Remote monitoring for post-op recovery.",
                "funding_source": "NSF grant",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("Enter a title with at least 10 characters.", form.errors["title"])

    def test_invalid_when_inventor_name_is_incomplete(self):
        form = InventionDisclosureForm(
            data={
                "title": "Novel Sensor Array",
                "summary": "This platform improves signal capture in remote monitoring environments." * 2,
                "inventors": "Cher",
                "department": "Biomedical Engineering",
                "technology_area": "medical_device",
                "novelty": "Uses a flexible architecture to reduce calibration drift.",
                "potential_applications": "Remote monitoring for post-op recovery.",
                "funding_source": "NSF grant",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("inventors", form.errors)

    def test_invalid_when_summary_and_novelty_match(self):
        text = "This invention introduces a modular control surface for robotic surgery."
        form = InventionDisclosureForm(
            data={
                "title": "Robotic Control Surface",
                "summary": text,
                "inventors": "Ada Lovelace",
                "department": "Robotics Lab",
                "technology_area": "medical_device",
                "novelty": text,
                "potential_applications": "Surgical robotics and simulation training.",
                "funding_source": "NIH",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("novelty", form.errors)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class DisclosureSubmissionFlowTests(TestCase):
    def setUp(self):
        self.researcher = User.objects.create_user(
            email="researcher@example.com",
            username="researcher@example.com",
            password="StrongPass123",
            user_type=User.UserType.UNIVERSITY,
            first_name="Riley",
            last_name="Nguyen",
        )
        self.company_user = User.objects.create_user(
            email="company@example.com",
            username="company@example.com",
            password="StrongPass123",
            user_type=User.UserType.COMPANY,
        )
        self.valid_payload = {
            "title": "Adaptive Hydrogel Sensor Platform",
            "summary": "A hydrogel-based sensor platform that detects strain and hydration changes with improved durability for clinical wearables.",
            "inventors": "Riley Nguyen, Jordan Lee",
            "department": "Materials Science",
            "technology_area": "materials",
            "novelty": "The platform combines adaptive cross-linking chemistry with low-cost readout hardware for higher durability and signal fidelity.",
            "potential_applications": "Clinical wearables, sports recovery monitoring, and remote rehabilitation tools.",
            "funding_source": "State translational research grant",
        }

    def test_login_required(self):
        response = self.client.get(reverse("disclosure_submit"))
        self.assertEqual(response.status_code, 302)

    def test_only_researchers_can_access_form(self):
        self.client.login(email="company@example.com", password="StrongPass123")
        response = self.client.get(reverse("disclosure_submit"))
        self.assertEqual(response.status_code, 403)

    def test_successful_submission_creates_disclosure_pipeline_card_and_email(self):
        self.client.login(email="researcher@example.com", password="StrongPass123")
        response = self.client.post(reverse("disclosure_submit"), data=self.valid_payload, follow=True)

        self.assertRedirects(response, reverse("disclosure_submit"))
        self.assertEqual(InventionDisclosure.objects.count(), 1)
        self.assertEqual(PipelineCard.objects.count(), 1)

        disclosure = InventionDisclosure.objects.get()
        pipeline_card = PipelineCard.objects.get()

        self.assertEqual(disclosure.researcher, self.researcher)
        self.assertEqual(pipeline_card.disclosure, disclosure)
        self.assertEqual(pipeline_card.stage, PipelineCard.Stage.NEW_DISCLOSURE)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(disclosure.reference_code, mail.outbox[0].subject)
        self.assertContains(response, "submitted successfully")

    def test_refresh_after_successful_submit_does_not_create_duplicate_pipeline_card(self):
        self.client.login(email="researcher@example.com", password="StrongPass123")

        response = self.client.post(reverse("disclosure_submit"), data=self.valid_payload)

        self.assertRedirects(response, reverse("disclosure_submit"), fetch_redirect_response=False)
        disclosure = InventionDisclosure.objects.get()
        pipeline_card = PipelineCard.objects.get(disclosure=disclosure)

        refresh_response = self.client.get(reverse("disclosure_submit"))

        self.assertEqual(refresh_response.status_code, 200)
        self.assertEqual(InventionDisclosure.objects.count(), 1)
        self.assertEqual(PipelineCard.objects.count(), 1)
        self.assertTrue(
            PipelineCard.objects.filter(pk=pipeline_card.pk, disclosure=disclosure).exists()
        )

    def test_invalid_submission_renders_inline_errors_and_does_not_create_records(self):
        self.client.login(email="researcher@example.com", password="StrongPass123")
        invalid_payload = self.valid_payload | {"summary": "Too short", "inventors": "Madonna"}

        response = self.client.post(reverse("disclosure_submit"), data=invalid_payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Provide a fuller summary")
        self.assertContains(response, "Each inventor should include a first and last name.")
        self.assertEqual(InventionDisclosure.objects.count(), 0)
        self.assertEqual(PipelineCard.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)
