# Generated by Django 2.2.10 on 2021-05-30 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0021_auto_20210524_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeKind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.SlugField(choices=[('commons', 'commons'), ('homepage', 'homepage'), ('jobs', 'jobs'), ('events', 'events'), ('locations', 'locations'), ('organizations', 'organizations'), ('schedule', 'schedule'), ('speakers', 'speakers'), ('tickets', 'tickets'), ('invoices', 'invoices'), ('api', 'api'), ('certificates', 'certificates'), ('quotes', 'quotes'), ('members', 'members'), ('notices', 'notices'), ('about', 'about'), ('legal', 'legal'), ('dev', 'dev')], max_length=24)),
                ('code', models.SlugField(max_length=32)),
                ('description', models.CharField(max_length=320)),
                ('template', models.CharField(max_length=512)),
            ],
            options={
                'verbose_name': 'Tipo de aviso',
                'verbose_name_plural': 'Tipos de aviso',
                'unique_together': {('app', 'code')},
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('send_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('delivered_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('rejected_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('reply_code', models.PositiveIntegerField(default=0)),
                ('reject_message', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='notices.NoticeKind')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='members.Member')),
            ],
            options={
                'verbose_name': 'Aviso para miembro',
                'verbose_name_plural': 'Avisos para miembros',
            },
        ),
    ]