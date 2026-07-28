import allure
import httpx
from jsonschema import validate
from .schema.pet_json_schema import PET_JSON

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

    @allure.title('Добавление нового питомца')
    def test_add_new_pet(self):
        body = {
            'id': 100,
            'name': 'Buddy',
            'status': 'available'
        }

        with allure.step('Отправка запроса на создание питомца'):
            response = httpx.post(url=f'{BASE_URL}/pet', json=body)
            response_json = response.json()
            with allure.step('Проверка статуса ответа и валидация JSON-схемы'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
                validate(response.json(), PET_JSON)

            with allure.step('Проверка параметров питомца в ответе'):
                assert response_json['id'] == body['id'], 'id питомца не совпадает с ожидаемым'
                assert response_json['name'] == body['name'], 'имя питомца не совпадает с ожидаемым'
                assert response_json['status'] == body['status'], 'статус питомца не совпадает с ожидаемым'

    @allure.title('Добавление нового питомца c полными данными')
    def test_add_new_pet_with_full_body(self):
        body = {
            'id': 77,
            'name': 'doggie',
            'category': {
                'id': 88,
                'name': 'Dogs'
            },
            'photoUrls': ['string'],
            'tags': [
                {
                    'id': 99,
                    'name': 'string'
                }
            ],
            'status': 'available'
        }

        with allure.step('Отправка запроса на создание питомца'):
            response = httpx.post(url=f'{BASE_URL}/pet', json=body)
            response_json = response.json()
            with allure.step('Проверка статуса ответа'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

            with allure.step('Валидация JSON схемы'):
                validate(response_json, PET_JSON)

            with allure.step('Проверка полей ответа'):
                assert response_json == body

    @allure.title('Получение информации о питомце по ID')
    def test_get_pet_id(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet['id']

        with allure.step('Отправка запроса на получение информации о питомце по ID'):
            response = httpx.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200
            assert response.json()['id'] == pet_id

    @allure.title('Обновление информации о питомце')
    def test_update_pet(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet['id']

        with allure.step('Подготовить данные для обновления'):
            body = {
                'id': pet_id,
                'name': 'Buddy_update',
                'status': 'sold'
            }

        with allure.step('Отправка запроса на обновление питомца'):
            response = httpx.put(url=f'{BASE_URL}/pet', json=body)
            response_json = response.json()

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200

        with allure.step('Проверка тела ответа'):
            assert response_json['id'] == pet_id
            assert response_json['name'] == body['name']
            assert response_json['status'] == body['status']

    @allure.title('Удаление питомца по ID')
    def test_delete_pet_id(self, create_pet):
        with allure.step('Получение ID созданного питомца'):
            pet_id = create_pet['id']

        with allure.step('Отправка запроса на удаление питомца по ID'):
            response = httpx.delete(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200

        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Pet deleted'

        with allure.step('Отправка запроса с удаленным ID питомца'):
            response = httpx.get(url=f'{BASE_URL}/pet/{pet_id}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'
