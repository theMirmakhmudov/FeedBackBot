import os
import logging
import asyncio

from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from buttons import button, contact, location
from aiogram.types import ReplyKeyboardRemove

load_dotenv(".env")
TOKEN = os.getenv("Token")
Admin = os.getenv("Admin1")
Channel = os.getenv("Channel")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class Form(StatesGroup):
    fullname = State()
    child_name = State()
    child_class = State()
    phone_number = State()
    address = State()
    izoh = State()
    finish = State()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"<b>Assalomu alaykum.Xurmatli {message.from_user.full_name}</b>", reply_markup=button)

    @router.message()
    async def starts(message: Message, state: FSMContext):
        if message.text == "Feedback qoldirish":
            await state.set_state(Form.fullname)
            await message.answer("<b>To'liq ism familiyangiz kiriting\nMisol uchun: Mirmakhmudov Mirabdullo</b>",
                                 reply_markup=ReplyKeyboardRemove())


@router.message(Form.fullname)
async def fullname(message: Message, state: FSMContext) -> None:
    await state.update_data(fullname=message.text)
    await state.set_state(Form.child_name)
    await message.answer(
        f"<b>{message.text} farzandingiz ism familiyasini kiriting\nMisol uchun: Mirmakhmudov Abdulmajid</b>")


@router.message(Form.child_name)
async def child_name(message: Message, state: FSMContext) -> None:
    await state.update_data(child_name=message.text)
    await state.set_state(Form.child_class)
    await message.answer(f"<b>Farzandingiz nechanchi sinfda o'qishini kiriting\nMisol uchun: 9B</b>")


@router.message(Form.child_class)
async def child_class(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(child_class=message.text)
    await state.set_state(Form.phone_number)
    await message.answer("<b>Contactingizni yuboring</b>", reply_markup=contact)


@router.message(Form.phone_number and F.contact)
async def process_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number1=message.contact.phone_number)
    await message.answer("<b>Address yuboring</b>", reply_markup=location)


@router.message(Form.address and F.location)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address1=message.location.latitude)
    await state.update_data(address2=message.location.longitude)
    await state.set_state(Form.izoh)
    await message.answer("<b>Feedback yozing yoki izoh kiriting</b>",reply_markup=ReplyKeyboardRemove())


@router.message(Form.izoh)
async def process_izoh(message: Message, state: FSMContext):
    await state.update_data(izoh=message.text)
    await state.set_state(Form.finish)
    await message.answer("<b>Ma'lumotlar qabul qilindi!</b>")
    await message.answer("<b>Arizangiz qabul qilindi!</b>")
    data = await state.get_data()
    await state.clear()
    fullname = data.get("fullname", "Unknown")
    child_name = data.get("child_name", "Unknown")
    child_class = data.get("child_class", "Unknown")
    phone_number1 = data.get("phone_number1", "Unknown")
    address1 = data.get("address1", "Unknown")
    address2 = data.get("address2", "Unknown")
    izoh = data.get("izoh", "Unknown")

    msg = f"<b>🧔🏻‍♂️ FISH: {fullname}\n👦 Farzandining ismi: {child_name}\n🏫 Farzandining sinfi: {child_class}\n📲 Telefon raqam: {phone_number1}\n📝 Izohi: {izoh}</b>"
    await bot.send_message(Channel, msg)
    await bot.send_location(Channel, latitude=address1, longitude=address2)  # noqa


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", )
    asyncio.run(main())
