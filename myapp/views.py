import requests
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from .models import CovidData, CovidStateData, CovidDisData
import datetime
import pytz
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

import urllib.request
import pandas as pd


# Create your views here.

def home(request):
    return render(request, 'base.html')


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        print(q)
        search_qs = CovidData.objects.filter(country__icontains=q).exclude(country=None).values_list('country',
                                                                                                     flat=True).distinct()
        # search_qs = CovidData.objects.filter(country__icontains=q)
        results = []
        print(search_qs)
        for r in search_qs:
            results.append(r.capitalize())
        data = json.dumps(results)
        # print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def getstatedata(request):
    if request.is_ajax():
        print(request.GET.get('field1', ''))
        data = request.GET.get('field1', '')
        # search_qs = CovidData.objects.filter(country__icontains=q).exclude(country=None).values_list('country',
        #  flat=True).distinct()

        state = CovidStateData.objects.get(state=data)
        dist = state.coviddisdata_set.all()
        # district.coviddisdata_set.create(district=tdk[0].text, total_cases=tdk[1].text)
        # search_qs = CovidData.objects.filter(country__icontains=q)
        results = []

        for r in dist:
            results.append(r.district + "-" + r.total_cases)
        data = json.dumps(results)

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

        get_data = CovidData.objects.filter(country=search.lower()).order_by('-pk')[1]

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


'''
def state_search(request):
    # search = request.POST.get('search')

    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024x1400")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.environ.get('CHROMEDRIVER_PATH'))

    driver.get("https://www.covid19india.org/")
    # assert "GitHub".lower() in driver.title.lower()

    # scrap info
    searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")
    searchlist = []

    CovidStateData.objects.all().delete()
    for td in searchdata_soup.find_all('tbody'):

        tds = td.find('tr')
        tdm = tds.find_all('td')
        try:

            t2 = tdm[2].text
            t3 = tdm[3].text
            t4 = tdm[4].text

            if tdm[4].text == "-":
                t4 = '0'
            if tdm[3].text == "-":
                t3 = '0'

            t1 = int(t2) + int(t3) + int(t4)

            print(tdm[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')
            # covid_obj1 = CovidData(country=tds[0].text.lower(), total_cases=tds[1].text, new_cases=tds[2].text,
            #            total_deaths=tds[3].text, new_deaths=tds[4].text, total_recovered=tds[5].text,
            ##          tot_cases=tds[8].text, tot_deaths=tds[9].text)

            # covid_obj1.save()

        except Exception as ee:

            print(ee)

    return render(request, 'myapp/state_wise.html', {'search': driver.page_source, })
'''


def state_search(request):
    error_message = ""
    get_data = ""
    get_total = ""
    try:

        if CovidStateData.objects.count() > 0:

            objverify = CovidStateData.objects.order_by('-created')[1]

            get_data = ""
            old_time = objverify.created
            new_time = datetime.datetime.now()
            new_time = pytz.utc.localize(new_time)
            val_time = new_time - datetime.timedelta(hours=1, minutes=15)
            if old_time < val_time:

                # search = request.POST.get('search')

                chrome_options = Options()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--window-size=1024x1400")

                driver = webdriver.Chrome(chrome_options=chrome_options,
                                          executable_path=os.environ.get('CHROMEDRIVER_PATH'))

                driver.get("https://www.covid19india.org/")
                # assert "GitHub".lower() in driver.title.lower()

                # scrap info
                searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")
                for match in searchdata_soup.find_all('span'):  # add these two extra two lines
                    match.replace_with('')

                CovidStateData.objects.all().delete()
                CovidDisData.objects.all().delete()
                state = CovidData.objects.filter(country='india').order_by('-pk')[1]
                for td in searchdata_soup.find_all('tr', {'class': 'state'}):

                    # tds = td.find('tr')
                    tdm = td.find_all('td')
                    try:

                        t2 = tdm[2].text
                        t3 = tdm[3].text
                        t4 = tdm[4].text

                        if tdm[4].text == "-":
                            t4 = '0'
                        if tdm[3].text == "-":
                            t3 = '0'

                        t1 = int(t2) + int(t3) + int(t4)

                        # print(tdm[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')

                        state.covidstatedata_set.create(state=tdm[0].text, total_cases=str(t1), total_recovered=t3,
                                                        total_deaths=t4, total_active=t2)

                        state.save()

                    except Exception as ee:

                        print(ee)
                get_data = CovidStateData.objects.all()
                get_total = CovidStateData.objects.get(state='Total')
            else:
                print(2)

                try:
                    get_data = CovidStateData.objects.all()
                    get_total = CovidStateData.objects.get(state='Total')
                except Exception as ee:
                    error_message = " Couldn't Retrevie Your Details "
        else:
            loadstatedata()
            get_data = CovidStateData.objects.all()
            get_total = CovidStateData.objects.get(state='Total')
    except Exception as ee:

        error_message = "Issue"

    return render(request, 'myapp/state_searchlocal.html', {'search': get_data, 'errormessage': error_message,
                                                            'headerdata': get_total})


