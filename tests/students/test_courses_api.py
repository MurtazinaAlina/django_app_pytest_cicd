
'''Фикстуры вынесла в отдельный  файл'''
from tests.students.fixtures import *


@pytest.mark.django_db
def test_get_course_retrieve(client, courses_factory, url): # проверка получения 1го курса (retrieve-логика)

    courses = courses_factory(_quantity=10)
    for index, course in enumerate(courses):
        res = client.get(url + f'{index + 1}/')
        assert res.status_code == 200 # проверка на возврат курса по коду

        data = res.json()
        assert data['name'] == courses[index].name # проверка на возврат конкретного курса


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

    for index, course in enumerate(courses):
        res = client.get(url, {'id': course.id})
        assert res.status_code == 200 # проверка на возврат отфильтрованного по 'id' курса по коду
        assert res.json()[0]['id'] == courses[index].id # проверка на возврат конкретного отфильтрованного по 'id' курса'

    for course in courses:
        res = client.get(url, {'name': course.name})
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

    courses = courses_factory(_quantity=10)

    for index, course in enumerate(courses):
        pk_for_patch = index + 1
        url_for_patch = f'{url}{pk_for_patch}/'
        data = {'name': 'new_name'}

        res = client.patch(url_for_patch, data)
        assert res.status_code == 200 # проверка по коду

        res = client.get(url_for_patch)
        data = res.json()
        assert data['name'] == 'new_name' # проверка по параметрам апдейта


@pytest.mark.django_db
def test_delete_course(client, url, courses_factory): # проверка успешного удаления курса

    courses = courses_factory(_quantity=10)

    for index, course in enumerate(courses):

        count = Course.objects.count()
        pk_for_delete = index + 1
        url_for_delete = f'{url}{pk_for_delete}/'

        res = client.delete(url_for_delete)
        assert res.status_code == 204 # проверка по коду удаления

        res = client.get(url)
        assert len(res.json()) == count - 1 # проверка на уменьшение списка


@pytest.mark.parametrize(  # валидация на максимальное число студентов на курсе – 20
    ['students_quantity', 'expected_status'],
    (
            (5, 200), (23, 400)
    )
)
@pytest.mark.django_db
def test_settings_limit_students(client, url, courses_factory, student_factory,
                                 students_quantity, expected_status):
    courses = courses_factory(_quantity=1)
    students = student_factory(_quantity=students_quantity)
    student_ids = [i.id for i in students]

    for index, course in enumerate(courses):
        res = client.patch(f'{url}{index+1}/', {'name': course.name,'students': student_ids})
        assert res.status_code == expected_status


@pytest.mark.parametrize( # валидация на максимальное число студентов, c переопределением лимита
    ['students_quantity', 'students_limit'],
    (
            (5, settings.MAX_STUDENTS_PER_COURSE), (2, 3)
    )
)
@pytest.mark.django_db
def test_settings_limit_students_without_instance(student_factory, students_quantity, students_limit):

    students = student_factory(_quantity=students_quantity)
    student_ids = [i.id for i in students]
    assert len(student_ids) <= students_limit


