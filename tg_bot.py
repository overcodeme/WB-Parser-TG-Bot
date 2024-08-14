from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from parser import parse_wildberries

TOKEN = '7389797526:AAFcwtuqshsfFs-ilgkfrqV1y-9xJGFwBCc'

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем роутер для обработки команд
router = Router()
dp.include_router(router)

# Создание минимального интерфейса
def get_main_menu():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Начать парсинг", callback_data="start_parsing"))
    keyboard.add(InlineKeyboardButton(text="Оплата", callback_data="payment"))
    return keyboard

# Функция для установки командных подсказок
async def set_bot_commands(my_bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/parse", description="Парсинг товаров"),
        # Добавьте дополнительные команды, если нужно
    ]
    await my_bot.set_my_commands(commands)

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer('Привет! Используйте команду /parse <URL>, чтобы получить информацию о товарах.')

# Обработчик команды /parse
@router.message(Command("parse"))
async def parse(message: types.Message):
    url = message.text[len("/parse "):].strip()

    if not url:
        await message.answer('Пожалуйста, укажите URL для парсинга.')
        return

    await message.answer('Начинаю парсинг...')

    try:
        products = parse_wildberries(url)
        if not products:
            await message.answer('Ничего не найдено.')
            return

        response = []
        for product in products[:10]:  # Отправляем только 10 товаров
            response.append(
                f"Название: {product['title']}\nСсылка: {product['link']}\nЦена без скидки: {product['old_price']}\nТекущая цена: {product['current_price']}\n")

        await message.answer("\n".join(response))
    except Exception as e:
        await message.answer(f'Ошибка при парсинге: {str(e)}')

# Функция для запуска бота
async def run_bot():
    await set_bot_commands(bot)  # Установка команд
    await dp.start_polling(bot, skip_updates=True)
