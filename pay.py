from aiocryptopay import AioCryptoPay, Networks
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
import sqlite3
import asyncio
import pytz
import datetime
from datetime import timedelta
from reply import buttons
from hand import offer_def, id_list_dispatch, id_list_auto, forward, average_rating, del_media, edit_def, start_def, text_def
from inf import CRYPTO, CHANNEL_ID
tz = pytz.timezone("Europe/Samara")

rt_5 = Router()
crypto = AioCryptoPay(token=CRYPTO, network=Networks.MAIN_NET)

async def curs(price):
    usd = await crypto.get_exchange_rates()
    usd = usd[0].rate
    price = int(price) / float(usd)
    return price

async def creat(price):
    invoice = await crypto.create_invoice(asset='USDT', amount=price)
    return invoice

async def creat_2(invoice):
    invoices = await crypto.get_invoices(invoice_ids=invoice.invoice_id)
    if invoices.status == 'paid':
        return True
    if invoices.status == 'active':
        return False

async def payment_question(message, button_data):
    print(button_data)
    rows = [[InlineKeyboardButton(text="Оплатить Crypto Bot", callback_data=f'{button_data}_pay')],
            [InlineKeyboardButton(text='Оплатить внутренним счетом', callback_data=f'{button_data}_loc')]]
    if button_data == 'dispatch_pay_cb':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='dispatch_offer')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == '7day':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='auto_posting')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        try:
            await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)
        except:
            await message.answer(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == '30day':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='auto_posting')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        try:
            await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)
        except:
            await message.answer(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == 'unblock_pay':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='pay')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == 'unblock_1_pay':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='unblock_col')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == 'unblock_5_pay':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='unblock_col')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)
    if button_data == 'unblock_10_pay':
        rows.insert(2, [InlineKeyboardButton(text='‹ Назад', callback_data='unblock_col')])
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.edit_text(text='Выберете способ оплаты', reply_markup=markup)

@rt_5.callback_query(lambda query: query.data in id_list_dispatch)
async def pay_offer_menu(call: CallbackQuery, bot: Bot):
    global call_data, call_inf, id_msg_2, id_list_dispatch
    await call.message.delete()
    id_list_dispatch.clear()
    call_data = call.data
    call_data = call_data.replace('_dispatch', '')
    call_inf = call
    id_msg_2 = await forward(call.message, call_data)
    await payment_question(call.message, 'dispatch_pay_cb')

# [InlineKeyboardButton(text='Ограничение кол-во объявлений', callback_data='unblock')],
# [InlineKeyboardButton(text='Купить размещение объявление', callback_data='unblock_col')],

@rt_5.callback_query(F.data == 'pay')
async def pay(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text=f'Рассылка объявления 99 ₽', callback_data='dispatch_offer')],
            [InlineKeyboardButton(text=f'Автопубликация', callback_data='auto_posting')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='back')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='💰 <b>Платные тарифы</b>\n\n'
                                      '<b>Рассылка объявлений</b>:\n'
                                      'Бот отправляет выбранное объявление в личные сообщения всем пользователям с пометкой "Реклама"\n\n'
                                      '<b>Автопубликация</b>:\n'
                                      'Бот публикует выбранное объявление каждый день в 12:00 МСК+1 на протяжении времяни выбранного тарифа\n'
                                      , reply_markup=markup, parse_mode='html')

