# Generated by Django 4.1.5 on 2023-01-30 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0002_apikey_id_alter_apikey_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=100),
        ),
    ]
