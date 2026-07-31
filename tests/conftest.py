import pytest
import allure
import httpx
from random import randint

BASE_URL_pet = 'http://5.181.109.28:9090/api/v3'
BASE_URL_store = 'http://5.181.109.28:9090/api/v3/store'


@pytest.fixture
def create_pet():
    '''Фикстура создания питомца'''
    body = {
        "id": randint(100, 999),
        "name": "Buddy",
        "status": "available"
    }
    with allure.step('Отправка запроса на создание питомца'):
        response = httpx.post(url=f'{BASE_URL_pet}/pet', json=body)
        assert response.status_code == 200
        return response.json()


@pytest.fixture
def create_order():
    '''Фикстура создания заказа'''

    body = {
        "id": randint(100, 999),
        "petId": randint(100, 999),
        "quantity": randint(100, 999),
        "status": "placed",
        "complete": True
    }
    with allure.step('Отправка запроса на размещение заказа'):
        response = httpx.post(f'{BASE_URL_store}/order', json=body)

    with allure.step('Проверка статусу'):
        assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
    return body, response.json()


@pytest.fixture()
def create_order_and_delete():
    '''Фикстура создания и удаления заказа'''

    body = {
        "id": randint(100, 999),
        "petId": randint(100, 999),
        "quantity": randint(100, 999),
        "status": "placed",
        "complete": True
    }
    with allure.step('Отправка запроса на размещение заказа'):
        response = httpx.post(f'{BASE_URL_store}/order', json=body)

    with allure.step('Проверка статусу'):
        assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'
    order_id = body['id']
    yield body, response.json()

    with allure.step(f'Отправляем запрос на удаление заказа по ID {order_id}'):
        response = httpx.delete(f'{BASE_URL_store}/order/{order_id}')

    with allure.step('Проверяем статус ответа'):
        assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

    with allure.step('Отправка запроса с удаленным ID заказа'):
        response = httpx.get(f'{BASE_URL_store}/order/{order_id}')

    with allure.step('Проверяем статус ответа с удаленным заказом'):
        assert response.status_code == 404, 'Код ответа не совпадает с ожидаемым'
