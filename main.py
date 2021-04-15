#!/usr/bin/env python

from config_reader.load_transport_config_files import read_transport_configs
from sql_functions.transport_sql_functions import create_transport_tables
from sql_functions.transport_sql_functions import fill_transport_tables
import sqlite3
import sys

conn = sqlite3.connect("test.sqlite")
cursor = conn.cursor()

create_transport_tables(conn, cursor)
fill_transport_tables(conn, cursor)
if len(sys.argv)>1:
    read_transport_configs(sys.argv[1],conn,cursor)
