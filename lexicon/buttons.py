from config_data.config import (ADRESS_URL_GOOGLE, ADRESS_URL_YANDEX,
                                ADRESS_URL_2GIS)

start_buttons = {
    'buttons': ['Авторизоваться 🔑', 'Мои записи 📖', 'Записаться ✏️',
                'Все услуги ✂️', 'Контакты 📍', 'Оставить отзыв мастеру 💇',
                'Оставить отзыв барбершопу ✂️', 'Отмена ❌'],
    'adjust': (1, 2, 2, 2, 1)
}

contacts_buttons = {
    'buttons': {'Найти в Google картах 🗺': ADRESS_URL_GOOGLE,
                'Найти в Яндекс картах 🗺': ADRESS_URL_YANDEX,
                'Найти в 2ГИС 🗺': ADRESS_URL_2GIS},
    'adjust': (1, 1, 1)
}

accept_cancel = {
    'Подтвердить ✅': 'accept',
    'Отменить ❌': 'cancel'
}

edit_cancel = {
    'Перенести ➡️': 'edit',
    'Отменить ❌': 'cancel'
}

recreate_record = {
    'Изменить запись 🔄': 'recreate',
    'Отменить ❌': 'cancel'
}

button_auth = {
    'Авторизоваться 🔑': 'auth'
}
