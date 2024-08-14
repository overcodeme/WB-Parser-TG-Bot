from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import Router
from parser import parse_wildberries

TOKEN = '7389797526:AAFcwtuqshsfFs-ilgkfrqV1y-9xJGFwBCc'

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем роутер для обработки команд
router = Router()
dp.include_router(router)

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
        # Получаем товары
        products = parse_wildberries(url)

        # Ограничиваем количество товаров до 10
        if not products:
            await message.answer('Ничего не найдено.')
            return

        # Формируем список строк с информацией о товарах
        response = []
        for product in products[:10]:  # Берем только первые 10 товаров
            response.append(
                f"Название: {product['title']}\nСсылка: {product['link']}\nЦена без скидки: {product['old_price']}\nТекущая цена: {product['current_price']}\n"
            )

        # Объединяем все части в одно сообщение
        full_message = "\n".join(response)

        # Отправляем сообщение по частям, если оно слишком длинное
        max_message_length = 4096
        for i in range(0, len(full_message), max_message_length):
            await message.answer(full_message[i:i + max_message_length])

    except Exception as e:
        await message.answer(f'Ошибка при парсинге: {str(e)}')

# Функция для запуска бота
async def run_bot():
    # Запускаем бота
    await dp.start_polling(bot, skip_updates=True)
