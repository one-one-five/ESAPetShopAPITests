import allure
import httpx
import pytest
from random import randint
from jsonschema import validate
from .schema.store_json_schema import STORE_JSON

from conftest import BASE_URL_store


@allure.feature('Store')
class TestStore:
    @allure.title('Размещение заказа (#42)')
    def test_placing_an_order(self, create_order):
        body, response_json_post = create_order

        with allure.step('Проверка, что ответ содержит переданные данные'):
            for key in body.keys():
                assert response_json_post[key] == body[key], f'Переданное значение {key} не совпадает с ответом'

    @allure.title('Получение информации о заказе по ID (#43)')
    def test_get_order_by_id(self, create_order):
        with allure.step('Получаем ID заказа'):
            body, response_json = create_order
            order_id = response_json['id']

        with allure.step(f'Получаем информацию о заказе с ID {order_id}'):
            response = httpx.get(f'{BASE_URL_store}/order/{order_id}')
            response_json_get = response.json()

        with allure.step('Проверяем статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

        with allure.step(f'Проверка ответ содержит данные заказа {order_id}'):
            for key in body.keys():
                assert response_json_get[key] == body[key], f'Переданное значение {key} не совпадает с ответом'

    @allure.title('Удаление заказа по ID (#44)')
    def test_delete_order_by_id(self, create_order):
        with allure.step('Получаем ID заказа'):
            body, response_json = create_order
            order_id = response_json['id']

        with allure.step(f'Отправляем запрос на удаление заказа по ID {order_id}'):
            response = httpx.delete(f'{BASE_URL_store}/order/{order_id}')

        with allure.step('Проверяем статус ответа'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

        with allure.step('Отправка запроса с удаленным ID заказа'):
            response = httpx.get(f'{BASE_URL_store}/order/{order_id}')

        with allure.step('Проверяем статус ответа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожидаемым'

    @allure.title('Попытка получить информацию о несуществующем заказе (#45)')
    def test_get_information_about_nonexistentorder(self):
        with allure.step('Отправка запроса с несуществующим ID'):
            response = httpx.get(f'{BASE_URL_store}/order/{randint(100, 900)}')

        with allure.step('Проверяем статус ответа'):
            assert response.status_code == 404, 'Код ответа не совпадает с ожидаемым'

    @allure.title('Получение инвентаря магазина (#46)')
    def test_get_shop_inventory(self):
        with allure.step('Отправляем запрос'):
            response = httpx.get(f'{BASE_URL_store}/inventory')
            response_json = response.json()

        with allure.step('Проверяем статус'):
            assert response.status_code == 200, 'Код ответа не совпадает с ожидаемым'

        with allure.step('Валидация JSON'):
            validate(response.json(),STORE_JSON), 'Тип ответа не словарь'

        # with allure.step('Проверка, что тело ответа — словарь'):
        #     assert isinstance(response_json, dict), '
        #     for key, value in response_json.items():
        #         assert isinstance(key, str), 'Тип ключа не строка'
        #         assert isinstance(value, int), 'Тип значения не число'
