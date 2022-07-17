import psycopg2
import tkinter.messagebox as md

class Mydatabase():
    def __init__(self, host = "localhost", user = "postgres", password = "password", db_name = "diplom"):
        try:
            self.conn = psycopg2.connect(host=host, user=user, password=password, database=db_name)

        except Exception as _ex:
            md.showerror("Ошибка", f"Ошибка подключения к базе данных '{_ex}'")
        self.cur = self.conn.cursor()
        self.result = None

    def query_to(self, query):
        self.conn.autocommit = True
        self.cur.execute(query)

    def sel(self, sel):
        self.conn.autocommit = True
        self.cur.execute(sel)
        self.result = self.cur.fetchall()
        return self.result

    def query(self, query):
        self.conn.autocommit = True
        self.cur.execute(query)
        self.result = self.cur.fetchall()
        return self.result

    def close(self):
        self.cur.close()
        self.conn.close()