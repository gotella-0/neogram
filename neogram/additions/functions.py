import os
import shutil
from ..beauty import Color
from .parser import *
from .database import *
from ..Api import Api, Manager, Worker
from aiogram import Bot, Dispatcher, executor, types
import toml
from multiprocessing import Queue, Process
from sys import exit
import time, string, random

def create_default_toml(name_project, path, database_type="mysql"):
    file = {}
    file["name_project"] = name_project
    file["bot_token"] = "write_here_bot_api_token"
    file["admins"] = ["write_here_id"]
    if database_type == "sqlite":
        file["database"] = {"type":"sqlite", "host":"", "login":"", "password":"", "port":""}
    else:
        file["database"] = {"type":"mysql", "host":"localhost", "login":"neogram", "password":"WRITE_YOUR_PASSWORD", "port":"3306"}
    file["commands"] = {"start" : {
    "text" : "Hi in bot made in NeoGram", 
    "action" : "send_text"}}
    parsed = toml.dumps(file)
    with open(f'{path}/config.toml', 'w') as f:
        f.write(parsed)


def create_project(name_project):
    path = os.getcwd()
    database_type = input(f"{Color.Cyan}[Database]{Color.END} Choose database (default - mysql):\n1.Mysql\n2.Postgresql\n3.SQLite\n\nAnswer: ")

    if database_type == "1" or database_type == "":
        database_type = "mysql"
    elif database_type == "3":
        database_type = "sqlite"

    if database_type == "sqlite":
        host = ""
        port = ""
        user = ""
        passwd = ""
    else:
        host = str(input(f"{Color.Cyan}[Database]{Color.END} Write ip database (default - localhost): "))
        port = str(input(f"{Color.Cyan}[Database]{Color.END} Write port database (default for mysql - 3306, for postgres - 5432): "))
        user = str(input(f"{Color.Cyan}[Database]{Color.END} Write login (default- neogram): "))
        passwd = str(input(f"{Color.Cyan}[Database]{Color.END} Write password: "))

        if host == "":
            host = "localhost"
        
        if port == "":
            if database_type == "mysql":
                port = "3306"
            elif database_type == "postgres":
                port = "5432"

        if user == "":
            user = "neogram"


    try:
        os.mkdir(path + '/' + name_project)
        print(f"{Color.Magenta}[Info]{Color.END} Creation of the folder {Color.ITALIC + name_project + Color.END} was successful")

    except FileExistsError:
        print(f"{Color.Red}[Error]{Color.END} Creation of the folder {Color.ITALIC + name_project + Color.END} was errored. Folder {Color.ITALIC + name_project + Color.END} is already exist")
        print(f"{Color.Yellow}[Info]{Color.END} Creating project was aborted")
        exit()
    
    try:
        os.mkdir(path + '/' + name_project + "/assets")
        print(f"{Color.Magenta}[Info]{Color.END} Creation of the folder {Color.ITALIC + name_project + '/assets' + Color.END} was successful")
    except FileExistsError:
        print(f"{Color.Red}[Error]{Color.END} Creation of the folder {Color.ITALIC + name_project + '/assets' + Color.END} was errored. Folder {Color.ITALIC + name_project + Color.END} is already exist")
        print(f"{Color.Yellow}[Info]{Color.END} Creating project was aborted")
        exit()
    
    try:
        os.mkdir(path + '/' + name_project + "/modules")
        print(f"{Color.Magenta}[Info]{Color.END} Creation of the folder {Color.ITALIC + name_project + '/modules' + Color.END} was successful")
    except FileExistsError:
        print(f"{Color.Red}[Error]{Color.END} Creation of the folder {Color.ITALIC + name_project + '/modules' + Color.END} was errored. Folder {Color.ITALIC + name_project + Color.END} is already exist")
        print(f"{Color.Yellow}[Info]{Color.END} Creating project was aborted")
        exit()
    
    create_default_toml(name_project, path + '/' + name_project, database_type=database_type)
    database = Database(name_project, host, user, passwd, database_type=database_type, port=port)
    database.create_db() # it's create database
    database.connect() # it's connect to database
    database.create_tables()
    

