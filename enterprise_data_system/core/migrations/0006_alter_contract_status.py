# Generated by Django 4.2.9 on 2024-12-21 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_account_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('P', 'Pending'), ('E', 'Expired'), ('C', 'Cancelled')], default='A', max_length=1),
        ),
    ]