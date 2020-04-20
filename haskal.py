import pandas as pd
import requests
from bs4 import BeautifulSoup


csv = pd.read_csv('first_state_3.csv')
myList = csv['Url'].tolist()
# genexps


def gen_rows(smthing):
    for row in smthing:
        yield row


def proxies_pool():
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


if __name__ == '__main__':
    # s_iter = (line.upper() for line in myList)
    # for x in s_iter:
    #     print(x)
    #     next(s_iter)
    print(len(myList))
    slist = [line for line in myList
                if not ';promoted' in line ]

    print(len(slist))