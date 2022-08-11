# Generated by Django 4.0.6 on 2022-08-02 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0016_alter_applicationform_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationform',
            name='allergies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='medical_aid',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='application_medical', to='precocare.insurancemodel'),
        ),
        migrations.AlterField(
            model_name='applicationform',
            name='reason_visit',
            field=models.TextField(blank=True, null=True),
        ),
    ]