@rt_5.callback_query(F.data == 'dispatch_offer')
async def dispatch(call: CallbackQuery):
    rows = await offer_def(call.message, 'dispatch')
    if len(rows) == 1:
        row = [[buttons[0]],
               [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
        markup = InlineKeyboardMarkup(inline_keyboard=row)
        await call.message.edit_text(text='У вас нет опубликованных объявлений', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await call.message.edit_text(text='⬇️ <b>Это ваши объявления</b>\n\n'
                                          'Выберите объявление для покупки тарифа', reply_markup=markup, parse_mode='html')

@rt_5.callback_query(F.data == 'dispatch_pay_cb_loc')
async def dispatch(call: CallbackQuery, bot: Bot):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    if float(data[0]) - 0.01 < 0:
        await call.message.edit_text(text='❌ Недостаточно средств')
    else:
        cur.execute(f"UPDATE users SET balance = {float(data[0]) - 0.01} WHERE id = '{call.from_user.id}'")
        await dispatch_def(call, bot)
    db.commit()
    db.close()

@rt_5.callback_query(F.data == 'dispatch_pay_cb')
async def dispatch(call: CallbackQuery):
    global pay_def
    pay_def = await creat(await curs(100))
    rows = [[InlineKeyboardButton(text='Оплатить', url=pay_def.bot_invoice_url)],
            [InlineKeyboardButton(text='Проверить оплату', callback_data='chek_dispatch_pay')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'sdsd', reply_markup=markup)

@rt_5.callback_query(F.data == 'chek_dispatch_pay')
async def dispatch(call: CallbackQuery, bot: Bot):
    chek = await creat_2(pay_def, call.message)
    if chek == True:
        await dispatch_def(call, bot)
    if chek == False:
        await bot.answer_callback_query(callback_query_id=call.id, text='❌ Оплата не прошла', show_alert=True)

async def dispatch_def(call, bot):
    await call.message.edit_text(text='Оплата прошла успешно')
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute("SELECT id FROM users")
    ids = cur.fetchall()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    a = name[0][2]
    a = a.split('|')
    a.pop(0)
    text = await text_def(call_data, call.message.chat.username)
    text = f"❗<b>РЕКЛАМА</b>❗\n\n{text}"
    builder = MediaGroupBuilder(caption=text)
    for i in a:
        builder.add_photo(media=f'{i}', parse_mode="HTML")
    for i in ids:
        await bot.send_media_group(chat_id=i[0], media=builder.build())

@rt_5.callback_query(F.data == 'auto_posting')
async def auto_posting_1(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='7 дней 99₽', callback_data='7day')],
            [InlineKeyboardButton(text='30 дней 349₽', callback_data='30day')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='Выберите периуд автопубликации вашего объявления', reply_markup=markup)
@rt_5.callback_query(F.data == '30day')
@rt_5.callback_query(F.data == '7day')
async def auto_posting_2(call: CallbackQuery):
    global ap_data
    rows = await offer_def(call.message, 'auto')
    if call.data == '7day':
        ap_data = '7day_auto'
    else:
        ap_data = '30day_auto'

    if len(rows) == 1:
        row = [[buttons[0]],
               [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
        markup = InlineKeyboardMarkup(inline_keyboard=row)
        await call.message.edit_text(text='У вас нет опубликованных объявлений', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await call.message.edit_text(text='⬇️ <b>Это ваши объявления</b>\n\n'
                                          'Выберите объявление для покупки тарифа', reply_markup=markup, parse_mode='html')

@rt_5.callback_query(lambda query: query.data in id_list_auto)
async def auto_posting_3(call: CallbackQuery):
    global call_data, call_inf, id_msg_2, id_list_auto
    id_list_auto.clear()
    call_data = call.data
    call_data = call_data.replace('_auto', '')
    call_inf = call

    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT offer_id_channel FROM auto_posting WHERE offer_id_channel = '{call_data}'")
    data = cur.fetchone()
    db.commit()
    db.close()
    if data != None:
        rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='auto_posting')]]
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        db = sqlite3.connect('users.db')
        cur = db.cursor()
        cur.execute(f"SELECT final FROM auto_posting WHERE offer_id_channel = '{call_data}'")
        still_time = cur.fetchone()
        db.commit()
        db.close()
        still_time_2 = still_time[0].split('-')
        still_time = datetime.datetime(int(still_time_2[0]), int(still_time_2[1]), int(still_time_2[2]), tzinfo=tz) - datetime.datetime.now(tz)
        await call.message.edit_text(text=f'Это объявление уже используется в тарифе.\n\nДо конца тарифа {still_time.days + 1} дней ', reply_markup=markup)
    else:
        await call.message.delete()
        id_msg_2 = await forward(call.message, call_data)
        if ap_data == '7day_auto':
            await payment_question(call.message, '7day')
        elif ap_data == '30day_auto':
            await payment_question(call.message, '30day')

@rt_5.callback_query(F.data == 'back_7day')
@rt_5.callback_query(F.data == 'back_30day')
async def auto_posting(call: CallbackQuery):
    if call.data == 'back_7day':
        await payment_question(call.message, "7day")
    else:
        await payment_question(call.message, "30day")

@rt_5.callback_query(F.data == '7day_pay')
async def auto_posting(call: CallbackQuery):
    global pay_def
    pay_def = await creat(0.05)
    rows = [[InlineKeyboardButton(text='Оплатить', url=pay_def.bot_invoice_url)],
            [InlineKeyboardButton(text='Проверить оплату', callback_data='chek_auto_pay_7')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='back_7day')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'❗<b>Подтвердите покупку</b>❗\n\n<b>Тариф:</b> Автопубликация 7 дней\n\n<b>Цена:</b> 99 ₽',reply_markup=markup, parse_mode="HTML")

@rt_5.callback_query(F.data == '30day_pay')
async def auto_posting(call: CallbackQuery):
    global pay_def
    pay_def = await creat(0.05)
    rows = [[InlineKeyboardButton(text='Оплатить', url=pay_def.bot_invoice_url)],
            [InlineKeyboardButton(text='Проверить оплату', callback_data='chek_auto_pay_30')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='back_30day')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'❗<b>Подтвердите покупку</b>❗\n\n<b>Тариф:</b> Автопубликация 30 дней\n\n<b>Цена:</b> 349 ₽', reply_markup=markup, parse_mode="HTML")

@rt_5.callback_query(F.data == '7day_loc')
async def auto_posting(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='Оплатить', callback_data='7day_pay_loc')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='back_7day')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'❗<b>Подтвердите покупку</b>❗\n\n<b>Тариф:</b> Автопубликация 7 дней\n\n<b>Цена:</b> 99 ₽', reply_markup=markup, parse_mode="HTML")

@rt_5.callback_query(F.data == '30day_loc')
async def auto_posting(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='Оплатить', callback_data='30day_pay_loc')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='back_30day')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'❗<b>Подтвердите покупку</b>❗\n\n<b>Тариф:</b> Автопубликация 30 дней\n\n<b>Цена:</b> 349 ₽', reply_markup=markup, parse_mode="HTML")

