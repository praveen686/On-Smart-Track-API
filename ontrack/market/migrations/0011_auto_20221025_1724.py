# Generated by Django 3.2.16 on 2022-10-25 11:54

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0010_auto_20221025_1702'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='participantactivity',
            managers=[
                ('backend', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='participantstatsactivity',
            managers=[
                ('backend', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='participantactivity',
            name='option_type',
            field=models.CharField(blank=True, choices=[('CE', 'Ce'), ('PE', 'Pe')], max_length=50, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='participantactivity',
            unique_together={('client_type', 'date', 'instrument', 'option_type')},
        ),
    ]
