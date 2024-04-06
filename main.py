import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from errors.errors import check_tokens
from handlers import user_handlers

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    check_tokens()
    try:
        logger.info('Starting bot')
        config: Config = load_config()
        bot = Bot(token=config.tg_bot.token,
                parse_mode='HTML')
        dp = Dispatcher()
        dp.include_router(user_handlers.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as error:
        logger.error(f'Ошибка в работе программы: {error}')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Программа остановлена пользователем вручную')
