def extractPrice(container):
    price_wrapper = container.find('p', class_='price')
    price = price_wrapper.find('strong').text
    # return prices.append(price)
    return price


def extractTitle(container):
    title_wrapper = container.find('h3')
    title = title_wrapper.find('strong').text
    # return prices.append(price)
    return title


def extractLocation(container):
    location_wrapper = container.find('i', attrs={'data-icon': 'location-filled'})
    location = location_wrapper.parent.text
    return location


def extractDate(container):
    date_wrapper = container.find('i', attrs={'data-icon': 'clock'})
    date = date_wrapper.parent.text
    return date