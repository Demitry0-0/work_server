from requests import get, post, delete
import datetime

print(get('http://localhost:5000/api/v2/users/5').json(), '\n')
print(post('http://localhost:5000/api/v2/users',
           json={'surname': '666',
                 'name': 'dfsfddsffsd',
                 'age': 15,
                 'position': '2',
                 'speciality': 'rsdffd',
                 'address': 'sdfsfd',
                 'email': 'dsf@fddssfdsdsdfsd.ru',
                 'hashed_password': 'asdfasdfsasaf'}).json())
print(get('http://localhost:5000/api/v2/users/5').json(), '\n')
print(delete('http://localhost:5000/api/v2/users/5').json())
print(get('http://localhost:5000/api/v2/users/5').json(), '\n')
