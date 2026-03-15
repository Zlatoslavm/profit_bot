from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ====== СПИСОК ДЛЯ ПРОФИТОВ (Краткий) ======
MODELS = [
    "iPhone 12", "iPhone 12 +","iPhone 12 P", "iPhone 12 PM",
    "iPhone 13", "iPhone 13 +", "iPhone 13 P", "iPhone 13 PM",
    "iPhone 14", "iPhone 14 +", "iPhone 14 P", "iPhone 14 PM",
    "iPhone 15", "iPhone 15 +", "iPhone 15 P", "iPhone 15 PM",
    "iPhone 16", "iPhone 16 e", "iPhone 16 +", "iPhone 16 P", "iPhone 16 PM",
    "iPhone 17", "iPhone 17 e", "iPhone 17 Air", "iPhone 17 P", "iPhone 17 PM",
]

# ====== СПИСОК ДЛЯ ЛОКОВ (Полный) ======
MODELS2 = [
    "iPhone 12", "iPhone 12 Mini","iPhone 12 Pro", "iPhone 12 Pro Max",
    "iPhone 13", "iPhone 13 Mini", "iPhone 13 Pro", "iPhone 13 Pro Max",
    "iPhone 14", "iPhone 14 +", "iPhone 14 Pro", "iPhone 14 Pro Max",
    "iPhone 15", "iPhone 15 +", "iPhone 15 Pro", "iPhone 15 Pro Max",
    "iPhone 16", "iPhone 16 e", "iPhone 16 +", "iPhone 16 Pro", "iPhone 16 Pro Max",
    "iPhone 17", "iPhone 17 e", "iPhone 17 Air", "iPhone 17 Pro", "iPhone 17 Pro Max",
]

# Универсальная кнопка отмены (текстовая)
def cancel_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("❌ Отмена"))

# Клавиатура устройств для ПРОФИТОВ
def device_kb(prefix="dev"):
    kb = InlineKeyboardMarkup(row_width=2)
    for m in MODELS:
        kb.insert(InlineKeyboardButton(m, callback_data=f"{prefix}:{m}"))
    kb.add(InlineKeyboardButton("❌ Отмена", callback_data="cancel_action"))
    return kb

# Клавиатура устройств для ЛОКОВ
def lock_device_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    for m in MODELS2:
        kb.insert(InlineKeyboardButton(m, callback_data=f"lock_dev:{m}"))
    kb.add(InlineKeyboardButton("❌ Отмена", callback_data="cancel_action"))
    return kb

# Кнопка НАЗАД + ОТМЕНА (инлайн)
def back_kb(callback_data):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("⬅️ Назад", callback_data=callback_data),
        InlineKeyboardButton("❌ Отмена", callback_data="cancel_action")
    )

# Статусы для профитов
def status_kb():
    kb = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Service", callback_data="status:done"),
        InlineKeyboardButton("Card", callback_data="status:skip"),
    )
    kb.add(InlineKeyboardButton("❌ Отмена", callback_data="cancel_action"))
    return kb

# Кнопка для повтора лока в конце сообщения
def new_lock_kb():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("🔒 Новый лок", callback_data="new_lock")
    )

# Админ-панель
def admin_kb():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Добавить админа", callback_data="admin:add"),
        InlineKeyboardButton("Удалить админа", callback_data="admin:del"),
        InlineKeyboardButton("Список админов", callback_data="admin:list"),
    )
    return keyboard