@rt_5.callback_query(F.data == '30day_pay_loc')
async def auto_posting(call: CallbackQuery):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    if float(data[0]) - 0.01 < 0:
        await call.message.edit_text(text='Недостаточно средств')
    else:
        cur.execute(f"UPDATE users SET balance = {float(data[0]) - 0.01} WHERE id = '{call.from_user.id}'")
        date = datetime.datetime.strptime(f'{datetime.date.today()}', '%Y-%m-%d')
        new_date = date + timedelta(days=30)
        cur.execute(
            f"INSERT INTO auto_posting VALUES ('{call.message.chat.id}', '{call_data}', '{call.from_user.username}', '{datetime.date.today()}', '{new_date.strftime('%Y-%m-%d')}')")
        msg = await call.message.edit_text(text='Успешно')
        await start_def(call.message)
        await asyncio.sleep(3)
        await msg.delete()
    db.commit()
    db.close()

@rt_5.callback_query(F.data == '7day_pay_loc')
async def auto_posting(call: CallbackQuery):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    if float(data[0]) - 0.01 < 0:
        await call.message.edit_text(text='Недостаточно средств')
    else:
        cur.execute(f"UPDATE users SET balance = {float(data[0]) - 0.01} WHERE id = '{call.from_user.id}'")
        date = datetime.datetime.strptime(f'{datetime.date.today()}', '%Y-%m-%d')
        new_date = date + timedelta(days=7)
        cur.execute(
            f"INSERT INTO auto_posting VALUES ('{call.message.chat.id}', '{call_data}', '{call.from_user.username}', '{datetime.date.today()}', '{new_date.strftime('%Y-%m-%d')}')")
        msg = await call.message.edit_text(text='Успешно')
        await start_def(call.message)
        await asyncio.sleep(3)
        await msg.delete()
    db.commit()
    db.close()

