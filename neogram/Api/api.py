from aiogram import Bot, Dispatcher, executor, types
from ..beauty import Color
from sys import exit
from multiprocessing import Process, Queue, Pipe
import os
import time


class Api:
    def __init__(self, bot_token, name_project, modules):
        self.token = bot_token
        self._check()
        self.state = {}
        self.logic_commands = {}
        self.name_project = name_project
        self.modules = modules
        self.menus = {}

    def _check(self):
        try:
            self.bot = Bot(token=self.token)
            self.dp = Dispatcher(self.bot)
        except:
            print(f"{Color.Red}[Error]{Color.END} Bot token is invalid!")
            exit()



    #Registration methods
    def register_command(self,command, args):
        self.logic_commands["/"+command] = dict(args)

        self._check_state("/"+command)
        self._check_buttons("/"+command) #if buttons exist - create menu, else pass
        self.dp.register_message_handler(self.handler, commands=command)
    
    def register_message(self, message, args):
        self.logic_commands[message] = dict(args)

        self._check_state(message)
        self._check_buttons(message)
        self.dp.register_message_handler(self.handler, lambda msg: msg.text == message)
    
    def register_callback(self, data, args):
        self.logic_commands[f"data:{data}"] = dict(args)

        self._check_state(f"data:{data}")
        self._check_buttons(f"data:{data}")
        self.dp.register_callback_query_handler(self.callback_handler, lambda callback_query: True)
    
    def register_file(self, prefix, type, args):
        self.logic_commands[f"{prefix}:"+type] = dict(args)

        self._check_state(f"{prefix}:"+type)
        self._check_buttons(f"{prefix}:"+type)
        self.dp.register_message_handler(self.file_handler, content_types=[type]) #document including audio?



    #Handlers
    async def callback_handler(self, call: types.CallbackQuery):
        start_time = time.time()#for debug
        try:
            try:
                cmd = self.logic_commands[f"data:{call.data}"][self.database.get_state(call.from_user.id)]
            except:
                cmd = self.logic_commands[f"data:{call.data}"]["any"]
        except:
            return
        try:
            if len(cmd) != 0:
                action = getattr(self, cmd['action'])
                await action(call, cmd)
        except:
            try:
                for i in cmd['actions']:
                    try:
                        action = getattr(self, i)
                        await action(call, cmd)
                    except:
                        try:
                            eval(i, self.modules, {"message":message, "callback":message, "database":self.database,})
                        except:
                            print(f"{Color.Red}[Error]{Color.END} Call function with name {i} was errored!")
            except:
                print(f"{Color.Red}[Error]{Color.END} In callback {call.data} parameter `action` is not defined!")
        print(f"All time for callback: {time.time() - start_time} sec\n")#for debug

    async def handler(self, message: types.Message): # it's multi-handler for all. (Boss handler)
        start_time = time.time()#for debug
        print(message.text)
        if message.is_command():
            magic_word = message.get_command()
            magic_word_type = 'command'
        else:
            magic_word = message.text
            magic_word_type = 'message'
        
        try:
            try:
                cmd = self.logic_commands[magic_word][self.database.get_state(message.from_user.id)]
            except:
                cmd = self.logic_commands[magic_word]["any"]
        except:
            return
        
        try:
            if len(cmd) != 0:
                action = getattr(self, cmd['action'])
                await action(message, cmd)
        except:
            try:
                for i in cmd['actions']:
                    try:
                        action = getattr(self, i)
                        await action(message, cmd)
                    except:
                        try:
                            eval(i, self.modules, {"message":message, "callback":message, "database":self.database})
                        except:
                            print(f"{Color.Red}[Error]{Color.END} Call function with name {i} was errored!")
            except:
                print(f"{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word} parameter `action` is not defined!")
        print(f"All time for all: {time.time() - start_time} sec") #for debug
    
    async def handler_any(self, message: types.Message):
        start_time = time.time()#for debug
        magic_word = "neogram_any"
        magic_word_type = 'message'
        
        try:
            try:
                cmd = self.logic_commands[magic_word][self.database.get_state(message.from_user.id)]
            except:
                cmd = self.logic_commands[magic_word]["any"]
        except:
            return

        try:
            if len(cmd) != 0:
                action = getattr(self, cmd['action'])
                await action(message, cmd)
        except:
            try:
                for i in cmd['actions']:
                    try:
                        action = getattr(self, i)
                        await action(message, cmd)
                    except:
                        try:
                            eval(i, self.modules, {"message":message, "callback":message, "database":self.database,})
                        except:
                            print(f"{Color.Red}[Error]{Color.END} Call function with name {i} was errored!")
            except:
                print(f"{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word} parameter `action` is not defined!")
        print(f"All time for all: {time.time() - start_time} sec") #for debug
    
    async def file_handler(self, message: types.Message):
        try:
            try:
                print(message) #for debug
                cmd = self.logic_commands[f"{self.prefixes[message.content_type]}:{message.content_type}"][self.database.get_state(message.from_user.id)]
            except:
                cmd = self.logic_commands[f"{self.prefixes[message.content_type]}:{message.content_type}"]["any"]
        except:
            return
        
        #if len(cmd) != 0:
        #        action = getattr(self, cmd['action'])
        #        await action(message, cmd)

        try:
            if len(cmd) != 0:
                action = getattr(self, cmd['action'])
                await action(message, cmd)
        except:
            try:
                for i in cmd['actions']:
                    try:
                        action = getattr(self, i)
                        await action(message, cmd)
                    except:
                        try:
                            eval(i, self.modules, {"message":message, "callback":message, "database":self.database,})
                        except:
                            print(f"{Color.Red}[Error]{Color.END} Call function with name {i} was errored!")
            except:
                print(f"{Color.Red}[Error]{Color.END} In files type {message.content_type} parameter `action` is not defined!")



    #API methods
    async def send_text(self, message, cmd):
        markup = None
        magic_word, magic_word_type = self._check_type(message)

        try:
            markup = self.menus[magic_word][self.database.get_state(message.from_user.id)]
        except:
            try:
                markup = self.menus[magic_word]['any']
            except:
                pass

        if "text" in cmd:
            try:
                text = eval('f"""' + cmd['text'] + '"""', self.modules, {"message":message, "callback":message})
            except KeyError:
                print(not(any(map(lambda x: x in magic_word, self.prefixes.values())))) # for debug
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text without param `text`! ')
            except AttributeError:
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text with problems function! ')
            
            try:
                await self.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
            except:
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text was errored! ')

        elif "texts" in cmd:
            for i in cmd['texts']:
                try:
                    text = eval('f"""' + i + '"""', self.modules, {"message":message, "callback":message})
                except KeyError:
                    print(not(any(map(lambda x: x in magic_word, self.prefixes.values())))) # for debug
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text without param `text`! ')
                except AttributeError:
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text with problems function! ')
                
                try:
                    await self.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)
                except:
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_text was errored! ')

        self.set_state(magic_word, message.from_user.id)

    async def send_photo(self, message, cmd):
        abs_path = os.getcwd() + "/" + self.name_project + "/assets/"
        caption = None
        markup = None
        magic_word, magic_word_type = self._check_type(message)

        try:
            markup = self.menus[magic_word][self.database.get_state(message.from_user.id)]
        except:
            try:
                markup = self.menus[magic_word]['any']
            except:
                pass

        try:
            path = abs_path + cmd["photo"]
            photo = types.InputFile(path)
        except:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_photo without param `path`! ')
        
        try:
            caption = eval('f"' + cmd['text'] + '"', self.modules, {"message":message})
        except KeyError:
            print(f'{Color.Yellow}[Warning]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_photo without param `text`! ')
        except AttributeError:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_photo with problems function! ')
        
        self.set_state(magic_word, message.from_user.id)
        
        try:
            await self.bot.send_photo(chat_id = message.from_user.id, photo= photo, caption= caption, reply_markup= markup)
        except:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_photo not found photo in a directory `assets` ! ')

    async def send_document(self, message, cmd):
        abs_path = os.getcwd() + "/" + self.name_project + "/assets/"
        caption = None
        markup = None
        magic_word, magic_word_type = self._check_type(message)

        try:
            markup = self.menus[magic_word][self.database.get_state(message.from_user.id)]
        except:
            try:
                markup = self.menus[magic_word]['any']
            except:
                pass
        if "document" in cmd:
            try:
                path = abs_path + cmd["document"]["name"]
                document = types.InputFile(path)
            except:
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_document without param `path`! ')

            try:
                caption = eval('f"' + cmd["document"]["text"] + '"', self.modules, {"message":message, "callback":message})
            except KeyError:
                print(not(any(map(lambda x: x in magic_word, self.prefixes.values())))) # for debug
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_document without param `text`! ')
            except AttributeError:
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_document with problems function! ')

            self.set_state(magic_word, message.from_user.id)

            try:
                await self.bot.send_document(chat_id = message.from_user.id, document= document, caption= caption, reply_markup= markup)
            except:
                print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_document not found document in a directory `assets` ! ')
        
        elif "documents" in cmd:
            for document in cmd["documents"]:
                try:
                    path = abs_path + document["name"]
                    document = types.InputFile(path)
                except:
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_document without param `path`! ')
    
                try:
                    caption = eval('f"' + document["text"] + '"', self.modules, {"message":message})
                except KeyError:
                    print(not(any(map(lambda x: x in magic_word, self.prefixes.values())))) # for debug
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_document without param `text`! ')
                except AttributeError:
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if ((not "data:" in magic_word) and (not(any(map(lambda x: x in magic_word, self.prefixes.values()))))) else magic_word[magic_word.find(":")+1:]} action send_document with problems function! ')
    
                self.set_state(magic_word, message.from_user.id)
    
                try:
                    await self.bot.send_document(chat_id = message.from_user.id, document= document, caption= caption, reply_markup= markup)
                except:
                    print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action send_document not found document in a directory `assets` ! ')

    async def resend_message(self, message, cmd): #update for work with files
        markup = None
        magic_word, magic_word_type = self._check_type(message)

        try:
            markup = self.menus[magic_word][self.database.get_state(message.from_user.id)]
        except:
            try:
                markup = self.menus[magic_word]['any']
            except:
                pass

        try:
            if message.text is not None:
                await self.bot.send_message(chat_id = message.from_user.id, text=message.text, reply_markup= markup)
            else:
                text = message.caption
                if message.photo is not None:
                    await self.bot.send_photo(chat_id = message.from_user.id, photo= message.photo[-1].file_id, reply_markup= markup, caption= text)
                elif message.document is not None:
                    await self.bot.send_document(chat_id = message.from_user.id, document= message.document.file_id, reply_markup= markup, caption= text)
        except:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action resend_message was errored! ')
 
    async def edit_text(self, message, cmd):
        start_time = time.time() # for debug
        markup = None
        magic_word, magic_word_type = self._check_type(message)

        try:
            markup = self.menus[magic_word][self.database.get_state(message.from_user.id)]
        except:
            try:
                markup = self.menus[magic_word]['any']
            except:
                pass
        
        try:
            text = eval('f"""' + cmd['text'] + '"""', self.modules, {"message":message, "callback":message})
        except KeyError:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action edit_text without param `text`! ')
        except AttributeError:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action edit_text with problems function! ')

        self.set_state(magic_word, message.from_user.id)
        try:
            if magic_word_type == "callback":
                await self.bot.edit_message_text(chat_id = message.from_user.id, text=text, reply_markup= markup, message_id = message.message.message_id)
            else:
                await self.bot.edit_message_text(chat_id = message.from_user.id, text=text, reply_markup= markup, message_id = message.message_id)
        except:
            print(f'{Color.Red}[Error]{Color.END} In {magic_word_type} {magic_word if not "data:" in magic_word else magic_word.split("data:")[1]} action edit_text was errored! ')
        print(f"For editing message passed: {time.time() - start_time} sec")# for debug
    
    async def get_photo(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.photo action `get_photo` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"

        photo = message["photo"][0]["file_id"]
        self.database.add_media(name, "photo", photo, owner)
    
    async def get_audio(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.audio action `get_audio` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        audio = message["audio"]["file_id"]
        self.database.add_media(name, "audio", audio, owner)
    
    async def get_voice(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.voice action `get_voice` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        voice = message["voice"]["file_id"]
        self.database.add_media(name, "voice", voice, owner)
    
    async def get_document(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.document action `get_document` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        document = message["document"]["file_id"]
        self.database.add_media(name, "document", document, owner)
    
    async def get_video(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.video action `get_video` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        video = message["video"]["file_id"]
        self.database.add_media(name, "video", video, owner)
    
    async def get_location(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.location action `get_location` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        location = message["location"]
        self.database.add_media(name, "location", location, owner)
    
    async def get_contact(self, message, cmd):
        try:
            name = cmd["name"]
        except:
            print(f"{Color.Red}[Error]{Color.END} In files.contact action `get_contact` required param `name`")
        
        try:
            owner = cmd["owner"]
        except:
            owner = "0"
        
        contact = message["contact"]
        self.database.add_media(name, "contact", contact, owner)

    #Private methods
    def set_state(self, command, user_id):
        try:
            if "set_state" in self.logic_commands[command][self.state[user_id]]:
                self.state[user_id] = self.logic_commands[command][self.state[user_id]]["set_state"]
        except:
            if "set_state" in self.logic_commands[command]["any"]:
                self.state[user_id] = self.logic_commands[command]["any"]["set_state"]

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
    
    def _check_type(self, message):
        try:
            if message.content_type == "text":
                if message.is_command():
                    magic_word = message.get_command()
                    magic_word_type = 'command'
                else:
                    magic_word = message.text
                    magic_word_type = 'message'
            else:
                magic_word = self.prefixes[message.content_type] + ":" + message.content_type
                magic_word_type = "files"
        except:
            magic_word = f"data:{message.data}"
            magic_word_type = "callback"
        return magic_word, magic_word_type
            


    def run(self):
        Process(target=executor.start_polling, daemon=True, args= (self.dp,)).start()