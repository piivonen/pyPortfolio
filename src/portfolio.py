import logging
import db
import transaction
import ystockquote
from collections import OrderedDict

class Portfolio():
    def __init__(self, dbname, prtid):
        self.db = db.TransactionDB(dbname)
        self.prtid = prtid
        self.tblprt = 'tbl_portfolios'
        self.tbltxn = 'tbl_transactions'
        self.tblnet = 'view_net'
        self.tblprice = 'tbl_currentprices'
        self.tblperf = 'view_performance'
        self.tbltypes = 'tbl_types'
        self.tblcurr = 'tbl_currencies'
        self.tblopen = 'view_openpos'
        self.conn = self.db.getconn()
        self.cursor = self.conn.cursor()
        self.init_tables()

############################################
# Create database tables and views         #
############################################

    def init_tables(self):
        logging.info("Initializing tables and views")
        self._create_portfolio_types_db()
        self._create_portfolio_db()
        self._create_currencies_db()
        self._create_transaction_db()
        self._create_price_db()
        self._create_net_view()
        self._create_open_view()
        self._create_performance_view()
        logging.info("Tables and views initialized. Adding default values.")
        self.fill_tables()
        
    def _create_portfolio_types_db(self):
        fields=OrderedDict([
            ('id', 'integer primary key'),
            ('type', 'text not null'),
            ('sheltered', 'integer not null')])
        self.db.createtable(self.tbltypes, fields)
    
    def _create_portfolio_db(self):
        fields=OrderedDict([
            ('id', 'integer primary key'),
            ('name', 'text not null'),
            ('type_id', 'integer references tbl_ptypes(id) on delete restrict \
                    deferrable initially deferred')])
        self.db.createtable(self.tblprt, fields)

    def _create_currencies_db(self):
        fields=OrderedDict([
            ('id', 'integer primary key'),
            ('currency', 'text not null')])
        self.db.createtable(self.tblcurr, fields)

    def _create_transaction_db(self):
        fields=OrderedDict([
        ('id','integer primary key'),
        ('p_id', 'integer references tbl_portfolios(id) on delete restrict \
        deferrable initially deferred'),
        ('c_id','integer references tbl_currencies(id) on delete restrict \
         deferrable initially deferred'), 
        ('symbol','text not null collate nocase'),
        ('desc','text collate nocase'),
        ('shares','decimal'),
        ('activity','integer not null check(activity>=0)'),
        ('pricepershare','decimal'),
        ('netamt','decimal'),
        ('fees','decimal'),
        ('datestamp','timestamp')])
        self.db.createtable(self.tbltxn, fields)

    def _create_price_db(self):
        fields=OrderedDict([
            ('symbol','text unique not null collate nocase'),
            ('price','decimal not null default 0')])
        self.db.createtable(self.tblprice, fields)

    def _create_net_view(self):
        '''creates a view that converts shares to positive or negative'''
        self.cursor.execute('''create view if not exists `{}` as select symbol, p_id, c_id,
        case when activity=1 then -shares else shares end as net_shares
        from `{}` where activity in (0,1)'''.format(self.tblnet, self.tbltxn))

    def _create_open_view(self):
         '''creates a view of open positions '''
         self.cursor.execute('''create view if not exists `{}` as select symbol, p_id, c_id,
        sum(net_shares) as net_shares from `{}` group by symbol, p_id, c_id having sum(net_shares) > 0'''.format(self.tblopen, self.tblnet))
         
    def _create_performance_view(self):
        ''' with joins on current price'''
        self.cursor.execute('''create view if not exists `{perf}` as select name, currency, type, view_net.symbol,  sum(net_shares) as net_shares,
        avg(pricepershare) as avgprice, -sum(netamt) as net_amount, sum(fees) as fees, price as current_price, net_shares * price as market_value,
        avg(pricepershare)* net_shares + fees as book_value from `{net}` on on p_id=tbl_portfolios.id join tbl_currencies on c_id=tbl_currencies.id
        join tbl_types on type_id=tbl_types.id left join tbl_currentprices on tbl_currentprices.symbol = view_net.symbol group by name, currency, type,
        view_net.symbol '''.format(perf=self.tblperf, net=self.tblnet))

      from view_net join tbl_portfolios ;
#######################################
#       Add defaults to tables        #
#######################################

    def fill_tables(self):
        logging.info("Filling tables with default values")
        self._add_default_types()
        self._add_default_portfolios()
        self._add_default_currencies()
        
    def refresh_prices(self):
        symbols = set([s[0] for s in self.all_positions()])
        for s in symbols:
            price = ystockquote.get_price(s)
            self._update_price(s, price)

    def _add_default_types(self):
        types=OrderedDict([
        ('margin', 0), 
        ('rrsp', 1),
        ('tfsa', 2),
        ('forex', 0)])
        sql = '''INSERT INTO `{}` (id, type, sheltered) VALUES (NULL, ?, ?)'''.format(
                self.tbltypes)
        if not self.db.exists('type', self.tbltypes):
            for t, s in types.items():
                self.cursor.execute(sql, (t, s))
            self.conn.commit()

    def _add_default_portfolios(self):
        types=OrderedDict([
        ('Margin Account', 0),
        ('RRSP Account', 1),
        ('TFSA Account', 2)])
        sql = '''INSERT INTO `{}` (id, name, type_id) VALUES (NULL, ?, ?)'''.format(
                self.tblprt)
        if not self.db.exists('name', self.tblprt):
            for t, s in types.items():
                self.cursor.execute(sql, (t, s))
            self.conn.commit()
        
    def _add_default_currencies(self):
        types=['CAD', 'USD'] 
        sql = '''INSERT INTO `{}` (id, currency) VALUES (NULL, ?)'''.format(
                self.tblcurr)
        if not self.db.exists('currency', self.tblcurr):
            for currency in types:
                self.cursor.execute(sql, (currency,))
            self.conn.commit()
        
    def _update_price(self, symbol, price):
        sql = '''insert or replace into `{}` ({}, {})
        values ('{}', {})'''.format(self.tblprice, 'symbol', 'price', symbol, price)
        logging.debug('Updating price with: ' + sql)
        self.cursor.execute(sql)
        self.conn.commit()   

########################################
#    Portfolio transaction methods     #
########################################

    def add_transaction(self, txn):
        # TODO: Make this more flexible, can't hard code currencies. 
        c_dict = {'CAD': 1, 'USD': 2}
        attr = txn.attributes()
        attr['prtid']=self.prtid
        c = attr['currency']
        attr['currency'] = c_dict[c] # so ugly, fix soon.
        
        rows = [i for i in attr.itervalues()]
        self.db.insertrow(self.tbltxn, rows)

########################################
#    Portfolio query methods           #
########################################

    def all_positions(self):
        self.cursor.execute('select symbol from "{}" where activity in (0,1)'.format(self.tblnet))
        return self.cursor.fetchall()

            
if __name__ == '__main__':
    p = Portfolio('test.db', 'myportfolio')


    
