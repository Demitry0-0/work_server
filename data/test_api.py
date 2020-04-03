from requests import get, post, delete

print(get('http://localhost:5000/api/v2/jobs').json())  # все работы
print(get('http://localhost:5000/api/v2/jobs/5').json())  # работа с 1 id
print(get('http://localhost:5000/api/v2/jobs/52').json())  # нет работы
print(get('http://localhost:5000/api/v2/jobs/q').json())  # не число

print(post('http://localhost:5000/api/v2/jobs').json())  # нет словаря
print(post('http://localhost:5000/api/v2/jobs', json={'job': 'Sonya'}).json())  # не все поля
# корректный запрос
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 2,
                 'id': 666,
                 'job': 'Текст новости',
                 'work_size': 15,
                 'collaborators': '2',
                 'is_finished': True}).json())
print(delete('http://localhost:5000/api/v2/jobs/999').json())  # id = 999 нет в базе, а если есть удалит
print(delete('http://localhost:5000/api/v2/jobs/2').json())  # корректный если еть такой id
