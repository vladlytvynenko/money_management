# Generated by Django 2.2.4 on 2019-08-25 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_budgetline_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budget',
            old_name='start_date',
            new_name='creation_date',
        ),
        migrations.RemoveField(
            model_name='budget',
            name='end_date',
        ),
    ]
