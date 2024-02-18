import logging

from aiogram import Bot, Dispatcher, executor, types
from keyboard import *
from database import *

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "6733527659:AAEaRUH7waFYNP228DOqtlTF9SHu5YcfipE"

bot = Bot(token=BOT_TOKEN, parse_mode='Markdown')
dp = Dispatcher(bot)

currencies = {
    'usd': ['🇺🇸 Доллар, США', 1],
    'rub': ['🇷🇺 Рубль', 92.5],
    'uzs': ['🇺🇿 Сум, Узбекистан', 12505],
    'eur': ['🇪🇺 Евро', 0.93],
    'gbp': ['🇬🇧 Фунт стерлинг', 0.79],
    'jpy': ['🇯🇵 Иена', 150.22],
    'cny': ['🇨🇳 Юань', 7.12],
    'try': ['🇹🇷 Турецкая лира', 30.84],
    'kzt': ['🇰🇿 Тенге', 450.04],
}


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await create_user(message.from_user.id)
    user = await get_user(message.from_user.id)
    btn = await start_reply(currencies[user[0]][0], currencies[user[1]][0])
    await message.answer('Здравствуйте\nТут можно быстро посчитать конвертацию в популярных валютах.\n*Напишите боту сумму которую хотите конвертировать.*', reply_markup=btn)


@dp.message_handler(text="🔄")
async def replace_handler(message: types.Message):
    user = await get_user(message.from_user.id)
    await update_user(user[2], user[1], user[0])
    btn = await start_reply(currencies[user[1]][0], currencies[user[0]][0])
    await message.answer(f'Теперь вы конвертируете с *{currencies[user[1]][0]}* на *{currencies[user[0]][0]}*', reply_markup=btn)


@dp.callback_query_handler(text_contains='from_cur:')
async def fromCur_query(call: types.CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    currency = call.data.split(':')[1]
    if currency != user[1]:
        await update_user(call.from_user.id, currency, user[1])
        btn = await start_reply(currencies[currency][0], currencies[user[1]][0])
        await call.message.answer(f'Теперь вы конвертируете с *{currencies[currency][0]}* на *{currencies[user[1]][0]}*', reply_markup=btn)
    else:
        await call.message.answer('*Нельзя конвертировать на одинаковые валюты!*')


@dp.callback_query_handler(text_contains='to_cur:')
async def toCur_query(call: types.CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    currency = call.data.split(':')[1]
    if currency != user[0]:
        await update_user(call.from_user.id, user[0], currency)
        btn = await start_reply(currencies[user[0]][0], currencies[currency][0])
        await call.message.answer(f'Теперь вы конвертируете с *{currencies[user[0]][0]}* на *{currencies[currency][0]}*', reply_markup=btn)
    else:
        await call.message.answer('*Нельзя конвертировать на одинаковые валюты!*')


@dp.message_handler()
async def text_handler(message: types.Message):
    user = await get_user(message.from_user.id)

    text_finded = False
    for value in currencies.values():
        if message.text in value:
            text_finded = value
            break
    else:
        text_finded = False

    if text_finded:
        currency = [key for key, value in currencies.items() if text_finded[0] in value][0]

        if user[0] == currency:
            btn = await currencies_inline(currencies, 'from_cur')
            await message.answer('Выберите валюту с которой конвертировать:', reply_markup=btn)
        elif user[1] == currency:
            btn = await currencies_inline(currencies, 'to_cur')
            await message.answer('Выберите валюту на которую конвертировать:', reply_markup=btn)
    else:
        try:
            cur_sum = float(message.text)
            cur_in_usd = currencies[user[0]][1]
            to_cur_in_usd = currencies[user[1]][1]
            sum = round(cur_sum / cur_in_usd * to_cur_in_usd, 2)
            await message.answer(f'*{cur_sum}* _{user[0].upper()}_ = *{sum}* _{user[1].upper()}_')
        except ValueError:
            await message.answer('*Введите только числа!*')


if __name__ == "__main__":
    create_tables()
    executor.start_polling(dp, skip_updates=True)