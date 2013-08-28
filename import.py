from transaction import *
import csv
import os
from decimal import Decimal
import util


def import_qt(csvfile):
    with open(csvfile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames
        transactions = []
        
        for row in reader:
            if row['Symbol'][0] == '.':
                symbol = row['Symbol'][1:] + '.TO'
            else:
                symbol = row['Symbol']
            qty = Decimal(row['Quantity'])
            price = Decimal(row['Price'])
            netamt = Decimal(util.convert_pformat(row['Net amount']))
            date = util.parse_shortdate(row['Trade Date'])
            if row['Action'] == 'Buy':
                activity = 0
            elif row['Action'] == 'Sell':
                activity = 1
            else:
                activity = 99
            # Converts (x.xx) to -x.xx 
            fees = Decimal(util.convert_pformat(row['Comm'])) + Decimal(util.convert_pformat(row['SEC fees']))
            transactions.append(Transaction(None, symbol, qty, activity, price,
                                            netamt, date))
        return transactions

        
    

    
