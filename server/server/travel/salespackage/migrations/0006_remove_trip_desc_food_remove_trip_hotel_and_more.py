# Generated by Django 5.0.3 on 2024-07-26 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salespackage', '0005_trip_desc_food_trip_hotel_trip_hotel_desc_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='desc_food',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel_desc',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel_img',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel_place',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='hotel_rating',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='imgnon_veg',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='imgveg',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='non_veg',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='veg',
        ),
    ]
