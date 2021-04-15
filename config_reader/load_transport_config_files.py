#!/usr/bin/env python

import json
import os.path
import sqlite3
from sql_functions.transport_sql_functions import insert_into_transport_table
from sql_functions.transport_sql_functions import insert_into_tcp_master_table
from sql_functions.transport_sql_functions import insert_into_tcp_slave_table
from sql_functions.transport_sql_functions import insert_into_uart_table

def read_transport_config(src:str,conn:sqlite3.Connection,cursor:sqlite3.Cursor):
    if not os.path.isfile(src):
        print("Файл {} отсутсвует!".format(src))
        return None
    with open(src,"r") as read_file:
        try:
            data = json.load(read_file)
        except json.decoder.JSONDecodeError:
            print("Синтаксическая ошибка в файле {}.".format(src))
            return None
        try:
            transport_id = data["id"]
        except KeyError:
            print("Отсутсвует поле id в файле {}.".format(src))
            return None
        try:
            transport_name = data["name"]
        except KeyError:
            print("Отсутсвует поле name в файле {}.".format(src))
            return None
        try:
            transport_role = data["role"]
        except KeyError:
            print("Отсутсвует поле role в файле {}.".format(src))
            return None
        try:
            transport_connect_type = data["connection_type"]
        except KeyError:
            print("Отсутсвует поле connect_type в файле {}.".format(src))
            return None
        if insert_into_transport_table(conn,cursor, transport_id,transport_name,transport_role,transport_connect_type) == None:
            return None
        if transport_role == "master":
            if transport_connect_type == "tcp" or transport_connect_type == "udp":
                try:
                    transport_address = data["address"]
                except KeyError:
                    print("Отсутсвует поле address в файле {}.".format(src))
                    return None
                try:
                    transport_port= data["port"]
                except KeyError:
                    print("Отсутсвует поле port в файле {}.".format(src))
                    return None
                if insert_into_tcp_master_table(conn,cursor,transport_address,transport_port,transport_id) == None:
                    return None
                return 1
            elif transport_connect_type == "uart":
                try:
                    transport_port = data["port"]
                except KeyError:
                    print("Отсутсвует поле port в файле {}.".format(src))
                    return None
                try:
                    transport_baudrate = data["baudrate"]
                except KeyError:
                    print("Отсутсвует поле baudrate в файле {}.".format(src))
                    return None
                if insert_into_uart_table(conn,cursor,transport_port,transport_baudrate,transport_id)==None:
                    return None
                return 1
        elif transport_role == "slave":
            if transport_connect_type == "tcp" or transport_connect_type == "udp":
                transport_listen_address = list();
                try:
                    for address in data["listen_addresses"]:
                        transport_listen_address.append(address);
                except KeyError:
                    print("Отсутсвует поле listen_addresses в файле {}.".format(src))
                    return None
                try:
                    transport_port= data["port"]
                except KeyError:
                    print("Отсутсвует поле port в файле {}.".format(src))
                    return None
                if insert_into_tcp_slave_table(conn,cursor,transport_listen_address,transport_port,transport_id) == None:
                    return None
                return 1
                
            elif transport_connect_type == "uart":
                try:
                    transport_port = data["port"]
                except KeyError:
                    print("Отсутсвует поле port в файле {}.".format(src))
                    return None
                try:
                    transport_baudrate = data["baudrate"]
                except KeyError:
                    print("Отсутсвует поле baudrate в файле {}.".format(src))
                    return None
                if insert_into_uart_table(conn,cursor,transport_port,transport_baudrate,transport_id)==None:
                    return None
                return 1
        
    
    return None

def read_transport_configs(src:str,conn:sqlite3.Connection,cursor:sqlite3.Cursor):
    if not os.path.isfile(src):
        print("Файл {} отсутсвует!".format(src))
        return None
    with open(src,"r") as read_file:
        try:
            data = json.load(read_file)
        except json.decoder.JSONDecodeError:
            print("Синтаксическая ошибка в файле {}.".format(src))
            return None
        try:
            for index in data["transport_files"]:
                if read_transport_config(index,conn,cursor) == None:
                    print("Не удалось обработать файл {}!".format(index))
                else:
                    print("Добавлены настройки из файла {}.".format(index))
        except KeyError:
            print("Отсутсвует поле transport_files в файле {}".format(src))
            return None
    return 1
