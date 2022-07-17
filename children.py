import time
from tkinter import *
from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Combobox
import shutil
from os import path
import psycopg2
from bd_data import Mydatabase
import tkinter.messagebox as mb

datetime_now = datetime.now()
data_write = datetime_now.date()
def file_read():
    global users
    files = open('texts/users.txt', 'r')
    users = files.read()
    files.close()
    return users

class Table(tk.Frame):
    """Создание таблицы для ввывожда информации из базы данных"""
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        scrolltable_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=table.xview)
        table.configure(xscrollcommand=scrolltable_x.set)
        scrolltable_x.pack(side=tk.TOP, fill=tk.X)
        table.pack(expand=tk.YES, fill=tk.BOTH)

device = ("Серийный номер", "Категория", "Инвентарный номер", "Наименование", "Производитель", "Дата покупки", "Цена", "На складе")

class InfoApp:
    """Созданиие класса окна в методете Info возращаеть один аргунемт 1 или 0 или 2 и сходя из того что возвращаеться
    заупскаеться файл, 1 возврыщыет информацию о приложении. 0 возврыщает информацию системных требоываниях.
    2 возвращает информацию о складе и о списанном оборудование"""
    def __init__(self, parent, width, height, title="Инвентаризация", resizable=(False, False), icon=r'icon\icon.ico'):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+10+10")
        self.root.resizable(resizable[1], resizable[1])
        if icon:
            self.root.iconbitmap(icon)
        self.root["bg"] = "SlateGray2"
        self.bd = Mydatabase()

    def Info(self, item):
        """Обрабатывается вся информацию"""
        if item == 1:
            with open("texts/InfoApp.txt", "r", encoding="utf8") as file:
                str1 = file.read()
            self.info = Text(self.root)
            self.info.insert(1.0, str1)
            self.info.pack()
        if item == 0:
            with open("texts/system_req.txt", "r", encoding="utf8") as file:
                str1 = file.read()
            self.info = Text(self.root)
            self.info.insert(1.0, str1)
            self.info.pack()
        if item == 2:
            self.on_stack = Button(self.root, text="Склад", bg='SkyBlue4', width=20, height=2,
                                   state='disabled', command=self.stack_draw)
            self.on_stack.pack(side=TOP)
            self.stack = Button(self.root, text="Списанная техника", bg='SkyBlue4', width=20, height=2,
                                state='active', command=self.off_equipment)
            Button(self.root, text="Закрыть", width=20, height=2, command=self.root.destroy).pack(
                side=TOP)
            self.stack.pack(side=TOP)
            self.dop()
        if item == 3:
            def list():
                a = self.list_del.get()
                if len(a) > 0:
                    print(a)
                    self.bd.query_to(f"DELETE FROM organization WHERE names='{a}'")
                    mb.showinfo(f"Организация {a} удалена!")
                    self.root.destroy()
                else:
                    mb.showerror("Ошибка", "Ошибка удаления, не выбрана организация которую удалять")
            list_del = self.bd.query(f"SELECT names FROM organization;")
            b_list = []
            for i in list_del:
                b_list.append(i[0])
            Label(self.root, text="Удаление организаций по ремонту", bg='SkyBlue3', font="Arial, 12").pack(side=TOP, padx=10)
            self.list_del = Combobox(self.root, values=b_list, width=30)
            self.list_del.pack(side=TOP, padx=10)
            Button(self.root, text="Удалить", width=20, height=2, command=lambda:list()).pack(side=TOP, padx=10)
            Button(self.root, text="Закрыть", width=20, height=2, command=self.root.destroy).pack(side=TOP)
        if item == 4:
            def query():
                name = self.name.get()
                current_datetime = datetime.now()
                curent_ = current_datetime.date()
                source_path = "data/invet.csv"
                if path.exists(source_path):
                    destination_path = f"save_invent/{name}_{curent_}.csv"
                    shutil.move(source_path, destination_path)
                else:
                    print("Неверный путь к файлу.")
                self.bd.query_to(f"INSERT INTO data_invent (name_invet, date_invet)"
                                 f"VALUES ('{name}', '{curent_}');")
                self.root.destroy()
            Label(self.root, text="Введите имя файла", bg='SlateGray2').pack(side=TOP, pady=5)
            self.name = Entry(self.root, width=30)
            self.name.pack(side=TOP, pady=5)
            Button(self.root, text="Сохранить", width=10, height=2,
                                state='active', command=lambda:query()).pack(side=TOP, pady=10)
            Button(self.root, text="Закрыть", width=10, height=2, command=self.root.destroy).pack(side=TOP)
        if item == 5:
            current = self.bd.query(f"SELECT * FROM data_invent;")
            table1 = Table(self.root, headings=('Номер инвентаризации', 'Наименование', 'Дата провидения'),
                          rows=(current))
            table1.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=30)

    def dop(self):
        """Ввыводит информацию о оборудование которое храниться на складе. Делает запрос в базу данных и возвращает от
        туда информацию с таблицы equipment, которая выполняет условие"""
        self.list_stock = LabelFrame(self.root, text="Склад",
                                     bg='SlateGray2', font="12")
        self.list_stock.pack(side=TOP, fil=BOTH)
        list_dop = self.bd.query(f"SELECT * FROM equipment WHERE warehous='Да';")
        table = Table(self.list_stock, headings=("Серийный номер", "Категория", "Инвентарный номер", "Наименование",
                                                 "На ремонте", "Производитель", "Дата покупки", "Цена", "На складе"),
                      rows=(list_dop))
        table.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=30)

    def stack_draw(self):
        self.off_equipment.pack_forget()
        self.on_stack.configure(state='disabled')
        self.stack.configure(state='active')
        self.dop()

    def off_equipment(self):
        def write():
            item = self.write_off.get()
            if len(item) > 0:
                self.bd.query_to(f"INSERT INTO write_off (serial_num, category, namess, invet_num) SELECT serial_num, "
                                 f"category, names, invet_num FROM equipment WHERE invet_num='{item}';")
                self.bd.query_to(f"DELETE FROM equipment WHERE invet_num='{item}';")
                mb.showinfo("Информация", "устройство списано")
            else:
                mb.showerror("Ошибка", "Не указано устройство для списания")
        self.list_stock.pack_forget()
        self.on_stack.configure(state='active')
        self.stack.configure(state='disabled')
        self.off_equipment = LabelFrame(self.root, text="Списанная техника", bg='SlateGray2', font="12")
        self.off_equipment.pack(side=TOP, fil=BOTH)
        self.write_off = Entry(self.off_equipment, width=30)
        self.write_off.pack(side=TOP, padx=10, pady=10)
        Button(self.off_equipment, text="Списать", width=30, height=2, command=lambda:write()).pack(side=TOP, padx=10, pady=5)
        sit = self.bd.query(f"SELECT * FROM write_off;")
        table = Table(self.off_equipment, headings=('Серийный номер', 'Категория', 'Наименование', 'Инвентарный номер'),
                      rows=(sit))
        table.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=30)

