from flask import Flask, render_template, url_for, request, session, redirect, g, jsonify
import hashlib, os
import server.controller as controller

app = Flask(__name__)
app.secret_key = os.urandom(24)
isFirstTime = True

@app.route('/mood-barometer')
def index():
    if g.user:
        checkSession()


        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/registration')
def registration():
    controller.setupDB()
    controller.connectDB()
    return render_template('registration.html')

@app.route('/admin', methods=['POST'])
def admin():
    if request.form['submit'] == 'add':
        username = request.form['username']
        password = request.form['password']
        if password.strip() != '':
            user = controller.addUser(username, password)
            print '_____add it=',user, '__and=', controller.getUsers()

    elif request.form['submit'] == 'remove':
        username = request.form['username']
        controller.removeUser(username)
        print '_____remove it=', controller.getUsers()
    return redirect(url_for('registration'))



@app.route('/', methods=['GET','POST'])
def login():
    controller.setupDB()
    controller.connectDB()
    if g.user:
        return render_template('index.html')
    if request.method == 'POST':
        session.pop('user', None)
        user = request.form['username']
        password = request.form['password']

        print 'gotcha______',password
        if user in controller.getUserNames():
            if controller.getUser(user, password):
                session['user'] = request.form['username']
                return redirect(url_for('index'))

    return render_template('login.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def dropSession():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/update',methods=['POST'])
def updatePassword():
    print 'user is====',request.json.get('user')
    print 'pass is====',request.json.get('npassword')
    user = request.json.get('user')
    opassword = request.json.get('opassword')
    npassword = request.json.get('npassword')
    if user in controller.getUserNames():
        if controller.getUser(user, opassword):
            controller.updateUser(user, npassword)
            print controller.getUsers()
            session.pop('user',None)
            return '/'
    return ''




@app.route('/_data_req')
def testy():
    try:
        req = request.args.get('req')
        if str(req).lower() == 'graph_data':
            return jsonify(response=controller.parcel(session['user']))
        else:
            return jsonify(response='try again')
    except Exception, e:
        return(str(e))

def checkSession():

    if isFirstTime:
        print("I'm about to change it______was=",isFirstTime)
        global isFirstTime
        controller.processTweets()
        isFirstTime = False
    else:
        controller.connectDB()
    print("it is_______",isFirstTime)


if __name__ == '__main__':
    app.run(debug=True)
