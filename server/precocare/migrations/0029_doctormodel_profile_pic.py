# Generated by Django 4.0.6 on 2022-08-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0028_alter_applicationform_time_slot_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctormodel',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
