from PIL import Image, ImageDraw, ImageFont

def generate_profit_image(user, amount, device, status):
    img = Image.open("assets/template.png").convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Загружаем шрифты
    font_main = ImageFont.truetype("assets/font.ttf", 30)
    font_small = ImageFont.truetype("assets/font.ttf", 30)

    # 1. Отрисовка Воркера
    draw.text((400, 460), user.upper(), font=font_main, fill="white")

    # 2. Отрисовка Суммы + Статуса (CARD/SERVICE)
    # Теперь статус пишется перед суммой в том же поле
    full_amount_text = f"{status.upper()} {amount} $"
    draw.text((950, 460), full_amount_text, font=font_main, fill="white")

    # 3. Отрисовка Устройства (теперь без статуса)
    draw.text((690, 570), device.upper(), font=font_small, fill="white")

    output_path = "assets/result.png"
    img.save(output_path)

    return output_path