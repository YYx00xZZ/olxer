
# from helpers import getSoup

# def run():
#     soup = getSoup('https://www.olx.bg/ads/q-ram-crucial/')
#     global d
#     wrapper = soup.find_all('div', class_='offer-wrapper')
#     for w in wrapper:
#         urls = []
#         names = []
#         moreInfoUrl = w.find('a', class_='thumb vtop inlblk rel tdnone linkWithHash scale4 detailsLink')
#         name = moreInfoUrl.img['alt']
#         urls.append(moreInfoUrl)
#         names.append(name)
#         global d
#         d = {'url': urls, 'name':names}
#         print(f'{d}\nfrom inside the for loop\n\n')
#     print(f'{d}\nfrom outside the for loop\n\n')
    
#     # for x in moreInfoUrl.children:
#         # print(x)
#         # return moreInfoUrl['href']
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
pageUrl = 'ram'
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("https://www.olx.bg/ads/q-ram-8gb-2x/")
    bsObj = BeautifulSoup(html)
    for link in bsObj.find_all("a", class_='linkWithHash'): #href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys
# pageUrl = 'ram'
try:
    def generate_urls(N):
        for i in range(1, N+1):
            u = f'https://www.olx.bg/ads/q-ram-8gb-2x/?page={i}'
            yield u

    pages = set()
    names = []
    def getLinks(pageUrl):
        global pages
        global names
        # html = urlopen(f"https://www.olx.bg/ads/q-ram-8gb-2x/")
        html = urlopen(pageUrl)
        # print(f'\nCurrent uri: {pageUrl}\n\n')
        bsObj = BeautifulSoup(html)
        # try:
        #     print(bsObj.find('h3', class_='lheight22 margintop5'))
        # except AttributeError:
        #     print(f'This page is missing something!')

        for link in bsObj.find_all("a",attrs={'data-cy':'listing-ad-title'}, class_='linkWithHash'): #href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    #We have encountered a new page
                    '''
                    newPage = link.attrs['href']
                    print(newPage)
                    pages.add(newPage)
                    getLinks(newPage)
                    '''
                    newPage = link.attrs['href']
                    print("----------------\n"+newPage)
                    pages.add(newPage)
                    getLinks(newPage)
            if link.strong != '':
                name = link.strong.text
                # print(name)
                names.append(name)

    print(names)

    uri = generate_urls(3)
    for x in uri:
        getLinks(x)
except KeyboardInterrupt:
    sys.exit()