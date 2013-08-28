import datetime

def parse_fulldate(date):
    '''Return a datetime object for a date in the form "%Y-%m-%d %H:%M:%S"'''
    try:
        return datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]),
        int(date[11:13]), int(date[14:16]), int(date[17:19]))
    except Exception, e:
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

def parse_shortdate(date, fmt="%d/%m/%y"):
    '''Returns a datetime from a text-format date. Default is day/month/year'''
    return datetime.datetime.strptime(date, fmt)
def convert_pformat(s):
    '''Converts from paranthesis format (3.94) to normal -3.98. Removes thousand separator.
    Returns string, convert elsewhere as needed to Decimal.
    '''
    if '(' in s:
        return '-' + s.translate(None, "(),")
    return s.translate(None, ",")
        
