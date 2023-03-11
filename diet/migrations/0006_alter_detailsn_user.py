# Generated by Django 4.1.5 on 2023-03-03 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diet", "0005_detailsn_bmr_detailsn_daily_calories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detailsn",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]