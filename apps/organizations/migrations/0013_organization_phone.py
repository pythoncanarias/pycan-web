# Generated by Django 3.2.13 on 2023-01-04 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0012_auto_20220510_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
