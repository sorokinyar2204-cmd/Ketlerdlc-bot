import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Здравствуйте!\n\n"
        "Опишите вашу проблему или вопрос одним сообщением. "
        "Ваша заявка будет рассмотрена в течение дня."
    )

@dp.message()
async def handle_support_message(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        return
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return
    try:
        await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
        await message.answer("✅ Ваша заявка принята!\nМы рассмотрим её в течение дня.")
    except Exception as e:
        await message.answer("⚠️ Ошибка. Попробуйте позже.")
        logging.error(e)

async def main():
    print("Бот запущен на сервере!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
