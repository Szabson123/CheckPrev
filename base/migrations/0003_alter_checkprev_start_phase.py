# Generated by Django 5.2 on 2025-04-17 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_checkprev_phase_checkprev_start_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkprev',
            name='start_phase',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
