# Generated by Django 3.2.16 on 2022-11-01 02:29

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0010_auto_20221031_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquityEodCalcutatedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resistance3', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('resistance2', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('resistance1', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('top_central_pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('bottom_central_pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support1', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support2', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support3', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('cpr', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('cpr_position', models.CharField(max_length=100)),
                ('cpr_strategy', models.CharField(max_length=100)),
                ('average_cpr', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('vwap', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('candle_type', models.CharField(max_length=100)),
                ('is_open_high', models.BooleanField(default=False)),
                ('is_open_low', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('pull_date', models.DateTimeField(auto_now=True)),
                ('average_quantity_per_trade', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('average_volumn', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('average_delivery_percentage', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('average_open_interest', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eod_calculated_data', to='market.equity')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'unique_together': {('entity', 'date')},
            },
            managers=[
                ('backend', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='IndexEodCalcutatedValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resistance3', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('resistance2', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('resistance1', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('top_central_pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('bottom_central_pivot', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support1', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support2', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('support3', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('cpr', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('cpr_position', models.CharField(max_length=100)),
                ('cpr_strategy', models.CharField(max_length=100)),
                ('average_cpr', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('vwap', models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True)),
                ('candle_type', models.CharField(max_length=100)),
                ('is_open_high', models.BooleanField(default=False)),
                ('is_open_low', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('pull_date', models.DateTimeField(auto_now=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eod_calculated_data', to='market.index')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'unique_together': {('entity', 'date')},
            },
            managers=[
                ('backend', django.db.models.manager.Manager()),
            ],
        ),
        migrations.DeleteModel(
            name='EquityEndOfDayCalcutated',
        ),
    ]