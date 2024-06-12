

async def notify_day(bot, user_id):
    await bot.send_message(user_id,
                           text="У вас запись через день!")


async def notify_hour(bot, user_id):
    await bot.send_message(user_id,
                           text="У вас запись через час!")


async def notify_week(bot, user_id):
    await bot.send_message(user_id,
                           text="Прошло 4 недели: Вы не были у нас уже 4 недели! Запишитесь на стрижку.")


async def notify_month(bot, user_id):
    await bot.send_message(user_id,
                           text="Прошло 4 месяца: Вы не были у нас уже 4 месяца! Запишитесь на стрижку.")
