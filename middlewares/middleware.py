import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class DBMiddleware(BaseMiddleware):
    """Класс-мидлваррь, получающий соединение с БД до попадания в фильтры и
    передающий это соединение в хэндлеры."""
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        engine = data['engine']
        print(engine)
        connection = engine.connect()
        Session = sessionmaker(bind=engine)
        session = Session(bind=connection)
        data['session'] = session
        logger.debug('DBMiddleware has worked.')

        result = await handler(event, data)

        logger.debug('DBMiddleware has worked.')
        return result
