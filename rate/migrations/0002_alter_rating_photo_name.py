# Generated by Django 5.0.4 on 2024-05-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='photo_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
