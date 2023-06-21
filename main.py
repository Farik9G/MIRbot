from aiogram import Bot, Dispatcher, executor, types
from emoji import emojize
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! {emojize(':waving_hand_light_skin_tone:')}"
                         f"\nДля начала работы пришлите фотографию рентгена лёгких {emojize(':lungs:')}")

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply(f"Сообщение не распознано {emojize(':pleading_face:')}\nПожалуйста, пришлите фотографию!")
if __name__ == '__main__':
    executor.start_polling(dp)