import requests
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import CovidData
import datetime
import pytz
import json
import urllib.request
import pandas as pd


# Create your views here.

def home(request):
    return render(request, 'base.html')


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        print(q)
        search_qs = CovidData.objects.filter(country__icontains=q, ).distinct()
        results = []

        for r in search_qs:
            results.append(r.country.capitalize())
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def new_search(request):
    search = request.POST.get('search')
    objverify = CovidData.objects.order_by('-created')[1]
    error_message = ""
    get_data = ""
    old_time = objverify.created
    new_time = datetime.datetime.now()
    new_time = pytz.utc.localize(new_time)
    val_time = new_time - datetime.timedelta(hours=1, minutes=15)
    if old_time < val_time:
        print(1)
        searchdata = requests.get('https://www.worldometers.info/coronavirus/#countries')
        searchdata_soup = BeautifulSoup(searchdata.text, "html.parser")
        searchlist = []
        CovidData.objects.all().delete()
        for td in searchdata_soup.find_all('tr'):

            tds = td.find_all('td')
            try:

                covid_obj1 = CovidData(country=tds[0].text.lower(), total_cases=tds[1].text, new_cases=tds[2].text,
                                       total_deaths=tds[3].text, new_deaths=tds[4].text, total_recovered=tds[5].text,
                                       active_cases=tds[6].text, serious_critical=tds[7].text,
                                       tot_cases=tds[8].text, tot_deaths=tds[9].text)

                covid_obj1.save()

            except Exception as ee:
                print(ee)
                try:
                    get_data = CovidData.objects.filter(country=search.lower()).order_by('-pk')[1]
                except Exception as ee:
                    error_message = " Couldn't Retrevie Your Details "



    else:
        print(2)

        try:
            get_data = CovidData.objects.filter(country=search.lower()).order_by('-pk')[1]
        except Exception as ee:
            error_message = " Couldn't Retrevie Your Details "

    return render(request, 'myapp/new_search.html', {'search': get_data, 'errormessage': error_message, })


def new_searchoverload(request):
    search = request.POST.get('search')
    searchdata = requests.get('https://www.worldometers.info/coronavirus/#countries')
    searchdata_soup = BeautifulSoup(searchdata.text, "html.parser")
    searchlist = []
    CovidData.objects.all().delete()
    for td in searchdata_soup.find_all('tr'):

        tds = td.find_all('td')
        try:

            covid_obj1 = CovidData(country=tds[0].text.lower(), total_cases=tds[1].text, new_cases=tds[2].text,
                                   total_deaths=tds[3].text, new_deaths=tds[4].text, total_recovered=tds[5].text,
                                   active_cases=tds[6].text, serious_critical=tds[7].text,
                                   tot_cases=tds[8].text, tot_deaths=tds[9].text)

            covid_obj1.save()

        except Exception as ee:

            print(ee)


    return HttpResponse("You're looking at answer ")
