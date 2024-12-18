# Generated by Django 5.1 on 2024-11-21 22:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('emitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emitted_notes', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
