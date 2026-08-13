from ..beauty import Color
from sys import exit
from .api import Api
from ..additions.database import *
from os import getpid
import asyncio
import time
from aiogram import Bot, types
from sys import platform, exit


if platform == "linux" or platform == "linux2":
    UVLOOP_MODE = True
    import uvloop
elif platform == "darwin":
    UVLOOP_MODE = False
elif platform == "win32":
    UVLOOP_MODE = False


class Worker(Api):
    def __init__(self, bot_token, name_project, modules, database, prefixes):
        self.token = bot_token
        self.bot = Bot(token=bot_token)
        self.database = Database(name_project, database["host"], database["login"], database["password"], database_type=database["type"], port= database["port"])
        self.database.connect()
        self.state = {}
        self.prefixes = prefixes
        self.logic_commands = {}
        self.name_project = name_project
        self.modules = modules
        self.menus = {}
        if UVLOOP_MODE:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()
        self.status = "Normal"

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("bot", None)
        state.pop("loop", None)
        if "database" in state:
            db = state["database"]
            state["database"] = Database(db.name_project, db.host, db.user, db.passwd, db.database_type, db.port)
        if "modules" in state:
            state["modules"] = {name: mod.__name__ for name, mod in state["modules"].items()}
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.modules = {name: __import__(mod_name) for name, mod_name in self.modules.items()}
        self.bot = Bot(token=self.token)
        if UVLOOP_MODE:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        self.loop = asyncio.get_event_loop()
        self.database.connect()

    def register_command(self,command, args):
        self.logic_commands["/"+command] = dict(args)

        self._check_state("/"+command)
        self._check_buttons("/"+command) #if buttons exist - create menu, else pass
    
    def register_message(self, message, args):
        print(message)
        self.logic_commands[message] = dict(args)

        self._check_state(message)
        self._check_buttons(message)
    
    def register_callback(self, data, args):
        self.logic_commands[f"data:{data}"] = dict(args)

        self._check_state(f"data:{data}")
        self._check_buttons(f"data:{data}")
    
    def register_file(self, type, args):
        self.logic_commands[f"{self.prefixes[type]}:"+type] = dict(args)

        self._check_state(f"{self.prefixes[type]}:"+type)
        self._check_buttons(f"{self.prefixes[type]}:"+type)


    def set_state(self, command, user_id): #Don't remove retries code
        current_state = self.database.get_state(user_id)
        print(current_state)
        try:
            if "set_state" in self.logic_commands[command][current_state]:
                state = self.logic_commands[command][current_state]["set_state"]
                self.database.update_state(user_id, state)
        except:
            if "set_state" in self.logic_commands[command]["any"]:
                state = self.logic_commands[command]["any"]["set_state"]
                self.database.update_state(user_id, state)

    def _check_state(self, command):
        tmp = {}
        cmd = self.logic_commands[command]
        tmp["any"] = cmd
        if "state" in cmd:
            for i in cmd['state']:
                try:
                    a = cmd["state"][i]["action"] # it's simple way to check syntax state;)
                    del a
                except:
                    print(f'{Color.Red}[Error]{Color.END} In command {command} error `state` syntax! ')
                    exit()
                tmp[i] = cmd["state"][i]
            tmp['any'].pop("state")
        self.logic_commands[command] = tmp

    def _check_buttons(self, command):
        cmd = self.logic_commands[command]
        self.menus[command] = {}
        for state in cmd:
            type = None
            if "buttons" in cmd[state]:
                for row in range(len(cmd[state]["buttons"])):
                    buttons = []
                    for button in cmd[state]["buttons"][row]:
                        try:
                            if type == None:
                                if button['type'] == "inline":
                                    markup = types.InlineKeyboardMarkup()
                                    buttons.append(types.InlineKeyboardButton(text= button["text"], callback_data=button['data'] ))
                                    type = "inline" 
                                elif button['type'] in ["text", "geolocation", "phone_number"]:
                                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                    if button['type'] == "text":
                                        buttons.append(types.KeyboardButton(button["text"]))
                                    elif button['type'] == "geolocation":
                                        buttons.append(types.KeyboardButton(button["text"], request_location=True))
                                    elif button['type'] == "phone_number":
                                        buttons.append(types.KeyboardButton(button["text"], request_contact=True))
                                    type =  "reply"
                            elif type == "reply":
                                if 'type' not in button:
                                    buttons.append(types.KeyboardButton(button["text"]))
                                elif button['type'] == "text":
                                    buttons.append(types.KeyboardButton(button["text"]))
                                elif button['type'] == "geolocation":
                                    buttons.append(types.KeyboardButton(button["text"], request_location=True))
                                elif button['type'] == "phone_number":
                                    buttons.append(types.KeyboardButton(button["text"], request_contact=True))
                            elif type == "inline":
                                buttons.append(types.InlineKeyboardButton(button["text"], callback_data=button['data']))
                        except:
                            print(f'{Color.Red}[Error]{Color.END} In command {command} have bad buttons! ')
                            
                    markup.row(*tuple(buttons)) # dict to tuple. what is `*` : Example: [1,2] to tuple (1,2), *tuple -> 1, 2
                self.menus[command][state] = markup

    async def check_updates(self, type_update, data):
        if type_update == "callback":
            data = types.callback_query.CallbackQuery().to_object(data)
            await self.callback_handler(data)
        elif type_update == "file":
            data = types.message.Message().to_object(data)
            await self.file_handler(data)
        elif type_update == "handler_any":
            data = types.message.Message().to_object(data)
            await self.handler_any(data)
        else:
            data = types.message.Message().to_object(data)
            await self.handler(data)

    async def _run(self, q):
        while True:
            data = q.get()
            await self.check_updates(data[0], data[1])
    
    def __del__(self):
        if hasattr(self, "loop"):
            self.loop.stop()
    
    def run(self, q):
        print(f"{Color.Yellow}[Info]{Color.END} Create worker with process id {getpid()}")
        self.loop.create_task(self._run(q))
        self.loop.run_forever()
