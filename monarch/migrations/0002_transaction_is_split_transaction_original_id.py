# Generated by Django 4.0.2 on 2022-05-26 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monarch', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='is_split',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='original_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
