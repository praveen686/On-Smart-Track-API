# Generated by Django 4.1.3 on 2022-12-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("market", "0004_equity_ticker_symbol_index_ticker_symbol"),
    ]

    operations = [
        migrations.CreateModel(
            name="MarketScreener",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=100)),
                (
                    "description",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("enabled", models.BooleanField(default=True)),
                ("weightage", models.IntegerField()),
            ],
            options={
                "verbose_name": "Market Screnner",
                "verbose_name_plural": "Market Screnners",
                "ordering": ["-created_at"],
                "abstract": False,
            },
        ),
    ]
