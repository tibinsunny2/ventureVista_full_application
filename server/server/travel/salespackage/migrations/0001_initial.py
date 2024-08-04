# Generated by Django 5.0.1 on 2024-07-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('about', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('attraction', models.CharField(max_length=255)),
                ('activity', models.CharField(max_length=255)),
                ('duration', models.IntegerField()),
                ('hotel', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('no_of_peoples', models.IntegerField()),
                ('destinations', models.TextField()),
                ('username', models.CharField(max_length=255)),
            ],
        ),
    ]