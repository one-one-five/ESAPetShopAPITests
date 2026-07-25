import allure
import httpx
from jsonschema import validate
from .schema.pet_json import PET_JSON

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Pet')
class TestPet:
    @allure.title('Попытка удалить несуществующего питомца')
    def test_delete_nonexistent_pet(self):
        with allure.step('Отправка запроса на удаление несуществующего питомца'):
            response = httpx.delete(url=f'{BASE_URL}/pet/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet deleted', 'Текст ошибки не совпал с ожидаемым '

    @allure.title('Попытка обновить несуществующего питомца')
    def test_update_nonexistent_pet(self):
        with allure.step('Отправка запроса на обновление несуществующего питомца'):
            body = {
                'id': 9999
                , 'name': 'Non-existent Pet'
                , 'status': 'available'
            }
            response = httpx.put(url=f'{BASE_URL}/pet', json=body)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым '

    @allure.title('Попытка получить информацию о несуществующем питомце')
    def test_get_nonexistent_pet(self):
        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = httpx.get(url=f'{BASE_URL}/pet/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet not found', 'Текст ошибки не совпал с ожидаемым'

    @allure.title('Добавление нового питомца c полными данными')
    def test_add_new_pet(self):
        body = {
            "id": 77
            , "name": "doggie"
            , "category": {
                "id": 88
                , "name": "Dogs"
            }
            , "photoUrls": ["string"]
            , "tags": [
                {
                    "id": 99
                    , "name": "string"
                }
            ]
            , "status": "available"
        }
        response = httpx.post(url=f'{BASE_URL}/pet', json=body)

        with allure.step('Отправка запроса на создание питомца'):
            with allure.step('Проверка статуса ответа'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

            response_json = response.json()

            with allure.step('Валидация JSON схемы'):
                validate(response_json, PET_JSON)

            with allure.step('Проверка полей ответа'):
                assert response_json == body
