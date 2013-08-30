import portfolio
import logging
import csv_import
import sys
import os

def init_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='log.txt',
        filemode='w',
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        )
    if not hasattr(sys, 'frozen'):
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(message)s',
            '%H:%M:%S',
        )
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    init_logging()
    dbname = 'portfolio.db'
    mp = portfolio.Portfolio('portfolio.db', 1)
    tp = portfolio.Portfolio('portfolio.db', 2)
    rp = portfolio.Portfolio('portfolio.db', 3)
    csvdir = os.path.join(os.getcwd(), 'csv')
    margintxn = csv_import.import_qt_tradehistory(os.path.join(csvdir,'margin.csv'))
    tsfatxn = csv_import.import_qt_tradehistory(os.path.join(csvdir,'tsfa.csv'))
    rrsptxn = csv_import.import_qt_tradehistory(os.path.join(csvdir,'rrsp.csv'))
    
    marginact = csv_import.import_qt_activity(os.path.join(csvdir,'mactivity.csv'))
    tsfaact = csv_import.import_qt_activity(os.path.join(csvdir,'tactivity.csv'))
    rrspact = csv_import.import_qt_activity(os.path.join(csvdir,'ractivity.csv'))