class Children_Device:
    """Созданиие класса окна"""
    def __init__(self, parent, item, width, height, title="Инвентаризация", resizable=(False, False), icon=r'icon\icon.ico'):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+10+10")
        self.root.resizable(resizable[0], resizable[0])
        self.root["bg"] = "SlateGray2"
        if icon:
            self.root.iconbitmap(icon)
        self.bd = Mydatabase()
        self.reinser = LabelFrame(self.root, text="Материально ответственное лицо")
        self.fr_name = LabelFrame(self.root, text="Учет техники")
        self.fr_label = Frame(self.fr_name, width=30)
        self.fr_entry = Frame(self.fr_name, width=30)
        self.serial_number = Entry(self.fr_entry, width=30)
        self.categorey = Combobox(self.fr_entry, values=["Компьютер", "Монитор", "IP-телефон", "Ноутбук", "Сканер штрихкода"], width=28)
        self.invet_number = Entry(self.fr_entry, width=30)
        self.name = Entry(self.fr_entry, width=30)
        self.repairs = Combobox(self.fr_entry, values=["Да", "Нет"])
        self.manufactyre = Entry(self.fr_entry, width=30)
        self.sales_date = Entry(self.fr_entry, width=30)
        self.price = Entry(self.fr_entry, width=30)
        self.warehous = Combobox(self.fr_entry, values=["Да", "Нет"], width=28)
        self.write_name = Entry(self.reinser, width=30)
        self.inventory_number = Entry(self.reinser, width=30)
        self.to_fix = Button(self.reinser, text="Передача", width=20, height=2, command=self.but_reinsertion)
        if item == 0:
            self.add_device()
        if item == 1:
            self.reinsertion()

    def add_device(self):
        """Создает окно для добавления техники на склад"""
        def put_into_wsrehouse():
            list_equipment = self.bd.query(f"SELECT serial_num FROM equipment")
            data_device = (f"{self.serial_number.get()}", f"{self.categorey.get()}", f"{self.invet_number.get()}",
                           f"{self.name.get()}", "нет", f"{self.manufactyre.get()}", f"{self.sales_date.get()}",
                           f"{self.price.get()}", f"{self.warehous.get()}")
            print(data_device[1])
            list_si = []
            for i in list_equipment:
                for ai in i:
                    list_si.append(ai)
            if data_device[0] in list_si:
                mb.showerror("Ошибка", f"Устройство с серийным номером {data_device[0]} уже есть в базе")
            else:
                try:
                    valid_date = time.strptime(data_device[6], '%d.%m.%Y')
                    def is_number(str):
                        """В функции is_number(), на третьей строке происходит попытка преобразования строки в число с
                        плавающей точкой. Если успешно, возвращается True, если строка кроме цифр, знака минуса и точки,
                         содержит другие символы, программа вернет False."""
                        try:
                            float(str)
                            return True
                        except ValueError:
                            return False
                    if is_number(data_device[7]):
                        print(data_device)
                        try:
                            self.bd.query_to(f"INSERT INTO equipment (serial_num, category, invet_num, names, repairs, manufacture, date_sale, price, warehous)"
                                    f"VALUES {data_device};")
                            mb.showinfo("Информация", "Устройство добавлено на склад")
                        except psycopg2.Error:
                            mb.showerror("Ошибка", f"Инвентарный номер {data_device[2]} уже используется")
                    else:
                        mb.showerror("Ошибка", "Проверьте правильность цены")
                except ValueError:
                    mb.showerror("Ошибка", "Проверьте правильность форматы даты")
        self.fr_name.pack(fil=BOTH, ipadx=30, ipady=20)
        self.fr_label.pack(side=LEFT, fil=BOTH, ipadx=30, ipady=20)
        self.fr_entry.pack(side=LEFT, fil=BOTH, ipadx=30, ipady=20)
        x = 10
        y = 5
        for item in device:
            Label(self.fr_label, text=f"{item}").pack(side=TOP, padx=f'{x}', pady=f'{y}')
            y += 0.5
        self.serial_number.pack(side=TOP, ipady=3, pady=5)
        self.categorey.pack(side=TOP, ipady=3, pady=4)
        self.invet_number.pack(side=TOP, ipady=3, pady=4)
        self.name.pack(side=TOP, ipady=3, pady=4)
        self.manufactyre.pack(side=TOP, ipady=3, pady=4)
        self.sales_date.pack(side=TOP, ipady=3, pady=4)
        self.price.pack(side=TOP, ipady=3, pady=4)
        self.warehous.pack(side=TOP, ipady=3, pady=4)
        Button(self.fr_name, text='Учет', width=20, height=2, command=lambda:put_into_wsrehouse()
               ).pack(side=TOP)
        Button(self.fr_name, text='Закрыть', width=20, height=2, command=self.root.destroy).pack(side=TOP)

    def reinsertion(self):
        self.reinser.pack()
        Label(self.reinser, text="ФИО Материально ответственного лица").pack(side=TOP, padx=5, pady=5)
        self.write_name.pack(side=TOP, padx=5, pady=5)
        Label(self.reinser, text="Инвентарный номер техники").pack(side=TOP, padx=5, pady=5)
        self.inventory_number.pack(side=TOP, padx=5, pady=5)
        self.to_fix.pack(side=TOP, padx=5, pady=5)
        Button(self.reinser, text="Закрыть", width=20, height=2, command=self.root.destroy).pack(side=TOP, padx=5, pady=5)

    def but_reinsertion(self):
        """Выполяеться обращение в базу данных для заполнения вспомогательной таблицы, и изменение данных
        в таблице оборудование"""

        name = self.write_name.get()
        names = name.split(' ')
        inventory_num = self.inventory_number.get()
        aut_id = self.bd.query(f"SELECT aut_id FROM users WHERE last_name='{names[0]}' AND first_name='{names[1]}' AND patronymic='{names[2]}';")
        aut_id_list = []

        for i in aut_id:
            aut_id_list.append(i[0])
        if len(aut_id) > 0:
            print(aut_id_list[0])
            print(data_write)
            try:
                self.bd.query_to(f"INSERT INTO additional(aut_id, ainvet_num, data_write)"
                                 f"VALUES ('{aut_id_list[0]}', '{inventory_num}', '{data_write}');")
                self.bd.query_to(f"UPDATE equipment SET warehous='Нет' WHERE invet_num='{inventory_num}';")
                mb.showinfo("Информация", "устройство закреплено за сотрудником")
            except psycopg2.Error:
                self.to_fix.configure(state='disabled')
                check_user = self.bd.query(f"SELECT last_name, first_name, patronymic FROM users as u INNER JOIN additional"
                                           f" ON u.aut_id=additional.aut_id WHERE additional.ainvet_num='{inventory_num}';")
                self.label = Label(self.reinser, text=f"Данное оборудование закреплено за сотрудником\n {check_user[0]},"
                                                      f" презакрепить за другим сотрудником?", font="Arial, 12")
                self.label.pack(side=TOP, padx=10, pady=5)
                self.yes = Button(self.reinser, text="Да", width=10, height=1, command=lambda:enter(aut_id_list[0],
                                                                                        data_write, inventory_num))
                self.yes.pack(side=TOP, padx=5, pady=5)
                self.noy = Button(self.reinser, text="Нет", width=10, height=1, command=lambda:noy())
                self.noy.pack(side=TOP, padx=5, pady=5)

        else:
            mb.showerror("Ошибка", "Не правильно указан ФИО сотрудника")

        def enter(a, b, c):
            self.to_fix.configure(state='active')
            self.bd.query_to(f"UPDATE additional SET aut_id='{a}', data_write='{b}' WHERE ainvet_num='{c}';")
            mb.showinfo("Информация", "Устройство закреплено за сотрудником")
            self.label.destroy()
            self.noy.destroy()
            self.yes.destroy()

        def noy():
            mb.showinfo("Информация", "Устройство не закреплено, для перезакрепеления \nвидите инвентраный "
                                      "номер устройство и ФИО сотрудника")
            self.to_fix.configure(state='active')
            self.label.destroy()
            self.noy.destroy()
            self.yes.destroy()

