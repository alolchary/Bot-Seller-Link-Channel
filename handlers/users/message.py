from aiogram import types, F
from loader import router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import keyboards.inline.keyboard as kb
from utils.db_api.db_file import DataBase



@router.message(Command('start'))
async def start_handler(message: types.Message, state: FSMContext, db: DataBase):
    
    await state.clear()
    await db.add_user(message.from_user.id)






    status = await db.get_status(message.from_user.id)
    if not status:
        await message.answer(f'Приветствую тебя, <code>{message.from_user.first_name}</code>', reply_markup=kb.get_keyboard())
        return

    

    await message.answer(f"Вы уже приобрели доступ к каналу ❤️‍🔥")


    
