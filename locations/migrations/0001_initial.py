# Generated by Django 2.1 on 2018-08-24 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
                ('capacity', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='events/locations/location/')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, upload_to='events/locations/venue/')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locations', to='locations.Venue'),
        ),
    ]