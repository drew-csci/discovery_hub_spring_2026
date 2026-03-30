from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="InventionDisclosure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference_code", models.CharField(editable=False, max_length=32, unique=True)),
                ("title", models.CharField(max_length=200)),
                ("summary", models.TextField()),
                ("inventors", models.TextField(help_text="List each inventor separated by commas or on separate lines.")),
                ("department", models.CharField(max_length=120)),
                ("technology_area", models.CharField(choices=[("software", "Software"), ("biotech", "Biotech"), ("medical_device", "Medical Device"), ("materials", "Materials"), ("energy", "Energy"), ("other", "Other")], max_length=30)),
                ("novelty", models.TextField()),
                ("potential_applications", models.TextField()),
                ("funding_source", models.CharField(max_length=160)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("researcher", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="disclosures", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PipelineCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stage", models.CharField(choices=[("new_disclosure", "New Disclosure"), ("under_review", "Under Review"), ("intake_complete", "Intake Complete")], default="new_disclosure", max_length=30)),
                ("owner_label", models.CharField(default="TTO Intake", max_length=120)),
                ("triage_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("disclosure", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="pipeline_card", to="pages.inventiondisclosure")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
