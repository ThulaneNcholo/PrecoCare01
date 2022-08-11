# Generated by Django 4.0.6 on 2022-08-03 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0023_clinictimeslotmodel_bookedtimeslotmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookedtimeslotmodel',
            name='service',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='booked_service', to='precocare.servicemodel'),
        ),
    ]