# Generated by Django 5.0.3 on 2024-07-26 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salespackage', '0003_alter_trip_amount_alter_trip_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='no_of_peoples',
        ),
    ]