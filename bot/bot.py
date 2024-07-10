import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
from aiogram import Router
from aiogram.filters.state import StateFilter
from dotenv import load_dotenv
from parsing.housekg.all_pages import get_pages
from ai.gpt import use_ai
from parsing.housekg.one_page import get_ad_data
import os

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)


class TestStates(StatesGroup):
    district = State()
    price_range = State()
    room_range = State()
    floors = State()


districts = [f"Район {i+1}" for i in range(99)]
district_buttons = [InlineKeyboardButton(text=district, callback_data=f"district_{district}") for district in districts]
district_buttons.append(InlineKeyboardButton(text="Далее ➡️", callback_data="next"))
district_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in district_buttons])

@router.message(Command("start"))
async def send_welcome(message: types.Message):
    start_button = InlineKeyboardButton(text='Начать тест', callback_data='start_test')
    start_keyboard = InlineKeyboardMarkup(inline_keyboard=[[start_button]])
    await message.reply("Привет! Нажми кнопку ниже, чтобы начать тест.", reply_markup=start_keyboard)

@router.callback_query(lambda c: c.data == 'start_test')
async def process_callback_start_test(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите районы вашей будущей квартиры:', reply_markup=district_keyboard)
    await state.set_state(TestStates.district)


@router.callback_query(lambda c: c.data.startswith('district_') or c.data == 'next')
async def process_district(callback_query: types.CallbackQuery, state: FSMContext):
    if await state.get_state() != TestStates.district:
        return
    data = await state.get_data()
    districts = data.get('districts', [])
    if callback_query.data.startswith('district_'):
        district = callback_query.data.split('_')[1]
        if district not in districts:
            districts.append(district)
            await state.update_data(districts=districts)
        await bot.answer_callback_query(callback_query.id, text=f"{district} добавлен.")
    
    if callback_query.data == 'next' or len(districts) >= 5:  # Предположим, достаточно 5 районов для примера
        await bot.send_message(callback_query.from_user.id, 'Введите желаемый ценовой диапазон (например, 3000000-5000000):')
        await state.set_state(TestStates.price_range)
    else:
        await bot.answer_callback_query(callback_query.id, text=f"Выберите еще районы или нажмите 'Далее'.")


@router.message(StateFilter(TestStates.price_range))
async def process_price_range(message: types.Message, state: FSMContext):
    price_range = message.text
    await state.update_data(price_range=price_range)
    await message.reply('Введите желаемое количество комнат (например, 2-4):')
    await state.set_state(TestStates.room_range)

@router.message(StateFilter(TestStates.room_range))
async def process_room_range(message: types.Message, state: FSMContext):
    room_range = message.text
    await state.update_data(room_range=room_range)
    await message.reply('Введите желаемые этажи через запятую (например, 3,5,7):')
    await state.set_state(TestStates.floors)

@router.message(StateFilter(TestStates.floors))
async def process_floors(message: types.Message, state: FSMContext):
    floors = message.text
    await state.update_data(floors=floors)

    await send_result(message.from_user.id)
    
    await state.clear()


async def send_result(user_id: int):
    items = get_pages()
    for item in items:
        ad = get_ad_data(item)
        ad = ("qwqqw", "asasas", "Квартира в центре города", "asasas", ["https://cdn.house.kg/house/images/c/0/b/c0bff90ea8c9b17d882c7b6596884115_1200x900.jpg", "https://cdn.house.kg/house/images/c/0/b/c0bff90ea8c9b17d882c7b6596884115_1200x900.jpg"])
        media = [types.InputMediaPhoto(media=url) for url in ad[4]]
        if media:
            media[-1].caption = use_ai(ad[2])
        try:
            await bot.send_media_group(user_id, media)
        except Exception as e:
            logging.error(f"Failed to send media group: {e}")
            await bot.send_message(user_id, f"Не удалось загрузить изображение: {e}")

if __name__ == '__main__':
    dp.run_polling(bot)
