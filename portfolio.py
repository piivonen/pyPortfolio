import db

class Portfolio():
    def __init__(self, dbname, tbl):
        self.db = db.TransactionDB(dbname)
        self.tbl = tbl

    def get_transactions(self):
        return self.db.allrows(self.tbl, '*')
        
