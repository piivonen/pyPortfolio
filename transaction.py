from collections import OrderedDict
from datetime import datetime
from decimal import Decimal

class Transaction():
    # Transaction types
    txntype = {0:'buy',
               1:'sell',
               2:'split',
               3:'dividend',
               4:'deposit',
               5:'withdrawal',
               99:'other'}

    def __init__(self, txnid, symbol, shares, activity, pricepershare,
                 netamt=None, fees=0, datestamp=None):
        self.txnid = txnid
        self.symbol = symbol
        self.shares = shares
        self.pricepershare = pricepershare
        self.fees = fees

        if type(activity) is not int:
            raise TypeError, 'Activity must be an integer.'
        self.activity = activity
        self.description = Transaction.txntype[activity].upper()
        if type(datestamp) in [unicode, str]:
            self.datestamp = util.parsedate(date)
        elif datestamp is None:
            self.datestamp = datetime.now()
        elif type(datestamp) is datetime:
            self.datestamp = datestamp            
        if not netamt:
            self.netamt = shares * price + fees
        else:
            self.netamt = netamt
            
    def __repr__(self):
        s = (str(self.datestamp)[:10] + ': ' + self.description + ' ' + str(self.shares) +
             ' ' + self.symbol + ' @ ' + str(self.pricepershare))
        return s
             
    def sqlify(self):
        return [None, self.symbol, self.shares, self.activity, self.pricepershare,
                self.netamt, self.fees, self.datestamp]
    
fields=OrderedDict([
    ('txnid','integer primary key'),
        ('symbol','text not null collate nocase'),
        ('shares','decimal not null check(shares>0)'),
        ('activity','integer not null check(activity>=0)'),
        ('pricepershare','decimal not null check(activity>=0)'),
        ('netamt','decimal'),
        ('fees','decimal'), 
        ('datestamp','timestamp')])

view = ('net_transactions', '''SELECT symbol, case when activity=2 then -shares
        else shares as net_shares end from transactions''')
openpositions = 'select symbol, sum(shares) from nettxn group by symbol having sum(shares)<>0'
