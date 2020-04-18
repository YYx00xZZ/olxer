import re

def normalizePrice(dataframe):
    itemPrice_new = ''

    for index, row in dataframe.iterrows():
        itemPrice_new = str(row['Price']).strip(' лв.')
        dataframe.at[index, 'Price'] = float(itemPrice_new)

    return dataframe


def normalizeLocation(dataframe):
    """ personal product location(city) data shape changed. TODO """
    for index,row in dataframe.iterrows():
        sep = ', '
        itemLocation_new = row['City'].strip()
        # print(f'from pipe normalLoc {itemLocation_new.split(sep, 2)[1]}')
        dataframe.at[index, 'City'] = itemLocation_new.split(sep, 2)[1]

    return dataframe

