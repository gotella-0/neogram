try:
    import mysql.connector
except ModuleNotFoundError:
    print("Please, write in bash command: pip install mysql-connector-python")
from mysql.connector import Error
from ...beauty import Color
from sys import exit


def sql_connect(host: str, user: str, passwd: str, port: str):
    try:
        conn = mysql.connector.connect(host=host, user=user, passwd= passwd, port=port)
        return conn
    except Error as e:
        print(f"{Color.Red}[Error]{Color.END} Can't connect to database")
        return None

def _create_database(conn, name_project):
    if conn != None:
        c = conn.cursor()
        c.execute(f'CREATE DATABASE `{name_project}` CHARACTER SET= "utf8mb4" ')
        conn.commit()
        conn.close()
    else:
        exit()

def create_database(name_project, host, user, passwd, port):
    _create_database(sql_connect(host, user, passwd, port), name_project) 