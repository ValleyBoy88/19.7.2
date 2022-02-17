from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


# Тест №1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


# Тест №2
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# Тест №3
def test_add_new_pet_with_valid_data(name='Шотландец', animal_type='Котокельт',
                                     age='3', pet_photo='images/4151.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Тест №4
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


# Тест №5
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# Тест №6
def test_add_new_pet_valid_data_but_without_photo(name='Ирландец', animal_type='Собакен', age='5'):
        """Проверяем, что можно добавить питомца с валидными данными, но без фото"""

        # Запрашиваем ключ api и сохраняем в переменую auth_key
        _, auth_key = pf.get_api_key(valid_email, valid_password)

        # Добавляем питомца
        status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        try:
            assert result['pet_photo'] == pet_photo
        except NameError as Exception:
            print('Фото отсутствует')


# Тест №7
def test_add_photo_of_a_pet(pet_photo='images/4152.jpg'):
    """Проверяем возможность добавления фото к питомцу, созданному без фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если последний добавленный мною питомец без фото
    if pet_photo in my_pets['pets'][0]['id']:
        # Добавляем нового питомца без фото
        _, my_pets = pf.add_new_pet_without_photo(auth_key, 'Ирландец2', 'Собакен2', '6')

    # Берем последнего добавленного питомца и меняем его фото
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    # Проверяем что статус ответа = 200 и есть фото питомца
    assert status == 200
    assert result['pet_photo'] != ''


# Тест №8
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """ Проверяем, что запрос api ключа не возвращает статус 200"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200


# Тест №9
def test_get_api_key_for_invalid_user(email=valid_password, password=invalid_password):
    """ Проверяем, что запрос api ключа не возвращает статус 200"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status != 200


# Тест №10
def test_add_new_pet_with_invalid_data(name='ееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееее еееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееееее',
                                       animal_type='Котокельт', age='3', pet_photo='images/4151.jpg'):
    """Проверяем, что нельзя ввести длинное имя"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем имя на заполненность
    if len(name) > 0 and len(name) < 50:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Имя питомца не может быть более 50 символов")


# Тест №11
def test_add_new_pet_with_invalid_age(name='Ирландец', animal_type='Собакен',
                                      age='йцуке', pet_photo='images/4152.jpg'):
    """Проверяем, что возраст питомца нельзя обозначить буквами"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result[age] is int


# Тест №12
def test_impossible_to_add_new_pet_with_negative_age_number(name='Ирландец', animal_type='Собакен',
                                     age='-5', pet_photo='images/4152.jpg'):
    """Проверяем, что нельзя добавить питомца с отрицательным значением в возрасте"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    if int(age) > 0:
        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Возраст выражен отрицательным числом")


# Тест №13
def test_add_new_pet_with_missing_name (name='', animal_type='Котокельт',
                                     age='30', pet_photo='images/4151.jpg'):
    """Проверяем поведение системы при введении пустого значения имени питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    if len(name) != 0:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Введите имя питомца")


# Тест №14
def test_add_new_pet_with_valid_data(name='Дружок', animal_type='Лабрадор',
                                     age='2', pet_photo='images/4153.png'):
    """Проверка загрузки валидных данных питомца с картинкой в формате png"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Тест #15
def test_unsuccessful_delete_pet_with_invalid_id():
    """Проверяем возможность удаления питомца с неверным ID"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id заведомо несуществующего индекса питомца и отправляем запрос на удаление
    pet_id = "9C4AEC87-37A4-4EE0-8F1B-3170C816536C00"
    if pet_id in my_pets.values():
        status, _ = pf.delete_pet(auth_key, pet_id)
        # Ещё раз запрашиваем список своих питомцев
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
        assert status == 200
        assert pet_id in my_pets.values()
    else:
        raise Exception('ID не существует')



