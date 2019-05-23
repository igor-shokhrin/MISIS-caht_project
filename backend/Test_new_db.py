from flask import Flask, render_template, request, url_for, jsonify
import kontakt, vk
import datetime
import weather
from dateutil.relativedelta import relativedelta
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import urllib
import sqlalchemy


app = Flask(__name__)

@app.route('/for_test', methods=['POST'])
def for_test():
    input_json = request.form["test_name"]
    print('data from client:', input_json)
    print(input_json['cmd'])
    if (input_json['cmd'] == 'VK_Autorization'):
        try:
            a = kontakt.get_user_photo(input_json['username'], input_json['password'])
        except vk.exceptions.VkAuthError:
            return render_template('for_test.html', {'answer': 'Incorrect username or password'})
    print("asdsad", a)
    # return render_template('for_test.html', {'answer': 'Autorization OK'})
    return render_template('for_test.html', {'answer': a})
    #return render_template('for_test.html', test_value=test_value)

@app.route('/')
def home():
        return render_template('for_test.html')

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    params = urllib.parse.quote_plus('Driver={SQL Server};'
                                     'Server=DESKTOP-SN1834C\SQLEXPRESS;'
                                     'Database=Server_chat;')
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    """
    table = Table('login', meta,
       Column('id', Integer, primary_key=True),
       Column('usr', String),
       Column('password', String))
    table = Table('Mess', meta,
       Column('id', Integer, primary_key=True),
       Column('usr', String),
       Column('mess', String))
    meta.create_all()
    """
    conn = engine.connect()
    meta = sqlalchemy.MetaData(engine, reflect=True)
    table = meta.tables['messaging']

    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print ('data from client:', input_json)
    print(input_json['cmd'])
    if(input_json['cmd'] == 'VK_Autorization'):
        try:
            a = kontakt.get_user_photo(input_json['username'],input_json['password'])
            # print(int(datetime.datetime.now().year) - int(str(a[0]['bdate'])[4:]))
            dictr = {"first_name": a[0]["first_name"], "last_name" : a[0]["last_name"], "pas" : input_json["password"], "login" : input_json["username"],  "D_birth" : a[0]["bdate"], "age" : int(datetime.datetime.now().year) - int(datetime.datetime.strptime(str(a[0]['bdate']), "%d.%m.%Y").year), "sex" : get_sex(a[0]["sex"]), "city" : a[0]["city"]["title"], "photo" :   a[0]["photo_50"], "status": ""}
            set_new_user(meta.tables['user'], conn, dictr)
            ans = login(meta.tables['user'], conn, {"pas" : input_json["password"], "login" : input_json["username"]})
        except vk.exceptions.VkAuthError:
            return jsonify({'answer' : 'Incorrect username or password'})
        return jsonify({'answer': ans})
    if(input_json['cmd'] == 'get_msg'):
        return jsonify(get_msg(meta.tables['messaging'], conn))
    elif(input_json['cmd'] == 'send_msg'):
        send_msg(meta.tables['messaging'], conn, input_json)
        return jsonify({'answer': 'send_msg OK'})
    elif(input_json['cmd'] == 'create_new_user'):
        set_new_user(meta.tables['user'], conn, input_json)
        return jsonify({'answer': 'create_new_user OK'})
    elif(input_json['cmd'] == 'create_new_dialog'):
        set_new_dialog(meta.tables['dialogs'], conn, input_json)
        return jsonify({'answer': 'create_new_dialog OK'})
    elif(input_json['cmd'] == 'get_users'):
        ans = get_users(meta.tables['user'], conn)
        return jsonify({'answer': ans})
    elif(input_json['cmd'] == 'get_dialogs'):
        ans = get_dialogs(meta.tables['dialogs'], conn)
        for i in ans:
            ans1 = get_user_from_dialog(meta.tables['dialogs'], conn,{"id_dialog" : int(i["id_dialog"])})

            i["users"] = ans1
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'test'):
        ans = test(meta.tables['user'], conn)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'login'):
        ans = login(meta.tables['user'], conn, input_json)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'registration'):
        ans = registration(meta.tables['user'], conn, input_json)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'get_user_info'):
        ans = get_user_info(meta.tables['user'], conn, input_json)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'get_user_from_dialog'):
        ans = get_user_from_dialog(meta.tables['user_dialog'], conn, input_json)
        for i in ans:
            ans1 = get_user_info(meta.tables["user"], conn, {"id_user": i["id_user"]})
            i["first_name"] = ans1["first_name"]
            i["last_name"] = ans1["last_name"]
            i["photo"] = ans1["photo"]
            print(ans1)
        return jsonify({'answer': ans})
        # return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'weather_now'):
        ans = weather.WeatherNow(weather.GetCityId(input_json["city"]))
        print(ans)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'weather_to_five_days'):
        ans = weather.WeatherToFiveDays(weather.GetCityId(input_json["city"]))
        print(ans)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'get_msg_from_dialog'):
        ans = get_msg_from_dialog(meta.tables["messaging"], meta.tables["user"], conn, input_json)
        print(ans)
        for i in ans:
            ans1 = get_user_info(meta.tables["user"], conn, {"id_user": i["id_user"]})
            i["first_name"] = ans1["first_name"]
            i["last_name"] = ans1["last_name"]
            i["photo"] = ans1["photo"]
            print(ans1)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'update_user_info'):
        update_user_info(meta.tables['user'], conn, input_json)
        return jsonify({'answer': 'update_user_info OK'})

