import toml
import os
import sys
from sys import exit
from ..beauty import Color

class Parser:
    def __init__(self, name_project):
        self.bot_token = ""
        self.name_project = name_project
        
        self.commands = {}
        self.messages = {}
        self.patterns = {}
        self.callbacks = {}
        self.files = {}
        self.states = []
        self.modules = {}
        self.admins = []
        self._run()
    
    def _run(self):
        path = os.getcwd() + "/" + self.name_project

        try:
            with open(f'{path}/config.toml', 'r') as f:
                config = f.read()
            config = toml.loads(config)
        except FileNotFoundError:
            print(f"{Color.Red}[Error]{Color.END} Not found project in this directory")
            exit()
        
        try:
            self.admins = config['admins']
            if ("write_here_id" in self.admins) and len(self.admins) == 1:
                print(f"{Color.Magenta}[Info]{Color.END} List of Admins is default. Please, change this variable")
        except:
            print(f"{Color.Red}[Error]{Color.END} In config file not 'admins' variable.\n{Color.Blue}Solution:{Color.END} add 'admins = [\"write_here_admin_id\"]' in config file")

        try:
            self.bot_token = config["bot_token"]
            if (self.bot_token == "write_here_bot_api_token"):
                print(f"{Color.Magenta}[Info]{Color.END} Bot token is default. Please, change this variable")
                print(f"{Color.Red}[Error]{Color.END} Unable to run bot without a valid bot token.")
        except KeyError:
            print(f"{Color.Red}[Error]{Color.END} In config file not 'bot_token' variable.\n{Color.Blue}Solution:{Color.END} add 'bot_token = \"write_here_bot_token\"' in config file")
        
        try:
            self.patterns.update(config["patterns"])
        except:
            pass

        try:
            self.commands.update(self._check_patterns(config["commands"]))
        except:
            print(f"{Color.Red}[Error]{Color.END} Commands not found\n{Color.Blue}Solution:{Color.END} add block '[commands.start]' and the necessary action for it")
            exit()
        
        try:
            if len(config["import"]) != 0:
                sys.path.insert(1, path + "/modules")
                for type in config["import"]:
                    if type == "module":
                        for i in config["import"]["module"]:
                            module = __import__(i)
                            self.modules[i] = module
                    elif type == "logic":
                        for i in config["import"]["logic"]:
                            self._check_addition(i)
        except KeyError:
            pass
        except Exception as e:
            print(e)
        
        
        try:
            self.messages.update(self._check_patterns(config["messages"]))
        except:
            pass

        try:
            self.callbacks.update(self._check_patterns(config["callbacks"]))
        except:
            pass

        try:
            self.files.update(self._check_patterns(config["files"]))
        except:
            pass
        
        try:
            if len(config["database"]) != 0:
                self.database = config["database"]
        except:
            print(f"{Color.Red}[Error]{Color.END} Database not found\n{Color.Blue}Solution:{Color.END} add block '[database]' and the necessary data for it (check docs)")
            exit()
        
    def _check_addition(self, name_module):
        path = os.getcwd() + "/" + self.name_project
        
        try:
            with open(f'{path}/{name_module}.toml', 'r') as f:
                config = f.read()
            config = toml.loads(config)
        except FileNotFoundError:
            print(f"{Color.Red}[Error]{Color.END} Not found project in this directory")
            exit()
        
        try:
            self.patterns.update(config["patterns"])
        except:
            pass

        try:
            self.commands.update(self._check_patterns(config["commands"]))
        except:
            pass

        try:
            self.messages.update(self._check_patterns(config["messages"]))
        except:
            pass

        try:
            self.callbacks.update(self._check_patterns(config["callbacks"]))
        except:
            pass

        try:
            self.files.update(self._check_patterns(config["files"]))
        except:
            pass
    
    def _check_patterns(self, config):
        config_s = str(config)
        for i in self.patterns:
            finding_text = f"'pattern': '{i}'"
            if finding_text in config_s:
                config_s = config_s.replace(finding_text, str(self.patterns[i])[1:-1] )

        config = eval(config_s)
        return config