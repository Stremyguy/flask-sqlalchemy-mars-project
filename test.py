from requests import get, put

print(put("http://127.0.0.1:5000/api/users/6",
          json={"name": "NAME!",
                "email": "123test@gmail.com",
                "password": "password"}).json())

print(get("http://127.0.0.1:5000/api/users").json())
