from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from admins import ADMIN_IDS

class AccessMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.from_user.id not in ADMIN_IDS:
            if message.text and message.text.startswith("/start"):
                await message.answer("❌ У вас нет доступа.")
            raise CancelHandler()

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict):
        if call.from_user.id not in ADMIN_IDS:
            await call.answer("❌ Доступ запрещен.", show_alert=True)
            raise CancelHandler()