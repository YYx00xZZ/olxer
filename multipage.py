# import click
# import requests
# import random
# import logging
# from time import sleep
# from itertools import cycle
# # from bs4 import BeautifulSoup
# from fake_useragent import UserAgent, FakeUserAgentError

from helpers import random_header, get_proxies, create_pools, getSoup

def getPages(link): #remove soup
    """ Fetch link for all pages """

    soup = getSoup(link)
    if (soup.find('div', class_='pager rel clr')) != None:
        lpage = soup.find(attrs={"data-cy" : "page-link-last"}).span.text
        links = [link+f'/?page={p}' for p in range(2,int(lpage))]
        pages = (page for page in links)
        return pages
    else:
        pass