from requests import get, post, delete

# GET
# 1. Получение всех работ
# 1.1 Корректный запрос
print(get("http://127.0.0.1:5000/api/v2/jobs").json())
print()
# 1.2 Некорректный запрос
print(get("http://127.0.0.1:5000/api/v2/jobs/").json())

print()
print("-" * 50)
print()

# 2. Получение одной работы через id
# 2.1 Корректные запросы
print(get("http://127.0.0.1:5000/api/v2/jobs/1").json())
print(get("http://127.0.0.1:5000/api/v2/jobs/3").json())
print(get("http://127.0.0.1:5000/api/v2/jobs/5").json())
print()
# 2.2 Некорректные запросы
print(get("http://127.0.0.1:5000/api/v2/jobs/999").json())
print(get("http://127.0.0.1:5000/api/v2/jobs/abc").json())

print()
print("-" * 50)
print()

# POST
# 3. Создание работы
# 3.1 Корректные запросы
print(post("http://127.0.0.1:5000/api/v2/jobs",
           json={"job": "Job Test Title 1",
                 "team_leader_id": 1,
                 "work_size": 35,
                 "collaborators": "1, 2",
                 "city_from": "Moscow",
                 "categories": [1, 2],
                 "is_finished": False}).json())
print(post("http://127.0.0.1:5000/api/v2/jobs",
           json={"job": "Job Test Title 2",
                 "team_leader_id": 2,
                 "work_size": 45,
                 "collaborators": "2, 3",
                 "city_from": "Washington",
                 "categories": [2, 3],
                 "is_finished": False}).json())
print()
# 3.2 Некорректные запросы
print(post("http://127.0.0.1:5000/api/v2/jobs",
           json={}).json())
print(post("http://127.0.0.1:5000/api/v2/jobs",
           json={"job": "My Job Title"}).json())

print()
print("-" * 50)
print()

# DELETE
# 3. Удаление работы
# 3.1 Корректные запросы 
# !!! работы с ID 7 и 8 были созданы в прошлых запросах
print(delete("http://127.0.0.1:5000/api/v2/jobs/7").json())
print(delete("http://127.0.0.1:5000/api/v2/jobs/8").json())
print()
# # 3.2 Некорректные запросы
print(delete("http://127.0.0.1:5000/api/v2/jobs/999").json())
print(delete("http://127.0.0.1:5000/api/v2/jobs/abc").json())
print(delete("http://127.0.0.1:5000/api/v2/jobs/").json())
