from flask import Flask, render_template, flash, redirect, request, url_for,session
import os
import requests


app = Flask(__name__)

app.secret_key = os.urandom(12)


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/out')
def out():
    session['logged_in'] = False
    return home()

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():

    login = "admin"
    password = "123"
    #dictToSend = {'cmd': 'login', "pas": request.form['pass'], "login": request.form['username']}
    #res = requests.post('http://192.168.31.195:5000/tests/endpoint', json=dictToSend).json()
    #print(res["answer"]['ans'])
    #if request.form['pass'] == password and request.form['username'] == login:
    return redirect(url_for("main"))
    """
    if True:#res["answer"]['ans'] == "Authorization success":
        session['logged_in'] = True
        print(url_for("main"))
        return redirect(url_for("main"))
    else:
        flash('wrong password!')
        return home()
    """



@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/friends')
def friends():
    return render_template('friends.html')

@app.route('/groups')
def groups():
    return render_template('groups.html')

@app.route('/notify')
def notify():
    return render_template('notify.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    return render_template('reg.html')

if __name__ == '__main__':
    app.run()
