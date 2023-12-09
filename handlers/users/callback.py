from aiogram import types, F
from loader import router
from aiogram.fsm.context import FSMContext
from utils.misc.pyaaio import Aaio
from utils.db_api.db_file import DataBase
import data.config as config
import time
import keyboards.inline.keyboard as kb
from datetime import datetime, timedelta
from aiogram import Bot

@router.callback_query(F.data == ('cancel'))
async def cancel_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Оплата отменена!", reply_markup=kb.get_keyboard())

@router.callback_query(F.data == ('back'))
async def cancel_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Главное меню", reply_markup=kb.get_keyboard())


@router.callback_query(F.data == ('buy_access'))
async def buy_access_handler(call: types.CallbackQuery, state: FSMContext, db: DataBase, aaio: Aaio):
    status = await db.get_status(call.from_user.id)


    if status:
        await call.answer('Вы уже приобрели доступ к каналу ❤️‍🔥', show_alert=True)
        return
    await call.message.delete()
    bill_id = f'{int(time.time())}_{call.from_user.id}'
    pay_url = aaio.build_form_url(amount=config.price_access, desc=f'Пополнение баланса {call.from_user.id}', order_id=bill_id)

    await call.message.answer(f"""
💳 Метод пополнения: Aaio
💸 Сумма к оплате: <code>{config.price_access}</code> rub
🆔 ID платежа: <code>{bill_id}</code>""", reply_markup=kb.keyboard_payment(url=pay_url))
    

@router.callback_query(F.data == ('check_pay'))
async def check_pay_handler(call: types.CallbackQuery, state: FSMContext, db: DataBase, aaio: Aaio, bot: Bot):


    bill_id = (call.message.text).split('\n')[-1].split(' ')[-1]
    status_payment = await aaio.get_order(payment_id=bill_id)
    status_ = status_payment.get('status') == 'success'
    if status_:
        await call.message.delete()
        expire_date = datetime.now() + timedelta(days=1)
        link = await bot.create_chat_invite_link(chat_id=config.channel_id, expire_date=expire_date.timestamp(), member_limit=1)        
        await call.message.answer(f"<b>✅ Платёж найден, спасибо за покупку!\n🔗 Ваша одноразовая ссылка: {link.invite_link}\n❗️ Переходите быстрее! Срок действия: 1 дн</b>")
        await db.set_status(call.from_user.id)
        for i in config.ADMINS:
            try:
                await bot.send_message(i, f"Пользователь: @{call.from_user.username} ({call.from_user.id}) оплатил подписку в канал")
            except:
                pass
    else:
        await call.answer("⚠️ Платёж не найден")



@router.callback_query(F.data == ('information'))
async def information_handler(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(config.information, reply_markup=kb.back_keyboard())
