# Generated by Django 2.2.10 on 2020-02-18 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businesses', '0002_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='token',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]