from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="🔎 Поиск клиник", callback_data="find_clinic"),
    InlineKeyboardButton(text="📍 Местоположение", callback_data="place")],
    [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
]

menu2 = [
    [InlineKeyboardButton(text="Название клиники", callback_data="clinic_name"),
    InlineKeyboardButton(text="Отзывы", callback_data="clinic_reviews")],
    [InlineKeyboardButton(text="Контакты", callback_data="clinic_contacts")]
]

yes_no = [
    [InlineKeyboardButton(text="Да", callback_data="yes"),
    InlineKeyboardButton(text="Нет", callback_data="no")]
]

exit_kb = [
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="exit")]
]

edit = [
    [InlineKeyboardButton(text="Изменить", callback_data="edit")],
    [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="exit")]
]

back_clinic = [
    [InlineKeyboardButton(text="◀️ К списку клиник", callback_data="find_clinic")]
]

back_clinic = InlineKeyboardMarkup(inline_keyboard=back_clinic)
edit = InlineKeyboardMarkup(inline_keyboard=edit)
exit_kb = InlineKeyboardMarkup(inline_keyboard=exit_kb)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
menu2 = InlineKeyboardMarkup(inline_keyboard=menu2)
yes_no = InlineKeyboardMarkup(inline_keyboard=yes_no)