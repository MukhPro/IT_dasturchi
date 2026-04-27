from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kirim", callback_data="add_income"),
         InlineKeyboardButton(text="➖ Chiqim", callback_data="add_expense")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="stats")]
    ])

def stats_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Kirim hisoboti", callback_data="report_income")],
        [InlineKeyboardButton(text="📉 Chiqim hisoboti", callback_data="report_expense")],
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="main_menu")]
    ])

def delete_kb(item_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delete_{item_id}")]
    ])

def clear_kb(t_type):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧹 Tarixni tozalash", callback_data=f"clear_{t_type}")]
    ])