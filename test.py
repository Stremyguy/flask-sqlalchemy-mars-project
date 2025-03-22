from requests import get, delete

# Некорректный запрос (не существующий id)
print(delete("http://127.0.0.1:5000/api/jobs/999").json())

# Некорректный запрос (передана строка)
print(delete("http://127.0.0.1:5000/api/jobs/abc").json())

# Корректный запрос
print(delete("http://127.0.0.1:5000/api/jobs/7").json())

# Убедимся, что созданная работа 
# успешно добавилась
print(get("http://127.0.0.1:5000/api/jobs").json())