import codecs
from transaction import Transaction
import csv
import os
from decimal import Decimal
import util


def import_qt_tradehistory(csvfile):
    """Imports Questrade Trade History CSV fles. Files should be in utf-8
format. Will eventually type check this. 
"""
    with codecs.open(csvfile, 'rb', 'utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames
        transactions = []
        dict_accounts = {'Canadian stocks and options' : 'CAD',
                         'U.S. stocks and options' : 'USD'}
        
        for row in reader:
            acct_code = 'Other'
            for a in dict_accounts:
                if a in row['CurrencyCode_Group_Account']:
                    acct_code = dict_accounts[a]
            if row['Symbol'] == '':
                continue # Option calls don't list symbols on QT
            elif row['Symbol'][0] == '.':
                symbol = row['Symbol'][1:] + '.TO'
            else:
                symbol = row['Symbol']
            txnid = row['Trade #']
            qty = Decimal(row['Quantity'])
            price = Decimal(row['Price'])
            netamt = Decimal(util.convert_pformat(row['Net amount']))
            date = util.parse_shortdate(row['Trade Date'])
            desc = row['Description']
            
            if row['Action'] == 'Buy':
                activity = 0
            elif row['Action'] == 'Sell':
                activity = 1
            else:
                activity = 99
            # Converts (x.xx) to -x.xx 
            fees = (Decimal(util.convert_pformat(row['Comm'])) +
            Decimal(util.convert_pformat(row['SEC fees'])))
            transactions.append(Transaction(txnid, symbol, acct_code, desc, qty, activity, price,
                                            netamt, fees, date))
        return transactions


def import_qt_activity(csvfile):
    """Imports Questrade Trade Activity CSV fles. Questrade exports these as
as an HTML file. User must save this as a CSV file manually, and delete
all extraneous rows (usually rows 1-10). Keep the headers.
Files should be in utf-8 format. Will eventually type check this. Maybe one day
I can convert from HTML to CSV too. 
"""
    with codecs.open(csvfile, 'rb', 'utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames
        transactions = []
        bypass = ('CV CNV', 'CV SPC')
        stopper = ('activity records found')
        dict_activity = {'C5 DIV': 3,
                         'DIV DIV': 3,
                         'GO DEP': 4,
                         'GO FCH': 7,
                         'GO FXT': 8,
                         'MRGN INT':6,
                         }

        for row in reader:
            # End of file reached
            try:
                date = util.parse_shortdate(row['Trade date'], '%m/%d/%Y')
            except ValueError, e :
                if stopper in row['Trade date']:
                    break
                else:
                    raise ValueError, e
                
            # These are superfluous transactions
            act_holder = row['Activity type']
            if act_holder in bypass:
                continue
            # Check against known activity types 
            if act_holder in dict_activity:
                act = dict_activity[act_holder]
            # ETF Distributions don't have an activity type but have price
            elif not row['Activity type'] and row['Price']>0:
                act = 3 
            else:
                act = 99 # May need other cases here.

            qty = row['Qty']
            price = (Decimal(util.convert_pformat(row['Price'])))
            amount = (Decimal(util.convert_pformat(row['Amount'])))
            desc = row['Description']
            curr = row['Currency']
            if row['Symbol']:
                sym = row['Symbol']
            else:
                sym = '_CASH_'
            transactions.append(Transaction(None, sym, curr, desc, qty, act, price,
                                            amount, 0, date))
        return transactions 

if __name__ == '__main__':
    txn = import_qt_tradehistory('margin.csv')
    act = import_qt_activity('activity.csv')
    
        
    

    
