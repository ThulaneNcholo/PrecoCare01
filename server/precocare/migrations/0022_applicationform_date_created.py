# Generated by Django 4.0.6 on 2022-08-02 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('precocare', '0021_applicationform_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
