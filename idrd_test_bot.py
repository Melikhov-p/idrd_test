import subprocess
import os
from pathlib import Path
import json
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType, File
from aiogram.utils import executor
from DetectFace import detect_face

with open('idrd_config.json', 'r', encoding='utf8') as config_file:
    config = json.load(config_file)

def ogg2wav(file):
    src_filename = file
    dest_filename = f'{file}.wav'
    process = subprocess.run(['ffmpeg', '-i', src_filename, '-ac', '1', '-f', 'wav', dest_filename], shell=True)
    if process.returncode != 0:
        raise Exception("Something went wrong")
    else:
        return 1


bot = Bot(token=config['TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Отправьте голосовое сообщение или фото.')


async def handle_convert_audio(file: File, file_name: str, path: str):
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"voices/{file_name}")
    convert = ogg2wav(f'voices/{file_name}')  # конвертация в wav
    if convert:
        os.remove(f'voices/{file_name}')  # удаления файла ogg
        return 1
    else:
        return 0


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: types.Message):
    voice = await message.voice.get_file()
    path = "/voices"
    save_file = await handle_convert_audio(file=voice, file_name=f"{message.from_user.id}_{voice.file_id}.ogg", path=path)
    if save_file:
        await bot.send_message(message.from_user.id, 'WAV сообщения сохранен.')
    else:
        await bot.send_message(message.from_user.id, 'Произошла ошибка.')


@dp.message_handler(content_types=[ContentType.PHOTO])
async def photo_message_handler(message: types.Message):
    photo = await message.photo[-1].get_file()
    photo_path = f'photos/{message.from_user.id}_{photo.file_id}.jpg'
    await bot.download_file(file_path=photo.file_path, destination=photo_path)
    faces_amount = detect_face(photo_path)
    if faces_amount > 0:
        await bot.send_message(message.from_user.id, f'Лицо найдено. Фото сохранено')
    else:
        os.remove(photo_path)
        await bot.send_message(message.from_user.id, 'Лицо не найдено.')

if __name__ == '__main__':
    executor.start_polling(dp)
