import datetime
import hashlib
from tkinter import *
from tkinter import messagebox


def save(table, NAME_Entry, PASSWORD_Entry, CONFIRM_Entry, ACCESS_Combobox, log_file, connection, cursor, lang):
    if (PASSWORD_Entry.get() != CONFIRM_Entry.get()):
        messagebox.showerror(lang[5], lang[10])
        return
    else:    
        name = NAME_Entry.get()
        password = PASSWORD_Entry.get()
        access = ACCESS_Combobox.get()
        cursor.execute("INSERT INTO users(name, password, access) VALUES (?, ?, ?)", (name, hashlib.sha256(password.encode('utf-8'))).hexdigest(), access)
        connection.commit()
        for item in table.get_children():
            table.delete(item)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        connection.commit()
        for user in users:
            table.insert("", END, values=user)

        log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Пользователь {table.get_children()[-1]} сохранен \n")
        NAME_Entry.delete(0, END)
        PASSWORD_Entry.delete(0, END)
        ACCESS_Combobox.delete(0, END)
    

def edit(table, NAME_Entry, PASSWORD_Entry, CONFIRM_Entry, ACCESS_Combobox, SAVE, log_file, connection, cursor, UPDATE, DELETE, lang):
    id = table.selection()
    if not id: 
        return
        
    NAME_Entry.delete(0, END)
    NAME_Entry.insert(0, table.item(id)["values"][1])
    PASSWORD_Entry.delete(0, END)
    PASSWORD_Entry.insert(0, table.item(id)["values"][2])
    ACCESS_Combobox.delete(0, END)
    ACCESS_Combobox.insert(0, table.item(id)["values"][3])

    SAVE.config(text="Применить", command=lambda: update(table, id, NAME_Entry, PASSWORD_Entry, CONFIRM_Entry,
                                                     ACCESS_Combobox, log_file, connection, cursor, UPDATE, DELETE, SAVE, lang))
    UPDATE.config(state=DISABLED)
    DELETE.config(state=DISABLED)

def update(table, id, NAME_Entry, PASSWORD_Entry, CONFIRM_Entry, ACCESS_Combobox, log_file, connection, cursor, UPDATE, DELETE, SAVE, lang):
    if not id: 
        return
        
    if (PASSWORD_Entry.get() != CONFIRM_Entry.get()):
        messagebox.showerror(lang[5], lang[10])
        return
    else:    
        name = NAME_Entry.get()
        password = PASSWORD_Entry.get()
        access = ACCESS_Combobox.get()

        cursor.execute("UPDATE users SET name = ?, password = ?, access = ? WHERE ID = ?;", 
                    (name, hashlib.sha256(password.encode('utf-8')).hexdigest(), access, table.item(id)['values'][0]))
                    
        log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Пользователь {id[0]} изменен \n")
        connection.commit()
        
        for item in table.get_children():
            table.delete(item)
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        connection.commit()
        for user in users:
            table.insert("", END, values=user)
            
        NAME_Entry.delete(0, END)
        PASSWORD_Entry.delete(0, END)
        ACCESS_Combobox.delete(0, END)
        SAVE.config(text="Сохранить", command=lambda: save(table, NAME_Entry, PASSWORD_Entry, ACCESS_Combobox, log_file, connection, cursor, lang))
        UPDATE.config(state=NORMAL)
        DELETE.config(state=NORMAL)
    

def delete(table, log_file, connection, cursor):
    id = table.selection()
    id_data = table.item(id)["values"][0]
    cursor.execute("DELETE FROM users WHERE ID = ?", (id_data,))
    connection.commit()
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    connection.commit()
    for user in users:
        table.insert("", END, values=user)

    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Пользователь {id[0]} удален \n")