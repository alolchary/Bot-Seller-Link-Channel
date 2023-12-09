from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



def get_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🔒 Приобрести доступ", callback_data="buy_access")],
        [InlineKeyboardButton(text="ℹ️ Информация о товаре", callback_data="information")],
        [InlineKeyboardButton(text="❗️ Связь", url="t.me/yula_parff")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def keyboard_payment(url: str) -> InlineKeyboardMarkup:


    buttons = [
        [InlineKeyboardButton(text="🔗 Ссылка на оплату", url=url),],
        [InlineKeyboardButton(text="✅ Оплатил", callback_data=f"check_pay"), InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]

    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_keyboard() -> InlineKeyboardMarkup:

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="back")]

    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
