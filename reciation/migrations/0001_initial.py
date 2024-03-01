# Generated by Django 3.2.21 on 2024-02-22 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100)),
                ('meaning', models.CharField(max_length=100)),
                ('example', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
