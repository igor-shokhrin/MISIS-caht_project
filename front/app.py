from flask import Flask, render_template, flash, redirect, request, url_for,session,jsonify,json
from flask_login import LoginManager,UserMixin,current_user, login_user,logout_user
import os
import requests


app = Flask(__name__)
login = LoginManager(app)
app.secret_key = os.urandom(12)
# ...
from flask_login import UserMixin
all_user = {}
class User(UserMixin):
    id_t = 0
    username = ""
    age = ""
    ava = ""
    birth = ""
    city = ""
    status = ""
    regtime = ""
    country = ""
    sex = ""
    curdial = 0
    def __init__(self, id):
        """Constructor"""
        self.id = id
    def getid(self):
        return self


@login.user_loader
def load_user(user):
    return User.getid(all_user[user])
ip = 'http://192.168.43.33:5000/tests/endpoint'
data_g = {}
@app.route('/main')
def main():

    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()

    print(current_user.id)
    data_i = {}
    data_i["dial"] = []
    data_i["mess_ch"] = []
    for d in res["answer"]:
        #print(current_user.id)
        dial = {}
        dial["id"] = d["id_dialog"]
        dial["text"] = d["description"]
        dial["url"] = d["id_dialog"]
        dial["name"] = d["Name"]
        dial["ava"] = d["photo"]
        dial["time"] = d["create_date"]

        if str(current_user.id) in d["users"]:
            data_i["dial"].append(dial)
    if data_i["dial"]:
        if not current_user.curdial:
            current_user.curdial = int(data_i["dial"][0]["id"])
        print(int(data_i["dial"][0]["id"]))
        dictToSend = {'cmd':'get_msg_from_dialog', "id_dialog": int(data_i["dial"][0]["id"])}
        m = requests.post(ip, json=dictToSend).json()
        for ms in m["answer"]:
            mess_in = {}
            mess_in["text"] = ms["msg"]
            mess_in["url"] = "/profile"
            mess_in["name"] = ms["first_name"] + " " + ms["last_name"]
            mess_in["ava"] = ms["photo"]
            mess_in["st"] = "in"
            if ms["id_user"] == current_user.id:
                mess_in["st"] = "out"
            mess_in["time"] = ms["time"]
            data_i["mess_ch"].append(mess_in)
    """
    data_in = {}
    data_in["name"] = "Никита Умников"
    data_in["mess_ch"] = []
    mess_in = {}
    mess_in["text"] = "Test which is a new approach to have all solutions"
    mess_in["url"] = "/profile"
    mess_in["name"] = "Игорь Шохрин"
    mess_in["ava"] = "https://ptetutorials.com/images/user-profile.png"
    mess_in["st"] = "in"
    mess_in["time"] = "11:01 AM | June 9"
    mess_out = {}
    mess_out["text"] = "Test which is a new approach to have all solutions"
    mess_out["name"] = "Игорь Шохрин"
    mess_out["st"] = "out"
    mess_out["time"] = "11:01 AM | June 9"
    data_in["mess_ch"].append(mess_in)
    data_in["mess_ch"].append(mess_out)
    data_in["mess_ch"].append(mess_in)
    data_in["mess_ch"].append(mess_in)
    data_in["mess_ch"].append(mess_out)
    data_in["mess_ch"].append(mess_in)
    data_in["dial"] = []
    dial = {}
    dial["text"] = "Test which is a new approach to have all solutions"
    dial["url"] = "/profile"
    dial["name"] = "Игорь Шохрин"
    dial["ava"] = "https://ptetutorials.com/images/user-profile.png"
    dial["time"] = "Dec 25"
    """

    #data_i["dial"].append(dial)
    #data_in["dial"].append(dial)
    #data_in["dial"].append(dial)
    #data_in["dial"].append(dial)
    #data_in["dial"].append(dial)

    #data = data_in
    """
    if request.form:
        dictToSend = {'cmd': 'send_msg', "text": request.form["msg"], "id_dialog": "1", "id_user":  int(current_user.id)}
        res = requests.post(ip, json=dictToSend).json()
    """
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('main.html',data_g=data_g,data=data_i)

