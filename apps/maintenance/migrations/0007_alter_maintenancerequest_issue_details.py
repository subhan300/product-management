# Generated by Django 4.2.5 on 2023-09-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0006_alter_maintenancerequest_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='issue_details',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]