from collections import OrderedDict
from decimal import Decimal
from db import TransactionDB    
from datetime import datetime

class Transaction():
    # Transaction types
    txntype = {0:'buy',
               1:'sell',
               2:'split',
               3:'dividend',
               4:'deposit',
               5:'withdrawal',
               6:'margin interest',
               7:'credit',
               8: 'conversion',
               
               99:'other'}

    def __init__(self, txnid, symbol, curr, desc, shares, activity, pricepershare,
                 netamt=None, fees=0, datestamp=None):
        self.txnid = txnid
        self.symbol = symbol
        self.curr = curr
        self.desc = desc
        self.shares = shares
        self.pricepershare = pricepershare
        self.fees = fees
        self.tbltxn = 'transactions'
        

        if type(activity) is not int:
            raise TypeError, 'Activity must be an integer.'
        self.activity = activity
        self.activity_text = Transaction.txntype[activity].upper()
        
        if datestamp is None:
            self.datestamp = datetime.now()
        elif type(datestamp) is datetime:
            self.datestamp = datestamp   
        else: 
            raise TypeError, "Datestamp is {}, not datetime.".format(str(type(datestamp)))         

        if netamt:
            self.netamt = netamt
        else:
            self.netamt = shares * pricepershare + fees
            
    def __str__(self):
        if self.activity in (1,2):
            s = (str(self.datestamp)[:10] + ': ' + self.activity_text + ' ' +
                 str(self.shares) + ' ' + self.symbol + ' @ ' +
                 str(self.pricepershare)) + ' [' + str(self.netamt) + ']'
        else:
            s = (str(self.datestamp)[:10] + ': ' + self.activity_text + ' ' +
                 str(self.symbol) + ' [' + str(self.netamt) + ']')
        return s

    def __repr__(self):
        rep = [str(i) for i in [self.txnid, self.symbol, self.shares,
                                          self.activity, self.pricepershare,
                                          self.netamt, self.fees, self.datestamp]]
        return 'Txn(' + ','.join(rep) + ')'
             
    def attributes(self):
        " Returns all attributes of the transaction, useful for sql inserts. "
        return OrderedDict([('txnid', None), # not yet supported
                           ('prtid', None),
                ('currency',self.curr),
                ('symbol',self.symbol),
                ('desc',self.desc),
                ('shares',self.shares),
                ('activity',self.activity),
                ('price',self.pricepershare),
                ('netamt',self.netamt),
                ('fees',self.fees),
                ('date',self.datestamp)])
        
if __name__ == '__main__':
    pass
