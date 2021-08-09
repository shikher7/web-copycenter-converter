from aiogram.dispatcher.filters.state import StatesGroup, State


class reques_city(StatesGroup):
    city = State()


class locat(StatesGroup):
    reqlocation = State()
    street = State()
    tmp_location = State()


class text_from_user(StatesGroup):
    user_text = State()


class print_settings(StatesGroup):
    copycount = State()
    doubleside = State()
    needpages = State()


class feedback(StatesGroup):
    userfeedback = State()