@rt_5.callback_query(lambda query: query.data in ['chek_auto_pay_7', 'chek_auto_pay_30'])
async def auto_posting(call: CallbackQuery, bot: Bot):
    chek = await creat_2(pay_def, call.message)

    if chek == True:
        if call.data == 'chek_auto_pay_7':
            tarif = 7
        if call.data == 'chek_auto_pay_30':
            tarif = 30
        date = datetime.datetime.strptime(f'{datetime.date.today()}', '%Y-%m-%d')
        new_date = date + timedelta(days=tarif)
        db = sqlite3.connect('users.db')
        cur = db.cursor()
        cur.execute(f"INSERT INTO auto_posting VALUES ('{call.message.chat.id}', '{call_data}', '{call.from_user.username}', '{datetime.date.today()}', '{new_date.strftime('%Y-%m-%d')}')")
        msg = await call.message.edit_text(text='Оплата прошла')
        await start_def(call.message)
        await asyncio.sleep(3)
        await msg.delete()
        db.commit()
        db.close()
    if chek == False:
        await bot.answer_callback_query(callback_query_id=call.id, text='Оплата не прошла', show_alert=True)

@rt_5.callback_query(F.data == 'unblock')
async def unblock(call: CallbackQuery):
    await payment_question(call.message, 'unblock_pay')

