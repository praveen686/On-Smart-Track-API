# Generated by Django 3.2.16 on 2022-10-26 13:29

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0013_auto_20221026_1426'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LiveEquityData',
            new_name='EquityLiveData',
        ),
        migrations.RenameModel(
            old_name='LiveEquityFuture',
            new_name='EquityLiveFuture',
        ),
        migrations.RenameModel(
            old_name='LiveEquityOpenInterest',
            new_name='EquityLiveOpenInterest',
        ),
        migrations.RenameModel(
            old_name='LiveEquityOptionChain',
            new_name='EquityLiveOptionChain',
        ),
        migrations.AlterModelManagers(
            name='equitylivedata',
            managers=[
                ('backend', django.db.models.manager.Manager()),
            ],
        ),
    ]
