from helpers import getSoup

def get_all_offers(page):
    print(f'SCRAPED - {page}')

def pageIter(pages):
    page = (page for page in pages)
    return page

def scrapePage(pages):
    
    for pageLink in pageIter(pages):
        print(pageLink)
        soup = getSoup(pageLink)
        itemContainer = soup.findAll('td', class_='title-cell')
        item = (item for item in itemContainer)
        for x in item:
            print(x.find('a', class_='linkWithHash')['href'])


# def scrapePage(links):

#     prices = []
#     urls = []
#     # itemsPreview = {}
#     for link in links:
#         soup = getSoup(link)
#         # prices = []
#         # urls = []
#         # itemsPreview = {}
#         # itemContainer = soup.findAll('td', class_='title-cell')
#         itemContainer = soup.findAll('div', class_='offer-wrapper')
#         for item in itemContainer:
#             price_wrapper = item.find('p', class_='price')
#             price = price_wrapper.find('strong').text
#             url = item.find('a', class_='linkWithHash')['href']

#             if not ';promoted' in url:
#                 prices.append(price)
#                 urls.append(url)
#             else:
#                 print('^')
#         # itemsPreview = {'price' : prices, 'url' : urls}
#         return prices, urls