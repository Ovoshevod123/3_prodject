from aiogram import types, Router, F, Bot
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.filters import Command
import sqlite3
import time
import asyncio
from hand import send_01

rt_6 = Router()

@rt_6.callback_query(F.data == 'ref')
async def ref_1(call: CallbackQuery):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT col_ref FROM users WHERE id = '{call.message.chat.id}'")
    col_ref = cur.fetchone()
    db.commit()
    db.close()
    rows = [[(InlineKeyboardButton(text='‹ Назад', callback_data='account'))]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'<b>👥 Меню реферальной системы</b>\n\n'
                                      f'🗣 Кол-во ваших рефералов: <b>{col_ref[0]}</b>\n\n'
                                      f'🔗 Ваша реферальная ссылка:\n'
                                      f'<code>https://t.me/VBaraholka_bot/?start={call.message.chat.id}</code>\n\n'
                                      f'<i><b>За каждого приглашенного пользователя вам начисляется 200 ₽</b></i>\n'  , reply_markup=markup, parse_mode='html')