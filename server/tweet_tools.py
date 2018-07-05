# Author Dalin Akrasi
# Student no.1528923
#
#
#
#
from datetime import datetime

def normaliseDate(date):
    d = (date).split('+0000')
    dd = d[0]+d[1]
    ddd = datetime.strptime(dd, '%a %b %d %H:%M:%S %Y')
    return str(ddd)



def _getDayFromDate(_date):
    # given a date string it returns the day value
    return int(str(normaliseDate(_date).split(' ')[0]).split('-')[2])



def _getMonthFromDate(_date):
    # given a date string it returns the month value
    return int(str(normaliseDate(_date).split(' ')[0]).split('-')[1])



def _getYearFromDate(_date):
    # given a date string it returns the year value
    return int(str(normaliseDate(_date).split(' ')[0]).split('-')[0])



def getTweetDay(_tweet):
    # given a tweet it returns the day in which it was posted
    return _getDayFromDate(_tweet.get('created_at'))



def getTweetMonth(_tweet):
    # given a tweet it returns the month in which it was posted
    return _getMonthFromDate(_tweet.get('created_at'))



def getTweetYear(_tweet):
    # given a tweet it returns the year in which it was posted
    return _getYearFromDate(_tweet.get('created_at'))



def getWeekFromDay(_day):
    # given a monthly day of the week it returns which week it is part of
    if 1 <= int(_day) <= 31:
        if int(_day) in range(1,8): return 1
        elif int(_day) in range(8,15): return 2
        elif int(_day )in range(15,22): return 3
        elif int(_day) in range(22,29): return 4
        else: return 5



def getRangeFromWeek(_week):
    # uses week number to return a range of days that curresponds to that week
    if 1 <= int(_week) <= 5:
        if _week == 1: return (1,7)
        elif _week == 2: return (8,14)
        elif _week == 3: return (15,21)
        elif _week == 4: return (22,28)
        elif _week == 5: return (29,31)
