import neo4j.exceptions
import psycopg2
from neo4j import GraphDatabase
import requests

from database.database_module import AppDatabase

app_db = AppDatabase()


def test_status_endpoint1_availability():
    response = requests.get("http://localhost:7474/")
    assert response.status_code == 200


def test_status_endpoint2_availability():
    response = requests.get("http://localhost:7687/")
    assert response.status_code == 200


def test_sql_database_connection():
    try:
        connection = psycopg2.connect(dbname="workers", user="postgres", password="postgres", host="127.0.0.1",
                                      port="5432")
        connection.close()
    except psycopg2.OperationalError:
        assert False, "operational error occurred"


def test_graph_database_connection():
    try:
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Murchick228"))
        driver.close()
    except neo4j.exceptions.ServiceUnavailable:
        assert False, "Service unavailable"


def test_all_employees():
    employees = app_db.get_all_employees()
    assert len(employees) == 5


def test_authenticate_employee():
    res1 = app_db.authenticate_employee("john1", 123, False)
    assert res1 == -1

    res2 = app_db.authenticate_employee("john1", 1234, False)
    assert len(res2) == 2

    res3 = app_db.authenticate_employee("admin1", 123, True)
    assert len(res3) == 1


def test_employee_by_login():
    res1 = app_db.find_employee_by_login("john1")
    assert 4 in res1[0]

    res2 = app_db.find_employee_by_login("john123")
    assert len(res2) == 0


def test_get_sick_leaves():
    res = app_db.get_sick_leaves(3)
    assert int(res[0].data()['s']["duration"]) == 21
    assert int(res[1].data()['s']["duration"]) == 14


def test_pensioners():
    res = app_db.get_pensioners()
    assert res[0][0] == 5


def test_get_workers_salary_less_than():
    res = app_db.get_workers_salary_less_than(5000)
    assert len(res) == 2


def test_average_age():
    res = app_db.get_average_age()
    assert res[0][0] == 31.4


def test_sick_leaves_duration_by_department():
    res = app_db.get_sick_leaves_duration_by_department("staff")
    assert res[0].data()['duration'] == 35


def test_worker_experience_by_department():
    res = app_db.get_worker_experience_by_department(3)
    assert res[0][0] == 23


def test_average_salary():
    res = app_db.get_average_salary('female')
    assert res[0][0] == 4000


def test_salary_by_department():
    res = app_db.get_worker_gender_salary_by_department(4, 'male')
    assert res[0][0] == 3000
