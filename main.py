import requests
import random
import pandas as pd
from bs4 import BeautifulSoup
from utils import extractPrice, extractTitle, extractLocation, extractDate
from mutils import normalizePrice, normalizeLocation

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def forgeQuery(partToSearch):
    link = 'https://www.olx.bg/elektronika/kompyutrni-aksesoari-chasti/q-'
    # query = input('Part to search for: ')
    url = link+str(partToSearch)
    return url


def forgeOutputPath(filename):
    return str(filename+'.csv')


def rotateUserAgent():
    rua = random.choice(user_agent_list)
    return {'User-Agent': rua }


def getSoup(url):
    headers = rotateUserAgent()
    response = requests.get(url, headers=headers)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    return soup


def nPages(soup):

    if soup.find('a', attrs={'data-cy':'page-link-last'}).find('span').text != None:
        # print("none")
        return int(soup.find('a', attrs={'data-cy':'page-link-last'}).find('span').text)
    else:
        return ''
        # pass


def howManyPages(supa):
    pager = supa.find('div', 'pager rel clr')
    # lastpage = pager.select('a[data-cy="page-link-last"]')
    if pager == None:
        # return print('single page result')
        # return int(1)
        return int(0)
    else:
        lpage = pager.find(attrs={"data-cy" : "page-link-last"})
        lastp = lpage.find('span')
        lastpage = lastp.text
        # return print(lastpage), print(type(lastpage))
        return int(lastpage)


def makeLink(page, url):
    if page != 0:
        n = page
        for i in range(n):
            # print(i)
            return i


def scraper_return(prices,titles,locations,dates,urls):
    data = {'Prices': prices,'Titles' : titles, 'Locations' : locations, 'Dates' : dates, 'Urls' : urls}
    return data

def scraper(url):
    soup = getSoup(url)

    p = howManyPages(soup)

    prices = []
    titles = []
    locations = []
    dates = []
    urls = []
    # promoted = []

    containers = soup.find_all('div', class_='offer-wrapper')
    if p == 0:
        for x in containers:
            # price_wrapper = x.find('p', class_='price')
            # price = price_wrapper.find('strong').text
            # prices.append(price)
            prices.append(extractPrice(x))
            
            # title_wrapper = x.find('h3')
            # title = title_wrapper.find('strong').text
            # titles.append(title)
            titles.append(extractTitle(x))

            # location_wrapper = x.find('i', attrs={'data-icon': 'location-filled'})
            # location = location_wrapper.parent.text
            # locations.append(location)
            locations.append(extractLocation(x))

            # date_wrapper = x.find('i', attrs={'data-icon': 'clock'})
            # date = date_wrapper.parent.text
            # dates.append(date)
            dates.append(extractDate(x))

            url = x.find('a', class_='linkWithHash')["href"]
            urls.append(url)

            # print(price)
            # print(title)
    else:
        for pageNum in range(1, p):
            pageUrl = url+'&page='+str(pageNum)
            soup = getSoup(pageUrl)

            for x in containers:
                # price_wrapper = x.find('p', class_='price')
                # price = price_wrapper.find('strong').text
                # prices.append(price)
                prices.append(extractPrice(x))
                
                # title_wrapper = x.find('h3')
                # title = title_wrapper.find('strong').text
                # titles.append(title)
                titles.append(extractTitle(x))

                # location_wrapper = x.find('i', attrs={'data-icon': 'location-filled'})
                # location = location_wrapper.parent.text
                # locations.append(location)
                locations.append(extractLocation(x))

                # date_wrapper = x.find('i', attrs={'data-icon': 'clock'})
                # date = date_wrapper.parent.text
                # dates.append(date)
                dates.append(extractDate(x))

                url = x.find('a', class_='linkWithHash')["href"]
                urls.append(url)
                # print(price)
                # print(title)

    data = {'Price': prices,'Title': titles, 'Location': locations, 'Date': dates, 'Url': urls}
    return data

def main():
    outputcsv = forgeOutputPath(input('ENTER FILE NAME: '))
    url = forgeQuery(input('SEARCH KEYWORD: '))


    data = scraper(url)
    df = pd.DataFrame(data, columns = ['Price','Title','Location','Date','Url'])
    data = normalizePrice(df)
    locdata = normalizeLocation(data)
    # print(df.head())
    # print(df.shape)
    locdata.to_csv(outputcsv, sep=',', index=False)

    
if __name__ == '__main__':
    main()