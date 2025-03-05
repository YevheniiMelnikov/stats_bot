from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from core.settings import settings

main_router = Router()


@main_router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Launch", web_app=WebAppInfo(url=f"{settings.WEBHOOK_HOST}/webapp"))]
        ]
    )
    await message.answer(text="Click the launch button", reply_markup=keyboard)
