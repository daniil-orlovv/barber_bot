from models.models import Client
from sqlalchemy.orm import Session


def create_object_client(kwargs):
    return Client(
        name=kwargs['name'],
        ycl_id=kwargs['ycl_id'],
        telegram_id=kwargs['telegram_id'],
        phone=kwargs['phone']
    )


def add_client_in_db(session: Session, state_data: dict):
    object_for_db = create_object_client(state_data)
    session.add(object_for_db)
    session.commit()


def get_ycl_id_of_user(session, telegram_id):
    ycl_id = session.query(Client.ycl_id).filter(
        Client.telegram_id == telegram_id).first()
    return ycl_id
