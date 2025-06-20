import os
import hashlib
import sqlite3
from encoding import *

def create_base():
    dirname=os.path.dirname(__file__)
    os.chdir(dirname)
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tab_1(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,  marka TEXT, vid TEXT, price INTEGER, date DATE)")
    zayavki = (("fsfsdfsdfsdfsdfsdf", "fdsfsfsdfdsf", "sdfdfsdfdsf", 20000, "2025-06-20"), ("sdfdfsghfgjh", "erwerewr", "bcvnbfgyujt", 20000, "2025-06-22"))
    for z in zayavki:
        cursor.execute("INSERT INTO tab_1 (name, marka, vid, price, date) VALUES (?, ?, ?, ?, ?)", (cezar(z[0]), cezar(z[1]), cezar(z[2]), cezar(str(z[3])), cezar(z[4])))
    cursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, access TEXT)")
    users = (
    ("admin", hashlib.sha256("admin".encode('utf-8')).hexdigest(), "a"),
    ("manager", hashlib.sha256("manager".encode('utf-8')).hexdigest(), "b"),
    ("user", hashlib.sha256("".encode('utf-8')).hexdigest(), "c")
)
    cursor.executemany("INSERT INTO users (name, password, access) VALUES (?, ?, ?)", users)
    connection.commit()
    connection.close()