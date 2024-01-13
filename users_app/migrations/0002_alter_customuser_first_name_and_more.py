# Generated by Django 5.0 on 2024-01-08 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Имя"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Фамилия"
            ),
        ),
    ]