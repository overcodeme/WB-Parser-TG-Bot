from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.filters import Command  # Импортируем Command для фильтрации по команде
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

TOKEN = '7389797526:AAFcwtuqshsfFs-ilgkfrqV1y-9xJGFwBCc'

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаем роутер для обработки команд
router = Router()
dp.include_router(router)

# Создаем клавиатуру с кнопкой "Start", которая будет отображаться всегда
start_button_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")]
    ],
    resize_keyboard=True  # Автоматическая подгонка размера кнопок
)

# Создаем инлайн-клавиатуру с кнопками для главного меню
main_inline_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Parse", callback_data="parse_callback")],
        [InlineKeyboardButton(text="Команда 1", callback_data="cmd1")],
        [InlineKeyboardButton(text="Команда 2", callback_data="cmd2")],
        [InlineKeyboardButton(text="Команда 3", callback_data="cmd3")],
    ]
)

# Функция для создания инлайн-клавиатуры с категориями по 4 кнопки в строке
def create_categories_inline_menu():
    categories = [
        ("Женщинам", "category_women"),
        ("Обувь", "category_shoes"),
        ("Детям", "category_kids"),
        ("Мужчинам", "category_men"),
        ("Дом", "category_home"),
        ("Красота", "category_beauty"),
        ("Аксессуары", "category_accessories"),
        ("Электроника", "category_electronics"),
        ("Игрушки", "category_toys"),
        ("Мебель", "category_furniture"),
        ("Товары для взрослых", "category_adults"),
        ("Продукты", "category_food"),
        ("Бытовая техника", "category_appliances"),
        ("Зоотовары", "category_pets"),
        ("Спорт", "category_sports"),
        ("Автотовары", "category_auto"),
        ("Школа", "category_school"),
        ("Книги", "category_books"),
        ("Для ремонта", "category_repair"),
        ("Сад и дача", "category_garden"),
        ("Здоровье", "category_health"),
        ("Канцтовары", "category_stationery"),
    ]

    # Создаем InlineKeyboardMarkup с пустым списком строк
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[])

    # Добавляем кнопки в инлайн-клавиатуру по 4 в строке
    row = []
    for name, callback_data in categories:
        button = InlineKeyboardButton(text=name, callback_data=callback_data)
        row.append(button)
        if len(row) == 4:
            inline_kb.inline_keyboard.append(row)
            row = []

    # Добавляем оставшиеся кнопки, если их меньше 4
    if row:
        inline_kb.inline_keyboard.append(row)

    return inline_kb


# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        'Добро пожаловать! Нажмите кнопку "Start", чтобы продолжить.',
        reply_markup=start_button_keyboard  # Отображаем клавиатуру с кнопкой "Start"
    )


# Обработчик кнопки "Start" в клавиатуре
@router.message(lambda message: message.text == "Start")
async def show_main_menu(message: types.Message):
    await message.answer(
        'Выберите команду:',
        reply_markup=main_inline_menu  # Показываем главное меню
    )


# Обработчик нажатий на инлайн-кнопки
@router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "parse_callback":
        # Показываем меню с категориями
        categories_inline_menu = create_categories_inline_menu()  # Создаем клавиатуру при каждом запросе
        await callback_query.message.answer("Выберите категорию:", reply_markup=categories_inline_menu)
    elif callback_query.data.startswith("category_"):
        # Обработка выбранной категории
        category = callback_query.data.split("_")[1]
        await callback_query.message.answer(f"Вы выбрали категорию: {category}")


# Очистка списка команд
async def clear_bot_commands(my_bot: Bot):
    await my_bot.set_my_commands([])  # Установка пустого списка команд


# Функция для запуска бота
async def run_bot():
    await clear_bot_commands(bot)  # Очистка команд
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(run_bot())