@app.route('/out')
def out():
    logout_user()
    session['logged_in'] = False
    return home()


@app.route('/')
def home():
    #return render_template('index1.html')

    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for("main"))


@app.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    login = "1"
    password = "1"

    if request.form:
        dictToSend = {'cmd': 'login', "pas": request.form['pass'], "login": request.form['username']}
        res = requests.post(ip, json=dictToSend).json()
        #if request.form['pass'] == password and request.form['username'] == login:
        if res["answer"]['ans'] == "Authorization success":

            data_g["id"] = res["answer"]['id']
            session['logged_in'] = True
            dictToSend = {'cmd':'get_user_info', "id_user" : res["answer"]['id']}
            res = requests.post(ip, json=dictToSend).json()
            data_g["name"] = res["answer"]['first_name'] + ' ' + res["answer"]['last_name']
            user = User(data_g["id"])
            user.username = data_g["name"]
            user.id_t = data_g["id"]
            user.age = res["answer"]['age']
            user.ava = res["answer"]['photo']
            user.birth = res["answer"]['D_birth']
            user.city = res["answer"]['city']
            user.status = res["answer"]['status']
            user.regtime = "--"#res["answer"]['age']
            user.country = "--"#res["answer"]['age']
            user.sex = res["answer"]['sex']
            all_user[str(data_g["id"])] = user
            login_user(user)
            return redirect(url_for("main"))
    return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    if request.form:
        dictToSend = {'cmd': 'registration', "pas": request.form['pass'], "login": request.form['username']}
        res = requests.post(ip, json=dictToSend).json()
        print(res)
        dictToSend = {'cmd': 'login', "pas": request.form['pass'], "login": request.form['username']}
        res = requests.post(ip, json=dictToSend).json()
        # if request.form['pass'] == password and request.form['username'] == login:
        if res["answer"]['ans'] == "Authorization success":
            data_g["id"] = res["answer"]['id']
            session['logged_in'] = True
            user = User(data_g["id"])
            user.username = request.form['username']
            all_user[str(data_g["id"])] = user
            login_user(user)
            return redirect(url_for("main"))
    return render_template('reg.html')

