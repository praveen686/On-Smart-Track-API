# Generated by Django 3.2.16 on 2022-11-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_auto_20221101_0759'),
    ]

    operations = [
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='average_cpr',
            new_name='average_central_pivot_range',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='bottom_central_pivot',
            new_name='central_pivot_range',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='cpr',
            new_name='ema_100',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='resistance1',
            new_name='ema_20',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='resistance2',
            new_name='ema_200',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='resistance3',
            new_name='ema_5',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='support1',
            new_name='ema_50',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='support2',
            new_name='relative_strength',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='support3',
            new_name='relative_strength_indicator',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='top_central_pivot',
            new_name='sma_100',
        ),
        migrations.RenameField(
            model_name='equityeodcalcutatedvalues',
            old_name='vwap',
            new_name='sma_20',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='average_cpr',
            new_name='average_central_pivot_range',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='bottom_central_pivot',
            new_name='central_pivot_range',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='cpr',
            new_name='ema_100',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='resistance1',
            new_name='ema_20',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='resistance2',
            new_name='ema_200',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='resistance3',
            new_name='ema_5',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='support1',
            new_name='ema_50',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='support2',
            new_name='relative_strength',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='support3',
            new_name='relative_strength_indicator',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='top_central_pivot',
            new_name='sma_100',
        ),
        migrations.RenameField(
            model_name='indexeodcalcutatedvalues',
            old_name='vwap',
            new_name='sma_20',
        ),
        migrations.RemoveField(
            model_name='equityeodcalcutatedvalues',
            name='cpr_position',
        ),
        migrations.RemoveField(
            model_name='equityeodcalcutatedvalues',
            name='cpr_strategy',
        ),
        migrations.RemoveField(
            model_name='equityeodcalcutatedvalues',
            name='is_open_high',
        ),
        migrations.RemoveField(
            model_name='equityeodcalcutatedvalues',
            name='is_open_low',
        ),
        migrations.RemoveField(
            model_name='indexeodcalcutatedvalues',
            name='cpr_position',
        ),
        migrations.RemoveField(
            model_name='indexeodcalcutatedvalues',
            name='cpr_strategy',
        ),
        migrations.RemoveField(
            model_name='indexeodcalcutatedvalues',
            name='is_open_high',
        ),
        migrations.RemoveField(
            model_name='indexeodcalcutatedvalues',
            name='is_open_low',
        ),
        migrations.AddField(
            model_name='equityeodcalcutatedvalues',
            name='sma_200',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='equityeodcalcutatedvalues',
            name='sma_5',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='equityeodcalcutatedvalues',
            name='sma_50',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='equityeodcalcutatedvalues',
            name='standard_deviation',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='indexeodcalcutatedvalues',
            name='sma_200',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='indexeodcalcutatedvalues',
            name='sma_5',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='indexeodcalcutatedvalues',
            name='sma_50',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
        migrations.AddField(
            model_name='indexeodcalcutatedvalues',
            name='standard_deviation',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=18, null=True),
        ),
    ]