def update_user_info(table, conn, input_json):
    dct = input_json.copy()
    print(dct)
    # map(dct.pop, ["id_user", "cmd"])
    del dct["id_user"]
    del dct["cmd"]
    print(dct)
    print(input_json)
    # conn.execute(sqlalchemy.update(table).where(table.c.id_user == input_json["id_user"]).values(dct))
    conn.execute(sqlalchemy.update(table).where(table.c.id_user == input_json["id_user"]).values(dct))

def get_msg_from_dialog(table, table_user, conn, input_json):
    lst = []
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    m = []
    for i in d:
        if(i["id_dialog"] == input_json["id_dialog"]):
            # ans = get_user_info(table_user, conn, {"id_user" : i["id_user"]})
            # lst.append({"id_user" : i["id_user"], "first_name" : ans["first_name"], "last_name" : ans["last_name"], "photo" : ans["photo"],   "msg" : i["text"]})
            lst.append({"id_user": i["id_user"], "msg": i["text"], "time" : i["time"]})
    return lst

def get_sex(id):
    if(id == 1): return "Female"
    if(id == 2): return "Male"
    if(id == 0): return "None"

def get_user_from_dialog(table, conn, input_json):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    print(d.keys())
    m = []
    for i in d:
        print(i)
        if(i["id_dialog"] == input_json["id_dialog"]):
            m.append(i["id_user"])
    if(len(m) > 0):
        return {"ans": m}
    return {"ans": "This dialog not found"}

def get_user_info(table, conn, input_json):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    print(d.keys())
    m = []
    s = {}
    for i in d:
        print(i)
        if(i["id_user"] == input_json["id_user"]):
            for k in range(len(d.keys())):
                if(d.keys()[k] != "pas"):
                    s[d.keys()[k]] = str(i[k])
            print(s)
            return s
    return {"ans": "User with this id not find"}

def registration(table, conn, input_json):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    for i in d:
        if (i["login"] == input_json["login"]):
            return {"ans": "Username is taken"}
    conn.execute(table.insert().values(pas = str(input_json["pas"]), login = str(input_json["login"])))
    ans = login(table, conn, input_json)
    return ans


def login(table, conn, input_json):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    for i in d:
       if(i["login"] == input_json["login"]):
           if(i["pas"] == input_json["pas"]):
               return {"ans" : "Authorization success", "id" : i["id_user"]}
           else:
               return {"ans" : "Incorrect login or password"}
    return {"ans": "Incorrect login or password"}


def test(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d, d.keys)
    for i in d:
        print(i["id_user"])
        # if(i["id_user"] == 1): i["photo"] = "asdas"
    # print(d.keys() == "id")
    m = []
    for i in d:
        m.append(i[1] + ': ' + i[2])
    tabl = sqlalchemy.Table(table)
    print(tabl)
    # conn.execute(sqlalchemy.update([table]).where("id_user" == 1).values(photo='user #5'))
    return {"msg":m}


def get_msg(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    m = []
    for i in d:
        m.append(i[1] + ': ' + i[2])
    return {"msg":m}

def send_msg(table, conn, dict):
    conn.execute(table.insert().values(text = str(dict["text"]), id_dialog=int(dict["id_dialog"]), id_user=int(dict["id_user"]), time = str(datetime.datetime.now().time().hour) + ':' + str(datetime.datetime.now().time().minute) + " | " + str(datetime.datetime.now().date().day) + " " + str(datetime.datetime.now().strftime("%B")) ) )

def set_new_user(table, conn, dict):
    conn.execute(table.insert().values(first_name = str(dict["first_name"]), last_name = str(dict["last_name"]), pas = str(dict["pas"]), login = str(dict["login"]),  D_birth=str(dict["D_birth"]), age=int(dict["age"]), sex = str(dict["sex"]), city = str(dict["city"]), photo = str(dict["photo"]), status =  str(dict["status"])))

def set_new_dialog(table, conn, dict):
        conn.execute(table.insert().values(Name = str(dict["Name"]), create_date=str(dict["create_date"]), capacity=int(dict["capacity"])))

def get_users(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    m = []
    for i in d:
        # s = {}
        # for k in range(len(d.keys())):
        #     s[d.keys()[k]] = str(i[k])
        # m.append(s)
        m.append({"id_user": i["id_user"], "first_name": i["first_name"], "last_name": i["last_name"], "photo": i["photo"]})

    return m

def get_dialogs(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    m = []
    for i in d:
        s = {}
        for k in range(len(d.keys())):
            s[d.keys()[k]] = str(i[k])
        m.append(s)
    return m



if __name__ == '__main__':
    # app.run(host='192.168.31.195', port=5000, debug=True)
    app.run(host='192.168.43.33', port=5000, debug=True)
    print("sad")
    # params = urllib.parse.quote_plus('Driver={SQL Server};'
    #                                  'Server=DESKTOP-SN1834C\SQLEXPRESS;'
    #                                  'Database=Server;')
    # engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    # """
    # table = Table('login', meta,
    #    Column('id', Integer, primary_key=True),
    #    Column('usr', String),
    #    Column('password', String))
    # table = Table('Mess', meta,
    #    Column('id', Integer, primary_key=True),
    #    Column('usr', String),
    #    Column('mess', String))
    # meta.create_all()
    # """
    # conn = engine.connect()
    # meta = sqlalchemy.MetaData(engine, reflect=True)
    # table_l = meta.tables['login']
    # table_m = meta.tables['Mess']

