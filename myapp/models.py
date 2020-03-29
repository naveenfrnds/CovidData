from django.db import models


# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)


class CovidData(models.Model):
    country = models.CharField(max_length=500)
    total_cases = models.CharField(max_length=500)
    new_cases = models.CharField(max_length=500)
    total_deaths = models.CharField(max_length=500)
    new_deaths = models.CharField(max_length=500)
    total_recovered = models.CharField(max_length=500)
    active_cases = models.CharField(max_length=500)
    serious_critical = models.CharField(max_length=500)
    tot_cases = models.CharField(max_length=500)
    tot_deaths = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}  -  {}'.format(self.country, self.total_cases)


class CovidStateData(models.Model):
    coviddata = models.ForeignKey(CovidData, on_delete=models.CASCADE)
    state = models.CharField(max_length=500)
    total_cases = models.CharField(max_length=500)
    total_recovered = models.CharField(max_length=500)
    total_deaths = models.CharField(max_length=500)
    total_active = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}  -  {}'.format(self.state, self.total_cases)
