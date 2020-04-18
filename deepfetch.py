import requests
import random
import pandas as pd
import click
from bs4 import BeautifulSoup
from utils import extractPrice, extractTitle, extractLocation, extractDate
from mutils import normalizePrice, normalizeLocation


def deepfetch(soup):
    prices = []
    titles = []
    cities = []
    dates = []

    productContainer = soup.find('div', attrs={'id':'offerdescription'})
    userContainer = soup.find('div', attrs={'id':'offeractions'})
    # container = div#offerdescription
    price = productContainer.find('strong', class_='pricelabel__value').text
    prices.append(price)

    title = productContainer.find('h1').text
    titles.append(title)

    date = productContainer.find('li', class_='offer-bottombar__item').em.strong.text
    dates.append(date)

    city = userContainer.find('div', attrs={'class': 'offer-user__address'}).p.text
    cities.append(city)

    data = {'Price': prices,'Title': titles, 'City': cities, 'Date': dates}
    return data


def deepfetch_price(soup):
    """ get price of single product"""
    productContainer = soup.find('div', attrs={'id':'offerdescription'})
    price = productContainer.find('strong', class_='pricelabel__value').text
    return price


def deepfetch_title(soup):
    """ get  title"""
    productContainer = soup.find('div', attrs={'id':'offerdescription'})
    title = productContainer.find('strong', class_='pricelabel__value').text
    return title


def deepfetch_date(soup):
    """ get  date"""
    productContainer = soup.find('div', attrs={'id':'offerdescription'})
    date = productContainer.find('li', class_='offer-bottombar__item').em.strong.text
    return date


def deepfetch_city(soup):
    """ get  city"""
    userContainer = soup.find('div', attrs={'id':'offeractions'})
    city = userContainer.find('div', attrs={'class': 'offer-user__address'}).p.text
    return city