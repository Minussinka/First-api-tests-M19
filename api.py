import json
import requests
from requests_toolbelt import MultipartEncoder


class PetFriends:
    """API-библиотека к веб-приложению PetFriends."""
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password) -> json:
        """Метод отправляет запрос на сервер и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролю."""
        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter) -> json:
        """Метод отправляет запрос на сервер и возвращает статус и результат в формате JSON
        со списком питомцев. Возможные значения фильтра: 'пустое значение' - получение списка всех питомцев,
        'my_pets' - получение списка своих питомцев."""
        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet(self, auth_key, name, animal_type, age, pet_photo) -> json:
        """Метод отправляет на сервер запрос с данными питомца и возвращает статус
         и результат в формате JSON с данными созданного питомца."""
        data = MultipartEncoder(fields={
            "name": name,
            "animal_type": animal_type,
            "age": age,
            "pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpeg")
        })
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url+"api/pets", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet(self, auth_key, pet_id) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает статус запроса
        в формате JSON с сообщением об успешном выполнении."""
        headers = {"auth_key": auth_key["key"]}

        res = requests.delete(self.base_url+f"api/pets/{pet_id}", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def update_pet_info(self, auth_key, pet_id, name, animal_type, age) -> json:
        """Метод отправляет на сервер запрос на изменение информации о питомце по указанному ID и возвращает
        статус и результат в формате JSON с новыми данными питомца."""
        data = MultipartEncoder(fields={
            "name": name,
            "animal_type": animal_type,
            "age": age,
        })
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.put(self.base_url + f"api/pets/{pet_id}", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_new_pet_without_photo(self, auth_key, name, animal_type, age) -> json:
        """Метод отправляет на сервер запрос с данными питомца и возвращает статус
         и результат в формате JSON с данными созданного питомца. Данный метод создает питомца без фотографии."""
        data = MultipartEncoder(fields={
            "name": name,
            "animal_type": animal_type,
            "age": age,
        })
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url+"api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_pet_photo(self, auth_key, pet_id, pet_photo) -> json:
        """Метод отправляет на сервер запрос на добавление фотографии в карточку питомца по указанному ID
        и возвращает статус и результат в формате JSON с данными питомца."""
        data = MultipartEncoder(fields={"pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpeg")})
        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url + f"api/pets/set_photo/{pet_id}", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
