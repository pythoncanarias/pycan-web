# Generated by Django 2.1 on 2018-08-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0002_auto_20180824_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='code',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]