# Generated by Django 4.1.7 on 2023-03-12 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0014_remove_foodlist_food_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foodlist',
            old_name='ENERC_kj',
            new_name='ENERC_kJ',
        ),
    ]
