#!/usr/bin/env python

import sqlite3

def create_transport_tables(conn:sqlite3.Connection,cursor:sqlite3.Cursor):
    try:
        cursor.execute("""create table if not exists transport_table (id integer unique, name text, role_id integer, connection_type_id integer)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу transport_table!")
        return None
    try:
        cursor.execute("""create table if not exists role_table (id integer primary key autoincrement, role text unique)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу role_table!")
        return None
    try:
        cursor.execute("""create table if not exists connection_type_table (id integer primary key autoincrement, connection_type text unique)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу connection_type_table!")
        return None
    try:
        cursor.execute("""create table if not exists baudrate_table (id integer primary key autoincrement, baudrate integer unique)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу baudrate_table!")
        return None
    try:
        cursor.execute("""create table if not exists uart_table (id integer primary key autoincrement, port text, baudrate_id integer, transport_id integer)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу uart_table!")
        return None
    try:
        cursor.execute("""create table if not exists tcp_master_table (id integer primary key autoincrement, address text, port integer, transport_id integer)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу tcp_master_table!")
        return None
    try:
        cursor.execute("""create table if not exists tcp_slave_table (id integer primary key autoincrement, listen_addresses text, port integer, transport_id integer)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу tcp_slave_table!")
        return None
    try:
        cursor.execute("""create table if not exists transport_log_table (id integer primary key autoincrement, time_stamp, transport_id integer, log_message text)""")
        conn.commit()
    except:
        print("Не удалось создать таблицу transport_log_table!")
        return None
    return 1

def fill_transport_tables(conn:sqlite3.Connection,cursor:sqlite3.Cursor):
    try:
        for item in ["master","slave"]:
            cursor.execute("""insert into role_table(role) values (?)""",(item,))
            conn.commit()
    except:
       print("Не удалось заполнить таблицу role_table!")
       return None
    try:
        for item in ['tcp', 'udp', 'uart']:
            cursor.execute("insert into connection_type_table(connection_type) values (?)",(item,))
        conn.commit()
    except:
        print("Не удалось заполнить таблицу connection_type_table!")
        return None
    try:        
        for item in [1200,2400,4800,9600,19200,38400,57600,76800,115200,230400,460800,921600,1382400,1843200,2764800]:
            cursor.execute("insert into baudrate_table(baudrate) values (?)",(item,))
        conn.commit()
    except:
        print("Не удалось заполнить таблицу baudrate_table!")
        return None
    return 1

def insert_into_transport_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor, id, name, role, connnection_type ):
    try:
        cursor.execute("""
        insert into transport_table (id,name,role_id,connection_type_id)
        select {},'{}',role_table.id,connection_type_table.id from role_table,connection_type_table
        where role like '%{}%' and connection_type like '%{}%'
        """.format(id,name,role,connnection_type))
        conn.commit()
    except:
        print("Не удалось добавить запись в таблицу transport_table id={}, name={}, role={}, connection_type={}!".format(id,name,role,connnection_type))
        return None
    return 1

def insert_into_tcp_master_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor,address,port,transport_id):
    try:
        cursor.execute("""insert into tcp_master_table(address,port,transport_id) values('{}',{},{},)""".format(address,port,transport_id))
        conn.commit()
    except:
        print("Не удалось добавить запись в таблицу tcp_master_table address={}, port={}, transport_id={}!".format(address,port,transport_id))
        return None
    return 1

def insert_into_tcp_slave_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor, listen_addresses, port, transport_id):
    try:
        for item in listen_addresses:
            cursor.execute("""insert into tcp_slave_table(listen_address,port,transport_id) values('{}',{},{},)""".format(item, port, transport_id))
        conn.commit()
    except:
        print("Не удалось добавить запись в таблицу tcp_slave_table listen_addresses={}, port={}, transport_id={}!".format(listen_addresses,port,transport_id))
        return None
    return 1

def insert_into_uart_table(conn: sqlite3.Connection, cursor: sqlite3.Cursor,port,baudrate,transport_id):
    try:
        cursor.execute("""insert into uart_table(port,baudrate_id,transport_id) select '{0}',baudrate_table.id,{2} from baudrate_table where baudrate={1}""".format(port, baudrate, transport_id))
        conn.commit()
    except:
        print()
        return None
    return 1
