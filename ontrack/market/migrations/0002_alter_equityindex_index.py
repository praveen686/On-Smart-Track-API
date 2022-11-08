# Generated by Django 3.2.16 on 2022-11-07 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equityindex',
            name='index',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equity_indices', to='market.index'),
        ),
    ]
