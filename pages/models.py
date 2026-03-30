from django.conf import settings
from django.db import models
from django.utils import timezone


class InventionDisclosure(models.Model):
    class TechnologyArea(models.TextChoices):
        SOFTWARE = "software", "Software"
        BIOTECH = "biotech", "Biotech"
        MEDICAL_DEVICE = "medical_device", "Medical Device"
        MATERIALS = "materials", "Materials"
        ENERGY = "energy", "Energy"
        OTHER = "other", "Other"

    researcher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="disclosures",
    )
    reference_code = models.CharField(max_length=32, unique=True, editable=False)
    title = models.CharField(max_length=200)
    summary = models.TextField()
    inventors = models.TextField(
        help_text="List each inventor separated by commas or on separate lines."
    )
    department = models.CharField(max_length=120)
    technology_area = models.CharField(max_length=30, choices=TechnologyArea.choices)
    novelty = models.TextField()
    potential_applications = models.TextField()
    funding_source = models.CharField(max_length=160)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference_code} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.reference_code:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.reference_code = f"DISC-{timestamp}"
        super().save(*args, **kwargs)


class PipelineCard(models.Model):
    class Stage(models.TextChoices):
        NEW_DISCLOSURE = "new_disclosure", "New Disclosure"
        UNDER_REVIEW = "under_review", "Under Review"
        INTAKE_COMPLETE = "intake_complete", "Intake Complete"

    disclosure = models.OneToOneField(
        InventionDisclosure,
        on_delete=models.CASCADE,
        related_name="pipeline_card",
    )
    stage = models.CharField(
        max_length=30,
        choices=Stage.choices,
        default=Stage.NEW_DISCLOSURE,
    )
    owner_label = models.CharField(max_length=120, default="TTO Intake")
    triage_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.disclosure.reference_code} - {self.get_stage_display()}"
