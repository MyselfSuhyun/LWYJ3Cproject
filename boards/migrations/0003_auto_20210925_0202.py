# Generated by Django 3.2.7 on 2021-09-24 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_auto_20210924_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='error_hum',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='error_tem',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
