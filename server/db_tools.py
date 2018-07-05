# Author Dalin Akrasi
# Student no.1528923
#
#
#
#

from collections import Counter
from db_interface import DbInterface
import tweet_tools as twtools
from pprint import pprint




db = DbInterface()

def isSameYear(_tweet):
    return db.isYearExisting(_tweet)

def isSameMonth(_tweet):
    month = twtools.getTweetMonth(_tweet)
    year = twtools.getTweetYear(_tweet)
    yearID = db.getYearID(year)
    return db.isMonthExisting(month, yearID)

def isSameWeek(week, month, year):
    return  db.isWeekExisting(week, month,  year)



def insertTweet(value, tweet):
    message = tweet.get('text')
    time = twtools.normaliseDate(tweet.get('created_at'))
    unique_id = int(tweet.get('id_str'))
    db.insertTweet(value, message, time, unique_id)


def checkYear(_tweet):
    year = twtools.getTweetYear(_tweet)
    db.setCurrentYear(year)
    yearID = db.getCurrentYearID()
    db.updateYear(db.generateYearAverage(yearID), yearID)



def checkMonth(_tweet):
    month = twtools.getTweetMonth(_tweet)
    year = twtools.getTweetYear(_tweet)
    yearID = db.getCurrentYearID()
    db.setCurrentMonth(month)
    db.updateMonth(db.generateMonthAverage(db.getCurrentMonthID()), db.getCurrentMonthID())


def checkWeek(_tweet):
    month = twtools.getTweetMonth(_tweet)
    year = twtools.getTweetYear(_tweet)

    day = twtools.getTweetDay(_tweet)
    week = twtools.getWeekFromDay(day)
    rng = twtools.getRangeFromWeek(week)
    db.setCurrentWeek(week)


    if isSameWeek(week, month, year):
        db.setCurrentWeekID(week, db.getMonthID(month, year))
        db.updateWeek(db.generateWeekAverage(rng), db.getCurrentWeekID())
    else:
        db.insertYear(0, year)
        yearID = db.getYearID(year)
        db.setCurrentYearID(yearID)
        db.insertMonth(0, month, db.getCurrentYearID())
        db.setCurrentMonthID(month, db.getCurrentYearID())
        db.insertWeek(db.generateWeekAverage(rng), week, db.getCurrentMonthID())




def refresh(_tweet):
    checkWeek(_tweet)
    checkMonth(_tweet)
    checkYear(_tweet)

def connectDB():
    db.connectDB()

def connectCursor():
    db.connectCursor()

def setUpDatabase():
    db.setup()

def getUser(username, password):
    return db.getUser(username, password)

def getUsers():
    return db.getUsers()

def removeUser(username):
    db.removeUser(username)

def addUser(username, password):
    return db.insertUser(username,password)

def updateUser(username, password):
    db.updateUser(username, password)

def getLiveValue(_id):
    return db.getLiveValue(_id)

def getAllLiveValues():
    return db.getAllLiveValues()

def getWeekAverage(week, month, year):
    return db.getWeekAverage(week, month, year)

def getAllWeeksAverages(month, year):
    return db.getAllWeeksAverages(month, year)

def getMonthAverage(month, year):
    return db.getMonthAverage(month, year)

def getAllMonthsAverages(year):
    return db.getAllMonthsAverages(year)

def getAllYearsAverages():
    res = dict()
    for year in db.getAllYears():
        res[year[0]] = getAllMonthsAverages(year[0])
    return res

def getAllYearsAverages3():
    print 'my year____s_______',db.getAllYears()[0][0]
    res = []
    for year in db.getAllYears():
        res.append({year[0] :{x:y for x,y in getAllMonthsAverages(year[0])}})
    return res

def getAllYearsAverages2():
    print 'my year____s_______',db.getAllYears()[0]
    res = []
    for year in db.getAllYears():
        res.append({'year':{'numeric':year[0], 'value':year[1]}, 'months':{x:y for x,y in getAllMonthsAverages(year[0])}})
    return res

        # res.append({
        # 'year':{
        #     'numeric':year[0],
        #     'value':year[1]},
        #     'months': {
        #         {'numeric': getAllMonthsAverages(year[0])[0],
        #         'value':getAllMonthsAverages(year[0])[1],
        #         'weeks': getAllWeeksAverages(year[0])[1]},
        #
        #         {'numeric': getAllMonthsAverages(year[0])[0],
        #         'value':getAllMonthsAverages(year[0])[1],
        #         'weeks': getAllWeeksAverages(year[0])[1]},
        #
        #         {'numeric': getAllMonthsAverages(year[0])[0],
        #         'value':getAllMonthsAverages(year[0])[1],
        #         'weeks': getAllWeeksAverages(year[0])[1]}
        #     }
        # })


def getYearAverage(year):
    return db.getYearAverage(year)
