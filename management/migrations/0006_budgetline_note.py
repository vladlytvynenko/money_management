# Generated by Django 2.2.4 on 2019-08-25 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_auto_20190825_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetline',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
