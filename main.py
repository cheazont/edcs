#!/usr/bin/env python


from sql_functions.transport_sql_functions import create_transport_tables
from sql_functions.transport_sql_functions import fill_transport_tables
import sqlite3
import sys
import getopt
import os.path
import config_reader.load_transport_config_files as tr_reader

def main(argv):
    database="test.sqlite"
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        create_transport_tables(conn, cursor)
        fill_transport_tables(conn, cursor)
        reader= tr_reader.transport_config_loader(conn,cursor)
        reader.load_config_files(os.path.abspath("/usr/share/edcs/configs/edcs.json"))
        
    for opt,argv in opts:
        if opt == '-h':
            print('main.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i","--ifile"):
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
            create_transport_tables(conn, cursor)
            fill_transport_tables(conn, cursor)
            reader= tr_reader.transport_config_loader(conn,cursor)
            reader.load_config_files(os.path.abspath(argv))
            



if __name__ == "__main__":
    main(sys.argv[1:])
