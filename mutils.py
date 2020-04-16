def normalizePrice(dataframe):
    itemPrice_new = ''

    for index, row in dataframe.iterrows():
        itemPrice_new = str(row['Price']).strip(' лв.')
        dataframe.at[index, 'Price'] = float(itemPrice_new)

    return dataframe


