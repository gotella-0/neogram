from aiogram import Bot, Dispatcher, executor, types
from beauty import Color
from sys import exit
from multiprocessing import Process, Queue
import os
import time


class Manager:
    def __init__(self, workers, dp):
        self.workers = workers
        self.dp = dp
        self.proccess = []
        self.q = Queue()
        for worker in self.workers:
            p = Process(target=worker.run, daemon=True, args= (self.q,))
            p.start()
            self.proccess.append(p)
            

    def register_command(self,command, args):
        self.dp.register_message_handler(self.handler, commands=command)
    
    def register_message(self, message, args):
        if message == "neogram_any":
            self.dp.register_message_handler(self.handler_any, content_types=["text"])
        else:
            self.dp.register_message_handler(self.handler, lambda msg: msg.text == message)
    
    def register_callback(self, data, args):
        self.dp.register_callback_query_handler(self.callback_handler, lambda callback_query: True)
    
    def register_file(self, type, args):
        self.dp.register_message_handler(self.file_handler, content_types=[type]) #document including audio?
    
    async def callback_handler(self, call: types.CallbackQuery):
        self.q.put_nowait(["callback", call.to_python()])
    
    async def handler_any(self, message: types.Message):
        self.q.put_nowait(["handler_any", message.to_python()])
    
    async def handler(self, message: types.Message):
        self.q.put_nowait(["handler", message.to_python()])
    
    async def file_handler(self, message: types.Message):
        self.q.put_nowait(["file", message.to_python()])

    def run(self):
        self.proc = Process(target=executor.start_polling, daemon=True, args= (self.dp,))
        self.proc.start()
    
    def stop(self):
        print(f'{Color.Yellow}[Info]{Color.END} Exiting...')
        for i in range(len(self.proccess)):
            self.proccess[i].terminate()
        self.proc.kill()