import json
import os

# Путь к файлу базы данных
ADMINS_FILE = os.path.join(os.path.dirname(__file__), 'admins_data.json')


def load_admins():
    # Эти админы будут в боте всегда по умолчанию
    default_admins = {
        8419332734: "Владелец",
        8364976888: "Админ2"
    }

    if not os.path.exists(ADMINS_FILE):
        return default_admins

    try:
        with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # JSON хранит ключи как строки, превращаем их обратно в числа
            return {int(k): v for k, v in data.items()}
    except:
        return default_admins


def save_admins(admins_dict):
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(admins_dict, f, ensure_ascii=False, indent=4)


# Загружаем список при старте бота
ADMIN_IDS = load_admins()