# Generated by Django 4.2.9 on 2024-12-21 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customeridentity_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('A', 'Active'), ('P', 'Pending'), ('I', 'Inactive'), ('S', 'Suspended')], default='A', max_length=1),
        ),
    ]
