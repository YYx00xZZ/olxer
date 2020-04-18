import requests
import random
import pandas as pd
import click
from bs4 import BeautifulSoup
from utils import extractPrice, extractTitle, extractLocation, extractDate
from mutils import normalizePrice, normalizeLocation

from deepfetch import deepfetch_price, deepfetch_title, deepfetch_city, deepfetch_date

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
    content = response.text
    #content = response.content
    soup = BeautifulSoup(content, 'lxml')
    # soup = BeautifulSoup(content, 'html.parser')

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
    print(f'from def scraper({url})')
    queryUrl = url

    soup = getSoup(url)

    p = howManyPages(soup)

    prices = []
    titles = []
    locations = []
    dates = []
    urls = []
    urls_promoted = []

    a = soup.findAll('td', class_='title-cell')
    # containers = soup.find_all('div', class_='offer-wrapper')
    if p == 0:
        for x in a:
            url = x.find('a', class_='linkWithHash')['href']
            name = x.find('a', class_='linkWithHash')('strong')

            if ';promoted' in url:
                urls_promoted.append(url)
            else:
                urls.append(url)
                titles.append(name)
    else:
        for pageNum in range(1, p):
            # print(f'from else: pageNum - {pageNum}')

            pageUrl = f'{queryUrl}/?page={str(pageNum)}'
            # print(f'from else: pageUrl - {pageUrl}')

            soup = getSoup(pageUrl)
            a = soup.findAll('td', class_='title-cell') 
            for x in a:
                url = x.find('a', class_='linkWithHash')['href']
                # print(f'from else_for: {url}')
                name = x.find('a', class_='linkWithHash')('strong')

                # urls.append(url)
                # print('from here', pageUrl)

                if ';promoted' in pageUrl:
                    urls_promoted.append(pageUrl)
                    # print('.')
                    # pass
                else:
                    urls.append(url)
                    titles.append(name)

    data = {'Price': prices,'Title': titles, 'Location': locations, 'Date': dates, 'Url': urls}
    data1 = {'Title': titles, 'Url': urls}
    return data1


def categ(choice):
    b = {
        1 : '/nedvizhimi-imoti',
        2 : '/avtomobili-karavani-lodki',
        3 : '/elektronika',
        4 : '/sport-knigi-hobi',
        5 : '/zhivotni',
        6 : '/dom-i-gradina',
        7 : '/moda',
        8 : '/za-bebeto-i-deteto',
        9 : '/ekskurzii-pochivki',
        10 : '/uslugi',
        11 : '/mashini-instrumenti-biznes-oborudvane',
        12 : '/rabota',
        13 : '/podaryavam',
        14 : '/ads',
    }
    # x = 
    return b[choice]


def neshto(nsh):
    t = nsh.replace(' ', '-')
    thing = f'/q-{t}'
    return thing

@click.command()
@click.option("--category", prompt="Choose search category:\n1. Недвижими имоти\n2. Автомобили, каравани, лодки\n3. Електроника\n4. Спорт, книги, хоби\n5. Животни\n6. Дом и градина\n7. Мода\n8. За бебето и детето\n9. Екскурзии, почивки\n10. Услуги\n11. Машини, инструменти, бизнес оборудване\n12. Работа\n13. Подарявам\n14. Всички\nEnter number 1-14:", help="Provide your name", type=int)
@click.option("--item", prompt="Your name", help="Provide your name")
def main(category, item):
    # url = f'https://www.olx.bg{categ(category)}{neshto(item)}'
    data = scraper(f'https://www.olx.bg{categ(category)}{neshto(item)}')
    df = pd.DataFrame(data, columns = ['Title', 'Url'])
    
    df.to_csv(f'first_state{category}.csv', sep=',', index=False)
    
    dPrices = []
    dTitles = []
    dCities = []
    dDates = []
    
    for label, row in df.iterrows():
        urlNd = row['Url']
        # print(row["Url"])
        # print(urlNd)
        profile = getSoup(urlNd)
        # print(profile)
        price = deepfetch_price(profile)
        dPrices.append(price)

        title = deepfetch_title(profile)
        dTitles.append(title)

        city = deepfetch_city(profile)
        dCities.append(city)

        date = deepfetch_date(profile)
        dDates.append(date)
    data = {'Price': dPrices,'Title': dTitles, 'City': dCities, 'Date': dDates}

    dataf = pd.DataFrame(data, columns=['Price', 'Title', 'City', 'Date'])
    
    dataTest = normalizePrice(dataf)
    
    dataTest.to_csv(f'searchOn_{category}.csv', sep=',', index=False)
    
if __name__ == '__main__':
    main()