import sqlite3
from datetime import datetime
from decimal import Decimal

class TransactionDB():
    def __init__(self, fname):
        sqlite3.register_adapter(Decimal, lambda x:str(x))
        sqlite3.register_converter('decimal', Decimal)
        self.conn = sqlite3.connect(fname, detect_types=sqlite3.PARSE_DECLTYPES) # Can be put into memory and pickled
        self.cursor = self.conn.cursor()
    def _createtable(self):
        self.cursor.execute("""CREATE TABLE transactions(txnid integer primary key, symbol text,
                            shares decimal, activity integer, price decimal, datestamp timestamp )""")

    def _insert(self, symbol, shares, activity, price, datestamp, datefmt='%m/%d/%Y %H:%M:%S'):
        '''Inserts a transaction into the database. Should be performing some pretty decent typechecking here
        12/25/2012 12:04'''
        mydate  = datetime.strptime(datestamp, datefmt)
        self.cursor.execute("INSERT INTO transactions VALUES(NULL, ?, ?, ?, ?, ?)", (symbol, shares, activity,
                                                                                         price, mydate))
        self.conn.commit()

    def _delete(self, txnid):
        self.cursor.execute("DELETE FROM transactions WHERE txnid = {}".format(txnid))

    def _allrows(self):
        self.cursor.execute("SELECT * from transactions")
        return self.cursor.fetchall()

    def _printfetchall(self):
        for row in self.cursor.fetchall():
            print row

    def _groupsymbols(self, symbol, activity=1):
        self.cursor.execute("""SELECT symbol, sum(shares), sum(shares * price) as cost
from transactions where symbol = ? and activity = ?""", (symbol, activity))
        
if __name__ == '__main__':
    import random
    t = TransactionDB('test.db')
    for i in range(10):
        txn1 = ('RY', random.randint(1,100), random.randint(0,1), round(random.uniform(50,100),2), '07/14/2013 13:08:14')
        t._insert(txn1[0], txn1[1], txn1[2], txn1[3], txn1[4])
    


