# Generated by Django 4.1.3 on 2022-12-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0014_marketscreener_weigtage"),
    ]

    operations = [
        migrations.AddField(
            model_name="marketscreener",
            name="rank",
            field=models.IntegerField(default=1),
        ),
    ]
