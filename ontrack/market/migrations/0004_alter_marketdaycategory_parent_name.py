# Generated by Django 3.2.16 on 2022-10-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_marketdaycategory_parent_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketdaycategory',
            name='parent_name',
            field=models.CharField(choices=[('Capital Market', 'Capital Market'), ('Debt Market', 'Debt Market'), ('Derivatives Market', 'Derivatives Market'), ('Weekend', 'Weekend'), ('Special Trading', 'Special Trading')], max_length=50),
        ),
    ]
