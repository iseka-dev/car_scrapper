# from django.shortcuts import render
# import requests
# import json
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from selenium import webdriver
# from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Car
from .serializers import CarSerializer


def scrap(request):
    browser = webdriver.Firefox()

    base_url_1 = (
        'https://www.truecar.com/shop/used/?filterType=brand&makeSlug=<brand>'
    )
    zipcode = '90210'
    brands = ['dodge', 'nissan', 'lamborghini', 'ferrari']

    for brand in brands:
        url = base_url_1.replace('<brand>', brand)
        browser.get(url)
        zip_input = browser.find_element(
            By.TAG_NAME,
            'input'
        )
        zip_input.clear()
        zip_input.send_keys(zipcode)
        zip_input.send_keys(Keys.ENTER)

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@data-qa="Listings"]')
            )
        )

        elements = browser.find_elements_by_xpath(
            '//div[@data-qa="Listings"]'
        )
        for car in elements:
            price = int(float(
                car.find_element_by_xpath(
                    './/div[@data-test="vehicleCardPricingBlockPrice"]'
                ).text.replace('$', '').replace(',', '')
            ))
            maker = car.find_element_by_xpath(
                './/span[@class="vehicle-header-make-model text-truncate"]'
            ).text.split()[0]
            model = car.find_element_by_xpath(
                './/span[@class="vehicle-header-make-model text-truncate"]'
            ).text.split()[1]
            year = car.find_element_by_xpath(
                './/span[@class="vehicle-card-year font-size-1"]'
            ).text
            if Car.objects.filter(
                maker=maker,
                model=model,
                year=year,
                price=price,
            ).exists():
                continue
            else:
                Car.objects.create(
                    maker=maker,
                    model=model,
                    year=year,
                    price=int(float(price))
                )
    return HttpResponse('Web Has Been Scrapped')


def cars_list(request):
    q_filters = Q()
    brand = request.GET.get('brand')
    if brand:
        q_filters.add(Q(maker=brand.capitalize()), Q.AND)
    model = request.GET.get('model')
    if model:
        q_filters.add(Q(model=model.capitalize()), Q.AND)
    start_year = request.GET.get('start_year')
    end_year = request.GET.get('end_year')
    if model:
        q_filters.add(Q(price__range=(start_year, end_year)), Q.AND)
    low_price = request.GET.get('low_price')
    high_price = request.GET.get('high_price')
    if model:
        q_filters.add(Q(price__range=(low_price, high_price)), Q.AND)
    cars = Car.objects.filter(
        q_filters
    )
    cars_dict = {
        'cars': CarSerializer(cars, many=True).data
    }
    return JsonResponse(cars_dict)
