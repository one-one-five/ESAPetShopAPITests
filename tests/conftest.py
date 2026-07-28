import pytest
import allure
import httpx
from random import randint

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@pytest.fixture
def create_pet():
    '''Фикстура создания питомца'''
    body = {
        "id": randint(100, 999),
        "name": "Buddy",
        "status": "available"
    }
    with allure.step('Отправка запроса на создание питомца'):
        response = httpx.post(url=f'{BASE_URL}/pet', json=body)
        assert response.status_code == 200
        return response.json()
