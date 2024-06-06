import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.mongodb import MongoDBJobStore
from config_data.config import Config, load_config
from errors.errors import check_tokens
from handlers.user_handlers import (create_record, edit_record, contacts,
                                    services, feedbacks, get_records, cancel_record)
from models.models import Base
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from middlewares.middleware import DBMiddleware

logger = logging.getLogger(__name__)


jobstores = {
    'default': MemoryJobStore()
}


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    check_tokens()
    try:
        logger.info('Starting bot')
        config: Config = load_config()
        bot = Bot(token=config.tg_bot.token,
                  parse_mode='HTML')
        scheduler = AsyncIOScheduler(jobstores=jobstores)
        engine = create_engine(
            'sqlite:///sqlite3.db',
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10
        )
        Base.metadata.create_all(engine)
        dp = Dispatcher()
        dp.include_router(create_record.router)
        dp.include_router(edit_record.router)
        dp.include_router(contacts.router)
        dp.include_router(services.router)
        dp.include_router(feedbacks.router)
        dp.include_router(get_records.router)
        dp.include_router(cancel_record.router)
        dp.update.outer_middleware(DBMiddleware())
        dp.workflow_data.update({
            'engine': engine, 'bot': bot, 'config': config,
            'scheduler': scheduler})

        await bot.delete_webhook(drop_pending_updates=True)
        scheduler.start()
        await dp.start_polling(bot)
    except Exception as error:
        logger.error(f'Ошибка в работе программы: {error}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Программа остановлена пользователем вручную')
