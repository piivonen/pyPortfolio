import portfolio
import logging
import csv_import
import sys

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
    mp = portfolio.Portfolio('portfolio.db', 1)
    tp = portfolio.Portfolio('portfolio.db', 2)
    rp = portfolio.Portfolio('portfolio.db', 3)
    margintxn = csv_import.import_qt_tradehistory('margin.csv')
    tsfatxn = csv_import.import_qt_tradehistory('tsfa.csv')
    rrsptxn = csv_import.import_qt_tradehistory('rrsp.csv')
    
    marginact = csv_import.import_qt_activity('mactivity.csv')
    tsfaact = csv_import.import_qt_activity('tactivity.csv')
    rrspact = csv_import.import_qt_activity('ractivity.csv')
    


