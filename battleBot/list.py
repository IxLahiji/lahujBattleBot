import asyncio
import copy
from threading import Lock


class My_List: #called this to avoid clobbering

    this_list = [] #called this to avoid clobbering with python's "list" type
    list_mutex = Lock()
    

    async def add(self, element):
        self.list_mutex.acquire()
        self.this_list.append(element)
        self.list_mutex.release()
        
        
    async def remove(self, element):
        self.list_mutex.acquire()
        self.this_list.remove(element)
        self.list_mutex.release()
        
        
    async def get_elements(self):
        self.list_mutex.acquire()
        temp_list = list(self.this_list)
        self.list_mutex.release()
        return temp_list