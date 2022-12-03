# Generated by Django 4.1.3 on 2022-12-01 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="strategytradeorder",
            name="direction",
            field=models.CharField(
                blank=True,
                choices=[("NEUTRAL", "Neutral"), ("LONG", "Long"), ("SHORT", "Short")],
                max_length=50,
                null=True,
            ),
        ),
    ]
