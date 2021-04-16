#!/usr/bin/env python
import sqlite3
class config_files_loader(object):
    'Родительский класс загрузчиков конфигурации.'
    def __init__(self,connect:sqlite3.Connection,cursor:sqlite3.Cursor):
        self._connect=connect
        self._cursor=cursor
    def load_config_files(self,src:str):
        pass
    def _load_config_file(self,src:str):
        pass
    
