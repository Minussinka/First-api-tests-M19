from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()


def test_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка получения ключа для зарегистрированного пользователя."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    """Проверка получения списка всех питомцев для зарегистрированного пользователя."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name="Хвостик", animal_type="двортерьер",
                                     age="2", pet_photo="images/hvostik.jpg"):
    """Проверка добавления питомца с верными данными."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name


def test_successful_delete_my_pet():
    """Проверка удаления собственного питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Шипучка", "кошка", 2, "tests/images/GEDC3654.JPG")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_my_pet_info(name="Дези", animal_type="кошка", age="3"):
    """Проверка изменения информации о собственном питомце."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("У вас нет питомцев.")


def test_api_key_for_invalid_user(email="fghytr@mail.ru", password="2154ghft"):
    """Проверка получения ключа для незарегистрированного пользователя."""
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_api_key_with_blank_credentials(email="", password=""):
    """Проверка получения ключа без ввода логина и пароля."""
    status, result = pf.get_api_key(email, password)
    assert status != 200
    assert "key" not in result


def test_add_new_pet_with_too_long_name(name="Хвостик"*35, animal_type="двортерьер", age="2"):
    """Проверка создания питомца со слишком длинным именем."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    # Баг: код состояния должен быть 400, питомец не должен создаваться.


def test_add_new_pet_with_blank_data(name="", animal_type="", age=""):

    """Проверка добавления питомца без заполнения полей."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    if status != 200:
        raise Exception("Незаполнены обязательные поля.")
    else:
        assert result["name"] == name


def test_add_pet_photo_successful(pet_photo="images/hvostik.jpg"):
    """Проверка добавления фото в карточку своего питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ""
    else:
        raise Exception("У вас нет питомцев.")


def test_add_pet_photo_wrong_file_format(pet_photo="images/hvostik1.tiff"):
    """Проверка добавления фото неподдерживаемого формата в карточку своего питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ""
    else:
        raise Exception("У вас нет питомцев.")
    # Баг: код состояния должен быть 400, фото не должно добавляться.


def test_get_my_pets_with_valid_key(filter="my_pets"):
    """Проверка получения списка своих питомцев."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) >= 0


def test_add_new_pet_with_negative_age(name="Хвостик", animal_type="двортерьер", age="-2"):
    """Проверка добавления питомца с отрицательным значением возраста."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result["name"] == name
    # Баг: код состояния должен быть 400, питомец не должен добавляться.


def test_delete_any_pet_successful():
    """Проверка удаления любого питомца."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    pet_id = pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, pets = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert pet_id not in pets.values()
    # Баг: код ошибки должен быть 403, питомец не должен быть удален.


def test_update_any_pet_info(name="Дези", animal_type="кошка", age="3"):
    """Проверка изменения информации о любом питомце."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    status, result = pf.update_pet_info(auth_key, pets["pets"][0]["id"], name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    # Баг: код ошибки должен быть 403, информация не должна быть обновлена.
