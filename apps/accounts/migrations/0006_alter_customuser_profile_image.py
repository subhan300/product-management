# Generated by Django 4.2.5 on 2023-09-26 06:47

import apps.accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0020_image_company'),
        ('accounts', '0005_customuser_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ForeignKey(blank=True,  null=True, on_delete=django.db.models.deletion.SET_NULL, to='maintenance.image'),
        ),
    ]
