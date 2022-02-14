import sqlite3
from sqlite3 import Error
import datetime

global conn
conn  = sqlite3.connect('sqlite_python.db', check_same_thread=False)
global cur
cur = conn.cursor()

# получение всех пользователей

def all_users():

    cur.execute("SELECT * FROM users;")
    result = cur.fetchall() # получение результата
    return result

# получение всех продуктов

def all_products():

    cur.execute("SELECT * FROM products;")
    result = cur.fetchall() # получение результата
    return result

# пролучение имейлов

def all_emails():

    l = list()
    cur.execute("SELECT * FROM users;")
    result = cur.fetchall() # получение результата
    for i in range(len(result)):
        l.append(result[i][2])
    return l

# регистрация

def register(name,email,password,public_id):
    elect=''
    basket=''
    cur.execute(f"INSERT INTO users VALUES (:id, :name, :email, :password, :elect, :public_id, :basket);",
    {'id': len(all_emails())+1, 'name': name, 'email': email, 'password': password,
                          'elect': elect, 'public_id':public_id, 'basket': basket})
    conn.commit() # сохранение данных
    return True

# поиск по имейлу

def user(email):
    cur.execute(f"SELECT * FROM users WHERE email=?", (email,))
    result = cur.fetchall()
    #print(result)
    return result

# поиск по публичному id

def public_id(public_id):
    cur.execute(f"SELECT * FROM users WHERE public_id=?", (public_id,))
    result = cur.fetchall() # получение результата
    #print(result)
    return result

# добавление в избранное

def elect_add(elect, current_user):
    cur.execute(f"SELECT * FROM users WHERE email=?", (current_user,))
    result = cur.fetchall()[0][4].split() # получение избранных пользователя
    ans = ''
    if elect not in result: # проверка на существование в списке таких же позиций
        result.append(elect) # добавление в список избранных
        for i in result:
            ans += i+' '
        cur.execute(f"UPDATE users SET elect=(:elect) WHERE email=(:current_user);",
                             {'elect': ans, 'current_user': current_user})
    conn.commit() # сохранение данных

# удаление из избранного

def elect_dell(elect, current_user):
    cur.execute(f"SELECT * FROM users WHERE email=?", (current_user,))
    result = cur.fetchall()[0][4].split() # получение избранных пользователя
    ans = ''
    if elect in result: # проверка на существование в списке таких же позиций
        result.pop(result.index(elect)) # удаление из списка избранных
        for i in result:
            ans += i+' '
        cur.execute(f"UPDATE users SET elect=(:elect) WHERE email=(:current_user);",
                             {'elect': ans, 'current_user': current_user})
    conn.commit() # сохранение данных

# добавление в корзину

def basket_add(elect, current_user):
    cur.execute(f"SELECT * FROM users WHERE email=?", (current_user,))
    result = cur.fetchall()[0][6].split() # получение корзины пользователя
    ans = ''
    if elect not in result: # проверка на существование в списке таких же позиций
        result.append(elect)  # добавление в список корзины
        for i in result:
            ans += i+' '
        cur.execute(f"UPDATE users SET basket=(:elect) WHERE email=(:current_user);",
                             {'elect': ans, 'current_user': current_user})
    conn.commit() # сохранение данных

# удаление из корзины

def basket_dell(elect, current_user):
    cur.execute(f"SELECT * FROM users WHERE email=?", (current_user,))
    result = cur.fetchall()[0][6].split() # получение корзины пользователя
    ans = ''
    if elect in result: # проверка на существование в списке таких же позиций
        result.pop(result.index(elect)) # удаление из списка корзины
        for i in result:
            ans += i+' '
        cur.execute(f"UPDATE users SET basket=(:elect) WHERE email=(:current_user);",
                             {'elect': ans, 'current_user': current_user})
    conn.commit() # сохранение данных
