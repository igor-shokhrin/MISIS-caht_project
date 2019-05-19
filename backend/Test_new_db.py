from flask import Flask, render_template, request, url_for, jsonify
import kontakt, vk
import datetime
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
            print(int(datetime.datetime.now().year) - int(str(a[0]['bdate'])[4:]))
        except vk.exceptions.VkAuthError:
            return jsonify({'answer' : 'Incorrect username or password'})
        print(datetime.datetime.now().year)
        print(a)
        return jsonify({'answer':'Autorization OK'})
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
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'test'):
        ans = test(meta.tables['user'], conn)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'login'):
        ans = login(meta.tables['user'], conn, input_json)
        return jsonify({'answer': ans})
    # elif (input_json['cmd'] == 'registration'):
    #     ans = registration(meta.tables['user'], conn, input_json)
    #     return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'get_user_info'):
        ans = get_user_info(meta.tables['user'], conn, input_json)
        return jsonify({'answer': ans})
    elif (input_json['cmd'] == 'get_user_from_dialog'):
        ans = get_user_from_dialog(meta.tables['user_dialog'], conn, input_json)
        return jsonify({'answer': ans})

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
                s[d.keys()[k]] = str(i[k])
            print(s)
            return s
    return {"ans": "User with this id not find"}



# def registration(table, conn, input_json): #Attention TO DO----------------------------------------------
#     d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
#     print(d)
#     for i in d:
#        if(i["login"] == input_json["login"]):
#            if(i["pas"] == input_json["pas"]):
#                return {"ans" : "Authorization success", "id" : i["id_user"]}
#            else:
#                return {"ans" : "Incorrect login or password"}
#     return {"ans": "Incorrect login or password"}


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
    for i in m:
        print(i)
        print(str(i), "utf8")
        for k in range(10000):
            print(k)
    return {"msg":m}

def send_msg(table, conn, dict):
    conn.execute(table.insert().values(text = str(dict["text"]), id_dialog=int(dict["id_dialog"]), id_user=int(dict["id_user"]), time = str("00:00")))

def set_new_user(table, conn, dict):
    conn.execute(table.insert().values(first_name = str(dict["first_name"]), last_name = str(dict["last_name"]), pas = str(dict["pas"]), login = str(dict["login"]),  D_birth=str(dict["D_birth"]), age=int(dict["age"]), sex = str(dict["sex"]), city = str(dict["city"])))

def set_new_dialog(table, conn, dict):
        conn.execute(table.insert().values(Name = str(dict["Name"]), create_date=str(dict["create_date"]), capacity=int(dict["capacity"])))

def get_users(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    print(d.keys())
    m = []
    for i in d:
        # s = {}
        # for k in range(len(d.keys())):
        #     s[d.keys()[k]] = str(i[k])
        # m.append(s)
        m.append({"id_user": i["id_user"], "first_name": i["first_name"], "last_name": i["last_name"], "photo": i["photo"]})
    for i in m:
        # print(i)
        # print(str(i), "utf8")
        for k in range(10000):
            pass
    return m

def get_dialogs(table, conn):
    d = conn.execute(sqlalchemy.select([table]), autoincrement=True)
    print(d)
    print(d.keys())
    m = []
    for i in d:
        s = {}
        for k in range(len(d.keys())):
            s[d.keys()[k]] = str(i[k])
        m.append(s)
    for i in m:
        # print(i)
        # print(str(i), "utf8")
        for k in range(10000):
            pass
    return m



if __name__ == '__main__':
    app.run(host='192.168.31.195', port=5000, debug=True)
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



