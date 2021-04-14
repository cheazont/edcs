#!/usr/bin/env python

from config_reader.load_transport_config_files import read_transport_config
import sqlite3

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

read_transport_config("test_transport.json",cursor)
