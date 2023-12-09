import asyncio
from utils.set_bot_commands import set_default_commands
import logging
import handlers
import data
import data.config as config
from utils.db_api.db_file import DataBase
from aiogram import Bot, Dispatcher
from loader import router
from utils.misc.pyaaio import Aaio

async def on_startup():
    db = DataBase(config.session_url)
    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher()

    aaio = Aaio(secret_key=config.secret_key, merchant_id=config.merchant_id, api_key=config.api_key)
    await db.check_start()
    await bot.delete_webhook(drop_pending_updates=True)
    await set_default_commands(bot)
    dp.include_router(router=router)
    await dp.start_polling(bot, db=db, aaio=aaio)


    


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(on_startup())
    except Exception as err:
        logging.exception(err)





