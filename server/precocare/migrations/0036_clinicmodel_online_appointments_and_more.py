# Generated by Django 4.0.6 on 2022-09-14 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0035_precocarecomments'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicmodel',
            name='online_appointments',
            field=models.CharField(blank=True, default='No', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clinicmodel',
            name='telephone_appointments',
            field=models.CharField(blank=True, default='No', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='clinicmodel',
            name='walk_in',
            field=models.CharField(blank=True, default='No', max_length=50, null=True),
        ),
    ]
