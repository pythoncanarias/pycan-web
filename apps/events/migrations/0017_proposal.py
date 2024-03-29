# Generated by Django 2.2.24 on 2022-05-09 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20220509_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('surname', models.CharField(max_length=256)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('title', models.CharField(max_length=340)),
                ('description', models.TextField(blank=True)),
                ('presented_at', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='proposals', to='events.Event')),
            ],
        ),
    ]
