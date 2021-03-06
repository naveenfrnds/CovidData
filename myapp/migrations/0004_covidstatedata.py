# Generated by Django 3.0.4 on 2020-03-27 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20200324_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidStateData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=500)),
                ('total_cases', models.CharField(max_length=500)),
                ('total_recovered', models.CharField(max_length=500)),
                ('total_deaths', models.CharField(max_length=500)),
                ('tot_deaths', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
                ('coviddata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.CovidData')),
            ],
        ),
    ]
