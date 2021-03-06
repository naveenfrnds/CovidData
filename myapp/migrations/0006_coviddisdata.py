# Generated by Django 3.0.4 on 2020-03-30 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200327_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidDisData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=500)),
                ('total_cases', models.CharField(max_length=500)),
                ('covidstatedata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.CovidStateData')),
            ],
        ),
    ]