def state_searchlocal(request):
    error_message = ""
    if CovidStateData.objects.count() > 0:

        objverify = CovidStateData.objects.order_by('-created')[1]

        get_data = ""
        old_time = objverify.created
        new_time = datetime.datetime.now()
        new_time = pytz.utc.localize(new_time)
        val_time = new_time - datetime.timedelta(hours=1, minutes=15)
        if old_time < val_time:

            # search = request.POST.get('search')

            chrome_options = Options()
            # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1024x1400")

            driver = webdriver.Chrome(chrome_options=chrome_options,
                                      executable_path="/Users/naveen/Desktop/codedd/myapplist/static/myapp/chromedriver")

            driver.get("https://www.covid19india.org/")
            # assert "GitHub".lower() in driver.title.lower()

            # scrap info
            searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")
            for match in searchdata_soup.find_all('span'):  # add these two extra two lines
                match.replace_with('')
            searchlist = []

            CovidStateData.objects.all().delete()
            state = CovidData.objects.filter(country='india').order_by('-pk')[1]
            for td in searchdata_soup.find_all('tr', {'class': 'state'}):

                # tds = td.find('tr')
                # tdm = tds.find_all('td')
                tds = td.find_all('td')
                # print(tds)
                try:

                    t2 = tds[2].text
                    t3 = tds[3].text.strip()
                    t4 = tds[4].text

                    if tds[4].text == "-":
                        t4 = '0'
                    if tds[3].text == "-":
                        t3 = '0'

                    t1 = int(t2) + int(t3) + int(t4)

                    print(tds[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')

                    state.covidstatedata_set.create(state=tds[0].text, total_cases=str(t1), total_recovered=t3,
                                                    total_deaths=t4, total_active=t2)

                    state.save()

                except Exception as ee:

                    print(ee)
            get_data = CovidStateData.objects.all()
            get_total = CovidStateData.objects.get(state='Total')
        else:
            print(2)

            try:
                get_data = CovidStateData.objects.all()
                get_total = CovidStateData.objects.get(state='Total')
            except Exception as ee:
                error_message = " Couldn't Retrevie Your Details "
    else:
        loadstatedata()
        get_data = CovidStateData.objects.all()
        get_total = CovidStateData.objects.get(state='Total')

    return render(request, 'myapp/state_searchlocal.html', {'search': get_data, 'errormessage': error_message,
                                                            'headerdata': get_total})


def state_searchlocaloverload(request):
    # search = request.POST.get('search')

    chrome_options = Options()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024x1400")

    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path="/Users/naveen/Desktop/codedd/myapplist/static/myapp/chromedriver")

    driver.get("https://www.covid19india.org/")
    # assert "GitHub".lower() in driver.title.lower()

    # scrap info
    searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")
    searchlist = []

    CovidStateData.objects.all().delete()
    state = CovidData.objects.filter(country='india').order_by('-pk')[1]
    for td in searchdata_soup.find_all('tbody'):

        tds = td.find('tr')
        tdm = tds.find_all('td')
        try:

            t2 = tdm[2].text
            t3 = tdm[3].text
            t4 = tdm[4].text

            if tdm[4].text == "-":
                t4 = '0'
            if tdm[3].text == "-":
                t3 = '0'

            t1 = int(t2) + int(t3) + int(t4)

            # print(tdm[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')

            state.covidstatedata_set.create(state=tdm[0].text, total_cases=str(t1), total_recovered=t3,
                                            total_deaths=t4, total_active=t2)

            state.save()

        except Exception as ee:

            print(ee)
    get_data = CovidStateData.objects.all()

    return HttpResponse("Thanks")


def loadstatedata():
    # search = request.POST.get('search')

    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024x1400")
    # driver = webdriver.Chrome(chrome_options=chrome_options,
    # executable_path="/Users/naveen/Desktop/codedd/myapplist/static/myapp/chromedriver")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.environ.get('CHROMEDRIVER_PATH'))

    driver.get("https://www.covid19india.org/")
    # assert "GitHub".lower() in driver.title.lower()

    # scrap info
    searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")
    for match in searchdata_soup.find_all('span'):  # add these two extra two lines
        match.replace_with('')

    CovidStateData.objects.all().delete()
    state = CovidData.objects.filter(country='india').order_by('-pk')[1]

    # for td in searchdata_soup.find_all('tr', {'class': 'state'}):
    for td in searchdata_soup.find_all('tr', {'class': 'state'}):

        tds = td.find_all('td')

        print(tds)

        try:

            t2 = tds[2].text
            t3 = tds[3].text.strip()
            t4 = tds[4].text

            if tds[4].text == "-":
                t4 = '0'
            if tds[3].text == "-":
                t3 = '0'

            t1 = int(t2) + int(t3) + int(t4)

            # print(tds[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')

            state.covidstatedata_set.create(state=tds[0].text, total_cases=str(t1), total_recovered=t3,
                                            total_deaths=t4, total_active=t2)

            state.save()

            # tdsdistrict = td.find_all('tr', {'class': 'district'})
            # print(tdsdistrict[0].text)

        except Exception as ee:

            print(ee)


def loaddisdata(request):
    # search = request.POST.get('search')

    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1024x1400")
    # driver = webdriver.Chrome(chrome_options=chrome_options,
    # executable_path="/Users/naveen/Desktop/codedd/myapplist/static/myapp/chromedriver")

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=os.environ.get('CHROMEDRIVER_PATH'))

    driver.get("https://www.covid19india.org/")
    # assert "GitHub".lower() in driver.title.lower()

    # scrap info
    searchdata_soup = BeautifulSoup(driver.page_source, "html.parser")

    CovidStateData.objects.all().delete()
    CovidDisData.objects.all().delete()
    state = CovidData.objects.filter(country='india').order_by('-pk')[1]
    for td in searchdata_soup.find_all('tbody'):

        tds = td.find('tr')
        tdm = tds.find_all('td')
        try:

            t2 = tdm[2].text
            t3 = tdm[3].text
            t4 = tdm[4].text

            if tdm[4].text == "-":
                t4 = '0'
            if tdm[3].text == "-":
                t3 = '0'

            t1 = int(t2) + int(t3) + int(t4)

            print(tdm[0].text + ' -- ' + str(t1) + " " + t2 + ' ' + t3 + ' ' + t4 + ' ')

            state.covidstatedata_set.create(state=tdm[0].text, total_cases=str(t1), total_recovered=t3,
                                            total_deaths=t4, total_active=t2)

            state.save()

            district = CovidStateData.objects.get(state=tdm[0].text)

            tdsdistrict = td.find_all('tr', {'class': 'district'})
            # print('hi')
            for it in tdsdistrict:
                tdk = it.find_all('td')
                district.coviddisdata_set.create(district=tdk[0].text, total_cases=tdk[1].text)

                district.save()

                # print(tdk[0].text + "-" + tdk[1].text)

        except Exception as ee:

            print(ee)
    return render(request, 'myapp/state_wise.html', {'search': 'hello', })
