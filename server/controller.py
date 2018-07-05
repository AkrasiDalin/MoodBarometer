import twitter_api
import db_tools
from classifier import Classifier
from textblob import TextBlob
tweets = twitter_api.getLocalData()


def setupDB():
    db_tools.setUpDatabase()

def connectDB():
    db_tools.connectDB()
    db_tools.connectCursor()


def processTweets():
    for tweet in tweets:

        analysis = TextBlob(tweet.get('text'))
        val = analysis.polarity
        # value = classifier.classify(tweet.get('text'))
        db_tools.insertTweet(val, tweet)
        db_tools.refresh(tweet)

def getUser(username, password):
    return db_tools.getUser(username, password)

def getUsers():
    return db_tools.getUsers()

def getUserNames():
    usernames = [x[1] for x in db_tools.getUsers()]
    return usernames

def removeUser(username):
    db_tools.removeUser(username)

def addUser(username, password):
    return db_tools.addUser(username,password)

def updateUser(username, password):
    db_tools.updateUser(username, password)


def getLiveValue(id):
    return db_tools.getLiveValue(id)

def getAllLiveValues():
    return db_tools.getAllLiveValues()

def getWeekAverage(week, month, year):
    return db_tools.getWeekAverage(week, month, year)

def getAllWeeksAverages(month, year):
    return db_tools.getAllWeeksAverages(month,year)

def getMonthAverage(month, year):
    return db_tools.getMonthAverage(month, year)

def getAllMonthsAverages(year):
    return db_tools.getAllMonthsAverages(year)

def getYearAverage(year):
    return db_tools.getYearAverage(year)

def getAllYearsAverages():
    return db_tools.getAllYearsAverages()

def parcel(user_ID):
    obj = {
    'user_id': user_ID,
    'dates_table':db_tools.getAllYearsAverages2(),
    'live': serializeLive(db_tools.getAllLiveValues())
    }
    return obj


def serializeLive(obj):
    temp = []
    for o in obj:
        item = {
           'value': o[0],
           'time': o[2],
           'text': o[1]
           }
        temp.append(item)
    return temp
