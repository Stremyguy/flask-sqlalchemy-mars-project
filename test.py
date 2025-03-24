from requests import get, post, delete

# GET
# 1. Получение всех пользователей
# 1.1 Корректный запрос
print(get("http://127.0.0.1:5000/api/v2/users").json())
print()
# 1.2 Некорректный запрос
print(get("http://127.0.0.1:5000/api/v2/users/").json())

print()
print("-" * 50)
print()

# 2. Получение одного пользователя через id
# 2.1 Корректные запросы
print(get("http://127.0.0.1:5000/api/v2/users/1").json())
print(get("http://127.0.0.1:5000/api/v2/users/3").json())
print(get("http://127.0.0.1:5000/api/v2/users/5").json())
print()
# 2.2 Некорректные запросы
print(get("http://127.0.0.1:5000/api/v2/users/999").json())
print(get("http://127.0.0.1:5000/api/v2/users/abc").json())

print()
print("-" * 50)
print()

# POST
# 3. Создание пользователя
# 3.1 Корректные запросы
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"email": "my_test_email_1@gmail.com",
                 "password": "test123_1",
                 "surname": "TestSurname1",
                 "name": "TestName1",
                 "city_from": "Moscow",
                 "age": 45,
                 "position": "Test position 1",
                 "speciality": "Test speciality 1",
                 "address": "Test address 1"}).json())
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"email": "my_test_email_2@gmail.com",
                 "password": "test123_2",
                 "surname": "TestSurname2",
                 "name": "TestName2",
                 "city_from": "Moscow",
                 "age": 55,
                 "position": "Test position 2",
                 "speciality": "Test speciality 2",
                 "address": "Test address 2"}).json())
print()
# 3.2 Некорректные запросы
print(post("http://127.0.0.1:5000/api/v2/users",
           json={}).json())
print(post("http://127.0.0.1:5000/api/v2/users",
           json={"name": "ABC Name"}).json())

print()
print("-" * 50)
print()

# DELETE
# 3. Удаление пользователя
# 3.1 Корректные запросы 
# !!! пользователи с ID 7 и 8 были созданы в прошлых запросах
print(delete("http://127.0.0.1:5000/api/v2/users/7").json())
print(delete("http://127.0.0.1:5000/api/v2/users/8").json())
print()
# 3.2 Некорректные запросы
print(delete("http://127.0.0.1:5000/api/v2/users/999").json())
print(delete("http://127.0.0.1:5000/api/v2/users/abc").json())
print(delete("http://127.0.0.1:5000/api/v2/users/").json())
