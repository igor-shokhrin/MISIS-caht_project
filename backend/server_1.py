from flask import Flask, render_template, request, url_for, jsonify
import kontakt, vk
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
            kontakt.get_user_photo(input_json['username'], input_json['password'])
        except vk.exceptions.VkAuthError:
            return render_template('for_test.html', {'answer': 'Incorrect username or password'})
    return render_template('for_test.html', {'answer': 'Autorization OK'})
    #return render_template('for_test.html', test_value=test_value)

@app.route('/')
def home():
        return render_template('for_test.html')

@app.route('/tests/endpoint', methods=['POST'])
def my_test_endpoint():
    params = urllib.parse.quote_plus('Driver={SQL Server};'
                                     'Server=DESKTOP-SN1834C\SQLEXPRESS;'
                                     'Database=Server;')
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
    table_l = meta.tables['login']
    table_m = meta.tables['Mess']
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print ('data from client:', input_json)
    print(input_json['cmd'])
    if(input_json['cmd'] == 'VK_Autorization'):
        try:
            kontakt.get_user_photo(input_json['username'],input_json['password'])
        except vk.exceptions.VkAuthError:
            return jsonify({'answer' : 'Incorrect username or password'})
        return jsonify({'answer':'Autorization OK'})
    if(input_json['cmd'] == 'get_msg'):
        return jsonify(send_msg(table_m, conn))

def send_msg(table, conn):
    d = conn.execute(sqlalchemy.select([table]))
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

if __name__ == '__main__':
    app.run(debug=True)
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



