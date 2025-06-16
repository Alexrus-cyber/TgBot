from asyncio.log import logger
from aiogram import Bot, Dispatcher, types, F
import easyocr
import asyncio
import random
import logging

from aiogram.filters import Command
from aiogram.types import Message,KeyboardButton,ReplyKeyboardMarkup



API_TOKEN = '5354076694:AAEFd2qD8VCVpb-Sg9watarCsAeEVuTbbhA'  # Замените на токен вашего бота

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Создаем диспетчер
TurnOn = False;

src = 'C:/Users/tappy/Desktop/xxx/photos/'  # Путь для сохранения фотографий


@dp.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [KeyboardButton(text="Посмотреть текст с картинки")],
        [KeyboardButton(text="Включить уведомления ✔️")],
        [KeyboardButton(text="Перейти в чат")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("Привет я бот мотивайдер, спасибо что выбрали меня", reply_markup=keyboard)



@dp.message(F.text == "Посмотреть текст с картинки")
async def with_picture(message: types.Message):
    await message.reply("Жду картинку!")


@dp.message(F.text == "Включить уведомления ✔️")
async def with_pushes(message: types.Message):
    kb = [
        [KeyboardButton(text="Посмотреть текст с картинки")],
        [KeyboardButton(text="Выключить уведомления ❌")],
        [KeyboardButton(text="Перейти в чат")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("Вы выбрали опцию Включить уведомления ✔️", reply_markup=keyboard)
    asyncio.create_task(send_reminders(message.chat.id, True)) 

@dp.message(F.text == "Выключить уведомления ❌")
async def without_pushes(message: types.Message):
    kb = [
        [KeyboardButton(text="Посмотреть текст с картинки")],
        [KeyboardButton(text="Включить уведомления ✔️")],
        [KeyboardButton(text="Перейти в чат")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("Вы выбрали опцию Выключить уведомления ❌", reply_markup=keyboard)
    asyncio.create_task(send_reminders(message.chat.id, False)) 

@dp.message(F.text == "Перейти в чат")
async def with_chat(message: types.Message):
    kb = [
        [KeyboardButton(text="Вернуться в меню")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("Вы выбрали опцию Перейти в чат", reply_markup=keyboard)

@dp.message(F.text == "Вернуться в меню")
async def with_menu(message: types.Message):
    kb = [
        [KeyboardButton(text="Посмотреть текст с картинки")],
        [KeyboardButton(text="Включить уведомления ✔️")],
        [KeyboardButton(text="Перейти в чат")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите опцию")
    await message.answer("Вы выбрали опцию вернуться в меню", reply_markup=keyboard)

async def send_reminders(chat_id, turnOn):
    global TurnOn
    TurnOn = turnOn

    list = [
        "Каждый день — это новый шанс стать лучше. 🌅",
        "Не бойтесь делать ошибки; они — шаги к успеху. 🚀",
        "Ваши мечты не имеют срока годности. 🌟",
        "Трудности делают вас сильнее. 💪",
        "Начните с того, что можете сделать, и сделайте это. 🏁",
        "Каждый маленький шаг приближает вас к цели. 👣",
        "Вы способны на большее, чем думаете. 🌈",
        "Успех — это не финал, а путь. 🛤️",
        "Верьте в себя, даже когда никто другой не верит. ✨",
        "Ваше время ограничено, не тратьте его на чужие мечты. ⏳",
        "Сложности — это возможности в маске. 🎭",
        "Сфокусируйтесь на процессе, а не только на результате. 🔍",
        "Каждый день — это возможность изменить свою жизнь. 🔄",
        "Не сравнивайте себя с другими; каждый идет своим путем. 🛤️",
        "Смелость — это не отсутствие страха, а умение действовать несмотря на него. 🦁",
        "Ваши мысли формируют вашу реальность. 💭",
        "Не останавливайтесь, когда устали; останавливайтесь, когда закончили. 🏆"
        "Каждый успех начинается с решения попробовать. ✔️",
        "Делайте то, что любите, и вы никогда не будете работать. ❤️",
        "Вы — автор своей истории; сделайте ее захватывающей! 📖",
        "Ваши мечты не имеют срока годности. 🌟"
        ]
    
    while TurnOn == True:
        random_message = random.choice(list)
        await bot.send_message(chat_id, random_message) # пауза 1 минуту
        await asyncio.sleep(10) 


@dp.message(F.photo)  # Обработчик фотографий
async def process_photo(message: Message):
    if message.photo:      
        try:
            # Загружаем фотографию по file_id
            await bot.download(
                message.photo[-1], 
                destination=f"C:/Users/tappy/Desktop/xxx/photos/{message.photo[-1].file_id}.jpg"
            )
            await message.answer("Файл записан в папку photos")  # Ответ пользователю

            reader = easyocr.Reader(['en', 'ru'])
            result = reader.readtext(f"C:/Users/tappy/Desktop/xxx/photos/{message.photo[-1].file_id}.jpg", detail=0, paragraph=True)
            if not result:
                await message.answer("Ничего не нашли")
            else:
                result_text = '\n'.join(result)
                await message.answer(result_text)

        except Exception as e:
            await message.answer(f"Произошла ошибка при загрузке: {e}")

with open('train_data.txt', 'r', encoding='utf-8') as file:
    text_of_book = file.read()


def load_data(file_path):
    qa_pairs = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if ':' in line:
                question, answer = line.split(':', 1)
                qa_pairs[question.strip().lower()] = answer.strip()
    return qa_pairs


@dp.message(F.text)
async def handle_message(message: types.Message):
    question = message.text.strip().lower()
    response = "Извините, я не понимаю. Попробуйте задать другой вопрос."
    for key in qa_pairs.keys():
        if any(word in question for word in key.split()):
            response = qa_pairs[key]
            break
    await message.answer(response)
    logger.info(f"Вопрос: {question} | Ответ: {response}")

# Метод main для запуска бота
async def main():
    global qa_pairs
    qa_pairs = load_data('train_data.txt') 
    await dp.start_polling(bot)  # Запуск бота с передачей объекта bot

if __name__ == '__main__':
    asyncio.run(main())
