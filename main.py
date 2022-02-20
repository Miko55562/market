from flask import Flask, request, jsonify, make_response, render_template, url_for, send_file, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps
import json
import db

# Инициализация приложения

app = Flask(__name__, static_url_path='/static')

# Секретный ключ для создания токина авторизании

SECRET_KEY = 'AD8dfdsgADs'

# получение фотографий по ссылке

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

# проверка токена

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        try:
            if 'X-Access-Tokens' in request.headers: # проверка наличия токена
                token = request.headers['X-Access-Tokens'] # получение токена из запроса
                data = jwt.decode(token, SECRET_KEY, "HS256") # расшифровка токена
                current_user = db.public_id(data['public_id'])[0][2] # получение email
                return f(current_user, *args, **kwargs) # возвращение к функции
            if not token:
                return jsonify({'message': 'a valid token is missing'})
        except:
            return jsonify({'message': 'your token is expired'})
    return decorator

# Запрос данных пользователя


@app.route('/user', methods=['GET'])
@token_required # проверка токена
def get_user(current_user):
    print(current_user)
    result = db.user(current_user) # получение всех пользователей
    return jsonify({'users': result}) # вывод пользователей JSON ответом


# Запрос всех продуктов


@app.route('/products', methods=['GET'])
def get_all_products():

    result = db.all_products() # получение всех продуктов

    return jsonify({'products': result}) # вывод продуктов JSON ответом


# Регистрация!


@app.route('/register', methods=['GET', 'POST'])
def signup_user():

    data = request.get_json() # чтение данных регистрации

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha1') # создание хеша пароля
    if data['email'] in db.all_emails(): # проверка на уже существующие имейлы
        return jsonify({'message': 'the email already exists'}) # вывод ошибки
    elif 'name' not in data:
        if db.register(data['email'],data['email'],hashed_password,str(uuid.uuid4())): # запрос на регистрацию
            return jsonify({'message': 'registered successfully'})
    elif 'name' in data:
        if db.register(data['name'],data['email'],hashed_password,str(uuid.uuid4())): # запрос на регистрацию
            return jsonify({'message': 'registered successfully'})
    else:
        return jsonify({'message': 'error'})

# Вход в систему!


@app.route('/login', methods=['GET', 'POST'])
def login_user():

  data = request.get_json()  # чтение данных авторизации
  print(data)
  user = db.user(data['email'])[0] # поиск существующего пользователя по почте

  if check_password_hash(user[3], data['password']): # проверка пароля
     token = jwt.encode({'public_id': user[5], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=30)}, SECRET_KEY, "HS256")  # создание токена
     return jsonify({'token' : token})  # отправка токена

  return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


# получение избранных продуктов

@app.route('/elect', methods=['GET'])
@token_required # проверка токена
def electget(current_user):
   data = request.get_json() # получение запроса
   result = db.user(current_user)[0][4] # получение избранных из данных о пользователе
   return jsonify({'message' : result})

# добавление в избранное

@app.route('/elect', methods=['POST'])
@token_required # проверка токена
def electadd(current_user):
   data = request.get_json() # получение запроса
   db.elect_add(data["elect"], current_user) # добавление в избранное
   return jsonify({'message' : data})

# удаление из избранного

@app.route('/elect', methods=['DELETE'])
@token_required # проверка токена
def electdell(current_user):
   data = request.get_json() # получение запроса
   db.elect_dell(data["elect"], current_user) # добавление в избранное
   return jsonify({'message' : data})

# получение корзины пользователя

@app.route('/basket', methods=['GET'])
@token_required # проверка токена
def basketget(current_user):
   data = request.get_json() # получение запроса
   result = db.user(current_user)[0][6] # получение корзины из данных о пользователе
   return jsonify({'message' : result})


# добавление в корзину

@app.route('/basket', methods=['POST'])
@token_required # проверка токена
def basketadd(current_user):
   data = request.get_json() # получение запроса
   db.basket_add(data["basket"], current_user) # добавление в избранное
   return jsonify({'message' : data})

# удаление из корзины

@app.route('/basket', methods=['DELETE'])
@token_required # проверка токена
def basketdell(current_user):
   data = request.get_json() # получение запроса
   db.basket_dell(data["basket"], current_user) # добавление в избранное
   return jsonify({'message' : data})


@app.route('/buy', methods=['GET'])
@token_required # проверка токена
def buy(current_user):
   db.buy(current_user) # добавление в избранное
   return jsonify({'message' : 'ok'})


if  __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
