# Generated by Django 3.2.21 on 2024-02-24 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='correct',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='word',
            name='correct_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='word',
            name='submission',
            field=models.IntegerField(default=0),
        ),
    ]
