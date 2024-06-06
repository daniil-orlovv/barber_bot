from models.models import Client
from sqlalchemy.orm import Session


def create_object_client(name, telegram_id, phone, user_token):
    return Client(
        name=name,
        telegram_id=telegram_id,
        phone=phone,
        user_token=user_token
    )


def check_exist_client_in_db(session: Session, state_data):
    ycl_id = state_data['client_ycl_id']
    exist = session.query(Client.ycl_id).filter(
        Client.ycl_id == ycl_id).first()
    return True if exist else False


def get_phone_client_from_db(session: Session, telegram_id):
    phone = session.query(Client.phone).filter(
        Client.telegram_id == telegram_id).scalar()
    return phone


def add_client_in_db(session: Session, name, telegram_id, phone, user_token):
    object_for_db = create_object_client(name, telegram_id, phone, user_token)
    session.add(object_for_db)
    session.commit()


def get_user_token_of_client(session, telegram_id):
    user = session.query(Client).filter(
        Client.telegram_id == telegram_id).first()
    user_token = user.user_token
    return user_token


def get_phone_by_telegram_id(session, telegram_id):
    user = session.query(Client).filter(
        Client.telegram_id == telegram_id).first()
    phone = user.phone
    return phone
