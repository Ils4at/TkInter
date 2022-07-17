import csv
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as md
from tkinter.ttk import Combobox
from children import InfoApp, Children_Device, Users
from bd_data import Mydatabase


category = ["Персональный компьютер", "Мониторы", "Принтеры", "IP-телефон", "Сканер штрихкода"]
admin = ('admin')
firstclick = True

def file_read():
    global users
    files = open('texts/users.txt', 'r')
    users = files.read()
    files.close()
    return users

lists = ("Устройство", "Сотрудники", "Ремонт", "Инвентаризация", "Администрирование")
device = ("Серийный номер", "Категория", "Инвентарный номер", "Наименование", "На ремонте", "Производитель", "Дата покупки", "Цена", "На складе")

class Table(tk.Frame):
    """Создание таблицы для ввывожда информации из базы данных"""
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, width=100, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable_y = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable_y.set)
        scrolltable_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrolltable_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=table.xview)
        table.configure(xscrollcommand=scrolltable_x.set)
        scrolltable_x.pack(side=tk.TOP, fill=tk.X)
        table.pack(expand=tk.YES, fill=tk.BOTH)

class Windows:
    """Созданиие класса окна"""
    def __init__(self, width, height, title="Инвентаризация", resizable=(True, True), icon=r'icon\icon.ico'):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+50+50")
        self.root.resizable(resizable[0], resizable[0])
        self.root["bg"] = "SlateGray2"
        if icon:
            self.root.iconbitmap(icon)
        global user
        user = file_read()
        self.bd = Mydatabase()
        self.draw_menu()
        self.frame_menu = Frame(self.root, bg='SkyBlue3', width=300, height=100)
        self.frame_work = Frame(self.root, bg='SlateGray2', width=1600, height=1000)
        self.search_frame = Frame(self.frame_work, bg='SlateGray1')
        self.dop_frame = Frame(self.frame_work, bg='SlateGray2', width=1600, height=600)
        self.dop_frame1 = Frame(self.dop_frame, bg='SlateGray2', width=1600, height=600)
        self.frame1 = Frame(self.dop_frame1, bg='SlateGray2', width=100, height=200)
        self.frame2 = Frame(self.dop_frame1, bg='SlateGray2', width=100, height=200)
        self.frame3 = Frame(self.dop_frame1, bg='SlateGray2', width=100, height=200)
        self.frame_device = Frame(self.frame_work, width=1200, height=600, bg='SkyBlue3')
        self.frame_device1 = Frame(self.frame_device, width=1200, height=600, bg='SkyBlue3')
        self.frame_device2 = Frame(self.frame_device, width=1200, height=600, bg='SkyBlue3')
        self.employee_frame = Frame(self.frame_work, width=1200, height=600, bg='SkyBlue3')
        self.employee_frame1 = Frame(self.employee_frame, width=1200, height=600, bg='SkyBlue3')
        self.employee_frame2 = Frame(self.employee_frame, width=1200, height=600, bg='SkyBlue3')
        self.employee_frame3 = Frame(self.employee_frame, width=1200, height=600, bg='SkyBlue3')
        self.frame_repair = Frame(self.frame_work, width=1200, height=600, bg='SkyBlue3')
        self.frame_repair1 = Frame(self.frame_repair, width=1200, height=600, bg='SkyBlue3')
        self.frame_repair2 = Frame(self.frame_repair, width=1200, height=600, bg='SkyBlue3')
        self.invent_fr1 = Frame(self.frame_work, width=1200, height=100, bg='SkyBlue3')
        self.invent_fr2 = Frame(self.frame_work, width=1200, height=500, bg='SkyBlue3')
        self.invent_fr3 = Frame(self.invent_fr2, width=800, height=500, bg='SkyBlue3')
        self.invent_fr4 = Frame(self.invent_fr2, width=200, height=600, bg='SkyBlue4')
        self.invent_fr5 = Frame(self.invent_fr1, width=1200, height=50, bg='SkyBlue3')
        self.invent_fr6 = Frame(self.invent_fr1, width=1200, height=50, bg='SkyBlue3')
        self.draw_Frame()
        self.frame_menu.pack(side=LEFT, fil=BOTH)
        self.frame_work.pack(fil=BOTH)
        self.root.mainloop()

    def create_child(self, item, width, height, title="Инвентаризация", resizable=(True, True), icon=r'icon\icon.ico'):
        self.info = InfoApp(self.root, width, height, title, resizable, icon)
        self.info.Info(item)

    def child_device(self, item, width=600, height=450, title="Инвентаризация", resizable=(True, True), icon=r'icon\icon.ico'):
        Children_Device(self.root, item, width, height, title, resizable, icon)

    def user_info(self, sela, width, height, title="Инвентаризация", resizable=(True, False), icon=r'icon\icon.ico'):
        Users(self.root, sela, width, height, title, resizable, icon)

    def draw_Frame(self):
        """Рисование врайма в приложении"""
        Button(self.frame_menu, width=15, height=2, text="Устройства", bg='SkyBlue4', font="Arial, 12",
               activebackground='LightSteelBlue1', relief=SUNKEN, command=self.device_widget).pack(side=TOP)
        Button(self.frame_menu, width=15, height=2, text="Сотрудники", bg='SkyBlue4', font="Arial, 12",
               activebackground='LightSteelBlue1', relief=SUNKEN, command=lambda: self.employee_widget(1)).pack(side=TOP)
        Button(self.frame_menu, width=15, height=2, text="Ремонт", bg='SkyBlue4', font="Arial, 12",
               activebackground='LightSteelBlue1', relief=SUNKEN, command=lambda:self.repair_widget(1)).pack(side=TOP)
        Button(self.frame_menu, width=15, height=2, text="Инвентаризация", bg='SkyBlue4', font="Arial, 12",
               activebackground='LightSteelBlue1', relief=SUNKEN, command=self.invent_widget).pack(side=TOP)
        self.main_menu()

    def main_menu(self):
        self.delete()
        self.search_frame.pack(side=TOP, fil=BOTH)
        self.dop_frame.pack(side=TOP, fil=BOTH)
        self.dop_frame1.pack(side=TOP, fil=BOTH)
        self.frame1.pack(side=LEFT, pady=30, padx=30, fil=BOTH)
        self.frame2.pack(side=LEFT, pady=30, padx=30, fil=BOTH)
        self.frame3.pack(side=LEFT, pady=30, padx=30, fil=BOTH)
        Button(self.frame1, width=20, height=2, text="Устройства", command=self.device_widget).pack(side=TOP, padx=20)
        Button(self.frame1, width=15, height=1, text="Учет техники", command=lambda: self.child_device(0)).pack(
            side=TOP, padx=10)
        Button(self.frame1, width=15, height=1, text="Склад", command=lambda: self.create_child(2, 800, 400)).pack(
            side=TOP, padx=10)
        Button(self.frame2, width=20, height=2, text="Сотрудники", command=lambda: self.employee_widget(1)).pack(side=TOP, padx=20)
        Button(self.frame2, width=15, height=1, text="МОЛ", command=lambda: self.child_device(1)).pack(
            side=TOP, padx=10)
        Button(self.frame2, width=15, height=1, text="Офисы", command=lambda:self.employee_widget(0)).pack(side=TOP, padx=10)
        Button(self.frame3, width=30, height=2, text="Ремонт", command=lambda:self.repair_widget(1)).pack(side=TOP, padx=20)
        Button(self.frame3, width=30, height=1, text="Список организаций", command=lambda:self.repair_widget(0)).pack(side=TOP, padx=10)
        Button(self.frame3, width=30, height=1, text="Список техники на ремонте", command=lambda:self.repair_widget(2)).pack(side=TOP, padx=10)
        Button(self.frame3, width=30, height=1, text="Отчеты", command=lambda:self.repair_widget(3)).pack(side=TOP, padx=10)

    def device_widget(self):
        """Рисования окна устройство для добавления просмотра """
        self.delete()
        self.frame_device.pack(side=TOP, fil=BOTH)
        self.frame_device1.pack(side=TOP, fil=BOTH)
        self.frame_device2.pack(side=TOP, fil=BOTH)
        Button(self.frame_device1, text="Учет техники", width=20, height=2,
               command=lambda: self.child_device(0)).pack(side=LEFT, padx=15, pady=10)
        Button(self.frame_device1, text="Склад", width=20, height=2, command=lambda: self.create_child(2, 800, 400)
               ).pack(side=LEFT, padx=15, pady=10)
        equipment = self.bd.query(f"SELECT * FROM equipment WHERE warehous='Нет';")
        table = Table(self.frame_device2, headings=(device),
                      rows=(equipment))
        table.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=30)

    def employee_widget(self, i):
        """Рисование виджетов длы окна сотрудники"""
        def search():
            """"Поиск сотрудников которые есть базе данных"""
            for parents in self.employee_frame3.winfo_children():
                parents.destroy()
            data = f"{self.office.get()}"
            data_list = data.split(' ')
            if len(data_list) == 1:
                list_info_user1 = self.bd.query(f"SELECT * FROM users WHERE last_name='{data_list[0]}';")
                self.table_employee = Table(self.employee_frame3, headings=(cash_user), rows=(list_info_user1))
                self.table_employee.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=20)
            if len(data_list) == 2:
                list_info_user1 = self.bd.query(f"SELECT * FROM users WHERE last_name='{data_list[0]}' AND "
                                                f"first_name='{data_list[1]}';")
                self.table_employee = Table(self.employee_frame3, headings=(cash_user), rows=(list_info_user1))
                self.table_employee.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=20)
            if len(data_list) == 3:
                list_info_user1 = self.bd.query(f"SELECT * FROM users WHERE last_name='{data_list[0]}' AND "
                                                f"first_name='{data_list[1]}' AND patronymic='{data_list[2]}';")
                self.table_employee = Table(self.employee_frame3, headings=(cash_user), rows=(list_info_user1))
                self.table_employee.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=20)

        def adres_office():
            for parents in self.employee_frame3.winfo_children():
                parents.destroy()
            list_office = self.bd.query(f"SELECT * FROM office;")
            self.table_office = Table(self.employee_frame3, headings=("Офис", "Адрес"), rows=(list_office))
            self.table_office.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=20)

        self.delete()
        self.employee_frame.pack(side=TOP, fil=BOTH)
        self.employee_frame1.pack(side=TOP, fil=BOTH)
        self.employee_frame2.pack(side=TOP, fil=BOTH)
        self.employee_frame3.pack(side=TOP, fil=BOTH)
        Button(self.employee_frame1, text="МОЛ", width=30, height=2,
               command=lambda: self.child_device(1)).pack(side=LEFT, padx=15, pady=15)
        Button(self.employee_frame1, text="Адреса офисов", width=20, height=2, command=lambda: adres_office()
               ).pack(side=LEFT, padx=15, pady=15)
        self.office = Entry(self.employee_frame2, width=50)
        self.office.pack(side=LEFT, padx=5, pady=3)
        Button(self.employee_frame2, text="Поиск сотрдуника", width=20, height=2, command=search).pack(
            side=LEFT, padx=20, pady=4)
        list_info_user = self.bd.query(f"select * from users ;")
        cash_user = ("Табельный номер", "Фамилия", "Имя", "Отчество", "Телефон", "Должность", "Офис",
                     "Электронная почта")
        self.table_employee = Table(self.employee_frame3, headings=(cash_user), rows=(list_info_user))
        self.table_employee.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=20)
        if i == 0:
            adres_office()

    def repair_widget(self, qwerty):
        """Рисование виджетов для окна ремонта"""
        def delete():
            self.frame_repair2.destroy()
            self.frame_repair2 = Frame(self.frame_repair, width=1200, height=600, bg='SkyBlue3')
            self.frame_repair2.pack(side=TOP, fil=BOTH)

        def info_reount():
            delete()
            list_del = self.bd.query(f"SELECT names FROM organization;")
            b_list = []
            for i in list_del:
                b_list.append(i[0])
            list_number = self.bd.query(f"SELECT serial_num FROM equipment;")
            number_list = []
            for i in list_number:
                number_list.append(i[0])
            self.frame_repair3 = Frame(self.frame_repair2, width=1000, bg='SkyBlue3')
            self.frame_repair4 = Frame(self.frame_repair2, bg='SkyBlue3')
            self.frame_repair4.pack(side=LEFT)
            self.frame_repair3.pack(side=LEFT)
            self.number_treaty = Entry(self.frame_repair3, width=30)
            Label(self.frame_repair4, text="Номер договора", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.number_treaty.pack(side=TOP, padx=5, pady=10)
            self.serial_number = Combobox(self.frame_repair3, values=number_list, width=30)
            Label(self.frame_repair4, text="Серийный номер устройство", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.serial_number.pack(side=TOP, padx=5, pady=10)
            self.data_to = Entry(self.frame_repair3, width=30)
            Label(self.frame_repair4, text="Дата начала ремонта", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.data_to.pack(side=TOP, padx=5, pady=10)
            self.data_end = Entry(self.frame_repair3, width=30)
            Label(self.frame_repair4, text="Оканчание ремонта", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.data_end.pack(side=TOP, padx=5, pady=10)
            self.price = Entry(self.frame_repair3, width=30)
            Label(self.frame_repair4, text="Стоимость", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.price.pack(side=TOP, padx=5, pady=10)
            self.organizate = Combobox(self.frame_repair3, values=b_list, width=30)
            Label(self.frame_repair4, text="Организация", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, pady=10,
                                                                                                   padx=5)
            self.organizate.pack(side=TOP, padx=5, pady=10)
            def add_report():
                data_list = (f'{self.number_treaty.get()}', f'{self.serial_number.get()}', f'{self.data_to.get()}',
                             f'{self.data_end.get()}', f'{self.price.get()}', f'{self.organizate.get()}')
                self.bd.query_to(f"INSERT INTO repair(number_repair, serial_num, date_start, date_end, sale, entity"
                                 f"VALUES('{data_list[0]}', '{data_list[1]}', '{data_list[2]}', '{data_list[3]}', '{data_list[4]}',"
                                 f" '{data_list[5]}', '{data_list[6]}')")
            try:
                Button(self.frame_repair2, text="Добавить отчет", width=20, height=1, command=lambda : add_report()).pack(side=TOP, padx=5)
            except IndexError:
                md.showerror("Ошибка", "Не заполнены поля")
            sel = self.bd.query(f"SELECT * FROM repair;")
            table = Table(self.frame_repair2, headings=('Номер договора', 'Серийный номер устройства',
                                                        'Дата начало ремонта', 'Окончание ремонта', 'Стоимость', 'Организация'),
                          rows=(sel))
            table.pack(expand=tk.YES, fill=tk.BOTH, padx=20, pady=30)

        def entity():
            """Выводит информацию о организациях которые есть"""
            def add_organization():
                """Добавить организацию"""
                add_str = f"{self.entry.get()}"
                add_list = add_str.split(',')
                if len(add_list) == 4:
                    self.bd.query_to(f"INSERT INTO organization (names, adress, telephone, email)"
                                     f"VALUES ('{add_list[0]}', '{add_list[1]}', '{add_list[2]}', '{add_list[3]}')")
                    md.showinfo("Информация", f"Организация {add_list[0]} добавлена")
                else:
                    md.showerror("Ошибка", "Заполните данные")

            delete()
            Label(self.frame_repair2, text="Для добавления организации заполните через запятую в порядке "
                                           "1) Имя организации 2) Адрес 3)Телефон 4) Почта", bg='SkyBlue3',
                  font="Arial 10").pack(side=TOP, padx=5)
            self.entry = Entry(self.frame_repair2, width=80)
            self.entry.pack(side=TOP)
            Button(self.frame_repair2, text="Добавить организацию", width=20, height=1, command=add_organization).pack(
                side=LEFT, padx=15, pady=15)
            Button(self.frame_repair2, text="Удалить организацию", width=20, height=1, command=lambda:
            self.create_child(3, 300, 400)).pack(
                side=LEFT, padx=15, pady=15)
            list_entity = self.bd.query(f"SELECT * FROM organization;")
            c = 1
            for item in list_entity:
                Label(self.frame_repair2, text=f"{c}) Организация, Адрес, Телефон, Почта \n{item}", bg='SkyBlue3',
                      font="Arial 14").pack(side=TOP, pady=10)
                c += 1

        def list_equment():
            """Выводит оборудование которые находятся на ремонте"""
            delete()
            def to_go_repair():
                int_n = (f"{self.go_remot.get()}")
                print(int_n)
                if len(int_n[0]) > 0:
                    self.bd.query_to(f"UPDATE equipment SET repairs='Да' WHERE invet_num='{int_n}'")
                    md.showinfo("Инфомация", "Оборудование передано на ремонт")
                else:
                    md.showerror("Ошибка", "Не указан инвентарный номер устройства")
            equemnt_list = self.bd.query(f"SELECT names, category, invet_num FROM equipment WHERE repairs='Да'")
            cur = []
            current = self.bd.query(f"SELECT names FROM organization;")
            for i in current:
                cur.append(i[0])
            self.go_remot = Entry(self.frame_repair2, width=30)
            Label(self.frame_repair2, text="Напишите инвентарный номер оборудование которое необходимо \n передать на ремонт и выберите "
                                           "организацию", bg='SkyBlue3', font="Arial, 14").pack(side=TOP, padx=5)
            self.go_remot.pack(side=TOP, pady=10)
            Button(self.frame_repair2, text="На ремонт", width=20, height=2, command=lambda:to_go_repair()).pack(side=TOP, padx=5)
            Label(self.frame_repair2, text="Для закрытия ремонта укажите инвентарный номер").pack(side=TOP, padx=3)
            self.return_repair = Entry(self.frame_repair2, width=30)
            self.return_repair.pack(side=TOP, padx=3)
            Button(self.frame_repair2, text="закрыть ремонт", width=20, height=2, command=lambda: return_repair).pack(side=TOP, padx=3)
            Label(self.frame_repair2, text="Список оборудование которое на ремонте", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, padx=3)
            for item in equemnt_list:
                Label(self.frame_repair2, text=f"{item}", bg='SkyBlue3', font="Arial, 10").pack(side=TOP, padx=3)

        self.delete()
        self.frame_repair.pack(side=TOP, fil=BOTH)
        self.frame_repair1.pack(side=TOP, fil=BOTH)
        Button(self.frame_repair1, text="Организации по ремонту", width=20, height=2, command=entity).pack(
            side=LEFT, padx=15, pady=15)
        Button(self.frame_repair1, text="Список устройств на ремонте", width=35, height=2, command=list_equment
               ).pack(side=LEFT, padx=15, pady=15)
        Button(self.frame_repair1, text="Отчеты", width=20, height=2, command=info_reount).pack(
            side=LEFT, padx=15, pady=15)
        if qwerty == 0:
            entity()
        if qwerty == 2:
            list_equment()
        if qwerty == 3:
            info_reount()

        def return_repair():
            return_num = f'{self.return_repair.get()}'
            print(return_num)
            self.bd.query_to(f"UPDATE equipment SET repairs='Нет' WHERE='{return_num}';")

    def invent_widget(self):
        """Рисование виджетов для окна инвентаризации устройство"""
        self.delete()
        date_invet = self.bd.query(f"SELECT date_invet FROM data_invent ORDER BY id_invent DESC LIMIT 1;")
        date = ""
        for i in date_invet:
            date = i[0]
        self.invent_fr1.pack(side=TOP, fil=BOTH)
        self.invent_fr2.pack(side=TOP, fil=BOTH)
        self.invent_fr3.pack(side=LEFT, fil=BOTH)
        self.invent_fr4.pack(side=LEFT, fil=BOTH)
        self.invent_fr5.pack(side=TOP, fil=BOTH)
        self.invent_fr6.pack(side=TOP, fil=BOTH)
        Label(self.invent_fr5, text="Категория техники", width=25, height=1, bg="SkyBlue3", font="Arial, 12"
              ).pack(side=LEFT, padx=15)
        Label(self.invent_fr5, text="Сотрудник", width=15, height=1, bg="SkyBlue3", font="Arial, 12").pack(
            side=LEFT, padx=70)
        Label(self.invent_fr5, text="Склад", width=10, height=1, bg="SkyBlue3", font="Arial, 12").pack(
            side=LEFT, padx=35)
        Label(self.invent_fr4, text=f"Дата последней инвентаризации \n {date}").pack(side=TOP, padx=10, pady=5)
        Button(self.invent_fr4, text="Список инвентаризаций", width=30, height=2, command=lambda:
        self.create_child(5, 400, 300)).pack(side=TOP, padx=15, pady=15)
        self.start = Button(self.invent_fr4, text="Начать инвентаризацию", width=20, height=2, command=self.button_invent)
        self.start.pack(side=TOP, padx=15, pady=5)

    def button_invent(self):
        """Рисование дополнительных кнопок для провидения инвентаризации"""
        def search_int():
            """данная функция предназначена для обработки поиска инвентаризации в sep возвращается список инвентарных
            номеров которые нужно проинвентаризировать, после получения списка проходимся по каждому элементу проверяем
            его наличие в базе данных, если такое номера нет записываем его в список not_colums """
            i = 0
            for parents in self.invent_fr3.winfo_children():
                parents.winfo_exists()
                i += 1
                if i > 2:
                    self.table_invent.destroy()
                    self.table_invent_no.destroy()
                    self.label.destroy()
            item = self.search_int.get("1.0", "end")
            sring = ''
            for line in item.split("\n"):
                if not line.strip():
                    continue
                a = line
                sring += a
            res_strin = sring.replace(' ', '')
            res_strin.lower()
            sep = res_strin.split(',')
            filtr_category = f'{self.category_list.get()}'
            filtr_employe_list = f'{self.employe_list.get()}'
            filtr_stock = f'{self.stock.get()}'
            filtr_employe_new = filtr_employe_list.split(' ')
            global colums
            colums = []
            not_colums = []
            not_number = []
            try:
                equipment = self.bd.query(f"SELECT e.invet_num FROM equipment as e "
                                          f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                                          f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                                          f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id) as "
                                          f"nt ON e.invet_num=nt.ainvet_num WHERE e.warehous='{filtr_stock}' AND e.category='{filtr_category}';")
                equipment_0index = []
                for i_0 in equipment:
                    for item1 in i_0:
                        print(item1)
                        equipment_0index.append(item1)
            except IndexError:
                print("исключение")
            try:
                equipment_wrehous = self.bd.query(f"SELECT e.invet_num FROM equipment as e "
                                          f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                                          f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                                          f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id) as "
                                          f"nt ON e.invet_num=nt.ainvet_num WHERE e.warehous='{filtr_stock}';")
                equipment_w = []
                for equ_w in equipment_wrehous:
                    for ite in equ_w:
                        equipment_w.append(ite)
            except IndexError:
                print("Исключение")
            equipment_warehous = self.bd.query(f"SELECT invet_num FROM equipment WHERE warehous='{filtr_stock}';")
            e_warehous = []
            for e_w in equipment_warehous:
                for item2 in e_w:
                    e_warehous.append(item2)
            equipment_warehous_cat = self.bd.query(
                f"SELECT invet_num FROM equipment WHERE warehous='{filtr_stock}' AND category='{filtr_category}';")
            e_w_cat = []
            for e_w_c in equipment_warehous_cat:
                for ite2 in e_w_c:
                    e_w_cat.append(ite2)
            try:
                equipment_employye = self.bd.query(f"SELECT e.invet_num FROM equipment as e "
                                                   f"INNER JOIN (SELECT ainvet_num FROM additional INNER JOIN (SELECT "
                                                   f"aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                                                   f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id) as "
                                                   f"nt ON e.invet_num=nt.ainvet_num;")
                e_employye = []
                for e_e in equipment_employye:
                    for item3 in e_e:
                        e_employye.append(item3)
            except IndexError:
                print("исключение2")
            try:
                equipment_employye_cat = self.bd.query(f"SELECT e.invet_num FROM equipment as e "
                                                       f"INNER JOIN (SELECT ainvet_num FROM additional INNER JOIN (SELECT aut_id, last_name, first_name, "
                                                       f"positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' AND "
                                                       f"first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id) as "
                                                       f"nt ON e.invet_num=nt.ainvet_num WHERE category='{filtr_category}';")
                e_employye_cat = []
                for e_e_c in equipment_employye_cat:
                    for item4 in e_e_c:
                        e_employye_cat.append(item4)
            except IndexError:
                print("третие исключение")

            def select1(tree):
                """данный запрос возвращает данные если были выбраны фильтр пользователь"""
                list_invent_off = self.bd.query(
                    f"SELECT nt.ainvet_num, nt.last_name, nt.first_name, nt.positions, nt.office, e.category, e.names, e.warehous  FROM equipment as e "
                    f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                    f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                    f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id  WHERE ainvet_num='{tree}') as "
                    f"nt ON e.invet_num=nt.ainvet_num;")
                return list_invent_off
            def select2(tree):
                """данный запрос возвращает данные если были выбраны такие фильтры как категория, пользователь и склад"""
                list_invent_off = self.bd.query(
                    f"SELECT nt.ainvet_num, nt.last_name, nt.first_name, nt.positions, nt.office, e.category, e.names, e.warehous  FROM equipment as e "
                    f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                    f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                    f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id  WHERE ainvet_num='{tree}') as "
                    f"nt ON e.invet_num=nt.ainvet_num WHERE e.warehous='{filtr_stock}' AND e.category='{filtr_category}';")
                return list_invent_off
            def select3(tree):
                """данный запрос возвращает данные если были выбраны такие фильтры как категория, пользователь"""
                list_invent_off = self.bd.query(
                    f"SELECT nt.ainvet_num, nt.last_name, nt.first_name, nt.positions, nt.office, e.category, e.names, e.warehous  FROM equipment as e "
                    f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                    f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                    f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id  WHERE ainvet_num='{tree}') as "
                    f"nt ON e.invet_num=nt.ainvet_num WHERE e.category='{filtr_category}';")
                return list_invent_off
            def select4(tree):
                """данный запрос возвращает данные если были выбраны такие фильтры как склад, пользователь"""
                list_invent_off = self.bd.query(
                    f"SELECT nt.ainvet_num, nt.last_name, nt.first_name, nt.positions, nt.office, e.category, e.names, e.warehous  FROM equipment as e "
                    f"INNER JOIN (SELECT ainvet_num, u.last_name, u.first_name, u.positions, u.office FROM additional "
                    f"INNER JOIN (SELECT aut_id, last_name, first_name, positions, office FROM users WHERE last_name='{filtr_employe_new[0]}' "
                    f"AND first_name='{filtr_employe_new[1]}' AND positions='{filtr_employe_new[2]}') as u ON additional.aut_id=u.aut_id  WHERE ainvet_num='{tree}') as "
                    f"nt ON e.invet_num=nt.ainvet_num WHERE e.warehous='{filtr_stock}';")
                return list_invent_off
            def prowerka(query):
                """данная функция записывает в список все элементы которые удовлетворяют требованиям"""
                for a in query:
                    colums.append(a)

            if len(filtr_category) > 0:
                """Проверка 1 на наличие категории сработала"""
                if len(filtr_employe_list) > 0:
                    """Проверка 2 на наличие категории и пользователя сработала"""
                    if len(filtr_stock) > 0:
                        """Проверка 3 на наличие всех фильтров сработала"""
                        for ic in sep:
                            sel = select2(ic)
                            if sel == []:
                                not_colums.append(ic)
                            prowerka(sel)
                        for equi in equipment_0index:
                            if equi not in sep:
                                not_number.append(equi)
                    else:
                        """провеврка 4 сработала така как выбрано только 2 фильтра категория м пользователи """
                        for ic in sep:
                            sen = select3(ic)
                            if sen == []:
                                not_colums.append(ic)
                            prowerka(sen)
                        for qwerty in e_employye_cat:
                            if qwerty not in sep:
                                not_number.append(qwerty)
                elif len(filtr_stock) > 0:
                    """проверяем фильтр категории и склад"""
                    for ic in sep:
                        category_stock = self.bd.query(
                        f"SELECT invet_num, nt.last_name, nt.first_name, nt.positions, nt.office, category, names, "
                        f"warehous FROM equipment INNER JOIN (SELECT ainvet_num, last_name, first_name, positions, "
                        f"office FROM users as u INNER JOIN additional ON additional.aut_id=u.aut_id) as nt on "
                        f"equipment.invet_num=nt.ainvet_num WHERE invet_num='{ic}' AND warehous='{filtr_stock}' "
                        f"AND category='{filtr_category}';")
                        if category_stock == []:
                            not_colums.append(ic)
                        prowerka(category_stock)
                    for a in e_w_cat:
                        if a not in sep:
                            not_number.append(a)

                elif len(filtr_category) > 0:
                    """Только категория фильтр"""
                    for ic in sep:
                        category_0 = self.bd.query(
                        f"SELECT invet_num, nt.last_name, nt.first_name, nt.positions, nt.office, category, names, "
                        f"warehous FROM equipment INNER JOIN (SELECT ainvet_num, last_name, first_name, positions, "
                        f"office FROM users as u INNER JOIN additional ON additional.aut_id=u.aut_id) as nt on "
                        f"equipment.invet_num=nt.ainvet_num WHERE invet_num='{ic}' AND category='{filtr_category}';")
                        if category_0 == []:
                            not_colums.append(ic)
                        prowerka(category_0)
            elif len(filtr_employe_list) > 0:
                """проверка пользователя если категория не выбрана"""
                if len(filtr_stock) > 0:
                    for ic in sep:
                        stock_user = select4(ic)
                        if stock_user == []:
                            not_colums.append(ic)
                        prowerka(stock_user)
                    for eq in equipment_w:
                        if eq not in sep:
                            not_number.append(eq)
                else:
                    for ic in sep:
                        list_invent_off = select1(ic)
                        if list_invent_off == []:
                            not_colums.append(ic)
                        prowerka(list_invent_off)
                    for eq_e in e_employye:
                        if eq_e not in sep:
                            not_number.append(eq_e)
            elif len(filtr_stock) > 0:
                """Проверка категории только по складу"""
                for ic in sep:
                    list_stock = self.bd.query(
                    f"SELECT invet_num, nt.last_name, nt.first_name, nt.positions, nt.office, category, names, "
                        f"warehous FROM equipment INNER JOIN (SELECT ainvet_num, last_name, first_name, positions, "
                        f"office FROM users as u INNER JOIN additional ON additional.aut_id=u.aut_id) as nt on "
                        f"equipment.invet_num=nt.ainvet_num WHERE invet_num='{ic}' AND warehous='{filtr_stock}';")
                    if list_stock == []:
                        not_colums.append(ic)
                    prowerka(list_stock)
                for warehous in e_warehous:
                    if warehous not in sep:
                        not_number.append(warehous)
            else:
                """не одна из категорий не выбрана"""
                for ic in sep:
                    list_invetn = self.bd.query(f"SELECT invet_num, nt.last_name, nt.first_name, nt.positions, nt.office, category, names, "
                        f"warehous FROM equipment INNER JOIN (SELECT ainvet_num, last_name, first_name, positions, "
                        f"office FROM users as u INNER JOIN additional ON additional.aut_id=u.aut_id) as nt on "
                        f"equipment.invet_num=nt.ainvet_num WHERE invet_num='{ic}';")
                    if list_invetn == []:
                        not_colums.append(ic)
                    prowerka(list_invetn)

            self.table_invent = Table(self.invent_fr3, headings=('Инвентарный номер', 'Фамилия', 'Имя', 'Должность',
                                                                 'Офис', 'Категория', 'Наименование', 'На складе'),
                                        rows=(colums))
            self.table_invent.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=5)
            missing = []
            for s in not_number:
                not_invet = self.bd.query(f"SELECT nt.invet_num, last_name, first_name, positions, office, nt.category, "
                f"nt.names, nt.warehous FROM users RIGHT JOIN (SELECT invet_num, category, names, warehous, ad.aut_id "
                f"FROM equipment as e LEFT JOIN additional as ad ON e.invet_num=ad.ainvet_num) as nt on "
                                          f"users.aut_id=nt.aut_id WHERE nt.invet_num='{s}';")

                missing.append(not_invet[0])
            self.table_invent_no = Table(self.invent_fr3, headings=('Инвентарный номер', 'Фамилия', 'Имя', 'Должность',
                                                                 'Офис', 'Категория', 'Наименование', 'На складе'),
                                      rows=(missing))
            self.label = Label(self.invent_fr3, text="Устройства которые числятся но не были найдены", bg="SkyBlue3",
                  font="Arial, 14")
            self.label.pack(side=TOP, padx=10)
            self.table_invent_no.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=5)
            if len(not_colums) > 0:
                md.showerror("Ошибка", f"Данные {not_colums} инвентарные номера не найдены")

        def update():
            self.search_int.delete("1.0", "end")

        def save():
            with open(f"data/invet.csv", 'w', newline='') as csvfile:
                fieldnames = ['Инвентарный номер', 'Фамилия', 'Имя', 'Должность', 'Офис', 'Категория', 'Наименование', 'На складе']
                write = csv.writer(csvfile, delimiter=';')
                write.writerows([fieldnames])
                for i in colums:
                    write.writerows([i])
            self.create_child(4, 400, 400)

        lists_category = ["Компьютер", "Монитор", "IP-телефон", "Ноутбук", "Сканер штрихкода"]
        employee = []
        lists_employ = self.bd.query(f"SELECT last_name, first_name, positions FROM users")
        for i in lists_employ:
            employee.append(i)
        self.category_list = Combobox(self.invent_fr6, values=lists_category, width=30)
        self.category_list.pack(side=LEFT, padx=25, pady=2)
        self.employe_list = Combobox(self.invent_fr6, values=employee, width=30)
        self.employe_list.pack(side=LEFT, padx=55, pady=2)
        self.stock = Combobox(self.invent_fr6, values=["Да", "Нет"], width=10)
        self.stock.pack(side=LEFT, padx=10, pady=2)
        self.start.configure(state='disabled')
        self.scroll_bar = tk.Scrollbar(self.invent_fr3, orient="vertical")
        self.scroll_bar.pack(side=RIGHT, fill=Y)
        self.search_int = Text(self.invent_fr3, width=90, height=2, yscrollcommand=self.scroll_bar.set)
        self.search_int.pack(side=TOP)
        self.scroll_bar.config(command=self.search_int.yview)
        self.btn1 = Button(self.invent_fr4, text="Проверить наличие", command=search_int)
        self.btn2 = Button(self.invent_fr4, text="Очистить лист", command=update)
        self.btn3 = Button(self.invent_fr4, text="Сохранить в файл", command=save)
        self.btn4 = Button(self.invent_fr4, text="Закончить инвентаризацию", command=self.actve_invent)
        self.btn1.pack(side=TOP, padx=10, pady=5)
        self.btn2.pack(side=TOP, padx=10, pady=5)
        self.btn3.pack(side=TOP, padx=10, pady=5)
        self.btn4.pack(side=TOP, padx=10, pady=5)

    def actve_invent(self):
        """"удаление дополнительных кнопок после окончание инвентаризации"""
        for parent in self.invent_fr3.winfo_children():
            parent.destroy()
        for parent in self.invent_fr6.winfo_children():
            parent.destroy()
        self.start.configure(state='active')
        self.search_int.destroy()
        self.scroll_bar.destroy()
        self.btn1.destroy()
        self.btn2.destroy()
        self.btn3.destroy()
        self.btn4.destroy()

    def run(self):
        """Запуск TKinter"""
        self.root.mainloop()

    def exit_app(self):
        """Выход из приложения"""
        self.root.destroy()

    def draw_menu(self):
        """Верхнее меню приложения"""
        menu_bar = Menu(self.root, bg='SteelBlue4', fg='blue3')
        user_menu = Menu(menu_bar, tearoff=0)
        user_menu.add_command(label=f'{user}', command=lambda: self.user_info(0, 600,400))
        user_menu.add_separator()
        user_menu.add_command(label='Выход', command=self.exit_app)
        if users == admin:
            new_item = Menu(menu_bar, tearoff=0)
            new_item.add_command(label='Добавление Сотрудника', command=lambda: self.user_info(1, 600, 400))
            new_item.add_command(label='Редактирование Сотрудника', command=lambda: self.user_info(2, 350, 400))
            menu_bar.add_cascade(label='Администрирование', menu=new_item)
        else:
            print("Зашел обычный пользователь")
        servec_menu = Menu(menu_bar, tearoff=0)
        servec_menu.add_command(label='Главная страница', command=self.main_menu)
        menu_bar.add_cascade(label='Пользователь', menu=user_menu)
        menu_bar.add_cascade(label='Сервис', menu=servec_menu)
        menu_bar.add_command(label='О приложении', command=lambda : self.create_child(1, 400, 400))
        self.root.configure(menu=menu_bar)

    def delete(self):
        for parent in self.dop_frame1.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        for parent in self.frame_device.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        for item in self.search_frame.winfo_children():
            item.destroy()
        for parent in self.employee_frame.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        for parent in self.frame_repair.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        for parent in self.invent_fr1.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        for parent in self.invent_fr2.winfo_children():
            for chil in parent.winfo_children():
                chil.destroy()
        self.search_frame.pack_forget()
        self.dop_frame.pack_forget()
        self.dop_frame1.pack_forget()
        self.frame_device.pack_forget()
        self.frame_device1.pack_forget()
        self.frame_device2.pack_forget()
        self.employee_frame.pack_forget()
        self.employee_frame1.pack_forget()
        self.employee_frame2.pack_forget()
        self.employee_frame3.pack_forget()
        self.frame_repair.pack_forget()
        self.frame_repair1.pack_forget()
        self.frame_repair2.pack_forget()
        self.invent_fr1.pack_forget()
        self.invent_fr2.pack_forget()
        self.invent_fr3.pack_forget()
        self.invent_fr4.pack_forget()
        self.invent_fr5.pack_forget()
        self.invent_fr6.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
