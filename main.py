import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import user_handlers
# from keyboards.main_menu import set_main_menu

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token,
              parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
