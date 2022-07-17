from tkinter import *
from myapp import Windows
import tkinter.messagebox as mb
from bd_data import Mydatabase

class Authorization:
    """Созданиие класса окна"""
    def __init__(self, width, height, title="Инвентаризация", resizable=(False, False), icon=r'icon\icon.ico'):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+50+50")
        self.root.resizable(resizable[0], resizable[0])
        self.root["bg"] = "SlateGray2"
        if icon:
            self.root.iconbitmap(icon)
        self.frame1 = Frame(self.root, bg='SlateGray2', width=400, height=400)
        self.login = Entry(self.frame1, width=30)
        self.password = Entry(self.frame1, show="*", width=30)
        self.widget_auth()
        self.entry_field()
        self.bd = Mydatabase()
        self.root.mainloop()


    def widget_auth(self):
        self.root.grab_set()
        self.root.focus_set()
        Label(self.frame1, width=30, height=5, text="Программа Инвентаризация \nIT-техники компании",
              font=("Times", "14", "bold"), bg='SlateGray2').pack(side=TOP)
        Label(self.frame1, text="Авторизация", font=("Times", "14"),  bg='SlateGray2').pack(side=TOP, padx=10, pady=20)
        self.frame1.pack(fil=BOTH, ipady=5)

    def entry_field(self):
        self.login.pack(side=TOP, padx=5, pady=10)
        self.password.pack(side=TOP, pady=10)
        Button(self.frame1, width=13, height=1, text="Вход", font=("Times", "12"),
               command=self.run).pack(padx=10, pady=5)
        Button(self.frame1, width=13, height=1, text="Выход", font=("Times", "12"),
               command=self.root.destroy).pack(padx=10, pady=30)

    def run(self):
        login = self.login.get()
        password = self.password.get()
        if self.bd.query(f"select logins, passwords from login_pass WHERE logins = '{login}' and passwords = '{password}';"):
            self.root.destroy()
            file_write(login)
            win = Windows(1300, 650)
        else:
            msg = "Неправильно имя пользователя или пароль. Попробуйте еще раз"
            mb.showerror("Ошибка", msg)

def file_write(item):
    login = item
    files = open('texts/users.txt', 'w')
    files.write(login)
    files.close()


if __name__=="__main__":
    run = Authorization(400, 450)
