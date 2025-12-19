from aiogram import types, F, Router
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import aiohttp
import requests
import kb
import text
import config
import db

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.message(F.text == "меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

async def is_address(text: str) -> bool:
    address_keywords = ["улица", "проспект", "площадь", "переулок", "шоссе", "аллея", "россия"]
    for keyword in address_keywords:
        if keyword in text:
            return True
    return False

@router.message()
async def input_message(msg: types.Message):
    if msg.text:
        text_input = msg.text.strip().lower()
        if await is_address(text_input):
            await handle_location(msg)
        else:
            await msg.answer(text.answer)
    else:
        await handle_location(msg)

@router.callback_query(F.data == "help")
async def help_handler(clbck: CallbackQuery):
    await clbck.message.answer(text.help, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "find_clinic")
async def finds_handler(clbck: CallbackQuery):
    user_id = clbck.from_user.id
    user_address = db.get_addresses(user_id)
    if user_address:
        latitude, longitude = await reverse_geocoder(user_address)
        nearby_clinics = await find_nearby_clinics(latitude, longitude)

        if nearby_clinics:
            clinic_buttons = [
                [InlineKeyboardButton(text=f"{i + 1}", callback_data=f"info_{i + 1}") for i in range(min(len(nearby_clinics), 5))]
            ]
            clinic_buttons_markup = InlineKeyboardMarkup(inline_keyboard=clinic_buttons + [[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="exit")]])

            clinic_list = "\n".join([f"{i + 1}. {clinic['properties']['name']}: {clinic['properties']['description']}" for i, clinic in enumerate(nearby_clinics[:5])])
            await clbck.message.answer(f"Вот список ближайших клиник:\n{clinic_list}", reply_markup=clinic_buttons_markup)
        else:
            await clbck.message.answer(text.no_clinic)
    else:
        await clbck.message.answer(text.no_address)

@router.callback_query(F.data.startswith("info_"))
async def info_clinic(clbck: CallbackQuery):
    button_number = clbck.data.split("_")[-1]  # Получаем номер кнопки из callback_data
    user_id = clbck.from_user.id
    user_address = db.get_addresses(user_id)
    if user_address:
        latitude, longitude = await reverse_geocoder(user_address)  # Получить координаты пользователя
        nearby_clinics = await find_nearby_clinics(latitude, longitude)

        if nearby_clinics:
            if button_number.isdigit() and int(button_number) <= len(nearby_clinics):
                clinic_info = nearby_clinics[int(button_number) - 1]  # Получить информацию о выбранной клинике
                clinic_name = clinic_info['properties']['name']
                clinic_phone = clinic_info['properties'].get('CompanyMetaData', {}).get('Phones', [])[0]['formatted']
                clinic_hours_info = clinic_info['properties'].get('CompanyMetaData', {}).get('Hours', {})
                clinic_hours_text = clinic_hours_info.get('text', 'Не указано')
                clinic_address = clinic_info['properties'].get('description', 'Адрес не указан')
                clinic_website = clinic_info['properties'].get('CompanyMetaData', {}).get('url', 'Сайт не указан')

                message_text = f"Название клиники: {clinic_name}\nАдрес: {clinic_address}\nНомер телефона: {clinic_phone}\nГрафик работы: {clinic_hours_text}\nСайт: {clinic_website}"
                await clbck.message.answer(message_text, reply_markup=kb.back_clinic)

@router.callback_query(F.data == "yes")
async def answer_yes(clbck: CallbackQuery):
    await clbck.message.answer(text.yes, reply_markup=kb.exit_kb)
    await clbck.message.delete()

@router.callback_query(F.data == "no")
async def answer_no(clbck: CallbackQuery):
    await clbck.message.answer(text.no)
    await clbck.message.delete()

@router.callback_query(F.data == "edit")
async def answer_no(clbck: CallbackQuery):
    await clbck.message.answer(text.no)
    await clbck.message.delete()
    
@router.callback_query(F.data == "exit")
async def answer_no(clbck:CallbackQuery):
    await clbck.message.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "place")
async def place_callback_handler(clbck: CallbackQuery):
    user_id = clbck.from_user.id
    address = db.get_addresses(user_id)
    if address:
        await clbck.bot.send_message(user_id, f"Ваше сохраненное местоположение: {address}",reply_markup=kb.edit)
    else:
        await clbck.bot.send_message(user_id, text="Пожалуйста, отправьте свою геопозицию",
                                     reply_markup=types.ReplyKeyboardMarkup(keyboard=
                                     [[types.KeyboardButton(text="📍 Отправить местоположение",
                                     request_location=True)]]
                                     ))

@router.message()
async def handle_location(msg: types.Message):
    if msg.content_type == types.ContentType.LOCATION:
        latitude = msg.location.latitude
        longitude = msg.location.longitude
        print(f"Получено местоположение: Широта - {latitude}, Долгота - {longitude}")

        address = await geocoder(latitude, longitude)

        user_id = msg.from_user.id
        db.add_address(user_id, address)
        await msg.answer(f"Ваше местоположение - {address}?", reply_markup=kb.yes_no)
    elif msg.content_type == types.ContentType.TEXT:
        user_id = msg.from_user.id
        manual_address = msg.text
        coordinates = await reverse_geocoder(manual_address)
        print("Координаты:", coordinates)
        if coordinates and len(manual_address.split(',')) == 4:
            latitude, longitude = coordinates
            print(f"Получено местоположение: Широта - {latitude}, Долгота - {longitude}")
            db.update_address(user_id, manual_address)
            await msg.answer(text.correct_address, reply_markup=kb.exit_kb)
        else:
            await msg.answer(text.uncorrect_address)

async def geocoder(latitude, longitude):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": config.GEOCODER,
        "geocode": f"{longitude},{latitude}",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        address = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["text"]
        return address
    except (IndexError, KeyError):
        return "Адрес не найден"

async def reverse_geocoder(address):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": config.GEOCODER,
        "geocode": address,
        "format": "json"
    }
    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    try:
        coordinates = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        longitude, latitude = map(float, coordinates.split())
        return latitude, longitude
    except (IndexError, KeyError):
        return "Адрес не найден"
    
async def find_nearby_clinics(latitude, longitude):
    url = "https://search-maps.yandex.ru/v1/"
    params = {
        "apikey": config.ORGANIZATION,
        "text": "Стоматология",
        "lang": "ru_RU",
        "type": "biz",
        "ll": f"{longitude},{latitude}",
        "spn": "0.02,0.02",  # Радиус поиска
        "rspn": 1,  # Учитывать радиус поиска
        "results": 500  # Количество результатов поиска
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            clinics = data.get("features", [])
            print("Количество найденных клиник:", len(clinics))
            #for clinic in clinics:
                #print(clinic)
            return clinics