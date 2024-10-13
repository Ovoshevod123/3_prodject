import datetime
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
import sqlite3
import asyncio
from reply import buttons, but_del, edit_but, buttons_edit
from inf import CHANNEL_ID
from feedback import average_rating, account_fb, feedback_chek_group

rt = Router()

photo = []
id_list = []
id_list_dispatch = []
id_list_auto = []
chek_ub = []

send_01 = Message
class new_product(StatesGroup):
    group = State()
    photo = State()
    name = State()
    description = State()
    price = State()
    locate = State()

async def start_def(message: Message):
    rows = [[buttons[5], buttons[1]],
            [buttons[6], InlineKeyboardButton(text='🆘 Тех. поддрежка', url='t.me/Kukuru3a')],
            [buttons[0]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    text = (f'<b>💨 VБарахолка 💨</b>\n\n'
            f'Покупайте, продавайте под системы, кальяты и т.д.\n\n'
            f'Подпичывайтесь на наш канал.\n\n'
            f'Ваши объявления публикуются здесь.')
    await message.answer(text=text, reply_markup=markup, parse_mode='HTML')

@rt.message(Command('start'))
async def start(message: Message, bot: Bot):
    global send_01
    rows = [[buttons[5], buttons[1]],
            [buttons[6], InlineKeyboardButton(text='🆘 Тех. поддрежка', url='t.me/Kukuru3a')],
            [buttons[0]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    text = (f'<b>💨 VБарахолка 💨</b>\n\n'
            f'Покупайте, продавайте под системы, кальяты и т.д.\n\n'
            f'Подпичывайтесь на наш канал.\n\n'
            f'Ваши объявления публикуются здесь.')
    send_01 = message
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT id FROM users WHERE id = '{send_01.from_user.id}'")
    info = cur.fetchone()
    if send_01.text == '/start':
        ref = None
        await message.answer(text=text, reply_markup=markup, parse_mode='HTML')
    else:
        ref = send_01.text.replace('/start ', '')
        if ref[0:2] == '2_':
            ref = ref.replace('2_', '')
            await feedback_chek_group(message, ref)
        elif ref[0:2] == '1_':
            if ref[2:] == str(send_01.from_user.id):
                ref = None
            else:
                cur.execute(f"SELECT id FROM users WHERE id = '{ref}'")
                await bot.send_message(chat_id=int(ref), text='По вашей ссылке')
            await message.answer(text=text, reply_markup=markup, parse_mode='HTML')

    if info == None:
        cur.execute(f"SELECT col_ref FROM users WHERE id = '{ref}'")
        col_ref = cur.fetchall()
        cur.execute(f"Update users set 'col_ref' = '{int(col_ref[0][0]) + 1}' where id = '{ref}'")
        cur.execute(f"INSERT INTO users VALUES ('{send_01.from_user.id}', '{send_01.from_user.username}', '0', '0', '{ref}')")
    db.commit()
    db.close()

@rt.callback_query(F.data == 'back')
async def back(call: CallbackQuery, state: FSMContext):
    global id_list, id_list_pay
    rows = [[buttons[5], buttons[1]],
            [buttons[6], InlineKeyboardButton(text='🆘 Помощь', url='t.me/Kukuru3a')],
            [buttons[0]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text=f'<b>💨 VБарахолка 💨</b>\n\n'
                              f'Покупайте, продавайте под системы, кальяты и т.д.\n\n'
                              f'Подпичывайтесь на наш канал.\n\n'
                              f'Ваши объявления публикуются здесь.', reply_markup=markup, parse_mode='HTML')
    await state.clear()
    id_list.clear()
    id_list_dispatch.clear()
    id_list_auto.clear()

# @rt.callback_query(F.data == 'new')
# async def new_1(callback: CallbackQuery, state: FSMContext):
#     rows = [[InlineKeyboardButton(text='Под система', callback_data='pod'), InlineKeyboardButton(text='Жидкость', callback_data='zhizha')],
#             [buttons[4]]]
#     markup = InlineKeyboardMarkup(inline_keyboard=rows)
#     photo.clear()
#     db = sqlite3.connect('users.db')
#     cur = db.cursor()
#     cur.execute(f"SELECT id FROM unblock WHERE id = '{send_01.from_user.id}'")
#     ub = cur.fetchone()
#     cur.execute(f"SELECT col FROM unblock_col WHERE id = '{send_01.from_user.id}'")
#     col = cur.fetchone()
#     if col == None:
#         col = [0]
#     if ub == None:
#         cur.execute(f"SELECT date FROM users_offer WHERE id = '{send_01.from_user.id}'")
#         b = cur.fetchall()
#         date = datetime.datetime.now()
#         if b == None:
#             await callback.message.edit_text(text=f'Вы начали заполнение анкеты нового товара.\n\nВыбирете класс объявления:',
#                                              reply_markup=markup)
#         else:
#             loc = []
#             for i in b:
#                 if str(i[0]) == str(date.date()):
#                     loc.append(True)
#             if not loc:
#                 await callback.message.edit_text(text=f'Вы начали заполнение анкеты нового товара.\n\nВыбирете класс объявления:',
#                                                  reply_markup=markup)
#             else:
#                 rows_2 = [[InlineKeyboardButton(text='Использовать токен', callback_data='use_token_ub')]]
#                 markup = InlineKeyboardMarkup(inline_keyboard=rows_2)
#                 await callback.message.edit_text(f'Вы сегодня уже публиковали объявление\nУ вас {col[0]} токенов', reply_markup=markup)
#                 loc.clear()
#     else:
#         await callback.message.edit_text(text=f'Вы начали заполнение анкеты нового товара.\n\nВыбирете класс объявления:',
#                                          reply_markup=markup)
#     db.commit()
#     db.close()

@rt.callback_query(F.data == 'new') # была F.data == use_token_ub
async def use_token_ub(call: CallbackQuery, state: FSMContext):
    if send_01.from_user.username != None:
        global chek_ub
        chek_ub.clear()
        rows = [[InlineKeyboardButton(text='Под система', callback_data='pod'), InlineKeyboardButton(text='Жидкость', callback_data='zhizha')],
                [buttons[4]]]
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        chek_ub.append(True)
        await call.message.edit_text(text=f'Вы начали заполнение анкеты нового товара.\n\nВыбирете класс объявления:',
                                         reply_markup=markup)
    else:
        await call.message.answer('У тебя нету публичного username, из за этого пользователи не смогут перейти в твой профиль и написать тебе\n\nПерейди в настройки Telegram и создай свой публичный username')

@rt.callback_query(F.data == 'pod')
@rt.callback_query(F.data == 'zhizha')
async def new_2_1(call: CallbackQuery, state: FSMContext):
    fsm_date = call.data
    await state.update_data(group=fsm_date)
    await call.message.edit_text(text='Пришлите фото')
    await state.set_state(new_product.photo)

@rt.message(new_product.photo)
async def new_2_2(message: Message, state: FSMContext):
    kb = [[types.KeyboardButton(text="Это все, сохранить фото")]]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    try:
        if message.text == 'Это все, сохранить фото':
            await state.update_data(photo=photo)
            await state.set_state(new_product.name)
            await message.answer(text='Фото сохранены.', reply_markup=types.ReplyKeyboardRemove())
            await message.answer(text='Введите название товара:')
        else:
            photo_1 = message.photo
            photo.append(photo_1[-1].file_id)
            col = len(photo)
            if col == 5:
                await message.answer(text='Фото добавлено – 5 из 5', reply_markup=types.ReplyKeyboardRemove())
                await message.answer(text='Введите название товара:', reply_markup=types.ReplyKeyboardRemove())
                while len(photo) > 5:
                    photo.pop()
                await state.update_data(photo=photo)
                await state.set_state(new_product.name)
            elif col > 5:
                await message.answer(text='Вы отправили больше 5 фото')
            else:
                await message.answer(text=f'Фото добавлено – {col} из 5. Еще одно?', reply_markup=markup)
    except TypeError:
        await message.answer(text='Пришлите фото!')

@rt.message(new_product.name)
async def new_3(message: Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer(text='Пришлите текст!')
    else:
        await state.update_data(name=message.text)
        await state.set_state(new_product.description)
        await message.answer(text='Введите описание товара:')

@rt.message(new_product.description)
async def new_4(message: Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer(text='Пришлите текст!')
    else:
        await state.update_data(description=message.text)
        await state.set_state(new_product.price)
        await message.answer(text='Введите цену товара:')

@rt.message(new_product.price)
async def new_5(message: Message, state: FSMContext):
    if message.content_type != types.ContentType.TEXT:
        await message.answer(text='Пришлите текст!')
    else:
        await state.update_data(price=message.text)
        await state.set_state(new_product.locate)
        await message.answer(text='Укажите место встречи с покупателем:')

@rt.message(new_product.locate)
async def new_6(message: Message, state: FSMContext, bot: Bot, ):
    if message.content_type != types.ContentType.TEXT:
        await message.answer(text='Пришлите текст!')
    else:
        await state.update_data(locate=message.text)
        data = await state.get_data()
        global text, send, name_ofer, data_state
        data_state = data
        average = await average_rating(message.from_user.username)
        if data['group'] == 'zhizha':
            data['group'] = 'Жидкость'
        else:
            data['group'] = 'Эл_сигарета'
        if average[1] == 1:
            fb = 'отзыв'
        elif average[1] == 2:
            fb = 'отзыва'
        elif average[1] == 3:
            fb = 'отзыва'
        elif average[1] == 4:
            fb = 'отзыва'
        else:
            fb = 'отзывов'
        text = (f"#{data['group']}\n\n"
                f"{data['price']} ₽\n"
                f"{data['name']}\n"
                f"{data['description']}\n"
                f"{data['locate']}\n\n"
                f"@{message.from_user.username}   <a href='t.me/VBaraholka_bot/?start=2_{message.from_user.username}'>посмотреть отзовы</a>\n"
                f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
                f"({average[1]} {fb})")
        builder = MediaGroupBuilder(caption=text)
        for i in data['photo']:
            builder.add_photo(media=f'{i}', parse_mode="HTML")
        send = await message.answer_media_group(media=builder.build())
        rows = [[buttons[3]],
                [buttons[2]]]
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer(text='⬆️ Вот так будет выглядить ваше объяевление', reply_markup=markup)
        await state.clear()

@rt.callback_query(F.data == 'good')
async def send_0(callback: CallbackQuery, bot: Bot):
    global send_01, send_02, chek_ub

    db = sqlite3.connect('users.db')
    cur = db.cursor()
    try:
        if chek_ub[0] == True:
            cur.execute(f"SELECT col FROM unblock_col WHERE id = '{callback.from_user.id}'")
            col = cur.fetchone()
            cur.execute(f"UPDATE unblock_col SET col = {int(col[0] - 1)} WHERE id = '{callback.from_user.id}'")
    except:
        pass

    col = len(photo)
    if col > 1:
        media = [
            types.InputMediaPhoto(media=photo[0], caption=text, parse_mode="HTML"),
            *[types.InputMediaPhoto(media=photo_id) for photo_id in photo[1:]]
        ]
    else:
        media = [types.InputMediaPhoto(media=photo[0], caption=text, parse_mode="HTML")]

    send_02 = await bot.send_media_group(chat_id=CHANNEL_ID, media=media)
    await bot.edit_message_caption(chat_id=CHANNEL_ID, message_id=send_02[0].message_id, caption=text + f'\n\nID: {send_02[0].message_id}', parse_mode="HTML")

    a = ''
    for i in data_state['photo']:
        a = a+'|'+i

    date = datetime.datetime.now()
    cur.execute(
        f"""INSERT INTO users_offer VALUES ('{send_01.chat.id}', '{send_02[0].message_id}', '{a}', '{data_state['name']}', '{data_state['description']}', '{data_state['price']}', '{data_state['locate']}', '{data_state['group']}', '{send_01.from_user.username}', '{date.date()}')""")
    db.commit()
    db.close()

    a = await callback.message.edit_text(
        text='Теперь твое объявление опубликованно <a href="https://web.telegram.org/a/#-1002160209777">здесь</a>.',
        parse_mode='HTML')
    await start_def(callback.message)
    await asyncio.sleep(5)
    await a.delete()
    photo.clear()

async def offer_def(msg, from_var):
    global id_list, id_list_dispatch, id_list_auto

    deff = but_del(msg, from_var)
    if from_var == 'menu':
        for i in deff[1].keys():
            id_list.append(f'{i[0]}_menu')

    if from_var == 'dispatch':
        for i in deff[1].keys():
            id_list_dispatch.append(f'{i[0]}_dispatch')

    if from_var == 'auto':
        for i in deff[1].keys():
            id_list_auto.append(f'{i[0]}_auto')
    row = deff[0]
    return row

@rt.callback_query(F.data == 'account')
async def account(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='Ваши отзывы', callback_data='stat'), buttons[7]],
            [InlineKeyboardButton(text='Реферальная система', callback_data='ref')],
            [buttons[4]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE id = '{send_01.chat.id}'")
    date = cur.fetchall()
    cur.execute(f"SElECT balance FROM users WHERE id = '{send_01.chat.id}'")
    balance = cur.fetchone()
    db.commit()
    db.close()
    col = len(date)
    average = await average_rating(send_01.from_user.username)
    await call.message.edit_text(text=
                                f'👤 <b>Личный кабинет</b>\n\n'
                                f'💰 <b>Баланс: </b>{balance[0]} ₽\n\n'
                                f'📣 <b>Количество объявлений: </b>{col}\n\n'
                                f'🏆 <b>Рейтинг:  </b>{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))} ({average[1]})'
                                 , reply_markup=markup, parse_mode='HTML')

@rt.callback_query(F.data == 'stat')
async def account(call: CallbackQuery):
    await account_fb(call, send_01)

@rt.callback_query(F.data == 'my_off')
async def delete_0(call: CallbackQuery):
    rows = await offer_def(call.message, 'menu')
    rows_2 = [[buttons[0]],
              [InlineKeyboardButton(text='‹ Назад', callback_data='account')]]
    if len(rows) == 1:
        markup = InlineKeyboardMarkup(inline_keyboard=rows_2)
        await call.message.edit_text(text='У вас нет активных объявлений(\n\nХотите создать новое объявление?', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=rows)
        await call.message.edit_text(text='⬇️ <b>Это ваши объявления</b>\n\n'
                                          'Здесь можно <i><b>удалить</b></i> или <i><b>отредактировать</b></i> ваше объявление', reply_markup=markup, parse_mode='html')

async def forward(message, offer_data):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{offer_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    a = name[0][2]
    a = a.split('|')
    a.pop(0)
    average = await average_rating(name[0][8])
    if average[1] == 1:
        fb = 'отзыв'
    elif average[1] == 2:
        fb = 'отзыва'
    elif average[1] == 3:
        fb = 'отзыва'
    elif average[1] == 4:
        fb = 'отзыва'
    else:
        fb = 'отзывов'
    text = (f"#{name[0][7]}\n\n"
            f"{name[0][5]} ₽\n"
            f"{name[0][3]}\n"
            f"{name[0][4]}\n"
            f"{name[0][6]}\n\n"
            f"@{name[0][8]}\n"
            f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
            f"({average[1]} {fb})\n\n"
            f"ID: {name[0][1]}")
    builder = MediaGroupBuilder(caption=text)
    for i in a:
        builder.add_photo(media=f'{i}')
    id_msg = await message.answer_media_group(media=builder.build())
    return id_msg

async def del_media(bot, id_offer):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT photo FROM users_offer WHERE offer_id_channel = '{id_offer}'")
    photo_ = cur.fetchone()
    db.commit()
    db.close()
    photo_ = photo_[0]
    photo_ = photo_.split('|')
    photo_.pop(0)
    col = len(photo_)
    for i in range(col):
        ii = int(id_offer) + col - 1
        ii = ii - i
        await bot.delete_message(chat_id=CHANNEL_ID, message_id=ii)

@rt.callback_query(lambda query: query.data in id_list)
async def delete_1(call: CallbackQuery, bot: Bot):
    global call_data, call_inf, id_msg_2, id_list
    await call.message.delete()
    id_list.clear()
    call_data = call.data
    call_data = call_data.replace('_menu', '')
    call_inf = call
    id_msg_2 = await forward(call.message, call_data)
    rows = [[edit_but[0], edit_but[1]],
            [edit_but[2]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.answer(text='⬆️ Это ваше объявление\n\nЧто хотите сделать?', reply_markup=markup)

@rt.callback_query(F.data == 'back_2')
async def back_edit(call: CallbackQuery, bot: Bot):
    await delete_0(call)

@rt.callback_query(F.data == 'sell')
async def del_1(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='Да', callback_data='yes'), InlineKeyboardButton(text='Нет', callback_data='no')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='Вы уверены что хотите удалить объявление', reply_markup=markup)

@rt.callback_query(F.data == 'dell')
async def del_1(call: CallbackQuery):
    rows = [[InlineKeyboardButton(text='Да', callback_data='del_yes'), InlineKeyboardButton(text='Нет', callback_data='del_no')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='Вы уверены что хотите удалить объявление', reply_markup=markup)

@rt.callback_query(F.data == 'del_yes')
async def back_edit(call: CallbackQuery, bot: Bot):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    data = cur.fetchall()
    cur.execute(f"SELECT photo FROM users_offer WHERE offer_id_channel = '{call_data}'")
    photo_ = cur.fetchone()
    cur.execute(f"DELETE from users_offer WHERE offer_id_channel = {call_data}")
    cur.execute(f"DELETE from auto_posting WHERE offer_id_channel = {call_data}")
    db.commit()
    db.close()
    photo_ = photo_[0]
    photo_ = photo_.split('|')
    photo_.pop(0)
    col = len(photo_)
    try:
        for i in range(col):
            ii = int(call_data) + col-1
            ii = ii - i
            await bot.delete_message(chat_id=CHANNEL_ID, message_id=ii)
    except:
        average = await average_rating(data[0][8])
        if average[1] == 1:
            fb = 'отзыв'
        elif average[1] == 2:
            fb = 'отзыва'
        elif average[1] == 3:
            fb = 'отзыва'
        elif average[1] == 4:
            fb = 'отзыва'
        else:
            fb = 'отзывов'
        text = (f"#{data[0][7]}\n\n"
                f"{data[0][5]} ₽\n"
                f"УДАЛЕННО{data[0][3]}УДАЛЕННО\n"
                f"{data[0][4]}\n"
                f"{data[0][6]}\n\n"
                f"@{data[0][8]}\n"
                f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
                f"({average[1]} {fb})\n\n"
                f"ID: {data[0][1]}")
        await bot.edit_message_caption(chat_id=CHANNEL_ID, message_id=call_data, caption=text)

    msg_del = await call.message.edit_text(text='🗑️ Объявление удалено')
    await start_def(call.message)
    await asyncio.sleep(3)
    await msg_del.delete()

@rt.callback_query(F.data == 'del_no')
async def back_edit(call: CallbackQuery):
    rows = [[edit_but[0], edit_but[1]],
            [edit_but[2]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='⬆️ Это ваше объявление\n\nЧто хотите сделать?', reply_markup=markup)

@rt.callback_query(F.data == 'edit')
async def edit_0(call: CallbackQuery):
    rows = [[buttons_edit[0]],
            [buttons_edit[1]],
            [buttons_edit[2]],
            [buttons_edit[3]],
            [buttons_edit[4]],
            [buttons_edit[5]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await call.message.edit_text(text='Выберите что хотите изменить', reply_markup=markup)

class edit_product(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()
    locate = State()

async def edit_def(a, b, c):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"Update users_offer set {a} = '{b}' where offer_id_channel = '{c}'")
    db.commit()
    db.close()

async def edit_media(message: Message, photo):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    a = photo.split('|')
    a.pop(0)
    average = await average_rating(name[0][8])
    if average[1] == 1:
        fb = 'отзыв'
    elif average[1] == 2:
        fb = 'отзыва'
    elif average[1] == 3:
        fb = 'отзыва'
    elif average[1] == 4:
        fb = 'отзыва'
    else:
        fb = 'отзывов'
    text = (f"#{name[0][7]}\n\n"
            f"{name[0][5]} ₽\n"
            f"{name[0][3]}\n"
            f"{name[0][4]}\n"
            f"{name[0][6]}\n\n"
            f"@{name[0][8]}\n"
            f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
            f"({average[1]} {fb})")
    builder = MediaGroupBuilder(caption=text)
    for i in a:
        builder.add_photo(media=f'{i}')
    b = await message.answer_media_group(media=builder.build())
    return a, b

@rt.callback_query(F.data == 'photo')
async def edit_photo(call: CallbackQuery, state: FSMContext, bot: Bot):
    global col_photos
    photo.clear()
    rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='edit')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT photo FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    col_photos = name[0][0].split('|')
    col_photos.pop(0)
    col_photos = len(col_photos)
    db.commit()
    db.close()

    await call.message.edit_text(text=f'Пришлите до {col_photos} новых фото:', reply_markup=markup)
    await state.set_state(edit_product.photo)

async def search(a):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    data = cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{a}'")
    db.commit()
    db.close()
    return data

@rt.message(edit_product.photo)
async def edit_photo_2(message: Message, state: FSMContext, bot: Bot):
    global send_media_msg, gl_data
    kb = [[types.KeyboardButton(text="Это все, сохранить фото")]]
    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    but = [[types.InlineKeyboardButton(text="Внести изменения", callback_data='edit_yes_text')],
           [types.InlineKeyboardButton(text="Заполнить заново", callback_data='photo')]]
    markup_2 = InlineKeyboardMarkup(inline_keyboard=but)
    try:
        if message.text == 'Это все, сохранить фото':
            await state.update_data(photo=photo)
            data = await state.get_data()
            gl_data = data
            a = ''
            for i in data['photo']:
                a = a + '|' + i
            await edit_def('photo', a, call_data)
            send_media_msg = await edit_media(message, a)
            await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
            await state.clear()
        else:
            photo_1 = message.photo
            photo.append(photo_1[-1].file_id)
            col = len(photo)
            if col == col_photos:
                await message.answer(text=f'Фото добавлено – {col_photos} из {col_photos}',
                                     reply_markup=types.ReplyKeyboardRemove())
                while len(photo) > col_photos:
                    photo.pop()
                await state.update_data(photo=photo)
                data = await state.get_data()
                gl_data = data
                edit_photo_list = ''
                for i in data['photo']:
                    edit_photo_list = edit_photo_list + '|' + i
                send_media_msg = await edit_media(message, edit_photo_list)
                await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
                await state.clear()
            elif col > col_photos:
                await message.answer(text=f'Вы отправили больше {col_photos} фото')
            else:
                await message.answer(text=f'Фото добавлено – {col} из {col_photos}. Еще одно?', reply_markup=markup)
    except TypeError:
        await message.answer(text='Пришлите фото!')

@rt.callback_query(F.data == 'edit_yes')
async def edit_photo_2(call: CallbackQuery, bot: Bot):
    edit_photo_list = ''
    for i in gl_data['photo']:
        edit_photo_list = edit_photo_list + '|' + i
    # await edit_def('photo', edit_photo_list, call_data)
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"Update users_offer set {'photo'} = '{edit_photo_list}' where offer_id_channel = '{call_data}'")
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    average = await average_rating(name[0][8])
    if average[1] == 1:
        fb = 'отзыв'
    elif average[1] == 2:
        fb = 'отзыва'
    elif average[1] == 3:
        fb = 'отзыва'
    elif average[1] == 4:
        fb = 'отзыва'
    else:
        fb = 'отзывов'
    text = (f"#{name[0][7]}\n\n"
            f"{name[0][5]} ₽\n"
            f"{name[0][3]}\n"
            f"{name[0][4]}\n"
            f"{name[0][6]}\n\n"
            f"@{name[0][8]}\n"
            f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
            f"({average[1]} {fb})")
    a = name[0][2]
    a = a.split('|')
    a.pop(0)
    iii = 0
    for photos in a:
        ii = int(call_data) + iii
        iii = iii + 1
        try:
            if ii == int(call_data):
                await bot.edit_message_media(media=InputMediaPhoto(media=photos, caption=text), chat_id=CHANNEL_ID, message_id=ii)
            else:
                await bot.edit_message_media(media=InputMediaPhoto(media=photos), chat_id=CHANNEL_ID, message_id=ii)
        except:
            # await call.message.answer(text='Вы пытветесь изменить фото на такое же!\nИзменения не были внесены!')
            pass
    del iii
    if len(a) < col_photos:
        for i in range(col_photos - len(a)):
            col = int(call_data) + int(col_photos) - 1 - i
            await bot.delete_message(chat_id=CHANNEL_ID, message_id=col)

    a = await call.message.edit_text(text='✏️ Объявление изменено')
    await start_def(call.message)
    await asyncio.sleep(5)
    await a.delete()
    photo.clear()

@rt.callback_query(F.data == 'edit_yes_text')
async def edit_photo_2(call: CallbackQuery, bot: Bot):
    rows = [[buttons[0], buttons[1]]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    average = await average_rating(name[0][8])
    if average[1] == 1:
        fb = 'отзыв'
    elif average[1] == 2:
        fb = 'отзыва'
    elif average[1] == 3:
        fb = 'отзыва'
    elif average[1] == 4:
        fb = 'отзыва'
    else:
        fb = 'отзывов'
    text = (f"#{name[0][7]}\n\n"
            f"{name[0][5]} ₽\n"
            f"{name[0][3]}\n"
            f"{name[0][4]}\n"
            f"{name[0][6]}\n\n"
            f"@{name[0][8]}\n"
            f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
            f"({average[1]} {fb})")
    await bot.edit_message_caption(chat_id=CHANNEL_ID, message_id=call_data, caption=text)
    a = await call.message.edit_text(text='✏️ Объявление изменено')
    await start_def(call.message)
    await asyncio.sleep(3)
    await a.delete()

async def send_media(message):

    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"SELECT * FROM users_offer WHERE offer_id_channel = '{call_data}'")
    name = cur.fetchall()
    db.commit()
    db.close()
    name = name[0]
    a = name[2]
    a = a.split('|')
    a.pop(0)
    average = await average_rating(name[8])
    if average[1] == 1:
        fb = 'отзыв'
    elif average[1] == 2:
        fb = 'отзыва'
    elif average[1] == 3:
        fb = 'отзыва'
    elif average[1] == 4:
        fb = 'отзыва'
    else:
        fb = 'отзывов'
    text = (f"#{name[7]}\n\n"
            f"{name[5]} ₽\n"
            f"{name[3]}\n"
            f"{name[4]}\n"
            f"{name[6]}\n\n"
            f"@{name[8]}\n"
            f"{average[0]} {'⭐' * round(average[0])}{' ☆' * (5 - round(average[0]))}\n"
            f"({average[1]} {fb})")

    builder = MediaGroupBuilder(caption=text)
    for i in a:
        builder.add_photo(media=f'{i}')
    await message.answer_media_group(media=builder.build())

@rt.callback_query(F.data == 'name')
async def edit_name(call: CallbackQuery, state: FSMContext):
    rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='edit')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await call.message.edit_text(text=f'Введите новое название товара:',
                                 reply_markup=markup)
    await state.set_state(edit_product.name)

@rt.callback_query(F.data == 'description')
async def edit_description(call: CallbackQuery, state: FSMContext):
    rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='edit')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await call.message.edit_text(text=f'Введите новое описание товара:',
                                 reply_markup=markup)
    await state.set_state(edit_product.description)

@rt.callback_query(F.data == 'price')
async def edit_price(call: CallbackQuery, state: FSMContext):
    rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='edit')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await call.message.edit_text(text=f'Введите новую цену товара:',
                                 reply_markup=markup)
    await state.set_state(edit_product.price)

@rt.callback_query(F.data == 'locate')
async def edit_locate(call: CallbackQuery, state: FSMContext):
    rows = [[InlineKeyboardButton(text='‹ Назад', callback_data='edit')]]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)

    await call.message.edit_text(text=f'Введите новое место встречи с покупателем:',
                                 reply_markup=markup)
    await state.set_state(edit_product.locate)

@rt.message(edit_product.name)
async def edit_photo_2(message: Message, state: FSMContext, bot: Bot):
    but = [[types.InlineKeyboardButton(text="Внести изменения", callback_data='edit_yes_text')],
           [types.InlineKeyboardButton(text="Заполнить заново", callback_data='name')]]
    markup_2 = InlineKeyboardMarkup(inline_keyboard=but)

    await state.update_data(name=message.text)
    data = await state.get_data()

    await edit_def('offer_name', data['name'], call_data)
    await send_media(message)
    await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
    await state.clear()

@rt.message(edit_product.description)
async def edit_photo_2(message: Message, state: FSMContext, bot: Bot):
    but = [[types.InlineKeyboardButton(text="Внести изменения", callback_data='edit_yes_text')],
           [types.InlineKeyboardButton(text="Заполнить заново", callback_data='description')]]
    markup_2 = InlineKeyboardMarkup(inline_keyboard=but)

    await state.update_data(description=message.text)
    data = await state.get_data()

    await edit_def('description', data['description'], call_data)
    await send_media(message)
    await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
    await state.clear()

@rt.message(edit_product.price)
async def edit_photo_2(message: Message, state: FSMContext, bot: Bot):
    but = [[types.InlineKeyboardButton(text="Внести изменения", callback_data='edit_yes_text')],
           [types.InlineKeyboardButton(text="Заполнить заново", callback_data='price')]]
    markup_2 = InlineKeyboardMarkup(inline_keyboard=but)

    await state.update_data(price=message.text)
    data = await state.get_data()

    await edit_def('price', data['price'], call_data)
    await send_media(message)
    await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
    await state.clear()

@rt.message(edit_product.locate)
async def edit_photo_2(message: Message, state: FSMContext, bot: Bot):
    but = [[types.InlineKeyboardButton(text="Внести изменения", callback_data='edit_yes_text')],
           [types.InlineKeyboardButton(text="Заполнить заново", callback_data='locate')]]
    markup_2 = InlineKeyboardMarkup(inline_keyboard=but)

    await state.update_data(locate=message.text)
    data = await state.get_data()

    await edit_def('locate', data['locate'], call_data)
    await send_media(message)
    await message.answer(text='⬆️ Вот так теперь выглядит ваше объявление', reply_markup=markup_2)
    await state.clear()
