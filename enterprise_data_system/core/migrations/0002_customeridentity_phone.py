# Generated by Django 4.2.9 on 2024-12-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeridentity',
            name='phone',
            field=models.CharField(max_length=20, null=True),
        ),
    ]