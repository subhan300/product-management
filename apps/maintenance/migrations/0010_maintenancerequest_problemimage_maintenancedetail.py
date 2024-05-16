# Generated by Django 4.2.5 on 2023-09-20 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0009_alter_companytechnician_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='problemImage',
            field=models.ManyToManyField(blank=True, null=True, to='maintenance.image'),
        ),
        migrations.CreateModel(
            name='MaintenanceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problemTitle', models.CharField(max_length=50)),
                ('problemDescription', models.TextField(blank=True)),
                ('maintenance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_detail', to='maintenance.maintenancerequest')),
            ],
        ),
    ]