@rt_5.callback_query(F.data == 'unblock_pay')
async def unblock_pay(call: CallbackQuery):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT id FROM unblock WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    db.commit()
    db.close()

    if data != None:
        rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await call.message.edit_text(text='Вы уже являетесь владельцем данного тавара', reply_markup=markup)
    else:
        global pay_def
        pay_def = await creat(0.02)
        rows = [[InlineKeyboardButton(text='Оплатить', url=pay_def.bot_invoice_url)],
                [InlineKeyboardButton(text='Проверить оплату', callback_data='chek_unblock_pay')],
                [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await call.message.edit_text(text='Оплата товара', reply_markup=markup)

@rt_5.callback_query(F.data == 'unblock_pay_loc')
async def unblock_pay(call: CallbackQuery):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    if float(data[0]) - 0.01 < 0:
        await call.message.edit_text(text='Недостаточно средств')
    else:
        cur.execute(f"UPDATE users SET balance = {float(data[0]) - 0.01} WHERE id = '{call.from_user.id}'")
        cur.execute(f"SELECT id FROM unblock WHERE id = '{call.from_user.id}'")
        data = cur.fetchone()

        if data != None:
            rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
            markup = InlineKeyboardMarkup(inline_keyboard=rows)
            await call.message.edit_text(text='Вы уже являетесь владельцем данного тавара', reply_markup=markup)
        else:
            await call.message.edit_text(text='Прошла оплата')
            date = datetime.datetime.now().date()
            cur.execute(f"INSERT INTO unblock VALUES ('{call.message.chat.id}', '{call.from_user.username}', '{date}')")

    db.commit()
    db.close()

@rt_5.callback_query(F.data == 'chek_unblock_pay')
async def chek_unblock_pay(call: CallbackQuery, bot: Bot):
    chek = await creat_2(pay_def, call.message)
    if chek == True:
        await call.message.edit_text(text='Прошла оплата')
        date = datetime.datetime.now().date()
        db = sqlite3.connect('users.db')
        cur = db.cursor()
        cur.execute(f"INSERT INTO unblock VALUES ('{call.message.chat.id}', '{call.from_user.username}', '{date}')")
        db.commit()
        db.close()
    if chek == False:
        await bot.answer_callback_query(callback_query_id=call.id, text='Оплата не прошла', show_alert=True)

@rt_5.callback_query(F.data == 'unblock_col')
async def unblock_col(call: CallbackQuery, bot: Bot):
   rows = [[InlineKeyboardButton(text='Купить 1 размещение', callback_data='unblock_1')],
           [InlineKeyboardButton(text='Купить 5 размещение', callback_data='unblock_5')],
           [InlineKeyboardButton(text='Купить 10 размещение', callback_data='unblock_10')],
           [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
   markup = InlineKeyboardMarkup(inline_keyboard=rows)
   await call.message.edit_text(text='Выбирете товар', reply_markup=markup)

@rt_5.callback_query(lambda query: query.data in ['unblock_1', 'unblock_5', 'unblock_10'])
async def chek_unblock_col(call: CallbackQuery, bot: Bot):
    global pay_def, call_data_ub
    call_data_ub = call.data
    if call.data == 'unblock_1':
        await payment_question(call.message, 'unblock_1_pay')
    if call.data == 'unblock_5':
        await payment_question(call.message, 'unblock_5_pay')
    if call.data == 'unblock_10':
        await payment_question(call.message, 'unblock_10_pay')

@rt_5.callback_query(lambda query: query.data in ['unblock_1_pay_loc', 'unblock_5_pay_loc', 'unblock_10_pay_loc'])
async def chek_unblock_col(call: CallbackQuery, bot: Bot):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT balance FROM users WHERE id = '{call.from_user.id}'")
    data = cur.fetchone()
    if float(data[0]) - 0.01 < 0:
        await call.message.edit_text(text='Недостаточно средств')
    else:
        cur.execute(f"UPDATE users SET balance = {float(data[0]) - 0.01} WHERE id = '{call.from_user.id}'")
        await call.message.edit_text(text='Прошла оплата')
        cur.execute(f"SELECT col FROM unblock_col WHERE id = '{call.from_user.id}'")
        col = cur.fetchone()
        data = call_data_ub.replace('unblock_', '')
        if col == None:
            cur.execute(f"INSERT INTO unblock_col VALUES ('{call.message.chat.id}', '{call.from_user.username}', '{data}')")
        else:
            cur.execute(f"UPDATE unblock_col SET col = {int(col[0]) + int(data)} WHERE id = {call.from_user.id}")
    db.commit()
    db.close()

@rt_5.callback_query(lambda query: query.data in ['unblock_1_pay', 'unblock_5_pay', 'unblock_10_pay'])
async def chek_unblock_col(call: CallbackQuery, bot: Bot):
    global pay_def, call_data_ub
    call_data_ub = call.data
    if call.data == 'unblock_1_pay':
        pay_def = await creat(0.02)
    if call.data == 'unblock_5_pay':
        pay_def = await creat(0.02)
    if call.data == 'unblock_10_pay':
        pay_def = await creat(0.02)
    rows = [[InlineKeyboardButton(text='Оплатить', url=pay_def.bot_invoice_url)],
            [InlineKeyboardButton(text='Проверить оплату', callback_data='chek_unblock_col_pay')],
            [InlineKeyboardButton(text='‹ Назад', callback_data='pay')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='Оплата товара', reply_markup=markup)

@rt_5.callback_query(F.data == 'chek_unblock_col_pay')
async def chek_unblock_col_pay(call: CallbackQuery, bot: Bot):
    chek = await creat_2(pay_def, call.message)
    if chek == True:
        await call.message.edit_text(text='Прошла оплата')
        db = sqlite3.connect('users.db')
        cur = db.cursor()
        cur.execute(f"SELECT col FROM unblock_col WHERE id = '{call.from_user.id}'")
        col = cur.fetchone()

        data = call_data_ub.replace('unblock_', '')
        if col == None:
            cur.execute(f"INSERT INTO unblock_col VALUES ('{call.message.chat.id}', '{call.from_user.username}', '{data}')")
        else:
            cur.execute(f"UPDATE unblock_col SET col = {int(col[0]) + int(data) } WHERE id = {call.from_user.id}")
        db.commit()
        db.close()
    if chek == False:
        await bot.answer_callback_query(callback_query_id=call.id, text='Оплата не прошла', show_alert=True)