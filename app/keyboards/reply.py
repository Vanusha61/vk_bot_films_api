from fastvk.keyboard import Button, Keyboard
from fastvk.enums import Color

def keyboard_menu():
    keyboard = Keyboard(one_time=False)

    keyboard.row(
        Button.text("Список жанров", color=Color.SECONDARY),
        Button.text("Поиск по названию", color=Color.SECONDARY)
    )
    keyboard.row(
        Button.text("По рейтингу", color=Color.SECONDARY),
        Button.text("Низкий бюджет", color=Color.SECONDARY),
        Button.text("Высокий бюджет", color=Color.SECONDARY)
    )
    keyboard.row(Button.text("История", color=Color.SECONDARY))
    return keyboard


def keyboard_pages_film_name():
    keyboard = Keyboard(inline=False).row(
        Button.text("➡️ Вперед", color=Color.PRIMARY),
        Button.text("⬅️ Назад", color=Color.PRIMARY),
        Button.text("❌ Выход", color=Color.NEGATIVE),
    )
    return keyboard

def keyboard_rating_film():
    keyboard = Keyboard(one_time=False)
    keyboard.row(
        Button.text("🔙", color=Color.SECONDARY),
        Button.text("🚪 Выход", color=Color.NEGATIVE),
        Button.text("🔜", color=Color.PRIMARY)
    )
    return keyboard

def keyboard_budget_min_film():
    keyboard = Keyboard(one_time=False)
    keyboard.row(
        Button.text("Назад", color=Color.SECONDARY),
        Button.text("Вперед", color=Color.NEGATIVE),
    )
    keyboard.row(
        Button.text("Выход", color=Color.PRIMARY)
    )
    return keyboard

def keyboard_budget_max_film():
    keyboard = Keyboard(one_time=False)
    keyboard.row(
        Button.text("🌙 Назад", color=Color.PRIMARY),
        Button.text("☀️ Вперед", color=Color.POSITIVE),
        Button.text("⛔ Выход", color=Color.NEGATIVE),
    )
    return keyboard
