import click
import requests
import random
import logging
from time import sleep
from itertools import cycle
from bs4 import BeautifulSoup
from fake_useragent import UserAgent, FakeUserAgentError

# from multipage import getPages
from helpers import random_header, get_proxies, create_pools, getSoup
import multipage

'''
def random_header():
    # Create a dict of accept headers for each user-agent.
    accepts = {"Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Safari, Chrome": "application/xml,application/xhtml+xml,text/html;q=0.9, text/plain;q=0.8,image/png,*/*;q=0.5"}
    
    # Get a random user-agent. We used Chrome and Firefox user agents.
    # Take a look at fake-useragent project's page to see all other options - https://pypi.org/project/fake-useragent/
    try: 
        # Getting a user agent using the fake_useragent package
        ua = UserAgent()
        if random.random() > 0.5:
            random_user_agent = ua.chrome
        else:
            random_user_agent = ua.firefox
    
    # In case there's a problem with fake-useragent package, we still want the scraper to function 
    # so there's a list of user-agents that we created and swap to another user agent.
    # Be aware of the fact that this list should be updated from time to time. 
    # List of user agents can be found here - https://developers.whatismybrowser.com/.
    except FakeUserAgentError  as error:
        # Save a message into a logs file. See more details below in the post.
        logging.error("FakeUserAgent didn't work. Generating headers from the pre-defined set of headers. error: {}".format(error))
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
        random_user_agent = random.choice(user_agents)
    
    # Create the headers dict. It's important to match between the user-agent and the accept headers as seen in line 35
    finally:
        valid_accept = accepts['Firefox'] if random_user_agent.find('Firefox') > 0 else accepts['Safari, Chrome']
        headers = {"User-Agent": random_user_agent,
                  "Accept": valid_accept}
    return headers
    
def get_proxies():
    url = 'https://www.sslproxies.org/'
    
    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    with requests.Session() as res:
        proxies_page = res.get(url)
        
    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(proxies_page.content, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')
  
    # Go through all rows in the proxies table and store them in the right format (IP:port) in our proxies list
    proxies = []
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append('{}:{}'.format(row.find_all('td')[0].string, row.find_all('td')[1].string))
    return proxies
    
# Generate the pools
def create_pools():
    proxies = get_proxies()
    headers = [random_header() for ind in range(len(proxies))] # list of headers, same length as the proxies list
    
    # This transforms the list into itertools.cycle object (an iterator) that we can run 
    # through using the next() function in lines 16-17.
    
    # proxies_pool = cycle(proxies)
    # headers_pool = cycle(headers)
    # return proxies_pool, headers_pool
    proxy = random.choice(proxies)
    header = random.choice(headers)
    return proxy, header
  '''

omg = click.style("Choose search category:\n1. Недвижими имоти\n2. Автомобили, каравани, лодки\n3. Електроника\n4. Спорт, книги, хоби\n5. Животни\n6. Дом и градина\n7. Мода\n8. За бебето и детето\n9. Екскурзии, почивки\n10. Услуги\n11. Машини, инструменти, бизнес оборудване\n12. Работа\n13. Подарявам\n14. Всички\nEnter number 1-14", fg='green')
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

'''
def getSoup(link):
    # if moved, import create_pools() etc.
    # Usage example
    proxy, headers = create_pools()
    # print(f'proxies={{"http": {proxy_pool}, "https": {proxy_pool}}},headers={headers_pool}')
    # Introduce the proxy and headers in the GET request
    with requests.Session() as req:
        page = req.get(link, proxies={"http": proxy, "https": proxy},headers=headers, timeout=30)
    content = page.text
    soup = BeautifulSoup(content, 'lxml')
    return soup
'''


@click.command()
@click.option("--category", prompt=omg, help="Provide your name", type=int)
@click.option("--item", prompt="Your name", help="Provide your name")
def main(category, item):
    category = categ(category)
    item = neshto(item)
    url = 'https://www.olx.bg'
    link = f'{url}{category}{item}'
    pages = []
    try:
        for x in multipage.getPages(link):
            pages.append(x)
    except TypeError:
        pages.append(link)


    # for each item in pages get desired content
        # a.k.a make getSoup request and scrape things
    print(pages)

'''
    if (soup.find('div', class_='pager rel clr') != None):
        #   #   add initial (query) link to list with links

        # pager = soup.find('div', class_='pager rel clr')
        # lpage = pager.find(attrs={"data-cy" : "page-link-last"}).span.text

        # links = (link+f'/?page={p}' for p in range(2,int(lpage)))
        # for page in links:
        #     pages.append(page)
        pagesUrls = getPages(link)
        for page in pagesUrls:
            pages.append(page)
            print(page)
        print('print from if')
        print(pages)
    else:
        print('print from else')
        print(pages)

    print('izvun, sled vsichko')
    print(pages)
'''

if __name__ == '__main__':
    main()