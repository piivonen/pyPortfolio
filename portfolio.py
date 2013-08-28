import db
import ystockquote
from collections import OrderedDict

class Portfolio():
    def __init__(self, dbname, txn='transactions', net='netview', price='price'):
        self.db = db.TransactionDB(dbname)
        self.tbltxn = txn
        self.tblnet = net
        self.tblprice = price
        self.conn = self.db.GetConn()
        self.cursor = self.conn.cursor()

    def _create_net_view(self):
        '''Creates a view that converts shares to positive or negative'''
        
        self.cursor.execute('''CREATE VIEW IF NOT EXISTS `{}` AS SELECT symbol,
        case when activity=1 then -shares else shares end as net_shares
        from `{}`'''.format(self.tblnet, self.tbltxn))
        
    def _create_transaction_db(self):
        fields=OrderedDict([
        ('txnid','integer primary key'),
            ('symbol','text not null collate nocase'),
            ('shares','decimal not null check(shares>0)'),
            ('activity','integer not null check(activity>=0)'),
            ('pricepershare','decimal not null check(activity>=0)'),
            ('netamt','decimal'),
            ('fees','decimal'), 
            ('datestamp','timestamp')])
        self.db.createtable(self.tbltxn, fields)

    def _create_price_db(self):
        fields=OrderedDict([
            ('symbol','text unique not null collate nocase'),
            ('price','decimal not null default 0')])
        self.db.createtable(self.tblprice, fields)

    def _create_performance_db(self):
        

    def _update_price(self, symbol, price):
        sql = '''INSERT OR REPLACE INTO `{}` ({}, {})
        VALUES ('{}', {})'''.format(self.tblprice, 'symbol', 'price', symbol, price)
        self.cursor.execute(sql)
        self.conn.commit()

    def get_transactions(self):
        return self.db.allrows(self.tbltxn, '*')

    def open_positions(self):
        self.cursor.execute('''SELECT symbol, sum(net_shares) from "{}" group by symbol
        having sum(net_shares)>0'''.format(self.tblnet))
        return self.cursor.fetchall()

    def refresh_prices(self):
        symbols = set([s[0] for s in self.open_positions()])
        for s in symbols:
            price = ystockquote.get_price(s)
            self._update_price(s, price)
            
            
            
            
if __name__ == '__main__':
    p = Portfolio('test.db')
    # p._create_transaction_db()
    # p._create_net_view()
    
