# Generated by Django 3.2.16 on 2022-10-17 09:32

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketBroker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketExchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('data_refresh_time', models.TimeField(blank=True, null=True)),
                ('time_zone', timezone_field.fields.TimeZoneField(choices_display='WITH_GMT_OFFSET', default='Asia/Kolkata')),
            ],
            options={
                'verbose_name': 'Exchange',
                'verbose_name_plural': 'Exchanges',
                'ordering': ['-created_at'],
                'abstract': False,
            },
            managers=[
                ('datapull_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='MarketSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('macro_economic_sector_code', models.CharField(max_length=100)),
                ('macro_economic_sector_name', models.CharField(max_length=100)),
                ('sector_code', models.CharField(max_length=100)),
                ('sector_name', models.CharField(max_length=100)),
                ('industry_code', models.CharField(max_length=100)),
                ('industry_name', models.CharField(max_length=100)),
                ('basic_industry_code', models.CharField(max_length=100)),
                ('basic_ndustry_name', models.CharField(max_length=100)),
                ('defination', models.TextField()),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketTradingStrategy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('enabled', models.BooleanField(default=True)),
                ('start_time', models.TimeField()),
                ('max_entry_time', models.TimeField()),
                ('square_off_time', models.TimeField()),
                ('product_type', models.CharField(choices=[('MIS', 'Mis'), ('NRML', 'Nrml'), ('CNC', 'Cnc')], default='NRML', max_length=50)),
                ('stop_loss_points', models.IntegerField()),
                ('target_points', models.IntegerField()),
                ('max_trades_per_day', models.IntegerField()),
                ('is_fno', models.BooleanField(default=True)),
                ('days_to_trade', models.CharField(max_length=200)),
                ('is_expiry_day_trade', models.BooleanField(default=True)),
                ('is_directional', models.BooleanField(default=True)),
                ('is_intraday', models.BooleanField(default=True)),
                ('can_run_parellel', models.BooleanField(default=True)),
                ('placeMarketOrder', models.BooleanField(default=True)),
                ('segment', models.CharField(choices=[('Equity_Delivery', 'Equity Delivery'), ('Equity_Intraday', 'Equity Intraday'), ('Equity_Futures', 'Equity Futures'), ('Equity_Options', 'Equity Options'), ('CURRENCY', 'Currency'), ('COMMADITY', 'Commadity')], default='Equity_Options', max_length=50)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketTradingStrategySymbol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('symbol', models.CharField(max_length=100)),
                ('strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategy_symbols', to='market_lookup.markettradingstrategy')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MarketDayType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(choices=[('Trading Holiday', 'Trading Holiday'), ('Clearing Holiday', 'Clearing Holiday'), ('Weekly Off Days', 'Weekly Off Days'), ('Special Trading Day', 'Special Trading Day')], max_length=50)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_types', to='market_lookup.marketexchange')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'unique_together': {('exchange', 'name')},
            },
        ),
        migrations.CreateModel(
            name='MarketDayCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_name', models.CharField(choices=[('Capital Market', 'Capital Market'), ('Debt Market', 'Debt Market'), ('Derivatives Market', 'Derivatives Market')], max_length=50)),
                ('display_name', models.CharField(choices=[('Weekend', 'Weekend'), ('Special Trading Hours', 'Special Trading Hours'), ('Corporate Bonds', 'Corporate Bonds'), ('Currency Derivatives', 'Currency Derivatives'), ('Equities', 'Equities'), ('Commodity Derivatives', 'Commodity Derivatives'), ('Equity Derivatives', 'Equity Derivatives'), ('Interest Rate Derivatives', 'Interest Rate Derivatives'), ('Mutual Funds', 'Mutual Funds'), ('New Debt Segment', 'New Debt Segment'), ('Negotiated Trade Reporting Platform', 'Negotiated Trade Reporting Platform'), ('Securities Lending & Borrowing Schemes', 'Securities Lending Borrowing Schemes')], max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('day_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='market_lookup.marketdaytype')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'unique_together': {('day_type', 'code')},
            },
        ),
        migrations.CreateModel(
            name='MarketDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('day', models.CharField(blank=True, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=50, null=True)),
                ('is_working_day', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='market_lookup.marketdaycategory')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
                'unique_together': {('category', 'date', 'day')},
            },
        ),
    ]