import sqlite3

from config import *

conn = sqlite3.connect(ITEMS_DB_PATH, check_same_thread=False)
c = conn.cursor()




class Items:
    def __init__(self):

        self.create_table(True)

    def create_table(self, true):
        self.true = true
        if self.true:
            c.execute("CREATE TABLE IF NOT EXISTS items(name TEXT, address TEXT, phone TEXT, price INT, PID TEXT)")
            conn.commit()
        else:
            pass

    def data_entry(self, name, desc, price, sku, pid):
        self.name = name
        self.desc = desc
        self.price = price
        self.sku = sku
        self.pid = pid

        c.execute("INSERT INTO items(name, description, price, sku, PID) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.desc, self.price, self.sku, self.pid))
        conn.commit()


    def read_from_db(self, name):
        self.name = name

        c.execute("SELECT * FROM items")
        for row in c.fetchall():
            if self.name == row[0]:
                return [row[1], row[2], row[3], row[4]]

    def read_all(self):
        c.execute("SELECT * FROM items")
        for row in c.fetchall():
            print(row)

# MemoryUnit().read_all()