from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sys import exit
from beauty import Color


class Database:
    def __init__(self, name_project, host, user, passwd, database_type, port):
        self.database_type = database_type
        self.name_project = name_project
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.engine = None
        self.supported_database = ["mysql", "postgres"]

    def create_db(self):
        if self.database_type == "mysql":
            from .databases import mysql_driver
            mysql_driver.create_database(self.name_project, self.host, self.user, self.passwd, self.port)
        else:
            print(f"{Color.Red}[Error]{Color.END} Database `{self.database_type}` is not supported. Please, use one of them databases: {Color.ITALIC}{str(self.supported_database)[1:-1]}{Color.END}")
            exit()
    
    def check(self):
        if self.database_type == "mysql":
            if self.engine == None:
                engine = create_engine(f"mysql+pymysql://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.name_project}?charset=utf8mb4", poolclass=NullPool)
                with engine.connect() as conn:
                    return True

    def connect(self):
        if self.database_type == "mysql":
            if self.engine == None:
                engine = create_engine(f"mysql+pymysql://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.name_project}?charset=utf8mb4", pool_size=5, pool_pre_ping=True, pool_use_lifo=True)
                with engine.connect() as conn:
                    self.engine = engine
    
    def create_tables(self):
        sqls = ["CREATE TABLE users (user_id BIGINT PRIMARY KEY, username TEXT, balance TEXT, who_invite INT, date_subscrie TEXT, ban INT, tags TEXT)",
        "CREATE TABLE states (user_id BIGINT PRIMARY KEY, state TEXT)",
        "CREATE TABLE `media` (name TEXT, type TEXT, file_id TEXT, owner BIGINT, CONSTRAINT MediaObject UNIQUE (name(70), type(50), owner) )"]
        with self.engine.connect() as conn:
            for sql in sqls:
                conn.execute(text(sql))
    
    def del_db(self):
        sql = f"DROP DATABASE {self.name_project}"
        with self.engine.connect() as conn:
            conn.execute(text(sql))
    
    def update_state(self, user_id, state):
        try:
            sql = "DELETE FROM `states` WHERE `user_id`='%s' " % (user_id)
            sql1 = "INSERT INTO `states` VALUES('%s', '%s') " % (user_id, state) 
            
            with self.engine.connect() as conn:
                conn.execute(sql)
                conn.execute(sql1)
        except Exception as e:
            print(f"{Color.Red}[Error]{Color.END} Database error: {e}")
    
    def delete_state(self, user_id):
        try:
            sql = "DELETE FROM `states` WHERE `user_id`='%s' " % (user_id)
            
            with self.engine.connect() as conn:
                conn.execute(sql)
        except Error as e:
            print(f"{Color.Red}[Error]{Color.END} Database error: {e}")
    
    def get_state(self, user_id):
        try:
            sql = "SELECT `state` FROM `states` WHERE `user_id` = '%s' " % (user_id)

            with self.engine.connect() as conn:
                state = conn.execute(sql)
                state = state.fetchone()
            try:
                return state[0]
            except:
                return False
        except Error as e:
            print(f"{Color.Red}[Error]{Color.END} Database error: {e}")
    
    def get_media(self, name, type, owner):
        sql = "SELECT `file_id` FROM `media` WHERE owner='%s' and type='%s' and name='%s'" % (owner, type, name)
        with self.engine.connect() as conn:
            media = conn.execute(sql)
            media = media.fetchone()
            print(media)
    
    def add_media(self, name, type, file_id, owner):
        sql = "INSERT IGNORE INTO `media` (name, type, file_id, owner) VALUES ('%s', '%s', '%s', '%s')" % (name, type, file_id, owner)
        with self.engine.connect() as conn:
            conn.execute(sql)