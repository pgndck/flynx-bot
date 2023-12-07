import aiofiles
import logging
import os

from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from urllib.parse import urlparse

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from modules.logger import logger
from modules.settings import Settings


class States(StatesGroup):
    regular_usage = State()
    user_contact = State()
    send_link = State()
    send_text = State()
    main_menu = State()


def simple_keyboard(options):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=option) for option in options],
        ],
        resize_keyboard=True,
    )


router = Router()

bot = Bot(token=Settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_router(Router())


class Processor:
    async def run(self):
        global bot
        global dp

        dp.include_router(router)

        await dp.start_polling(bot)


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(States.user_contact)
    await message.answer("йо йо йо, ти тут щоб звʼязатись з нами?")
    await message.answer("то ти в правильному місці!")
    await message.answer(
        "для зручності даю тобі менюшку 🧜‍♀️",
        reply_markup=simple_keyboard(
            ["дати лінк на подію на фб", "написати нам своїми словами"]
        ),
        parse_mode=ParseMode.HTML,
    )


@router.message((F.from_user.id in Settings.ADMINS) & (F.text.casefold() == "/admin"))
async def admin(message: Message, state: FSMContext) -> None:
    await state.set_state(States.user_contact)
    await message.answer("а я тебе знаю")
    await message.answer("ти тут адміном працюєш")
    await message.answer("зараз тут нічого немає, але тут скоро буде адмінка!")
    await message.answer(
        "а поки що пиздуй в меню",
        reply_markup=simple_keyboard(
            ["дати лінк на подію на фб", "написати нам своїми словами"]
        ),
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("help"))
@router.message(F.text.casefold() == "/help")
async def help(message: Message, state: FSMContext) -> None:
    """
    Handle the command to display the help message.
    """
    logger.info(message)

    await message.answer("віу віу віу 🚑")
    await message.answer("це дуже маленький бот, тому в допомозі нічого немає")
    await message.answer(
        "сорямба 🌈",
        reply_markup=simple_keyboard(
            ["дати лінк на подію на фб", "написати нам своїми словами"]
        ),
        parse_mode=ParseMode.HTML,
    )

    await state.set_state(States.user_contact)


@router.message(States.user_contact)
async def user_contact(message: Message, state: FSMContext) -> None:
    next_state = {
        "дати лінк на подію на фб": States.send_link,
        "написати нам своїми словами": States.send_text,
    }.get(message.text, None)

    if next_state:
        await state.set_state(next_state)

        if message.text == "написати нам своїми словами":
            await message.reply(
                "будь ласка, пиши сюди всі компліменти, зауваження, взагалі все що можна!",
                reply_markup=ReplyKeyboardRemove(),
            )
            await message.answer("можеш розповісти тут про подію, або ще щось цікаве")
            await message.answer("тільки щоб це було одне повідомлення, окей? 🧜‍♀️")
            await message.answer("це я можу писати багато")
            await message.answer("а ти")
            await message.answer("ні")
            await message.answer("🧜‍♀️")
            await message.answer(
                "(правда, обмежся одним повідомленням, бо далі тебе поверне в меню)"
            )
        elif message.text == "дати лінк на подію на фб":
            await message.answer(
                "окей, чекаю на лінку! і краще б їй бути прикольною... 🧜‍♀️",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await state.set_state(States.user_contact)

        await message.reply(
            "ой, щось пішло не так... мабуть хтось любить писати від себе а не натискати кнопочки?"
        )
        await message.answer("а тепер все заново...")
        await message.answer(
            "... і ось менюшка 🧜‍♀️",
            reply_markup=simple_keyboard(
                ["дати лінк на подію на фб", "написати нам своїми словами"]
            ),
            parse_mode=ParseMode.HTML,
        )


@router.message(States.send_link)
async def send_link(message: Message, state: FSMContext) -> None:
    await state.set_state(States.user_contact)

    if message.text != "wrong link":
        # TODO: check facebook links

        await message.reply("ой яка подія, просто краса!")
        await message.answer("(я так відповідаю на всі події, сорі нот сорі)")
        await message.answer(
            "але дуже дякую! мої кльові адміни подивляться обовʼязково 🧜‍♀️"
        )
        await message.answer(
            "тут більше нема чого робити... тому ось менюшка!",
            reply_markup=simple_keyboard(
                ["дати лінк на подію на фб", "написати нам своїми словами"]
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        await message.reply("здається мені, що це не зовсім робоче посилання на подію")
        await message.answer("будь ласка, переконайся, що воно виглядає приблизно так:")
        await message.answer("https://www.facebook.com/events/12345678/")
        await message.answer("або так: https://facebook.com/events/12345678/")
        await message.answer("або навіть так: facebook.com/events/12345678/")
        await message.answer(
            "а в покарання ми тебе повертаємо в меню!",
            reply_markup=simple_keyboard(
                ["дати лінк на подію на фб", "написати нам своїми словами"]
            ),
            parse_mode=ParseMode.HTML,
        )


@router.message(States.send_text)
async def send_text(message: Message, state: FSMContext) -> None:
    # global bot

    await state.set_state(States.user_contact)

    if message.photo:
        await bot.send_photo(
            chat_id=Settings.ADMIN_GROUP,
            photo=message.photo[-1].file_id,
            caption=get_text_for_admins(message),
        )
    elif message.audio:
        await bot.send_audio(
            chat_id=Settings.ADMIN_GROUP,
            audio=message.audio.file_id,
            caption=get_text_for_admins(message),
        )
    elif message.video:
        await bot.send_video(
            chat_id=Settings.ADMIN_GROUP,
            video=message.video.file_id,
            caption=get_text_for_admins(message),
        )
    elif message.voice:
        await bot.send_message(
            chat_id=Settings.ADMIN_GROUP, text=get_text_for_admins(message)
        )
        await bot.send_voice(
            chat_id=Settings.ADMIN_GROUP,
            voice=message.voice.file_id,
        )
    elif message.video_note:
        await bot.send_message(
            chat_id=Settings.ADMIN_GROUP, text=get_text_for_admins(message)
        )
        await bot.send_video_note(
            chat_id=Settings.ADMIN_GROUP, video_note=message.video_note.file_id
        )
    elif message.sticker:
        await bot.send_message(
            chat_id=Settings.ADMIN_GROUP, text=get_text_for_admins(message)
        )
        await bot.send_sticker(
            chat_id=Settings.ADMIN_GROUP, sticker=message.sticker.file_id
        )
    else:
        await bot.send_message(
            chat_id=Settings.ADMIN_GROUP, text=get_text_for_admins(message)
        )

    await message.answer("вау, який текст! огого!")
    await message.answer("(я не знаю що там, просто мене так запрограмували)")
    await message.answer(
        "мої людинодрузі подивляться що там від тебе прийшло, а зараз..... менюшка!",
        reply_markup=simple_keyboard(
            ["дати лінк на подію на фб", "написати нам своїми словами"]
        ),
        parse_mode=ParseMode.HTML,
    )


def get_text_for_admins(message):
    return (
        f"🌈 увага! увага! 🌈\n"
        f"пісьмо від @{message.from_user.username}:\n"
        f"==========\n"
        f"{message.text if message.text else ''}"
        f"{message.caption if message.caption else ''}"
    )