def run_project(name_project):
    data = Parser(name_project)
    #single_mode 
    '''api = Api(data.bot_token, name_project, data.modules)

    try:
        for command in data.commands:
            api.register_command(command, data.commands[command])
    except:
        pass
    
    try:
        for message in data.messages:
            api.register_message(message, data.messages[message])
    except:
        pass

    for callback in data.callbacks:
        api.register_callback(callback, data.callbacks[callback])

    api.run()
    time.sleep(1200)'''

    #multiprocess mode
    try:
        bot = Bot(token=data.bot_token)
        dp = Dispatcher(bot)
    except:
        print(f"{Color.Red}[Error]{Color.END} Bot token is invalid!")
        exit()
    
    try:
        database = data.database
        database = Database(name_project, database["host"], database["login"], database["password"], database_type=database["type"], port=database["port"])
        database.check()
    except:
        try:
            database.create_db() # it's create database
            database.connect() # it's connect to database
            database.create_tables()
            database.check()
        except:
            print(f"{Color.Red}[Error]{Color.END} Connection to database was errored. Please, check your database configuration in config file!")
            exit()
    
    prefixes = {"photo": ''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "video": ''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "audio":''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "document":''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "voice":''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "location":''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6)),
    "contact":''.join(random.SystemRandom().choice(string.ascii_letters + string.punctuation) for _ in range(6))}


    COUNT_WORKERS = 4
    workers = []
    for i in range(COUNT_WORKERS):
        worker = Worker(data.bot_token, name_project, data.modules, data.database, prefixes)
        try:
            for command in data.commands:
                worker.register_command(command, data.commands[command])
        except:
            pass
        
        try:
            for message in data.messages:
                worker.register_message(message, data.messages[message])
        except:
            pass

        try:
            for callback in data.callbacks:
                worker.register_callback(callback, data.callbacks[callback])
        except AttributeError:
            pass

        try:
            for type in data.files:
                worker.register_file(type, data.files[type])
        except:
            pass

        workers.append(worker)
    
    manager = Manager(workers, dp)
    try:
        for command in data.commands:
            manager.register_command(command, data.commands[command])
    except:
        pass
        
    try:
        for message in data.messages:
            manager.register_message(message, data.messages[message])
    except:
        pass
    
    try:
        for callback in data.callbacks:
            manager.register_callback(callback, data.callbacks[callback])
    except AttributeError:
        pass

    try:
        for type in data.files:
            manager.register_file(type, data.files[type])
    except:
        pass

    manager.run()
    try:
        time.sleep(120000)
    except KeyboardInterrupt:
        manager.stop()


def remove_project(name_project):
    project_path = os.path.join(os.getcwd(), name_project)

    data = Parser(name_project)
    host = data.database['host']
    user = data.database['login']
    passwd = data.database['password']
    database_type = data.database['type']
    port = data.database['port']

    passwd = 'password'

    database = Database(name_project, host, user, passwd, database_type=database_type, port=port)

    actions = []

    if os.path.exists(name_project):
        print(f"{Color.Magenta}[Info]{Color.END} Directory found")
        actions.append("directory")
    else:
        print(f"{Color.Magenta}[Info]{Color.END} Directory not found")

    if database.check():
        print(f"{Color.Magenta}[Info]{Color.END} Database found")
        actions.append("database")
    else:
        print(f"{Color.Magenta}[Info]{Color.END} Database not found")

    if len(actions) == 0:
        print(f"{Color.Red}[Error]{Color.END} No such project exists.")
        print(f"{Color.Yellow}[Info]{Color.END} Removing project was aborted")
    else:
        yer_or_no = input(f'{Color.Yellow}[*]{Color.END} Are you sure you want to remove the project? Y/N\n').lower()

        if yer_or_no == 'y':
            print(f'{Color.Yellow}[*]{Color.END} Removing project...')
            if 'database' in actions:
                database.connect()
                database.del_db()
            if 'directory' in actions:
                shutil.rmtree(project_path)
            print(f"{Color.Yellow}[Info]{Color.END} The project has been removed successfully.")
        else:
            print(f"{Color.Yellow}[Info]{Color.END} Removing project was aborted")
