# Generated by Django 3.0.4 on 2020-03-27 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_covidstatedata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='covidstatedata',
            old_name='tot_deaths',
            new_name='total_active',
        ),
    ]