# Generated by Django 5.2.1 on 2025-05-30 09:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_preferito'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilo',
            name='utente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profilo', to=settings.AUTH_USER_MODEL),
        ),
    ]
