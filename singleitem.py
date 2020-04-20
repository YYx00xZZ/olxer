from helpers import getSoup


def getitem(items):
    """ Fetch data for single item """
    productPrices = []
    productTitles = []
    productAddDates = []
    userLocs = []

    for x in items:
        print(x)
        supa = getSoup(x)

        productContainer = supa.find('div', attrs={'id': 'offerdescription'})
        userContainer = supa.find('div', attrs={'id': 'offeractions'})

        productPrice = productContainer.find('div', class_='pricelabel').strong.text.strip()
        productTitle = productContainer.find('div', class_='offer-titlebox').h1.text.strip()
        productAddDate = productContainer.find('ul', class_='offer-bottombar__items').li.em.strong.text.strip()
        userLoc = userContainer.find('div', class_='offer-user__address').address.p.text.strip()

    productPrices.append(productPrice)
    productTitles.append(productTitle)
    productAddDates.append(productAddDate)
    userLocs.append(userLoc)
    # bigData = {'productPrice': productPrices,'productTitle': productTitles,'productAddDate': productAddDates,'userLoc': userLocs}

    return productPrices