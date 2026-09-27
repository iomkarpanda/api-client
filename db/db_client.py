import sqlite3

database = sqlite3.connect(r"D:\Projects\personal\api client\database.db")
database.execute("PRAGMA foreign_keys = ON")



