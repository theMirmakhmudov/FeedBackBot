import os
import logging
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router,F
from aiogram.filters import Command
from aiogram.types import Message
from buttons import button

load_dotenv(".env")
TOKEN = os.getenv("Token")
Admin = os.getenv("Admin1")
Channel = os.getenv("Channel")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


class Form(StatesGroup):
    fullname = State()
    child_name = State()
    child_class = State()
    phone_number = State()
    address = State()
    finish = State()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Salom {message.from_user.full_name}", reply_markup=button)

    @router.message()
    async def starts(message: Message, state: FSMContext):
        if message.text == "Feedback qoldirish":
            await state.set_state(Form.fullname)
            await message.answer("To'liq ism familiyangiz kiriting\nMisol uchun: Mirmakhmudov Mirabdullo")
        else:
            await message.answer("Xatolik qayta urining")


@router.message(Form.fullname)
async def fullname(message: Message, state: FSMContext) -> None:
    await state.update_data(fullname=message.text)
    await state.set_state(Form.child_name)
    await message.answer(f"{message.text} farzandingiz ism familiyasini kiriting\nMisol uchun: Mirmakhmudov Abdulmajid")


@router.message(Form.child_name)
async def child_name(message: Message, state: FSMContext) -> None:
    await state.update_data(child_name=message.text)
    await state.set_state(Form.child_class)
    await message.answer(f"Farzandingiz nechanchi sinfda o'qishini kiriting\nMisol uchun: 9B")


@router.message(Form.child_class)
async def child_class(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(child_class=message.text)
    await state.set_state(Form.phone_number)
    await message.answer(
        "Telefon raqamingizni kiriting\nPs.Agar telegramingizdagi nomerni ulashmoqchi bo'lsangiz pastdagi contact ulashishga bosing\nAgar boshqa nomer kiritmoqchi bo'lsangiz +998 orqali text xolatida yozing")


@router.message(Form.phone_number)
async def process_phone_number(message: Message, state: FSMContext):
    if F.contact:
        await message.answer("Siz contact yubordizngiz")
    elif F.text:
        await message.answer("Telefon raqamingizni text ko'rinishida yubordingiz!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", )
    asyncio.run(main())
