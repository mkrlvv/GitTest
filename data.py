import datetime
from tkinter import *
from encoding import *
from tkinter.ttk import Treeview

ID = 1
 #  save(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor)
def save(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Entry, DATE_Entry, today, log_file, connection, cursor):

    name = FIO_Entry.get()
    marka = MARKA_Combobox.get()
    vid = VIDI_Combobox.get()
    price = PRICE_Entry.get()
    date = DATE_Entry.get() if not today else datetime.date.today()
    cursor.execute(
        'INSERT INTO tab_1(name, marka, vid, price, date) VALUES (?, ?, ?, ?, ?);', (cezar(name), cezar(marka), cezar(vid), cezar(price), cezar(str(date))))
    connection.commit()
    for item in table.get_children():
        table.delete(item)
    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)

    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {table.get_children()[-1]} сохранена \n")
    FIO_Entry.delete(0, END)
    MARKA_Combobox.delete(0, END)
    VIDI_Combobox.delete(0, END)
    PRICE_Entry.delete(0, END)
    DATE_Entry.delete(0, END)



def edit(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Combobox, DATE_Entry, SAVE, today, log_file, connection, cursor, UPDATE, DELETE):
    id = table.selection()
    if not id:
        return

    ID_T = table.item(id)["values"][0]
    DATE_Entry.delete(0, END)

    date_str = table.item(id)["values"][5]
    if isinstance(date_str, str):
        try:
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
                except ValueError:
                    pass
        except ValueError as e:
            print(f"Ошибка преобразования даты: {e}")
            date_obj = datetime.date.today()
    else:
        date_obj = date_str

    DATE_Entry.set_date(date_obj)
    FIO_Entry.insert(0, table.item(id)["values"][1])
    MARKA_Combobox.insert(0, table.item(id)["values"][2])
    VIDI_Combobox.insert(0, table.item(id)["values"][3])
    PRICE_Combobox.insert(0, table.item(id)["values"][4])

    SAVE.config(text="Применить", command=lambda: update(table, SAVE, id,
                                                           FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Combobox,
                                                           DATE_Entry, today, log_file, connection, cursor, UPDATE, DELETE))
    UPDATE.config(state=DISABLED)
    DELETE.config(state=DISABLED)

    

def update(table, SAVE, id,
           FIO_Entry, MARKA_Combobox, VIDI_Combobox, PRICE_Combobox, DATE_Entry, today, log_file, connection, cursor, UPDATE, DELETE):
    name = FIO_Entry.get()
    marka = MARKA_Combobox.get()
    vid = VIDI_Combobox.get()
    price = PRICE_Combobox.get()
    date = DATE_Entry.get() if not today else datetime.date.today()

    cursor.execute("UPDATE tab_1 SET name = ?, marka = ?, vid = ?, price = ?, date = ? WHERE ID = ?;", (cezar(name), cezar(marka), cezar(vid), cezar(price), cezar(str(date)), table.item(id[0])['values'][0]))
    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {id[0]} изменена \n")
    connection.commit()
    for item in table.get_children():
        table.delete(item)
    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)
    FIO_Entry.delete(0, END)
    MARKA_Combobox.delete(0, END)
    VIDI_Combobox.delete(0, END)
    PRICE_Combobox.delete(0, END)
    DATE_Entry.delete(0, END)
    SAVE.config(text="Сохранить", command=lambda: save(table, FIO_Entry, MARKA_Combobox, VIDI_Combobox,
                                                         PRICE_Combobox, DATE_Entry, today, log_file, connection, cursor))
    UPDATE.config(state=NORMAL)
    DELETE.config(state=NORMAL)

def delete(table: Treeview, log_file, connection, cursor):

    id = table.selection()
    id_data = table.item(id)["values"][0]
    cursor.execute("DELETE FROM tab_1 WHERE ID = ?", (id_data,))
    connection.commit()
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)

    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {id[0]} удалена \n")
    
def setup_right_click_handler(table, cursor, connection, log_file):
    
    def on_right_click(event):
        item = table.identify_row(event.y)
        if item:
            table.selection_set(item)
            show_context_menu(event)
    
    def show_context_menu(event):
        menu = Menu(table, tearoff=0)
        menu.add_command(
            label="Удалить", 
            command=lambda: delete(table, log_file, connection, cursor)
        )
        menu.post(event.x_root, event.y_root)
    
    table.bind("<Button-3>", on_right_click)