@app.route('/regvk', methods=['GET', 'POST'])
def regvk():
    #if current_user.is_authenticated:
    #    return redirect(url_for("main"))
    if request.form:
        dictToSend = {'cmd': 'registration', "pas": request.form['pass'], "login": request.form['username']}
        res = requests.post(ip, json=dictToSend).json()
        print(res)
        dictToSend = {'cmd': 'login', "pas": request.form['pass'], "login": request.form['username']}
        res = requests.post(ip, json=dictToSend).json()
        # if request.form['pass'] == password and request.form['username'] == login:
        if res["answer"]['ans'] == "Authorization success":
            data_g["id"] = res["answer"]['id']
            session['logged_in'] = True
            user = User(data_g["id"])
            user.username = request.form['username']
            all_user[str(data_g["id"])] = user
            login_user(user)
            #return redirect(url_for("main"))
    return render_template('reg.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    dictToSend = {'cmd': 'get_msg_from_dialog', "id_dialog": 1}
    res = requests.post(ip, json=dictToSend).json()
    data_in = {}
    data_in["messages"] = []
    for m in res["answer"]:
        message = {}
        message["name"] = m["first_name"] + m["last_name"]
        message["message"] = m["msg"]
        message["profile"] = "/profile"
        message["ava"] = m["photo"]
        data_in["messages"].append(message)
    data = {}
    data["messages"] = []
    if request.form:
        for mes in data_in["messages"]:
            if request.form["searchtext"].lower() in mes["message"].lower():
                data["messages"].append(mes)
    return render_template('search.html', data=data,data_g=data_g)


@app.route('/groups')
def groups():
    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()
    data_in = {}
    data_in["groups"] = []
    for d in res["answer"]:
        group = {}
        group["name"] = d["Name"]
        group["descr"] = "Описание"
        group["url"] = d["id_dialog"]
        group["ava"] = d["photo"]
        if str(current_user.id) in d["users"]:
            data_in["groups"].append(group)


    data = data_in
    return render_template('groups.html', data=data,data_g=data_g)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    dictToSend = {'cmd': 'get_user_from_dialog', "id_dialog": int(request.form["id"])}
    #dictToSend = {'cmd':'get_user_from_dialog', "id_dialog": request.form["id"]}
    res = requests.post(ip, json=dictToSend).json()
    print(res)
    data_in = {}
    data_in["name"] = "Никита Умников"
    data_in["members"] = []
    member = {}
    member["name"] = "Игорь Шохрин"
    member["status"] = "Привет всем!"
    member["url"] = "/profile"
    member["ava"] = "https://ptetutorials.com/images/user-profile.png"
    data_in["members"].append(member)
    data_in["members"].append(member)
    data_in["members"].append(member)
    data_in["members"].append(member)
    data = data_in

    return render_template('friends.html',data=data,data_g=data_g)

@app.route('/notify')
def notify():
    data_in = {}
    data_in["name"] = "Никита Умников"
    data_in["notifyes"] = []
    notify = {}
    notify["name"] = "Дата совещания"
    notify["text"] = "Совещание назначено на 8 апреля"
    data_in["notifyes"].append(notify)
    notify1 = {}
    notify1["name"] = "Вы были приглашены в диалог"
    notify1["text"] = "Вы были приглашены в диалог: 'Менеджеры'"
    data_in["notifyes"].append(notify1)
    notify2 = {}
    notify2["name"] = "Молодец"
    notify2["text"] = "Альбина, хорошая работа"
    data_in["notifyes"].append(notify2)
    data = data_in
    return render_template('notify.html',data=data,data_g=data_g)

@app.route('/profile', methods=['GET', 'POST']  )
def profile():
    dictToSend = {'cmd': 'get_user_info', "id_user": data_g["id"]}
    res = requests.post(ip, json=dictToSend).json()
    #data_g["id"] = res["answer"]['last_name']
    profile = {}
    profile["name"] = data_g["name"]
    profile["country"] = "Россия"
    profile["status"] = res["answer"]['status']
    profile["regdate"] = "12-06-2016"
    profile["bd"] = res["answer"]['D_birth']
    profile["city"] = res["answer"]['city']
    profile["sex"] = res["answer"]['sex']
    profile["age"] = res["answer"]['age']
    profile["ava"] = res["answer"]['photo']
    data_g["profile"] = profile
    """
    data = {}
    data["name"] = "Никита Умников"
    profile = {}
    profile["name"] = "Иван Пупкин"
    profile["country"] = "Россия"
    profile["status"] = "Здарова"
    profile["regdate"] = "12-06-2016"
    profile["lastseen"] = "	12-06-2016 / 09:11"
    profile["city"] = "Киев"
    profile["sex"] = "Мужской"
    profile["age"] = "11"
    profile["ava"] = "http://m.168.ru/files/news/mob/161538237725.jpg"
    data["profile"] = profile
    """
    return render_template('profile.html',data_g=data_g)

@app.route('/calen')
def calen():
    data = {}
    data["name"] = "Никита Умников"
    return render_template('calen.html',data_g=data_g)

@app.route('/index')
def index():
    data = {}
    data["name"] = "Никита Умников"
    return render_template('index.html',data_g=data_g)


@app.route('/_add_numbers')
def add_numbers():
    print(1)
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/get_len', methods=['GET', 'POST'])
def get_len():
    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()

    data_i = {}
    data_i["dial"] = []
    data_i["mess_ch"] = []
    dial = {}

    for d in res["answer"]:
        #print(current_user.id)
        dial["id"] = d["id_dialog"]
        dial["text"] = d["description"]
        dial["url"] = d["id_dialog"]
        dial["name"] = d["Name"]
        dial["ava"] = d["photo"]
        dial["time"] = d["create_date"]
        if str(current_user.id) in d["users"]:
            data_i["dial"].append(dial)
    if current_user.curdial:
        dictToSend = {'cmd':'get_msg_from_dialog', "id_dialog": int(current_user.curdial)}
        m = requests.post(ip, json=dictToSend).json()
        for ms in m["answer"]:
            mess_in = {}
            mess_in["text"] = ms["msg"]
            mess_in["url"] = "/profile"
            mess_in["name"] = ms["first_name"] + " " + ms["last_name"]
            mess_in["ava"] = ms["photo"]
            mess_in["st"] = "in"
            mess_in["id"] = ms["id_user"]
            if ms["id_user"] == int(current_user.id):
                mess_in["st"] = "out"
            mess_in["time"] = ms["time"]
            data_i["mess_ch"].append(mess_in)

    return json.dumps({'len': data_i,'idd':current_user.id_t} if not current_user.is_anonymous else 0)

@app.route('/sm', methods=['GET', 'POST'])
def sm():

    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()
    if request.form:
        if request.form["msg"]:
            dictToSend = {'cmd': 'send_msg', "text": request.form["msg"], "id_dialog": int(current_user.curdial),"id_user": int(current_user.id)}
            requests.post(ip, json=dictToSend).json()
    data_i = {}
    data_i["dial"] = []
    data_i["mess_ch"] = []
    dial = {}

    for d in res["answer"]:
        #print(current_user.id)
        dial["id"] = d["id_dialog"]
        dial["text"] = d["description"]
        dial["url"] = d["id_dialog"]
        dial["name"] = d["Name"]
        dial["ava"] = d["photo"]
        dial["time"] = d["create_date"]
        if str(current_user.id) in d["users"]:
            data_i["dial"].append(dial)
    print("pepa1")
    print(current_user.curdial)
    if current_user.curdial:
        print("pepa")
        print(current_user.curdial)
        dictToSend = {'cmd':'get_msg_from_dialog', "id_dialog": int(current_user.curdial)}
        m = requests.post(ip, json=dictToSend).json()
        for ms in m["answer"]:
            mess_in = {}
            mess_in["text"] = ms["msg"]
            mess_in["url"] = "/profile"
            mess_in["name"] = ms["first_name"] + " " + ms["last_name"]
            mess_in["ava"] = ms["photo"]
            mess_in["st"] = "in"
            mess_in["id"] = ms["id_user"]
            if ms["id_user"] == int(current_user.id):
                mess_in["st"] = "out"
            mess_in["time"] = ms["time"]
            data_i["mess_ch"].append(mess_in)
    return json.dumps({'len': data_i,'idd':current_user.id_t} if not current_user.is_anonymous else 0)

@app.route('/dailm', methods=['GET', 'POST'])
def dailm():
    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()
    idd = 0
    if request.form:
        for i in request.form:
            idd = i
            break

    current_user.curdial = idd
    print("idd")
    print(idd)
    data_i = {}
    data_i["dial"] = []
    data_i["mess_ch"] = []
    dial = {}

    for d in res["answer"]:
        #print(current_user.id)
        dial["id"] = d["id_dialog"]
        dial["text"] = d["description"]
        dial["url"] = d["id_dialog"]
        dial["name"] = d["Name"]
        dial["ava"] = d["photo"]
        dial["time"] = d["create_date"]
        if str(current_user.id) in d["users"]:
            data_i["dial"].append(dial)
    if current_user.curdial:
        dictToSend = {'cmd':'get_msg_from_dialog', "id_dialog": int(idd)}
        m = requests.post(ip, json=dictToSend).json()
        for ms in m["answer"]:
            mess_in = {}
            mess_in["text"] = ms["msg"]
            mess_in["url"] = "/profile"
            mess_in["name"] = ms["first_name"] + " " + ms["last_name"]
            mess_in["ava"] = ms["photo"]
            mess_in["st"] = "in"
            mess_in["id"] = ms["id_user"]
            if ms["id_user"] == int(current_user.id):
                mess_in["st"] = "out"
            mess_in["time"] = ms["time"]
            data_i["mess_ch"].append(mess_in)

    return json.dumps({'len': data_i,'idd':current_user.id_t} if not current_user.is_anonymous else 0)

if __name__ == '__main__':
    app.run(host='192.168.31.116',port=5000,debug=True)
