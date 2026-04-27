import asyncio
import logging
from config import bot, dp
from hammasi import hammasi_router

import db as db_logic


dp.include_router(hammasi_router)

async def main():
    await db_logic.init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())