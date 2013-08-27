def parsedate(date):
    '''Return a datetime object for a date in the form "%Y-%m-%d %H:%M:%S"'''
    try:
        return datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]),
        int(date[11:13]), int(date[14:16]), int(date[17:19]))
    except Exception, e:
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
