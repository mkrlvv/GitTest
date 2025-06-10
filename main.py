# pip install tkcalendar

import os
import sqlite3
from datetime import datetime
from login import loging
from admin import show_admin_panel
from data import save, edit, delete, setup_right_click_handler
from about import show_about
from settings import show_settings, del_all_windows, open_windows
from sort import setup_sorting
from tkinter import *
from encoding import *
from tkinter import ttk
from tkcalendar import DateEntry
from lang import main_ru, main_en
from theme import apply_theme
from language import load_language, load_theme

dirname = os.path.dirname(__file__)
os.chdir(dirname)

if not os.path.exists("log"):
    os.mkdir("log")

now = datetime.now()
name = now.strftime("%d.%m.%Y_%H.%M.%S")

log_file = open(rf"log\log_{name}.txt", "w", encoding="utf-8")

connection = sqlite3.connect("base.db")
cursor = connection.cursor()


def on_closing(tk):
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Программа завершила работу")
    log_file.close()
    connection.close()
    tk.destroy()


def handle_enter(event, table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor):
    widget = event.widget
    if widget == FIO_Entry:
        MARKA_Combobox.focus_set()
    elif widget == MARKA_Combobox:
        VIDI_Combobox.focus_set()
    elif widget == VIDI_Combobox:
        PRICE_Entry.focus_set()
    elif widget == PRICE_Entry:
        save(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor)


def main_window(access):
    
    user = "admin" if access == "a" else ("manager" if access == "b" else "user")
    
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Программа начала работу. Пользователь: {user}\n")
    
    global open_windows, tk
    lang = main_ru if load_language() == "ru" else main_en
    
    tk = Tk()
    
    open_windows[tk] = lambda: main_window(access)
        
    tk.title(lang[0])
    tk.geometry("1200x800+300+100")
    tk.protocol("WM_DELETE_WINDOW", lambda: on_closing(tk))
    
    
    spravka_menu = Menu(tearoff=0)
    if access == "a":
        spravka_menu.add_command(label=lang[1], command=lambda: show_admin_panel(log_file, connection))
    spravka_menu.add_command(label=lang[2], command=lambda:show_about(log_file))
    
    exit_menu = Menu(tearoff=0)
    exit_menu.add_command(label=lang[16], command=lambda: restart())
    exit_menu.add_command(label=lang[17], command=lambda: del_all_windows())
    
    main_menu = Menu()
    main_menu.add_command(label=lang[3],command=lambda:show_settings(log_file))
    main_menu.add_cascade(label=lang[4], menu=spravka_menu)
    main_menu.add_cascade(label=lang[15], menu=exit_menu)
 
    tk.config(menu=main_menu)

    marki = ["Lada", "Haval", "BMW", "Mercedes", "Toyota", "Mazda", "Nissan", "Audi"]
    vidi_raboti = ["Техническое обслуживание", "Диагностика", "Ремонт ходовой части", "Ремонт двигателя", "Ремонт трансмиссии", "Шиномонтаж и балансировка","Сход-развал", "Кузовной ремонт и покраска", "Ремонт электрики и электроники"]

    new_work = LabelFrame(tk, text=lang[5], font=("Arial", 15))
    today = IntVar()
    FIO_Label = Label(new_work, text=lang[6], font=("Arial", 13))
    FIO_Entry = Entry(new_work)
    MARKA_Label = Label(new_work, text=lang[7], font=("Arial", 13))
    VIDI_Label = Label(new_work, text=lang[8], font=("Arial", 13))
    MARKA_Combobox = ttk.Combobox(new_work, values=marki)
    VIDI_Combobox = ttk.Combobox(new_work, values=vidi_raboti)
    TODAY_CheckButton = ttk.Checkbutton(new_work, text=lang[9], variable=today)
    DATE_Entry = DateEntry(new_work, font=("Arial", 13))
    PRICE_Label = Label(new_work, text=lang[10], font=("Arial", 13))
    PRICE_Entry = Entry(new_work)
    SAVE = Button(new_work, text=lang[11], command=lambda: save(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor), font=("Arial", 13))
    UPDATE = Button(new_work, text=lang[12], command=lambda: edit(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox,
                                                                    PRICE_Entry, DATE_Entry, SAVE, today, log_file, connection,
                                                                    cursor, UPDATE, DELETE), font=("Arial", 13))
    DELETE = Button(new_work, text=lang[13], command=lambda: delete(table, log_file, connection, cursor), font=("Arial", 13))
    
    if access == "c":
        SAVE.config(state=DISABLED)
        UPDATE.config(state=DISABLED)
        DELETE.config(state=DISABLED)

    FIO_Label.place(x=10, y=10)
    MARKA_Label.place(x=10, y=50)
    VIDI_Label.place(x=10, y=90)
    VIDI_Combobox.place(x=120, y=90, width=200)
    FIO_Entry.place(x=120, y=10, width=200)
    MARKA_Combobox.place(x=120, y=50)
    TODAY_CheckButton.place(x=10, y=130)
    DATE_Entry.place(x=100, y=130)
    PRICE_Label.place(x=10, y=170)
    PRICE_Entry.place(x=120, y=170)
    SAVE.place(x=10, y=210)
    UPDATE.place(x=10, y=260)
    DELETE.place(x=120, y=260)
    new_work.place(x=20, y=20, width=370, height=350)

  
    FIO_Entry.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor))
    MARKA_Combobox.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor))
    VIDI_Combobox.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor))
    PRICE_Entry.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor))


    columns = ("ID", "FIO", "markaAuto", "vidRabot", "price", "datePriem")
    table = ttk.Treeview(tk, columns=columns, show="headings")
    table.heading("ID", text="Id", anchor="center")
    table.heading("FIO", text=lang[6], anchor="center")
    table.heading("markaAuto", text=lang[7], anchor="center")
    table.heading("vidRabot", text=lang[8], anchor="center")
    table.heading("price", text=lang[10], anchor="center")
    table.heading("datePriem", text=lang[14], anchor="center")
    table.column("ID", width=15, anchor="w")
    table.column("FIO", width=220, anchor="w")
    table.column("markaAuto", width=75, anchor="w")
    table.column("vidRabot", width=180, anchor="w")
    table.column("price", width=75, anchor="w")
    table.column("datePriem", width=75, anchor="w")

    table.place(x=400, y=33, width=785, height=750)

    cursor.execute("SELECT * FROM tab_1;")

    pipls=cursor.fetchall()
    connection.commit()

    for data in pipls:
        new_zayav = []
        for i in data:
            new_zayav.append(rev_cezar(str(i)) if data.index(i) != 0 else str(i))

        table.insert("", END, values=new_zayav)


    setup_sorting(table)
    if access in ('a', 'b'):
        setup_right_click_handler(table, cursor, connection, log_file)

    apply_theme(tk, load_theme())
    
    tk.mainloop()


def start():
    a = loging(log_file)
    if a in ('a', 'b', 'c'):
        main_window(a)

def restart():
    del_all_windows()
    start()
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Выполнен выход из аккаунта\n")
    
start()