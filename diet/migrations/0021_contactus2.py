# Generated by Django 4.1.7 on 2023-03-16 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('diet', '0020_contactus_alter_mealplan_day'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('bmi', models.CharField(max_length=100, null=True)),
                ('bmr', models.CharField(max_length=50, null=True)),
                ('diabetes_type', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=11)),
                ('feedback', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
