from aiogram.types import *


async def start_reply(from_cur, to_cur):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn.add(
        KeyboardButton(f'{from_cur}'),
        KeyboardButton(f'🔄'),
        KeyboardButton(f'{to_cur}'),
    )
    return btn


async def currencies_inline(currencies, target):
    btn = InlineKeyboardMarkup()

    count = 0
    row = []
    for currency in currencies:
        row.append(InlineKeyboardButton(text=currencies[currency][0], callback_data=f"{target}:{currency}"))
        count += 1
        if count == 3:
            btn.row(*row)
            count = 0
            row = []
    btn.row(*row)

    return btn