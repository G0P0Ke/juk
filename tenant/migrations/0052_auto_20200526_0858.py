# Generated by Django 3.0.5 on 2020-05-26 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tenant', '0051_auto_20200525_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='ya_num',
            field=models.IntegerField(default=-1),
        ),
    ]
