
'''Фикстуры вынесла в отдельный  файл'''
from tests.students.fixtures import *


@pytest.mark.django_db
def test_get_course_retrieve(client, courses_factory, url): # проверка получения 1го курса (retrieve-логика)

    course = courses_factory(_quantity=1)
    res = client.get(url)
    assert res.status_code == 200 # проверка на возврат курса по коду
    assert len(res.json()) == len(course)

    data = res.json()
    assert data[0]['name'] == course[0].name # проверка на возврат конкретного курса


@pytest.mark.django_db
def test_get_courses_list(client, courses_factory, url): # проверка получения списка курсов (list-логика)

    courses = courses_factory(_quantity=10)
    res = client.get(url)
    assert res.status_code == 200 # проверка на возврат списка курсов
    assert len(res.json()) == len(courses)

    for index, course in enumerate(res.json()):
        assert course['name'] == courses[index].name # проверка на возврат конкретных курсов


@pytest.mark.django_db
def test_get_courses_filter(client, courses_factory, url): # проверка фильтрации списка курсов

    courses = courses_factory(_quantity=10)
    filter_url = f'{url}?id={courses[1].id}'

    res = client.get(filter_url)
    assert res.status_code == 200 # проверка на возврат отфильтрованного по 'id' курса по коду
    assert  res.json()[0]['id'] == courses[1].id # проверка на возврат конкретного отфильтрованного по 'id' курса'

    for course in courses:
        filter_url = f'{url}?name={course.name}'

        res = client.get(filter_url)
        assert res.status_code == 200 # проверка на возврат отфильтрованного по 'name' курса по коду
        assert res.json()[0]['name'] == course.name # проверка на возврат конкретного отфильтрованного по 'name' курса


@pytest.mark.django_db
def test_create_course(client, url): # проверка успешного создания курса

    data = {'name': 'django'}
    res = client.post(url, data)
    assert res.status_code == 201

    res = client.get(url)
    assert res.json()[0]['name'] == 'django'


@pytest.mark.django_db
def test_update_course(client, url, courses_factory): # проверка успешного обновления курса

    course = courses_factory(_quantity=1)
    pk_for_patch = 1
    url = f'{url}{pk_for_patch}/'
    data = {'name': 'new_name'}

    res = client.patch(url, data)
    assert res.status_code == 200 # проверка по коду

    res = client.get(url)
    data = res.json()
    assert data['name'] == 'new_name' # проверка по параметрам апдейта


@pytest.mark.django_db
def test_delete_course(client, url, courses_factory): # проверка успешного удаления курса

    course = courses_factory(_quantity=1)
    count = Course.objects.count()
    pk_for_delete = 1
    url_for_delete = f'{url}{pk_for_delete}/'

    res = client.delete(url_for_delete)
    assert res.status_code == 204 # проверка по коду удаления

    res = client.get(url)
    assert len(res.json()) == count - 1 # проверка на уменьшение списка
