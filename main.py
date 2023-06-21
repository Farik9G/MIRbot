from aiogram import Bot, Dispatcher, executor, types
from emoji import emojize
from dotenv import load_dotenv
import os, math
import tensorflow as tf
import numpy as np


def round_to_nonzero(number):
    if number == 0:
        return 0

    sign = math.copysign(1, number)
    abs_number = abs(number)
    exponent = math.floor(math.log10(abs_number))
    factor = 10 ** (exponent + 1)
    rounded_number = math.ceil(abs_number / factor) * factor * sign

    return rounded_number

load_dotenv()
model = tf.keras.models.load_model('xray_model.h5')
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMTZJNkGIamnpxjz05Cwn-1oJu1e3QAAgkPAAKUZFBJX3_8eLbYP38vBA')
    await message.answer(f"Здравствуйте, <b>{message.from_user.first_name}</b>! {emojize(':waving_hand_light_skin_tone:')}"
                         f"\nДля начала работы пришлите фотографию рентгена лёгких {emojize(':lungs:')}", parse_mode="HTML")

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply(f"Сообщение не распознано {emojize(':pleading_face:')}\nПожалуйста, пришлите фотографию!")

@dp.message_handler(content_types=['photo'])
async def check_photo(message: types.Message):
    # Сохранение фотографии
    photo = message.photo[-1]
    photo_path = 'photo.jpg'
    await photo.download(photo_path)

    # Загрузка и обработка изображения
    image = tf.io.read_file(photo_path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, [180, 180])
    image = np.expand_dims(image, axis=0)
    result = round_to_nonzero(model.predict(image)[0][0])

    await message.reply(f"<b>Вероятность пневмонии на данном фото == {result}%</b> {emojize(':check_mark_button:')}", parse_mode="HTML")

if __name__ == '__main__':
    executor.start_polling(dp)