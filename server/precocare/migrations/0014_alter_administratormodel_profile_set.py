# Generated by Django 4.0.6 on 2022-07-29 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0013_rename_clinic_id_doctorservices_doctor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administratormodel',
            name='profile_set',
            field=models.CharField(blank=True, default='Incomplete', max_length=50, null=True),
        ),
    ]
