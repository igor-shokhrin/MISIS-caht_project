from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import urllib
import sqlalchemy


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
