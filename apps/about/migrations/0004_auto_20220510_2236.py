# Generated by Django 3.2.13 on 2022-05-10 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0003_faqitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ally',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='faqitem',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