class Users:
    """Созданиие класса окна, принимает параметры такие как paran(список содержащию информацию о сотруднике который
    запустил приложение. Другой пареметр sale определяет какую функцию запустить добавление пользователя редактирование
    пользователя или же настройка соеддиниея с баззой данных"""
    def __init__(self, parent, sale, width, height, title="Инвентаризация", resizable=(False, False), icon=r'icon\icon.ico'):
        self.root = Toplevel(parent)
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+10+10")
        self.root.resizable(resizable[0], resizable[0])
        self.root["bg"] = "SlateGray2"
        self.bd = Mydatabase()
        if icon:
            self.root.iconbitmap(icon)
        if sale == 0:
            def info_users__():
                list_info_user = self.bd.query(
                    f"select * from users INER JOIN login_pass on aut_id=id_users WHERE login_pass.logins='{file_read()}';")
                list_users = []
                for item in list_info_user:
                    for i in item:
                        list_users.append(i)
                to_go_info = {
                    'Табельный номер': list_users[0],
                    'Фамилия': list_users[1],
                    'Имя': list_users[2],
                    'Отчество': list_users[3],
                    'Телефон': list_users[4],
                    'Должность': list_users[5],
                    'Офис': list_users[6],
                    'Электронная почта': list_users[7]
                }
                return to_go_info
            self.info_user(info_users__())
        if sale == 1:
            self.edeting()
        if sale == 2:
            self.editing_user()

    def info_user(self, parament):
        Label(self.root, text="Информация о пользователе").pack(side=TOP, padx=15, pady=5)
        for item in parament:
            Label(self.root, text=f"{item}: {parament[item]}", bg='SlateGray2', font="Arial, 12").pack(
                side=TOP, padx=15, pady=5)
        Button(self.root, text="Закрыть", command=self.root.destroy).pack(side=TOP)

    def edeting(self):
        def add_users():
            """Добавление нового пользователя в базу данных, идет проверка всех параметров у пользователя, в начале
            проверяется то что табельный номер это число. После него идет проверка телефонного номера также. Потом
            постепенно идет проверка длины всех веденных данных что бы при вводе не пропустили какое либо поле.
            если все ведено правильно то пользователь добавляется в базу данных"""
            date = (f"{self.aut_id.get()}", f"{self.name.get()}", f"{self.first_name.get()}", f"{self.patronymic.get()}", f"{self.telephone.get()}", f"{self.position.get()}", f"{self.office.get()}", f"{self.email.get()}")
            if date[0].isnumeric():
                if date[4].isnumeric():
                    if len(date[0]) == 7:
                        if len(date[4]) == 11:
                            if len(date[1]) > 0 and len(date[2]) > 0 and len(date[3]) > 0 and len(date[5]) > 0 \
                                    and len(date[6]) > 0 and len(date[7]) > 0:
                                a = self.bd.query(f"SELECT aut_id FROM users WHERE aut_id='{date[0]}';")
                                b = self.bd.query(f"SELECT telephone FROM users WHERE telephone='{date[4]}';")
                                c = self.bd.query(f"SELECT aut_id FROM users WHERE email='{date[7]}';")
                                try:
                                    if date[0] not in a[0]:
                                        print("первое исключение")
                                except IndexError:
                                    try:
                                        if date[4] not in b[0]:
                                            print("второе исключение")
                                    except IndexError:
                                        if date[7] not in c:
                                            self.bd.query_to(
                                                f"INSERT INTO users (aut_id, last_name, first_name, patronymic, telephone, positions, office, email)"
                                                f"VALUES ('{date[0]}', '{date[1]}', '{date[2]}', '{date[3]}', '{date[4]}', '{date[5]}', "
                                                f"'{date[6]}', '{date[7]}');")
                                            mb.showinfo("Информация",
                                                         f"Пользователь {date[1], date[2], date[3]} успешно добавлен")
                                            self.exit()
                                        else:
                                            mb.showerror("Error",
                                                         f"Адрес почты используеться сотрудником {c}, проверте правильность почты")
                                    else:
                                        mb.showerror("Error",
                                                     f"Данный номер телефона присвоен сотруднику {b}, проверьте правильность номера")
                                else:
                                    mb.showerror("Error", "Данный сотрудник уже есть в базе")
                            else:
                                mb.showerror("Ошибка заполнения", "Не заполнили обязательное поле")
                        else:
                            mb.showerror("Ошибка заполнения", "Введен не правильный номер телефона")
                    else:
                        mb.showerror("Ошибка заполнения", "Введен не правильный табельный номер")
                else:
                    mb.showerror("Ошибка заполнения", "Проверьте правильность номера телефона")
            else:
                mb.showerror("Error", "не правильно виден табельный номер")

        self.frame_list = Frame(self.root, width=400, height=50, bg='SlateGray2')
        self.frame_list.pack(side=LEFT, fil=BOTH)
        list = ("Табельный номер сотрудника", "Фамилия", "Имя", "Отчество", "Телефон", "Должность", "Офис", "Почта")
        x = 10
        y = 10
        for item in list:
            Label(self.frame_list, text=f"{item}").pack(side=TOP, padx=f'{x}', pady=f'{y}')
        query = []
        list_office = self.bd.query(f"SELECT office FROM office;")
        for i in list_office:
            query.append(i[0])
        self.aut_id = Entry(self.root)
        self.name = Entry(self.root)
        self.first_name = Entry(self.root)
        self.patronymic = Entry(self.root)
        self.telephone = Entry(self.root)
        self.position = Entry(self.root)
        self.office = Combobox(self.root, values=query, width=30)
        self.email = Entry(self.root)
        self.aut_id.pack(side=TOP, pady=10)
        self.name.pack(side=TOP, pady=10)
        self.first_name.pack(side=TOP, pady=10)
        self.patronymic.pack(side=TOP, pady=10)
        self.telephone.pack(side=TOP, pady=11)
        self.position.pack(side=TOP, pady=12)
        self.office.pack(side=TOP, pady=10)
        self.email.pack(side=TOP, pady=11)
        Button(self.frame_list, text="Добавить пользователя", width=20, height=2, command=add_users).pack(
            side=LEFT, padx=5, pady=10)
        Button(self.root, text="Закрыть", width=20, height=2, command=self.exit).pack(side=LEFT, padx=5, pady=20)

    def exit(self):
        self.root.destroy()

    def editing_user(self):
        """Редактирование данных о пользователе, изменение пароля"""
        def user(count):
            login = self.login.get()
            password = self.password.get()
            aut_id = self.aut_id.get()
            lis = self.bd.query(f"SELECT logins FROM login_pass")
            log_user = []
            for item in lis:
                for i in item:
                    print(i, "djsj")
                    log_user.append(i)
            if count == 0:
                if login not in log_user:
                    if len(password) > 8:
                        self.bd.query_to(
                            f"INSERT INTO login_pass (logins, passwords, id_users)"
                            f"VALUES ('{login}', '{password}', '{aut_id}');")
                        mb.showinfo("Информация", "Пользователю предоставлен доступ")
                        self.exit()
                    else:
                        mb.showinfo("Информация", "Пароль не удовлетворяет политике безопасности")
                else:
                    mb.showinfo("Информация", "У данного пользователя есть доступ")
            if count == 1:
                if login in log_user:
                    if len(password) > 8:
                        self.bd.query_to(f"UPDATE login_pass SET passwords='{password}' WHERE logins='{login}'")
                        mb.showinfo("Информация", f"Пароль для пользователя '{login}' изменен")
                        self.exit()
                    else:
                        mb.showinfo("Информация", "Пароль не удовлетворяет политике безопасности")
                else:
                    mb.showinfo("Информация", "У данного пользователя нет логина и пароля")

        self.login = Entry(self.root)
        self.password = Entry(self.root, show="*")
        self.aut_id = Entry(self.root)
        Label(self.root, text="Логин").pack(side=TOP, padx=20)
        self.login.pack(side=TOP, padx=20, pady=10)
        Label(self.root, text="Пароль").pack(side=TOP, padx=20)
        self.password.pack(side=TOP, padx=20, pady=10)
        Label(self.root, text="Табельный номер").pack(side=TOP, padx=20)
        self.aut_id.pack(side=TOP, padx=20, pady=10)
        Button(self.root, text="Предоставить доступ", width=20, height=2, command=lambda:user(0)).pack(side=TOP, padx=20, pady=15)
        Button(self.root, text="Сменить пароль", width=20, height=2, command=lambda:user(1)).pack(side=TOP, padx=20, pady=15)
        Button(self.root, text="Закрыть", width=20, height=2, command=self.exit).pack(side=TOP, padx=20, pady=15)
