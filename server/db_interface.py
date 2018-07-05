# Author Dalin Akrasi
# Student no.1528923
#
#
#
#

import sqlite3
from datetime import date
import tweet_tools as twtools


class DbInterface:

    def __init__(self):
        self.conn = ''
        self.setCurrents()


    def setCurrents(self):
        self.current_day = date.today().day

        self.current_week = twtools.getWeekFromDay(self.current_day)
        self.current_week_id = 1

        self.current_month = date.today().month
        self.current_month_id = 1

        self.current_year = date.today().year
        self.current_year_id = 1

        self.existing_years = []

    def setup(self):
        self.connectDB()
        self.connectCursor()
        self.createTables()

    def connectDB(self):
        self.conn = sqlite3.connect('moodbarometer.db')

    def createTables(self):
        self.createYearTable()
        self.createMonthTable()
        self.createWeekTable()
        self.createTweetTable()
        self.createUserTable()


    def initialiseTables(self,_week, _month, _monthID, _year, _yearID):
        self.insertYear(0,_year)
        self.insertMonth(0,_month, _yearID)
        self.insertWeek(0,_week, _monthID)
        self.existing_years.append(_year)


    def saveChanges(self):
        self.conn.commit()
        self.cursor.close()


    def connectCursor(self):
        self.cursor = self.conn.cursor()

    def isWeekExisting(self, _week, _month, _year):
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(id ,0)
                        FROM WeekTable
                        WHERE week = ? AND month = (SELECT id FROM MonthTable WHERE month = ?
                        AND year = (SELECT id FROM YearTable WHERE year = ? ) )'''
                        ,(_week,_month, _year))

        res = self.cursor.fetchone()
        if res ==  None:
            return False
        else:
            return True


    def isMonthExisting(self, _month, _yearID):
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(id ,0)
                        FROM MonthTable
                        WHERE month = ? AND year = ?'''
                        ,(_month,_yearID))

        res = self.cursor.fetchone()
        if res ==  None:
            return False
        else:
            return True



    def isYearExisting(self, _year):
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(id ,0)
                        FROM YearTable
                        WHERE year = ?'''
                        ,(_year,))
        res = self.cursor.fetchone()

        if res == None:
            return False
        else: return True


    # _________________________________________________________create

    def createUserTable(self):
        # create tweets table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UserTable(
                        id INTEGER PRIMARY KEY,
                        username REAL NOT NULL,
                        password TEXT NOT NULL,
                        UNIQUE(username))''')


    def createTweetTable(self):
        # create tweets table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TweetTable(
                        id INTEGER PRIMARY KEY,
                        value REAL NOT NULL,
                        tweet TEXT NOT NULL,
                        time TEXT NOT NULL,
                        statusID INTEGER NOT NULL,
                        UNIQUE(time, statusID))''')


    def createWeekTable(self):
        # create week table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WeekTable(
                        id INTEGER PRIMARY KEY,
                        value REAL NOT NULL DEFAULT 0,
                        week INTEGER NOT NULL,
                        month INTEGER NOT NULL,
                        UNIQUE(week, month),
                        FOREIGN KEY(month) REFERENCES MonthTable(id))''')


    def createMonthTable(self):
        # create month table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS MonthTable(
                        id INTEGER PRIMARY KEY,
                        value REAL NOT NULL DEFAULT 0,
                        month INTEGER NOT NULL,
                        year INTEGER NOT NULL,
                        UNIQUE(month, year),
                        FOREIGN KEY(year) REFERENCES YearTable(id))''')


    def createYearTable(self):
        # create year table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS YearTable(
                        id INTEGER PRIMARY KEY,
                        value REAL NOT NULL DEFAULT 0,
                        year INTEGER NOT NULL,
                        UNIQUE(year))''')


    # _________________________________________________________setters

    def insertUser(self,_username, _password):
        response = True
        self.connectCursor()
        try:
            self.cursor.execute('INSERT INTO UserTable(username, password) VALUES(?,?)',(_username, _password))
        except sqlite3.IntegrityError:
            response = False
            print "____USER____already EXISTS________"
        self.saveChanges()
        return response

    def removeUser(self,_username):
        self.connectCursor()
        try:
            self.cursor.execute('DELETE FROM UserTable WHERE username = ?',(_username,))
        except sqlite3.IntegrityError:
            print "____USER____DOESNT EXISTS________"
        self.saveChanges()

    def updateUser(self,_username, _password):
        self.connectCursor()
        self.cursor.execute('''UPDATE UserTable
                            SET password = ?
                            WHERE username= ?'''
                        ,(_password,_username))
        self.saveChanges()


    def insertTweet(self,_value, _tweet, _time, _statusID):
        self.connectCursor()
        try:
            self.cursor.execute('INSERT INTO TweetTable(value, tweet, time, statusID) VALUES(?,?,?,?)',(_value, _tweet, _time, _statusID))
        except sqlite3.IntegrityError:
            print "____item with ID___",_statusID,"__and date:",str(_time),"____already EXISTS________"
        self.saveChanges()


    def insertWeek(self,_value, _week, _monthID):
        try:
            self.connectCursor()
            self.cursor.execute('''INSERT INTO WeekTable(value, week, month)
                                VALUES(?,?,?)'''
                            ,(_value, _week,_monthID))
        except sqlite3.IntegrityError:
            print "____item with ID___",_statusID,"____already EXISTS________"
        self.saveChanges()


    def updateWeek(self,_value, _id):
        self.connectCursor()
        self.cursor.execute('''UPDATE WeekTable
                            SET value = ?
                            WHERE id=?'''
                        ,(_value,_id))
        self.saveChanges()


    def insertMonth(self,_value, _month, _yearID):
        try:
            self.connectCursor()
            self.cursor.execute('''INSERT INTO MonthTable(value, month, year)
                            VALUES(?,?,?)''',(_value, _month, _yearID))
        except sqlite3.IntegrityError:
            print "____month___",_month,"____already EXISTS________"
        self.saveChanges()


    def updateMonth(self,_value, _id):
        self.connectCursor()
        self.cursor.execute('''UPDATE MonthTable
                            SET value = ?
                            WHERE id=?'''
                        ,(_value,_id))
        self.saveChanges()



    def insertYear(self,_value, _year):
        try:
            self.connectCursor()
            self.cursor.execute('''INSERT INTO YearTable(value, year)
                                VALUES(?,?)'''
                                ,(_value, _year))
        except sqlite3.IntegrityError:
            print "____year___",_year,"____already EXISTS________"
        self.saveChanges()


    def updateYear(self,_value, _id):
        self.connectCursor()
        self.cursor.execute('''UPDATE YearTable
                            SET value = ?
                            WHERE id=?'''
                        ,(_value,_id))
        self.saveChanges()


    # _________________________________________________________getters
    def getUser(self, _username, _password):
        self.connectCursor()
        self.cursor.execute('''SELECT id FROM UserTable
                                WHERE username = ? AND
                                password = ?''',(_username, _password))
        res = self.cursor.fetchone()
        if res ==  None:
            return False
        else:
            return True

    def getUsers(self):
        self.connectCursor()
        self.cursor.execute('SELECT * FROM UserTable')
        res = self.cursor.fetchall()
        if res ==  []:
            return ''
        else:
            return res

    def getLiveValue(self,_id):
        self.connectCursor()
        self.cursor.execute('SELECT IFNULL(value,0), IFNULL(tweet,0), IFNULL(time,0)  FROM TweetTable WHERE id = ?',(_id,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]


    def getYears(self):
        self.connectCursor()
        self.cursor.execute('SELECT year FROM YearTable')
        res = self.cursor.fetchall()
        if res == []:
            return [0]
        else:
            return res[0]


    def getAllLiveValues(self):
        self.connectCursor()
        self.cursor.execute('SELECT IFNULL(value,0), IFNULL(tweet,0), IFNULL(time,0) FROM TweetTable')
        return self.cursor.fetchall()


    def getTweet(self,_id):
        self.connectCursor()
        self.cursor.execute('SELECT IFNULL(value,0) FROM TweetTable WHERE id = ?',(_id,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]

    def getAllTweets(self):
        self.connectCursor()
        self.cursor.execute('SELECT * FROM TweetTable')
        return self.cursor.fetchall()




    def getWeekAverage(self,_week, _month,_year):
        # get week avg having YEAR and MONTH and then DAY
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(value ,0)
                        FROM WeekTable
                        WHERE week = ?
                        AND month = (SELECT id FROM MonthTable WHERE month = ?
                        AND year = (SELECT id FROM YearTable WHERE year = ?))'''
                        ,(_week,_month,_year))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]


    def getAllWeeksAverages(self,_month, _year):
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(week ,0), IFNULL(value ,0)
                        FROM WeekTable
                        WHERE month = (SELECT id FROM MonthTable WHERE month = ?
                        AND year = (SELECT id FROM YearTable WHERE year = ? ) )
                        '''
                        ,(_month, _year))
        res = self.cursor.fetchall()
        if res != []:
            return res
        else:
            return 0



    def generateWeekAverage(self,_range):
        # get week avg having YEAR and MONTH and then DAY
        self.connectCursor()
        self.cursor.execute('''SELECT avg(value)
                        FROM TweetTable
                        WHERE CAST(strftime("%d", time) AS INT)
                        between ? AND ?'''
                        ,(_range))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]



    def getMonthID(self,_month, _year):
        self.connectCursor()
        self.cursor.execute('''SELECT id
                        FROM MonthTable
                        WHERE month = ? AND year = (SELECT id FROM YearTable WHERE year = ?)'''
                        ,(_month, _year))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]



    def getMonthAverage(self,_month, _year):
        # get week avg having YEAR and MONTH
        self.connectCursor()
        self.cursor.execute('''SELECT value
                            FROM MonthTable
                            WHERE month = ? AND
                            year = (SELECT id FROM YearTable WHERE year = ? )''',
                            (_month,_year))
        self.conn.commit();
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]


    def getAllMonthsAverages(self,_year):
        self.connectCursor()
        self.cursor.execute('''SELECT IFNULL(month ,0), IFNULL(value,0)
                            FROM MonthTable
                            WHERE year = (SELECT id FROM YearTable WHERE year = ? )''',
                            (_year,))
        res = self.cursor.fetchall()
        if res != []:
            return res
        else:
            return 0

    def generateMonthAverage(self,_monthID):
        self.connectCursor()
        self.cursor.execute('''SELECT avg(value)
                        FROM WeekTable
                        WHERE CAST(month AS INT) = ?'''
                        ,(_monthID,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]




    def getYearAverage(self,_year):
        self.connectCursor()
        self.cursor.execute("SELECT value FROM YearTable WHERE CAST(year AS INT) = ?", (_year,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]

    def generateYearAverage(self,_yearID):
        self.connectCursor()
        self.cursor.execute('''SELECT avg(value)
                        FROM MonthTable
                        WHERE CAST(year AS INT) = ?'''
                        ,(_yearID,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]



    # ---------------------------------------------------CURRENT WEEK
    def getCurrentDay(self):
        return self.current_day

    def getCurrentWeek(self):
        return int(self.current_week)

    def setCurrentWeek(self,_week):
        self.current_week = int(_week)

    def getCurrentWeekID(self):
        return self.current_week_id

    def setCurrentWeekID(self,_week, _monthID):
        self.connectCursor()
        self.cursor.execute("SELECT id FROM WeekTable WHERE week = ? AND month = ?", (_week,_monthID))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            self.current_week_id = int(res[0])

    def actualiseWeek(self,_week, _monthID):
        self.setCurrentWeekID(_week, _monthID)
        self.setCurrentWeek(_week)

    # ---------------------------------------------------CURRENT MONTH

    def getCurrentMonth(self):
        return int(self.current_month)

    def setCurrentMonth(self,_month):
        self.current_month = int(_month)

    def getCurrentMonthID(self):
        return self.current_month_id

    def setCurrentMonthID(self,_month, _yearID):
        self.connectCursor()
        self.cursor.execute("SELECT id FROM MonthTable WHERE CAST(month AS INT) = ? AND CAST(year AS INT) = ?", (_month, _yearID))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            self.current_month_id =  int(res[0])

    def actualiseMonth(self,_month, _yearID):
        self.setCurrentMonthID(_month, _yearID)
        self.setCurrentMonth(_month)

    # ---------------------------------------------------CURRENT YEAR

    def getAllYears(self):
        self.connectCursor()
        self.cursor.execute("SELECT year, value FROM YearTable")
        res = self.cursor.fetchall()
        if res != []:
            return res
        else:
            return []


    def getCurrentYear(self):
        # gets local (self.year number egs 2017)
        return int(self.current_year)


    def setCurrentYear(self,_year):
        # sets local (self.year number egs 2017)
        self.current_year = int(_year)


    def getCurrentYearID(self):
        # gets local (self.year id)
        return self.current_year_id

    def getYearID(self, _year):
        self.connectCursor()
        self.cursor.execute("SELECT id FROM YearTable WHERE year = ?", (_year,))
        res = self.cursor.fetchone()
        if res ==  None:
            return 0
        else:
            return res[0]



    def setCurrentYearID(self,_yearID):
        # sets local (self.year id)
        self.current_year_id =  int(_yearID)


    def actualiseYear(self,_year):
        # updates local (self.year id)
        self.setCurrentYearID(_year)
        self.setCurrentYear(_year)
