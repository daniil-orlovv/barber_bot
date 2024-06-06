from aiogram.types import CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext

from api.create_record import (get_free_staff, get_free_services,
                                          get_free_date, get_free_time)


class CheckFreeStaff(BaseFilter):

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in get_free_staff().values()


class CheckFreeService(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery,
            state: FSMContext
    ) -> bool:

        state_data = await state.get_data()
        return callback.data in get_free_services(
            state_data['staff_id']).values()


class CheckFreeDate(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery,
            state: FSMContext
    ) -> bool:

        state_data = await state.get_data()
        staff_id = state_data['staff_id']
        month, day = callback.data.split('-')
        free_days = get_free_date(staff_id)
        if month in free_days and day in free_days[month]:
            return True
        return False


class CheckFreeTime(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery,
            state: FSMContext
    ) -> bool:

        state_data = await state.get_data()
        date = state_data['date']
        staff_id = state_data['staff_id']
        return callback.data in get_free_time(staff_id, date)


class CheckCallbackAccept(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery
    ) -> bool:
        """Метод проверяющий соответствие callback == "accept"
        """

        return callback.data == 'accept'


class CheckCallbackCancel(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery
    ) -> bool:
        """Метод проверяющий соответствие callback == "accept"
        """

        return callback.data == 'cancel'


class CheckCallbackFeedback(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery
    ) -> bool:
        """Метод проверяющий соответствие callback == "feedback"
        """

        return callback.data == 'feedback'


class CheckCallbackRecreateRecord(BaseFilter):

    async def __call__(
            self,
            callback: CallbackQuery
    ) -> bool:
        """Метод проверяющий соответствие callback == "recreate"
        """

        return callback.data == 'recreate'
