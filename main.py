import json
import os
import time
from typing import Type

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import asyncio
from profile_parser import profile_parse
from steam_parser import steam_parse

from tm_link_parser import parse_tmlinks

users = [1178604862, 415604189, 536462052, 722676643]

bot = Bot(token="5159794184:AAGWi-_kw-lO7wTzW6tEbnP-OgyKjVa3Y0s",
          parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if message.from_user.id in users:
        await message.answer(f"Access received {message.from_user.id}")
    else:
        await message.answer(f"Access denied {message.from_user.id}")


@dp.message_handler()
async def get_data(message: types.Message):
    if message.from_user.id in users:
        try:
            data = parse_tmlinks(message.text)
            new_data = steam_parse(data)
            full_data = profile_parse(new_data)
            filtered_data = list(filter(lambda i: i["trade_link"], full_data))
            if len(filtered_data) == 0:
                await message.answer("Не найдены профиля с возможной трейд ссылкой!")
            for index, item in enumerate(filtered_data):
                if index != 0 and index % 5 == 0:
                    time.sleep(5)
                name = item["name"]
                link = item["link"]
                csgo_float = item["Link_to_csgofloat_db"]
                price = item["price"]
                float = item["item_float"]
                steam_link = item["steam_link"]
                card = f'Name: {name}\n{hlink("CsgoTm", link)}\n{hlink("Csgo Float Db", csgo_float)}\nPrice: {price}$\nFloat: {float}\n{hlink("Steam Profile",steam_link)}'
                await message.answer(card)
        except Exception:
            await message.answer("Bad link")
            print(Exception)
        data = []
    else:
        await message.answer(f"Access denied {message.from_user.id}")


def main():
    print(os.getenv("TOKEN"))
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
