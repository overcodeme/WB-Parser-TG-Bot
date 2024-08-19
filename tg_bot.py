from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from parser import parse_wildberries

TOKEN = '7389797526:AAFcwtuqshsfFs-ilgkfrqV1y-9xJGFwBCc'

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем роутер для обработки команд
router = Router()
dp.include_router(router)

# Функция для установки командных подсказок
async def set_bot_commands(my_bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать работу с ботом"),
        BotCommand(command="/parse", description="Парсинг товаров"),
    ]
    await my_bot.set_my_commands(commands)

# Создаем главную клавиатуру с кнопкой "Start"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")]
    ],
    resize_keyboard=True  # Автоматическая подгонка размера кнопок
)

# Создаем инлайн клавиатуру для кастомного меню
custom_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start_callback")],  # Добавляем кнопку Start
        [InlineKeyboardButton(text="Команда 1", callback_data="cmd1")],
        [InlineKeyboardButton(text="Команда 2", callback_data="cmd2")],
        [InlineKeyboardButton(text="Команда 3", callback_data="cmd3")],
    ]
)

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        'Добро пожаловать! Выберите команду:',
        reply_markup=custom_menu  # Показываем кастомное меню
    )

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

# Обработчик нажатий на инлайн-кнопки
@router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "start_callback":
        # Обрабатываем нажатие кнопки Start
        await start(callback_query.message)
    elif callback_query.data == "cmd1":
        await callback_query.message.answer("Вы выбрали команду 1")
    elif callback_query.data == "cmd2":
        await callback_query.message.answer("Вы выбрали команду 2")
    elif callback_query.data == "cmd3":
        await callback_query.message.answer("Вы выбрали команду 3")

# Функция для запуска бота
async def run_bot():
    await set_bot_commands(bot)  # Установка команд
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_bot())
