from config_data.config import (ADRESS_URL_GOOGLE, ADRESS_URL_YANDEX,
                                ADRESS_URL_2GIS)

start_buttons = {
    'buttons': ['Мои записи', 'Записаться', 'Контакты',
                'Отмена'],
    'adjust': (2, 1)
}

contacts_buttons = {
    'buttons': {'Найти в Google картах': ADRESS_URL_GOOGLE,
                'Найти в Яндекс картах': ADRESS_URL_YANDEX,
                'Найти в 2ГИС': ADRESS_URL_2GIS},
    'adjust': (1, 1, 1)
}

accept_cancel = {
        'Подтвердить': 'accept',
        'Отменить': 'cancel'
    }

edit_cancel = {
        'Перенести': 'edit',
        'Отменить': 'cancel'
    }
