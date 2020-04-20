from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

html = urlopen('http://olx.bg')
bs = BeautifulSoup(html.read(), 'html.parser')

def getOffer(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        offer = bsObj.find_all('div', class_='offer-wrapper')
    except AttributeError as e:
        return None
    # return offer
    for of in offer:
        print(of)


def toExport():
    offer = getOffer('http://olx.bg/q-ram-crucial')
    if offer == None:
        print("Title could not be found")
    else:
        print(offer)

if __name__ == '__main__':
    toExport()