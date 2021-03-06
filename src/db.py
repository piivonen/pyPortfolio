import sqlite3
from datetime import datetime
from decimal import Decimal
import logging

class TransactionDB():
    def __init__(self, fname):
        sqlite3.register_adapter(Decimal, lambda x:str(x))
        sqlite3.register_converter('decimal', Decimal)
        logging.info('Connecting to database.')
        self.conn = sqlite3.connect(fname, detect_types=sqlite3.PARSE_DECLTYPES) # Can be put into memory and pickled
        self.cursor = self.conn.cursor()

    def getconn(self):
        return self.conn
        
    def createtable(self, tblname, fields):
        '''Create a table, fields is a dictionary with column names as keys
        and all other options as values
        '''
        first = True
        s = 'CREATE TABLE if not exists "{}" ('.format(tblname)
        for col, options in fields.items():
            if first: 
                s += col + ' ' + options
                first = False
            else :
                s += ', ' + col + ' ' + options
        s += ')'
        logging.debug('Creating table: {}'.format(tblname))
        self.cursor.execute(s)

    def createindex(self, tblname, idxname, cols, unique=False):
        s = 'CREATE  '
        if unique:
            s += 'UNIQUE INDEX '
        else:
            s += 'INDEX '
        s += idxname + ' on ' + tblname + ' (' + cols + ')'
        self.cursor.execute(s)

        
    def insertrow(self, tblname, row):
        '''Inserts a transaction into the database. Rows is a dictionary of
        column names as keys and values as..values. Typechecking should be
        performed earier in the chain.
        '''
        self.cursor.execute('INSERT INTO "{}" values('.format(
                                tblname) + ','.join("?" * len(row)) + ')', row)
        self.conn.commit()

    def deletetxn(self, tblname, txnid):
        self.cursor.execute("DELETE FROM {} WHERE txnid = {}".format(tblname,
                                                                     txnid))

    def allrows(self, tblname):
        self.cursor.execute("SELECT * from `?`", tblname)
        return self.cursor.fetchall()

    def exists(self, col, tbl):
            self.cursor.execute("SELECT {} from {}".format(col, tbl))
            if self.cursor.fetchall():
                return True
            return False
        
    def _printfetchall(self):
        for row in self.cursor.fetchall():
            print row

    def _print10(self, tblname):
        self.cursor.execute("SELECT * from {}".format(tblname))
        for n, row in enumerate(self.cursor.fetchall()):
            print row
            if n >= 10:
                break
        
if __name__ == '__main__':
    d = TransactionDB('test.db')
    

