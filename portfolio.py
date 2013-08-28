import db
import ystockquote

class Portfolio():
    def __init__(self, dbname, tbl):
        self.db = db.TransactionDB(dbname)
        self.tbl = tbl
        self.netview = 'netview'

    def _create_net_view(self, dbname, tbl):
        '''Creates a view that converts shares to positive or negative'''
        self.db.createview(self.netview, '''SELECT symbol, case when activity=1 then -shares
        else shares as net_shares end from transactions''')

    def get_transactions(self):
        return self.db.allrows(self.tbl, '*')

    def open_positions(self):
        sql = 'SELECT symbol, sum(net_shares) from {} group by symbol having sum(shares)>0'.format(self.netview)
        return self.db.execute(sql)

    def refresh_prices(self):
        for symbol in open_positions():
            price = ystockquote.get_price('RY')
            
            
        
