# Generated by Django 4.1.3 on 2022-12-15 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_alter_account_parent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="name",
            field=models.CharField(max_length=200),
        ),
    ]
