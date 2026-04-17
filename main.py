import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram import executor
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import BOT_TOKEN, CHANNEL_ID_1, CHANNEL_ID_2, MAIN_ADMIN_ID
from keyboards import status_kb, device_kb, lock_device_kb, admin_kb, cancel_kb
from states import ProfitForm, AdminForm
from admins import ADMIN_IDS, save_admins  # Импортируем сохранение
from filters import IsAdmin

class LockForm(StatesGroup):
    device = State()
    worker = State()
    locker = State()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.filters_factory.bind(IsAdmin)

# --- ГЛОБАЛЬНАЯ ОТМЕНА ---
@dp.message_handler(lambda m: m.text in ["❌ Отмена", "❌ Назад"], state="*", is_admin=True)
async def global_cancel(msg: types.Message, state: FSMContext):
    await state.finish()
    await start(msg)

@dp.callback_query_handler(lambda c: c.data == "cancel_action", state="*", is_admin=True)
async def cancel_callback(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await start(call.message)

# --- СТАРТ ---
@dp.message_handler(commands="start", is_admin=True)
async def start(msg: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Новый профит"), types.KeyboardButton("Новый лок"))
    kb.add(types.KeyboardButton("Админ"))
    await msg.answer("⚡️ Меню управления:", reply_markup=kb)

# --- НОВЫЙ ЛОК ---
@dp.message_handler(lambda m: m.text == "Новый лок", is_admin=True)
async def lock_1(msg: types.Message):
    await msg.answer("🔒 Выберите устройство для лока:", reply_markup=lock_device_kb())
    await LockForm.device.set()

@dp.callback_query_handler(lambda c: c.data.startswith("lock_dev:"), state=LockForm.device)
async def lock_2(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(device=call.data.split(":")[1])
    await call.message.answer("👤 Введите юзернейм воркера:", reply_markup=cancel_kb())
    await LockForm.worker.set()

@dp.message_handler(state=LockForm.worker, is_admin=True)
async def lock_3(msg: types.Message, state: FSMContext):
    await state.update_data(worker=msg.text)
    await msg.answer("Введите IMEI:", reply_markup=cancel_kb())
    await LockForm.locker.set()

@dp.message_handler(state=LockForm.locker, is_admin=True)
async def lock_finish(msg: types.Message, state: FSMContext):
    # 1. Сначала сохраняем текст сообщения (IMEI) в состояние
    await state.update_data(locker=msg.text)
    
    # 2. Теперь получаем обновленные данные
    data = await state.get_data()
    
    # 3. Формируем текст (теперь 'locker' точно есть в data)
    text = (
        f"🔐🔑УСПЕХ! 💥 Мамонт в клетке! 🦣Пароль установлен!\n\n"
        f"📱 Устройство: {data['device']}\n"
        f"👨‍💻 Воркер: {data['worker']}\n"
        f"⚙️ IMEI/Serial: {data['locker']}"
    )
    
    await bot.send_message(CHANNEL_ID_1, text)
    await bot.send_message(CHANNEL_ID_2, text)
    await state.finish()
    await msg.answer("✅ Лок опубликован!")
    await start(msg)

# --- НОВЫЙ ПРОФИТ ---
@dp.message_handler(lambda m: m.text == "Новый профит", is_admin=True)
async def prof_1(msg: types.Message):
    await msg.answer("👤 Введите воркера:", reply_markup=cancel_kb())
    await ProfitForm.user.set()

@dp.message_handler(state=ProfitForm.user, is_admin=True)
async def prof_2(msg: types.Message, state: FSMContext):
    await state.update_data(worker=msg.text)
    await msg.answer("💰 Сумма:", reply_markup=cancel_kb())
    await ProfitForm.amount.set()

@dp.message_handler(state=ProfitForm.amount, is_admin=True)
async def prof_3(msg: types.Message, state: FSMContext):
    await state.update_data(amount=msg.text)
    await msg.answer("📱 Устройство:", reply_markup=device_kb())
    await ProfitForm.device.set()

@dp.callback_query_handler(lambda c: c.data.startswith("dev:"), state=ProfitForm.device)
async def prof_4(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(device=call.data.split(":")[1])
    await call.message.edit_text("📌 Статус:", reply_markup=status_kb())
    await ProfitForm.status.set()

@dp.callback_query_handler(lambda c: c.data.startswith("status:"), state=ProfitForm.status)
async def prof_finish(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    from generate_image import generate_profit_image
    status = "Service" if "done" in call.data else "Card"
    path = generate_profit_image(data["worker"], data["amount"], data["device"], status)
    with open(path, "rb") as f:
        await bot.send_photo(CHANNEL_ID_1, f)
    with open(path, "rb") as f:
        await bot.send_photo(CHANNEL_ID_2, f)
    await state.finish()
    await call.message.answer("✅ Профит улетел")
    await start(call.message)

# --- АДМИНКА ---
@dp.message_handler(lambda m: m.text == "Админ", is_admin=True)
async def adm_menu(msg: types.Message):
    await msg.answer("⚙ Админка:", reply_markup=admin_kb())

@dp.message_handler(lambda m: m.text == "Добавить админа", is_admin=True)
async def adm_add(msg: types.Message):
    await msg.answer("Введите ID нового админа:", reply_markup=cancel_kb())
    await AdminForm.add_id.set()

@dp.message_handler(state=AdminForm.add_id, is_admin=True)
async def adm_add_id(msg: types.Message, state: FSMContext):
    await state.update_data(new_id=int(msg.text))
    await msg.answer("Введите имя:", reply_markup=cancel_kb())
    await AdminForm.add_name.set()

@dp.message_handler(state=AdminForm.add_name, is_admin=True)
async def adm_add_name(msg: types.Message, state: FSMContext):
    d = await state.get_data()
    ADMIN_IDS[d['new_id']] = msg.text
    save_admins(ADMIN_IDS)  # СОХРАНЕНИЕ
    await state.finish()
    await msg.answer(f"✅ Админ {msg.text} добавлен")
    await start(msg)

@dp.message_handler(lambda m: m.text == "Удалить админа", is_admin=True)
async def adm_del(msg: types.Message):
    await msg.answer("Введите ID для удаления:", reply_markup=cancel_kb())
    await AdminForm.del_id.set()

@dp.message_handler(state=AdminForm.del_id, is_admin=True)
async def adm_del_id(msg: types.Message, state: FSMContext):
    target_id = int(msg.text)
    if target_id == 8581982067:
        await msg.answer("❌ Нельзя удалить владельца!")
    else:
        ADMIN_IDS.pop(target_id, None)
        save_admins(ADMIN_IDS)  # СОХРАНЕНИЕ
        await msg.answer("🗑 Удалено")
    await state.finish()
    await start(msg)

@dp.message_handler(lambda m: m.text == "Список админов", is_admin=True)
async def adm_list(msg: types.Message):
    t = "\n".join(f"{k}: {v}" for k, v in ADMIN_IDS.items())
    await msg.answer(t or "Список пуст")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
