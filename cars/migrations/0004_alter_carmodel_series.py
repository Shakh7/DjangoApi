# Generated by Django 4.1.5 on 2023-02-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_alter_car_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='series',
            field=models.CharField(blank=True, default=None, max_length=120, null=True),
        ),
    ]
