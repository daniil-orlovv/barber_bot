from sqlalchemy.orm import Session

from models.models import Client


def create_object_client(name: str, telegram_id: int, phone: str,
                         user_token: str) -> Client:
    """Функция получает данные для создания объекта модели Client и возвращает
    его."""

    return Client(
        name=name,
        telegram_id=telegram_id,
        phone=phone,
        user_token=user_token
    )


def check_exist_client_in_db(session: Session, telegram_id: int) -> bool:
    """Функция делает запрос в БД, проверяет наличие клиента в БД и отправляет
    True или False."""

    exist = session.query(Client.ycl_id).filter(
        Client.telegram_id == telegram_id).first()
    return True if exist else False


def get_phone_client_from_db(session: Session, telegram_id: int) -> str:
    """Получает телефон пользователя по id телеграма и возвращает его."""

    return session.query(Client.phone).filter(
        Client.telegram_id == telegram_id).scalar()


def add_client_in_db(session: Session, name: str, telegram_id: int, phone: str,
                     user_token: str) -> None:
    """Функция добавляет пользователя в БД, используя имя, номер, telegram-id
    и токен."""

    object_for_db = create_object_client(name, telegram_id, phone, user_token)
    session.add(object_for_db)
    session.commit()


def get_user_token_of_client(session: Session, telegram_id: int) -> str:
    """Функция получает user-token из БД по telegram-id пользователя и
    возвращает его"""

    user = session.query(Client).filter(
        Client.telegram_id == telegram_id).first()
    return user.user_token


def get_phone_by_telegram_id(session: Session, telegram_id: int) -> str:
    """Функция получает телефон пользователя по его telegram-id и возвращает
    его."""

    user = session.query(Client).filter(
        Client.telegram_id == telegram_id).first()
    return user.phone
