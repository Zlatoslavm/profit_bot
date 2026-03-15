from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from admins import ADMIN_IDS


class IsAdmin(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        is_admin = message.from_user.id in ADMIN_IDS
        return is_admin == self.is_admin