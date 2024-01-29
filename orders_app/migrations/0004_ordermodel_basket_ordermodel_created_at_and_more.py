# Generated by Django 5.0 on 2024-01-26 21:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders_app", "0003_alter_ordermodel_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="ordermodel",
            name="basket",
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ordermodel",
            name="status",
            field=models.SmallIntegerField(
                choices=[
                    (0, "Создан"),
                    (1, "Оплачен"),
                    (2, "В пути"),
                    (3, "Доставлен"),
                ],
                default=0,
            ),
        ),
    ]