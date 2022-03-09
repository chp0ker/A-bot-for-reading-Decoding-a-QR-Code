from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from pyzbar import pyzbar
import aiogram
import os
import cv2

TOKEN_TG = "УКАЖИТЕ ВАШ ТОКЕН"

storage = MemoryStorage()
bot = Bot(token=TOKEN_TG, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class photo(StatesGroup):
    getting = State()


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    await message.answer("Бот для считывания QR-кода")
    await message.answer("Отправьте фотографию для считывания данных с QR-кода")
    await photo.getting.set()


@dp.message_handler(content_types=["photo"], state=photo.getting)
async def qr_code_bot(message: types.Message):
    name = message.photo[-1].file_unique_id + ".png"
    await message.photo[-1].download(destination_file=name)

    qr_codes = pyzbar.decode(cv2.imread(name))
    for qr_code in qr_codes:
        qr_codeData = qr_code.data.decode("utf-8")
    try:
        await message.answer(qr_codeData)
    except:
        await message.answer("Не удалось расшифровать QR-код")
    finally:
        os.remove(name)
        await message.answer("Отправьте фотографию для считывания данных с QR-кода")


if __name__ == "__main__":
    executor.start_polling(dp)
