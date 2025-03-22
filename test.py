from requests import get, post

# Некорректный запрос (пустой json, нет информации 
# для добавления новой работы)
print(post("http://127.0.0.1:5000/api/jobs",
           json={}).json())

# Некорректный запрос (не достаточно информации 
# для добавления новой работы (только параметр "job"))
print(post("http://127.0.0.1:5000/api/jobs",
           json={"job": "Test job"}).json())

# Некорректный запрос (пытаемся добавить 
# несуществующий ключ "key")
print(post("http://127.0.0.1:5000/api/jobs",
           json={"key": 123}).json())

# Корректный запрос
print(post("http://127.0.0.1:5000/api/jobs",
           json={"job": "Test job",
                 "team_leader_id": 1,
                 "work_size": 90,
                 "collaborators": "1, 2, 3",
                 "categories": [1],
                 "is_finished": True}).json())

# Убедимся, что созданная работа 
# успешно добавилась
print(get("http://127.0.0.1:5000/api/jobs").json())