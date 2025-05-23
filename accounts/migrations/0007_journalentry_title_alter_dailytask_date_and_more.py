# Generated by Django 5.2 on 2025-04-18 17:03

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_rename_completed_dailytask_breakfast_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='title',
            field=models.CharField(default='Untitled', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterUniqueTogether(
            name='dailytask',
            unique_together={('user', 'date')},
        ),
    ]
