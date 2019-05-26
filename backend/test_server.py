from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import urllib
import sqlalchemy


class InvalidUser(Exception):
    pass

def login(table, conn, client):
    results = conn.execute(sqlalchemy.select([table]))
    login = []
    paswd = []
    id = []
    for r in results:
        login.append(r[1])
        paswd.append(r[2])
        id.append(r[0])
    client.send(bytes("\nLogin or Register?\n", "utf8"))

    a = client.recv(BUFSIZ).decode("utf8")
    f = 0
    if((a[0] == 'L') or (a[0] == 'l')):
        while(f == 0):
            try:
                client.send(bytes("Enter your username", "utf8"))
                u = client.recv(BUFSIZ).decode("utf8")
                client.send(bytes("Enter your password", "utf8"))
                p = client.recv(BUFSIZ).decode("utf8")
                if ((u in login)and(p == paswd[login.index(u)])):
                    client.send(bytes("Login is correct", "utf8"))
                    return 0,u
                else:
                    client.send(bytes("Username or password is invalid", "utf8"))
                    raise InvalidUser
            except InvalidUser as i:
                client.send(bytes("Repeat please", "utf8"))
    else:
        print("Registration")
        client.send(bytes("Registration", "utf8"))
        while(f == 0):
            client.send(bytes("Enter your username", "utf8"))
            u = client.recv(BUFSIZ).decode("utf8")
            if (u in login):
                client.send(bytes("username already taken", "utf8"))
                print("username already taken")
            else:
                f = 1
        print("Enter your password\n")
        client.send(bytes("Enter your password\n", "utf8"))
        p = client.recv(BUFSIZ).decode("utf8")
        print(u,p)
        conn.execute(table.insert().values(id='1', usr=u, password=p))
        return 1, u

def start_chat(n,user, table,conn, client):
    if (n == 1):
        print("Hi, new user: " + user + "!")
        client.send(bytes("Hi, new user: " + user + "!", "utf8"))
    d = conn.execute(sqlalchemy.select([table]))
    print(d)
    m = []
    for i in d:
        m.append(i[1] + ': ' + i[2])
    if (n == 1):
        m = m[-50:]
    for i in m:
        print(i)
        client.send(bytes(str(i), "utf8"))
        for k in range(10000):
            print(k)

    p = 'asda'
    while (p != 'quit'):
        p = client.recv(BUFSIZ).decode("utf8")
        if (p != 'quit'):
            broadcast(bytes(user + ': ' + p, "utf8"))
            conn.execute(table.insert().values(id='1', usr=user, mess=p))



def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Just press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    n,name = login(table_l, conn, client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    start_chat(n,name, table_m, conn, client)

    client.send(bytes("{quit}", "utf8"))
    client.close()
    del clients[client]
    broadcast(bytes("%s has left the chat." % name, "utf8"))


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


clients = {}
addresses = {}



HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)




if __name__ == "__main__":
    SERVER.listen(5)
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
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
