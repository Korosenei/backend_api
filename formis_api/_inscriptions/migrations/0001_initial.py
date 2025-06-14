# Generated by Django 5.1.7 on 2025-05-26 18:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_soumission', models.DateTimeField(auto_now_add=True)),
                ('statutCandidature', models.CharField(choices=[('Soumis', 'Soumis'), ('Approuvé', 'Approuvé'), ('Rejeté', 'Rejeté')], default='Soumis', max_length=20)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Inscription',
                'verbose_name_plural': 'Inscriptions',
            },
        ),
        migrations.CreateModel(
            name='DocumentCandidature',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fichier', models.FileField(upload_to='documents/')),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'DocumentCandidature',
                'verbose_name_plural': 'DocumentCandidatures',
            },
        ),
        migrations.CreateModel(
            name='TypeDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date_update', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'TypeDocument',
                'verbose_name_plural': 'Types Documents',
            },
        ),
    ]
