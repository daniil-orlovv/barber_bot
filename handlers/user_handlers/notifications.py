from aiogram import Bot


async def notify_day(bot: Bot, user_id: int) -> None:
    """Отправляет сообщение пользователю с уведомлением о записи."""

    await bot.send_message(
        user_id,
        text="У вас запись через день!"
    )


async def notify_hour(bot: Bot, user_id: int) -> None:
    """Отправляет сообщение пользователю с уведомлением о записи."""

    await bot.send_message(
        user_id,
        text="У вас запись через час!"
    )


async def notify_week(bot: Bot, user_id: int) -> None:
    """Отправляет сообщение пользователю с уведомлением о повторной записи."""

    await bot.send_message(
        user_id,
        text=('Прошло 4 недели: Вы не были у нас уже 4 недели!'
              'Запишитесь на стрижку.')
    )


async def notify_month(bot: Bot, user_id: int):
    """Отправляет сообщение пользователю с уведомлением о повторной записи."""

    await bot.send_message(
        user_id,
        text=('Прошло 4 месяца: Вы не были у нас уже 4 месяца!'
              'Запишитесь на стрижку.')
    )
