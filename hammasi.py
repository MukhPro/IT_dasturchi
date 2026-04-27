from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import db as db_logic
import keyboards as kb
from states import FinanceStates

hammasi_router = Router()

@hammasi_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Xush kelibsiz! Kerakli bo'limni tanlang:", reply_markup=kb.main_menu())

@hammasi_router.callback_query(F.data == "main_menu")
async def back_to_main(call: CallbackQuery):
    await call.message.edit_text("Asosiy menyu:", reply_markup=kb.main_menu())

@hammasi_router.callback_query(F.data == "stats")
async def show_stats_menu(call: CallbackQuery):
    await call.message.edit_text("Hisobot turini tanlang:", reply_markup=kb.stats_menu())

@hammasi_router.callback_query(F.data.in_(["add_income", "add_expense"]))
async def start_transaction(call: CallbackQuery, state: FSMContext):
    t_type = "kirim" if call.data == "add_income" else "chiqim"
    await state.update_data(t_type=t_type)
    await call.message.answer(f"💰 {t_type.capitalize()} summasini kiriting:")
    await state.set_state(FinanceStates.waiting_for_amount)

@hammasi_router.message(FinanceStates.waiting_for_amount)
async def process_amount(message: types.Message, state: FSMContext):
    if not message.text.replace('.', '', 1).isdigit():
        return await message.answer("Iltimos, faqat raqam kiriting!")
    await state.update_data(amount=float(message.text))
    await message.answer("📝 Tavsif kiriting:")
    await state.set_state(FinanceStates.waiting_for_desc)

@hammasi_router.message(FinanceStates.waiting_for_desc)
async def process_desc(message: types.Message, state: FSMContext):
    data = await state.get_data()
    t_type, amount = data['t_type'], data['amount']
    
    time_now = await db_logic.add_transaction(message.from_user.id, t_type, amount, message.text)

    await message.answer(
        f"✅ Saqlandi!\n\n💰 Summa: {amount}\n📝 Tavsif: {message.text}\n⏰ Vaqt: {time_now}", 
        reply_markup=kb.main_menu()
    )
    await state.clear()

@hammasi_router.callback_query(F.data.startswith("report_"))
async def show_report(call: CallbackQuery):
    t_type = "kirim" if "income" in call.data else "chiqim"
    rows = await db_logic.get_report(call.from_user.id, t_type)

    if not rows:
        return await call.answer("Ma'lumot topilmadi.", show_alert=True)

    await call.message.answer(f"📋 {t_type.capitalize()}lar ro'yxati:")
    total = 0
    for row in rows:
        total += row[1]
        text = f"🆔 ID: {row[0]}\n💰 {row[1]} | 📝 {row[2]}\n⏰ {row[3]}"
        await call.message.answer(text, reply_markup=kb.delete_kb(row[0]))

    await call.message.answer(f"🧮 Jami: {total}", reply_markup=kb.clear_kb(t_type))

@hammasi_router.callback_query(F.data.startswith("delete_"))
async def delete_item(call: CallbackQuery):
    item_id = call.data.split("_")[1]
    await db_logic.delete_transaction(item_id)
    await call.message.delete()
    await call.answer("O'chirildi")

@hammasi_router.callback_query(F.data.startswith("clear_"))
async def clear_history(call: CallbackQuery):
    t_type = call.data.split("_")[1]
    await db_logic.clear_user_history(call.from_user.id, t_type)
    await call.message.answer(f"🧹 Barcha {t_type}lar tarixi tozalandi!", reply_markup=kb.main_menu())