import sys
import logging

from config_data.config import (PARTNER_TOKEN, USER_TOKEN, COMPANY_ID,
                                load_config, Config)

config: Config = load_config()
logger = logging.getLogger(__name__)


def check_tokens():
    if not all([PARTNER_TOKEN, USER_TOKEN, COMPANY_ID, config.tg_bot.token]):
        logger.critical('Отсутствуют обязательные переменные.')
        sys.exit(1)
