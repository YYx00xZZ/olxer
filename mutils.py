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
        itemLocation_new = row['Location']
        dataframe.at[index, 'Location'] = itemLocation_new.split(sep, 1)[0]

    return dataframe

