# Generated by Django 4.0.6 on 2022-09-19 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0037_applicationform_admin_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliniclocationsmodel',
            name='contact1',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cliniclocationsmodel',
            name='contact2',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
