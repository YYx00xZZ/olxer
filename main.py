import requests
import re
import random
import time
from bs4 import BeautifulSoup

prices = []

models = ['11 Pro', '11', 'XS Max', 'XS', 'X']
memory = [None, '32', '64', '128', '256']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
}

proxy = {
    "http": "http://213.135.60.74:80"
}

proxyServers = [
    "http://213.135.60.74:80",
    "http://51.68.141.240:3128",
    "http://192.162.62.197:59246",
    "http://79.190.145.140:3128",
    "http://185.69.198.250:8080"
]

userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


def rotateUserAgent(userAgents):
    randomIndex = createRandomIndex(userAgents)
    headers['User-Agent'] = userAgents[randomIndex]


def rotateProxyServer(proxyServers):
    randomIndex = createRandomIndex(proxyServers)
    proxy['http'] = proxyServers[randomIndex]


def createRandomIndex(optionList):
    return random.randint(0, len(optionList)-1)


def createUrl(query, page=1):
    preparedQuery = prepareQuery(query)
    url = f"https://www.olx.pl/elektronika/telefony-komorkowe/iphone/q-{preparedQuery}/"

    if page > 1:
        url += f"?page={page}"

    return url


def prepareQuery(query):
    prefix = 'iPhone '
    searchName = prefix + query.strip()
    result = searchName.replace(" ", "-")
    return result


def getSoup(response, page):
    soup = BeautifulSoup(response.content, 'html.parser')
    getResults(soup)

    if page == 1:
        return getPageNumber(soup)
    else:
        pass


def getPageNumber(soup):
    try:
        numPages = soup.find('a', attrs={'data-cy':'page-link-last'}).find('span').text
    except:
        numPages = 1
    return numPages


def getResults(soup):
    results = soup.find_all('div', class_='offer-wrapper')
    handleResults(results)


def handleResults(results):
    for result in results:
        price_wrapper = result.find('p', class_='price')
        price = price_wrapper.find('strong').text
        nonDecimal = removeDecimalValues(price)
        stripped = removeNonNumerical(nonDecimal)
        url = result.find('a', class_='linkWithHash')["href"]

        price_dict = {stripped: url}
        
        if stripped != "":
            prices.append(price_dict)


def removeDecimalValues(price):
    return re.sub(r',[0-9]+', "", price)


def removeNonNumerical(nonDecimal):
    return re.sub(r'\D', "", nonDecimal)


def calculateAvg(prices):
    length = len(prices)
    total = 0

    for price in prices:
        total += int(list(price)[0])
    
    try:
        avg = total / length
    except:
        avg = 0
    print(f"Średnia cena wybranego telefonu wynosi {avg}")
    return avg


def getRequest(userChoice, page=1):
    try:
        response = requests.get(createUrl(userChoice, page), headers=headers, proxies=proxy)
        rotateUserAgent(userAgents)
        rotateProxyServer(proxyServers)
        return getSoup(response, page)
    except:
        rotateProxyServer(proxyServers)
        getRequest(userChoice, page)


def getUserChoice():
    return createPossibilities(models, memory)


def pageCrawl():
    printHelloMessage()
    userChoice = getUserChoice()
    pageCount = getRequest(userChoice)

    if int(pageCount) > 1:
        for i in range(2, int(pageCount) + 1):
            getRequest(userChoice, i)
    
    print(f"Znaleziono {len(prices)} wyników pasujących do wybranego modelu")

    getDetailsForSearch()
    

def getDetailsForSearch():
    avg = calculateAvg(prices)
    time.sleep(0.5)

    print('Wybierz co chcesz znaleźć spośród wyników zapytania')
    displayOptions(avg)


def displayOptions(avg):
    optionsMatrix = [
        ["wyniki w zakresie x od średniej", "x wyników najbliższych średniej"],
        ["próba znalezienia wyniku o cenie x", "próba znalezienia wyniku o x tańszego od średniej"]
    ]
    optionsLength = 0

    for i, optionList in enumerate(optionsMatrix):
        for j, option in enumerate(optionList):
            print(i*(len(optionsMatrix))+j+1, " => ", option)
            optionsLength += 1

    choice = getChoice()

    if evalChoice(choice, optionsLength) == True:
        choice = getChoice()

    handleChoice(choice, avg)


def evalChoice(choice, optionsLength):
    result = ((choice is None) or (choice < 0) or (choice > optionsLength))
    return result

def handleChoice(choice, avg):
    if choice == 1:
        print("Podaj zakres")
        x = int(input())
        getNeighboursDistancedBy(x, avg)
    elif choice == 2:
        print("Podaj ilość ogłoszeń do wyświetlenia")
        x = int(input())
        getNearestNeighbours(x, avg)
    elif choice == 3:
        print("Podaj cenę w zł")
        x = int(input())
        findResult(x)
    elif choice == 4:
        print("Podaj o ile zł conajmniej tańszy ma być telefon")
        x = int(input())
        findResultCheaperBy(x, avg)


def getChoice():
    print("Podaj liczbę oznaczającą wybór")
    time.sleep(0.5)
    return int(input())


def getNeighboursDistancedBy(maxRange, avg):
    if maxRange < 0:
        print("Podany zakres jest mniejszy od 0")
    else:
        findAvgPricedListing(avg, maxRange)


