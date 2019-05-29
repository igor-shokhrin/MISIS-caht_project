from flask import Flask, render_template, flash, redirect, request, url_for,session,jsonify,json
from flask_login import LoginManager,UserMixin,current_user, login_user,logout_user
import os
import requests,datetime


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
    ava = "https://fashion-stickers.ru/26762-thickbox_default/znak-voprosa.jpg"
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
ip = 'http://192.168.31.195:5000/tests/endpoint'
data_g = {}
@app.route('/main')
def main():

    dictToSend = {'cmd': 'get_dialogs'}
    res = requests.post(ip, json=dictToSend).json()

    print(current_user.id)
    data_i = {}
    data_i["dial"] = []
    data_i["mess_ch"] = []
    res["answer"]=list(reversed(res["answer"]))
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
            mess_in["id"] = ms["id_user"]
            if ms["id_user"] == current_user.id:
                mess_in["st"] = "out"
            mess_in["time"] = ms["time"]
            data_i["mess_ch"].append(mess_in)

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
    #return render_template('pogoda.html')
    #return redirect(url_for("pogoda"))
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

@app.route('/logvk', methods=['GET', 'POST'])
def logvk():
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
    return render_template('logvk.html')

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
        print(request.form)
        dictToSend = {'cmd': 'VK_Autorization', "password": request.form['pass'], "username": request.form['username']}
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
    return render_template('regvk.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    dictToSend = {'cmd': 'get_msg_from_dialog', "id_dialog": 1}
    res = requests.post(ip, json=dictToSend).json()
    data_in = {}
    data_in["messages"] = []
    res["answer"] = list(reversed(res["answer"]))
    for m in res["answer"]:
        message = {}
        message["name"] = m["first_name"] + m["last_name"]
        message["message"] = m["msg"]
        message["profile"] = "/profile"
        message["ava"] = m["photo"]
        message["id"] = str(m["id_user"])
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
    print(res)
    data_in["groups"] = []
    res["answer"] = list(reversed(res["answer"]))
    for d in res["answer"]:
        group = {}
        group["name"] = d["Name"]
        group["descr"] = d["description"]
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
    urs = res["answer"]["users"]
    data_in = {}
    data_in["members"] = []

    for ur in urs:
        print(ur)
        member = {}
        member["name"] = ur["first_name"] + " " + ur["last_name"]
        member["status"] =ur["status"]
        member["url"] = "/profile"
        member["ava"] = ur["photo"]
        member["id"] = str(ur["id_user"])
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

    print("hey")
    if request.form:
        print(request.form)
        prof_id = int(request.form["id"])
    else:
        prof_id = int(current_user.id)
    sel = False
    if int(prof_id) == int(current_user.id):
        sel = True
    dictToSend = {'cmd': 'get_user_info', "id_user": prof_id}
    res = requests.post(ip, json=dictToSend).json()
    profile = {}
    current_user.username = res["answer"]['first_name'] + " " +  res["answer"]['last_name']
    profile["country"] = "Россия"
    current_user.status = res["answer"]['status']
    profile["regdate"] = "12-06-2016"
    current_user.birth = res["answer"]['D_birth']
    current_user.city = res["answer"]['city']
    current_user.sex = res["answer"]['sex']
    current_user.age = res["answer"]['age']
    current_user.ava = res["answer"]['photo']
    eid = res["answer"]['id_user']
    data_g["profile"] = profile

    return render_template('profile.html',data_g=data_g,sel=sel,eid = eid)

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

@app.route('/changeprof', methods=['GET', 'POST']  )
def changeprof():
    dictToSend = {'cmd': 'get_user_info', "id_user": int(current_user.id_t)}
    res = requests.post(ip, json=dictToSend).json()
    print(res)
    data_g = {}
    profile = {}
    profile["name"] = res["answer"]["first_name"]
    profile["sname"] = res["answer"]["last_name"]
    profile["country"] = "---"
    profile["status"] = res["answer"]['status']
    profile["regdate"] = "12-06-2016"
    profile["bd"] = res["answer"]['D_birth']
    profile["city"] = res["answer"]['city']
    profile["sex"] = res["answer"]['sex']
    profile["age"] = res["answer"]['age']
    profile["ava"] = res["answer"]['photo']
    data_g["profile"] = profile

    return render_template('changeprof.html',data_g=data_g)

@app.route('/pogoda', methods=['GET', 'POST']  )
def pogoda():
    dictToSend = {'cmd': 'weather_now', "city": "Moscow"}
    res = requests.post(ip, json=dictToSend).json()
    print(res)
    timep = []
    conv = {}
    conv["rain"] = "rain"
    conv["clear sky"] = "sunny"
    conv["clear"] = "sunny"
    conv["scattered clouds"] = "sunny"
    conv["broken clouds"] = "sunny"
    conv["overcast clouds"] = "cloudy"
    conv["few clouds"] = "sunny"
    conv["moderate rain"] = "rain"
    conv["light rain"] = "rain"
    data={}
    data["cond"] = conv[res["answer"]["conditions"]]
    data["t"] = int(res["answer"]["temp"])
    dictToSend = {'cmd':'weather_to_five_days', "city": "Moscow"}
    res = requests.post(ip, json=dictToSend).json()
    print(res)
    df = []
    day = []
    count = 0
    cc=0
    for p  in res["answer"]:
        cc+=1
        m = {}
        m["conditions"] =  conv[p["conditions"]]
        m["temp"] = p["temp"]

        day.append(m)
        count += 1
        if count == 8:
            timep.append(p["time"].split()[0])
            df.append(day)
            day = []
            count = 0
    print(timep)
    return render_template('pogoda.html', data=data, datac = df,timep=timep, opo=zip(df,range(0,5)))


@app.route('/createdial')
def createdial():
    dictToSend = {'cmd': 'get_users'}
    res = requests.post(ip, json=dictToSend).json()
    print(res)

    urs = res["answer"]
    data_in = {}
    data_in["members"] = []
    for ur in urs:
        print(ur)
        member = {}
        member["name"] = str(ur["first_name"]) + " " + str(ur["last_name"])
        member["id"] = str(ur["id_user"])
        member["url"] = "/profile"
        member["ava"] = ur["photo"]
        data_in["members"].append(member)

    data = data_in

    return render_template('createdial.html',data=data,data_g=data_g)


@app.route('/create', methods=['GET', 'POST'])
def create():
    newdial = {}
    data = []
    if request.form:
        print(request.form)
        for atr in request.form:
            if atr=="name":
                newdial["name"] =request.form[atr]
            elif atr=="fname":
                newdial["fname"] = request.form[atr]
            elif atr == "ava":
                newdial["ava"] = request.form[atr]
            else:
                data.append(atr)
    print(data)
    ids = []
    for i in range(0,len(data)):
        try:
            if str(data[i]).startswith("a"):
                ids.append(int(data[i][1:]))
        except IndexError:
            break
    print(ids)
    dictToSend = {'cmd': 'create_new_dialog', "Name": newdial["name"], "create_date": str(datetime.datetime.now()),"capacity": "100","users" : ids,"photo" : newdial["ava"] }  # Create new dialog
    res = requests.post(ip, json=dictToSend).json()
    return redirect(url_for("groups"))


@app.route('/sendprof', methods=['GET', 'POST'])
def sendprof():
    if request.form:
        if request.form["age"] =="None":
            aag = 0
        else:
            aag = request.form["age"]
        dictToSend = {'cmd': 'update_user_info',"id_user": int(current_user.id_t), "first_name": request.form["name"],"last_name":request.form["fname"],
                      "status": request.form["status"],"D_birth": request.form["bd"],"city": request.form["city"],
                      "sex": request.form["sex"],"age": int(aag),"photo": request.form["ava"]}
        res = requests.post(ip, json=dictToSend).json()
    return redirect(url_for("profile"))




if __name__ == '__main__':
    app.run(host='192.168.31.116',port=5000,debug=True)
