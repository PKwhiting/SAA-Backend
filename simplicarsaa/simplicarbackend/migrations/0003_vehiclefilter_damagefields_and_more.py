# Generated by Django 4.2.6 on 2023-11-22 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplicarbackend', '0002_user_drivers_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclefilter',
            name='damageFields',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehiclefilter',
            name='vehicle_starts',
            field=models.BooleanField(default=False),
        ),
    ]