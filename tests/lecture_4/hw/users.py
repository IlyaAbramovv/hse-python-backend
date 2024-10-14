import base64
from http import HTTPStatus

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from lecture_4.demo_service.api.contracts import UserResponse
from lecture_4.demo_service.api.main import create_app

faker = Faker()
app = create_app()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def user(password, client):
    username = 'test_user_1'

    name = 'test_name_1'
    birthdate = str(faker.date_time().isoformat())

    resp = client.post('/user-register', json={
        'username': username,
        'name': name,
        'birthdate': birthdate,
        'password': password,
    })
    json = resp.json()
    return UserResponse(uid=json['uid'], username=username, name=name, birthdate=birthdate, role=json['role'])


@pytest.fixture()
def password():
    return "secret_password_12345"


@pytest.fixture()
def admin_creds():
    return base64.b64encode(f"admin:superSecretAdminPassword123".encode("ascii")).decode("utf-8")


def test_register_user(password, user, client):
    username = 'test_user'
    name = 'test_name'
    birthdate = str(faker.date_time().isoformat())

    resp = client.post('/user-register', json={
        'username': username,
        'name': name,
        'birthdate': birthdate,
        'password': password,
    })
    json = resp.json()

    assert resp.status_code == HTTPStatus.OK
    assert json['username'] == username
    assert json['birthdate'] == birthdate
    assert json['name'] == name


def test_register_user_with_username_already_taken(client, password, user):
    resp = client.post('/user-register', json={
        'username': user.username,
        'name': user.name,
        'birthdate': str(user.birthdate),
        'password': password,
    })

    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_register_with_invalid_password(client):
    resp = client.post('/user-register', json={
        'username': 'user1',
        'name': 'user1',
        'birthdate': str(faker.date_time().isoformat()),
        'password': '1',
    })

    assert resp.status_code == HTTPStatus.BAD_REQUEST


def test_get_unknown_user(password, admin_creds, client):
    response = client.post(
        "/user-get",
        params={'username': 'unknown'},
        headers={"Authorization": "Basic " + admin_creds},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_user_username_and_id_provided(user, admin_creds, client):
    response = client.post(
        "/user-get",
        params={'username': user.username, 'id': user.uid},
        headers={"Authorization": "Basic " + admin_creds},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_neither_username_nor_id_provided(user, admin_creds, client):
    response = client.post(
        "/user-get",
        headers={"Authorization": "Basic " + admin_creds},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_by_id(user, admin_creds, client):
    response = client.post(
        "/user-get",
        params={'id': user.uid},
        headers={"Authorization": "Basic " + admin_creds},
    )

    json = response.json()
    assert response.status_code == HTTPStatus.OK
    assert json['username'] == user.username
    assert json['uid'] == user.uid
    assert json['role'] == user.role


def test_user_get_with_invalid_password(user, client):
    creds = base64.b64encode(f"admin:wrong-password".encode("ascii")).decode("utf-8")
    response = client.post(
        "/user-get",
        params={'id': user.uid},
        headers={"Authorization": "Basic " + creds},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_user_promote(user, admin_creds, client):
    response = client.post(
        '/user-promote',
        params={'id': user.uid},
        headers={"Authorization": "Basic " + admin_creds}
    )

    assert response.status_code == HTTPStatus.OK


def test_user_promote_not_being_admin(user, password, client):
    creds = base64.b64encode(f"{user.username}:{password}".encode("ascii")).decode("utf-8")
    response = client.post(
        '/user-promote',
        params={'id': user.uid},
        headers={"Authorization": "Basic " + creds}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_user_promote_unknown_user(user, password, admin_creds, client):
    response = client.post(
        '/user-promote',
        params={'id': 12345},
        headers={"Authorization": "Basic " + admin_creds}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
