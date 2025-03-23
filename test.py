from requests import get, put

# Некорректный запрос (не существующий id)
print(put("http://127.0.0.1:5000/api/jobs/1",
           json={}).json())

# Некорректный запрос (не существующий id)
print(put("http://127.0.0.1:5000/api/jobs/abc",
           json={"job": "abc",
                 "work_size": 15}).json())

# Корректный запрос
print(put("http://127.0.0.1:5000/api/jobs/7",
           json={"job": "Test 3",
                 "team_leader_id": 1,
                 "work_size": 999,
                 "collaborators": "1, 2, 3",
                 "categories": [1, 2],
                 "is_finished": True}).json())

# Убедимся, что работа успешно изменилась
print(get("http://127.0.0.1:5000/api/jobs").json())