def findAvgPricedListing(price, maxRange):
    priceList = createNearPrices(int(price), maxRange)

    for listing in prices:
        if int(list(listing.keys())[0]) in priceList:
            print(f"Te urządzenie może cię zainteresować, cena {list(listing.keys())[0]}zł, link {listing[list(listing.keys())[0]]}")


def createNearPrices(price, maxRange):
    similarPrices = []

    for i in range(1, maxRange):
        similarPrices.append(price+i)
        similarPrices.append(price-i)
    
    return similarPrices


def getNearestNeighbours(amount, avg):
    if amount <= 0:
        print("Podana ilość jest mniejsza lub równa 0")
    elif amount >= len(prices):
        printListings(prices)
    else:
        printNearest(amount, avg, prices)


def printNearest(amount, avg, prices):
    prices = sortListings(prices)
    nearList = []
    avgIndex = 0

    for i, item in enumerate(prices):
        
        if int(list(item.keys())[0]) <= avg and int(list(prices[i+1].keys())[0]) > avg:
            avgIndex = i

        if (avgIndex != 0) and ((i - avgIndex) < (amount//2)):
            nearList.append(item)
        
    lenList = len(nearList)

    for i in range(1, amount - lenList + 1):
        nearList.append(prices[avgIndex-i])

    printListings(nearList)

def printListings(nearList):
    for i, item in enumerate(nearList):
        print(f"{i+1} wynik najbliższy średniej: cena {list(item.keys())[0]}, link: {list(item.values())[0]}")
        

def findResult(price):
    if price < 0:
        print("Podana cena jest mniejsza od 0")
    else:
        result = binarySearch(prices, 0, len(prices)-1, price)

        if result == -1:
            print("Nie znaleziono telefonu o podanej cenie")
        else:
            print(f"Oto znaleiony telefon: {list(result.values())[0]}")


def binarySearch(prices, left, right, x): 
    prices = sortListings(prices)

    while left <= right: 
        mid = left + (right - left) // 2

        if int(list(prices[mid].keys())[0]) == x: 
            return prices[mid]
  
        elif int(list(prices[mid].keys())[0]) < x: 
            left = mid + 1
  
        else: 
            right = mid - 1
      
    return -1
  


def findResultCheaperBy(priceDiff, avg):
    if (avg - float(priceDiff)) < 0:
        print("Różnica średniej i podanej ceny jest mniejsza od zera")
    else:
        for i in range(int(avg) - priceDiff, int(avg)):
            for phones in prices:
                if int(list(phones.keys())[0]) == i:
                    print(f"Znaleziono telefon tańszy o {int(avg)-i}zł od średniej, link: {list(phones.values())[0]}")
                    break
                else:
                    continue
            else:
                continue
            break
        else:
            print(f"Nie znaleziono telefonu tańszego o conajmniej {priceDiff}zł od średniej")


def createPossibilities(models, memory):
    matrix = []

    for i in range(5):
        row = []
        for j in range(5):
            row.append(models[i] + handleMemory(memory[j]))
        matrix.append(row)

    return showPossibleModels(matrix)


def handleMemory(value):
    if value is None:
        return ""
    else:
        return " " + value + "GB"


def showPossibleModels(matrix):
    for i, line in enumerate(matrix):
        print(i+1, " => ", line[0])
    
    chosenModel = getUserInput(matrix) - 1
    return showPossibleCombinations(matrix[chosenModel])


def printHelloMessage():
    print("Witam w programie przeszukającym OLX w celu ustalenia średniej ceny telefonów marki Apple na rynku wtórnym. \n")
    time.sleep(0.5)
    print("Kliknij ENTER aby kontynuować lub wpisz :q i zatwierdź klawiszem ENTER aby wyjść z programu")
    choice = input()
    checkIfExit(choice)
    time.sleep(0.5)


def checkIfExit(choice):
    if choice == ":q":
        exit()


def showPossibleCombinations(row):
    for i, combination in enumerate(row):
        print(i+1, ' => ', combination)
    chosenCombination = getUserInput(row)
    return row[chosenCombination-1]
        

def getUserInput(options):
    option = int(input("Wpisz numer oznaczający wybór "))

    if option > 0 and option <= len(options):
        return option
    else:
        print(option)
        getUserInput(options)
    

def sortListings(base):
    return sorted(base, key = lambda i: int(list(i.keys())[0]))


def testSortListings():
    assert sortListings([{'1948': 'fdfdf'}, {'300': 'fdfdf'}, {'10000': 'fdfdf'}]) == [{'300': 'fdfdf'}, {'1948': 'fdfdf'}, {'10000': 'fdfdf'}]

    
def testRemoveDecimalValues():
    assert removeDecimalValues("5,1234") == "5"
    assert removeDecimalValues("2900") == "2900"


def testRemoveNonNumerical():
    assert removeNonNumerical("Zamiana") == ""
    assert removeNonNumerical("1999")


def testPrepareQuery():
    assert prepareQuery("11 Pro") == "iPhone-11-Pro"
    assert prepareQuery("XS Max 256GB") == "iPhone-XS-Max-256GB"


def testHandleMemory():
    assert handleMemory(None) == ""
    assert handleMemory("256") == " 256GB"


if __name__ == "__main__":
    pageCrawl()
    print(prices)