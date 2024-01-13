# Generated by Django 5.0 on 2024-01-13 22:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users_app", "0002_alter_customuser_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_verified",
            field=models.BooleanField(default=False, verbose_name="Подтвержден email?"),
        ),
        migrations.CreateModel(
            name="EmailVerificationModel",
            fields=[
                (
                    "code",
                    models.UUIDField(editable=False, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expired_at", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]