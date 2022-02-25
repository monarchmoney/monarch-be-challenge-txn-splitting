# Generated by Django 4.0.2 on 2022-02-25 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monarch', '0003_account_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='data_provider_id',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together={('account', 'data_provider_id')},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'category',
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='monarch.category'),
        ),
    ]