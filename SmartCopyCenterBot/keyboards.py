from aiogram import Bot, Dispatcher, executor, types


def city_select_keyboard():
    loc_select_kb = types.InlineKeyboardMarkup()
    text_type = types.InlineKeyboardButton("Написать город текстом", callback_data='cityselect_text_type')
    location_type = types.InlineKeyboardButton("Передать местоположение", callback_data='cityselect_location_type')
    loc_select_kb.add(text_type, location_type)
    return loc_select_kb


def point_select_keyboard():
    point_select_kb = types.InlineKeyboardMarkup()
    point_address = types.InlineKeyboardButton("По адресу", callback_data='pointselect_address_type')
    point_id = types.InlineKeyboardButton("По ID принтера", callback_data='pointselect_id_type')
    point_favorite = types.InlineKeyboardButton("Из списка избранных", callback_data='pointselect_favorite_type')
    point_nearest = types.InlineKeyboardButton("Ближашие точки к вашему местоположению",
                                               callback_data='pointselect_nearest_type')
    point_select_kb.add(point_address, point_id, point_favorite, point_nearest)
    return point_select_kb


def add_favorite_keyboard():
    add_fav_kb = types.InlineKeyboardMarkup()
    add_fav_yes = types.InlineKeyboardButton("Да", callback_data='add_fav_yes')
    add_fav_no = types.InlineKeyboardButton("Нет", callback_data='add_fav_no')
    add_fav_kb.add(add_fav_yes, add_fav_no)
    return add_fav_kb


def list_buttoncreate_keyboard(streetlist):
    button_create_keyboard = types.InlineKeyboardMarkup()
    button_create_buttons = [types.InlineKeyboardButton(text=x, callback_data="created_streetbtb_call") for x in streetlist]
    button_create_keyboard.add(*button_create_buttons)
    return button_create_keyboard


def upload_select_keyboard():
    upload_select_kb = types.InlineKeyboardMarkup()
    choose_upload_btn = types.InlineKeyboardButton("Загрузить файл", callback_data="choose_upload_type")
    #choose_create_btn = types.InlineKeyboardButton("Создать текстовый файл", callback_data="choose_create_type")
    upload_select_kb.add(choose_upload_btn)
    return upload_select_kb


def printparam_select_keyboard():
    param_select_kb = types.InlineKeyboardMarkup()
    param_select_print_btn = types.InlineKeyboardButton("Напечатать", callback_data="printparam_select_type")
    param_select_setparam_btn = types.InlineKeyboardButton("Проставить параметры печати", callback_data="printparam_set_type")
    param_select_kb.add(param_select_print_btn, param_select_setparam_btn)
    return param_select_kb


def print_set_keyboard():
    print_settings_kb = types.InlineKeyboardMarkup(resize_keyboard=True)
    print_settings_copycount = types.InlineKeyboardButton("Количество копий", callback_data="printsettings_count_type")
    print_settings_doubleside = types.InlineKeyboardButton("Двухстронняя печать", callback_data="printsetting_doubleside_type")
    print_settings_needpages = types.InlineKeyboardButton("Выбор отдельных страниц", callback_data="printsetting_needpages_type")
    print_settings_ready = types.InlineKeyboardButton("Готово", callback_data="printsetting_ready_type")
    print_settings_kb.row(print_settings_copycount).add(print_settings_doubleside, print_settings_needpages).row(print_settings_ready)
    return print_settings_kb


def pay_keyboard():
    pay_kb = types.InlineKeyboardMarkup()
    pay_btn = types.InlineKeyboardButton("Оплатить", callback_data="pay_type")
    pay_kb.add(pay_btn)
    return pay_kb


def fdbck_menu_keyboard():
    feedback_mn_kb = types.InlineKeyboardMarkup()
    feedback_btn = types.InlineKeyboardButton("Оставить отзыв", callback_data='feedback_btn')
    menu_btn = types.InlineKeyboardButton("Перейти в меню", callback_data='menu_btn')
    feedback_mn_kb.add(feedback_btn, menu_btn)
    return feedback_mn_kb

def menu_keyboard():
    menu_kb = types.ReplyKeyboardMarkup()
    tmp_btn = types.KeyboardButton("Временная кнопка")
    menu_kb.add(tmp_btn)
    return menu_kb