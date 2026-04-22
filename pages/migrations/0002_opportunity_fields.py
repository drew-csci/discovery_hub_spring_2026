# Generated migration for Opportunity model updates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='industry',
            field=models.CharField(
                choices=[
                    ('fintech', 'FinTech'),
                    ('healthcare', 'Healthcare'),
                    ('logistics', 'Logistics'),
                    ('ai', 'AI/Machine Learning'),
                    ('ecommerce', 'E-Commerce'),
                    ('energy', 'Clean Energy'),
                    ('biotech', 'Biotech'),
                    ('software', 'Software'),
                    ('other', 'Other'),
                ],
                default='other',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='stage',
            field=models.CharField(
                choices=[
                    ('early', 'Early Stage (Seed/Pre-seed)'),
                    ('growth', 'Growth Stage'),
                    ('mature', 'Mature'),
                    ('expansion', 'Expansion'),
                ],
                default='early',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='founded_year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='patent_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='revenue_annual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='employee_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='funding_needed',
            field=models.DecimalField(decimal_places=2, default=100000, max_digits=15),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterModelOptions(
            name='opportunity',
            options={'ordering': ['-created_at']},
        ),
    ]
