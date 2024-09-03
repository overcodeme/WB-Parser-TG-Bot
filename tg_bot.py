from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

TOKEN = '7389797526:AAFcwtuqshsfFs-ilgkfrqV1y-9xJGFwBCc'

# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Создаем клавиатуру с кнопкой "Start", которая будет отображаться всегда
start_button_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Start")]
    ],
    resize_keyboard=True  # Автоматическая подгонка размера кнопок
)


# Основные категории
def create_categories_inline_menu():
    return {
        'Футболки': {
            'Мужские': {
                'callback_data': 'category_tshirts_men',
                'url': 'https://wildberries.ru/catalog/muzhchiny/odezhda/futbolki'
            },
            'Женские': {
                'callback_data': 'category_tshirts_women',
                'url': 'https://wildberries.ru/catalog/zhenshchiny/odezhda/futbolki'
            }
        },
        'Лонгсливы': {
            'Мужские': {
                'callback_data': 'category_longsleeves_men',
                'url': 'https://wildberries.ru/catalog/muzhchiny/odezhda/longslivy'
            },
            'Женские': {
                'callback_data': 'category_longsleeves_women',
                'url': 'https://wildberries.ru/catalog/zhenshchiny/odezhda/longslivy'
            }
        },
        'Кроссовки': {
            'Мужские': {
                'callback_data': 'category_sneakers_men',
                'url': 'https://wildberries.ru/catalog/muzhchiny/obuv/krossovki'
            },
            'Женские': {
                'callback_data': 'category_sneakers_women',
                'url': 'https://wildberries.ru/catalog/zhenshchiny/obuv/krossovki'
            }
        },
        'Носки': {
            'Мужские': {
                'callback_data': 'category_socks_men',
                'url': 'https://wildberries.ru/catalog/muzhchiny/aksessuary/noski'
            },
            'Женские': {
                'callback_data': 'category_socks_women',
                'url': 'https://wildberries.ru/catalog/zhenshchiny/aksessuary/noski'
            }
        }
    }


def generate_inline_keyboard(categories):
    """Функция для создания инлайн-клавиатуры для текущего уровня категорий."""
    inline_kb = InlineKeyboardMarkup(row_width=2)  # Ряд из двух кнопок по умолчанию

    for category_name, subcategory_info in categories.items():
        button = InlineKeyboardButton(
            text=category_name,
            callback_data=subcategory_info['callback_data']
        )
        inline_kb.add(button)

    return inline_kb


def generate_subcategories_keyboard(subcategories):
    """Функция для создания инлайн-клавиатуры для подкатегорий."""
    inline_kb = InlineKeyboardMarkup(row_width=2)  # Ряд из двух кнопок по умолчанию

    for subcategory_name, subcategory_info in subcategories.items():
        button = InlineKeyboardButton(
            text=subcategory_name,
            url=subcategory_info['url']
        )
        inline_kb.add(button)

    return inline_kb


# Основные категории
categories = create_categories_inline_menu()


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
    main_menu = generate_inline_keyboard(categories)
    await message.answer("Выберите категорию:", reply_markup=main_menu)


# Обработчик нажатий на инлайн-кнопки
@router.callback_query()
async def process_callback(callback_query: types.CallbackQuery):
    category_key = callback_query.data

    # Ищем категорию по ключу
    selected_category = next(
        (info for name, info in categories.items() if info['callback_data'] == category_key),
        None
    )

    if selected_category:
        subcategories_menu = generate_subcategories_keyboard({
            name: {'url': info['url']}
            for name, info in selected_category.items() if 'url' in info
        })
        await callback_query.message.edit_text("Выберите подкатегорию:", reply_markup=subcategories_menu)
    else:
        await callback_query.message.answer("Неправильный выбор.")


# Очистка списка команд
async def clear_bot_commands(my_bot: Bot):
    await my_bot.set_my_commands([])  # Установка пустого списка команд


# Функция для запуска бота
async def run_bot():
    await clear_bot_commands(bot)  # Очистка команд
    await dp.start_polling(bot, skip_updates=True)

