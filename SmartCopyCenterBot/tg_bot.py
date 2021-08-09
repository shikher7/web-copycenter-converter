from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import reques_city, locat, text_from_user, print_settings, feedback
from aiogram.dispatcher.storage import FSMContext
from keyboards import city_select_keyboard, point_select_keyboard, list_buttoncreate_keyboard, upload_select_keyboard, printparam_select_keyboard, print_set_keyboard, pay_keyboard, fdbck_menu_keyboard, menu_keyboard
from random import randint

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def user_location(message: types.Message):
    await bot.send_message(message.chat.id, "Отлично ✌\nВыбери свой город для начала работы",
                           reply_markup=city_select_keyboard())


@dp.callback_query_handler(lambda call: True)
async def callback_processing(callback_query: types.CallbackQuery, state: FSMContext):
    # обработка текстового ввода города
    if callback_query.data == 'cityselect_text_type':
        await bot.send_message(callback_query.from_user.id, "Введите город")
        await reques_city.city.set()
    # обработка города по геолокации
    elif callback_query.data == 'cityselect_location_type':
        await bot.send_message(callback_query.from_user.id, "Передайте свою геолокацию")
        await locat.reqlocation.set()
    elif callback_query.data == 'pointselect_address_type':
        await bot.send_message(callback_query.from_user.id,
                               "Напишите название улицы, на которой стоит принтер\n Например: Карла Маркса")
        await locat.street.set()
    elif callback_query.data == 'pointselect_id_type':
        # вытащить адрес по idшнику принтера
        await bot.send_message(callback_query.from_user.id, "Пока что пусто, на этом этапе работают первая и четвертая кнопка")
    elif callback_query.data == 'pointselect_favorite_type':
        # вытащить список доступных точек из списка избранных
        await bot.send_message(callback_query.from_user.id, "Пока что пусто, на этом этапе работают первая и четвертая кнопка")
    elif callback_query.data == 'pointselect_nearest_type':
        await bot.send_message(callback_query.from_user.id, "Передайте свое местоположение")
        await locat.tmp_location.set()
    elif callback_query.data == "created_streetbtb_call":
        await bot.send_message(callback_query.from_user.id, "Загрузите файл", reply_markup=upload_select_keyboard())
    elif callback_query.data == "choose_upload_type":
        await bot.send_message(callback_query.from_user.id, ("Загрузи или перешли файл, который ты желаешь распечатать\n\n"
                                                 "Поддерживаемые форматы (PDF,DOC,DOCX, XLS, XLSX, PPT, PPTX, PNG, "
                                                 "JPG, JPEG, BMP, EPS, GIF, TXT, RTF, HTML)"))
        await text_from_user.user_text.set()
        #await bot.send_message(callback_query.from_user.id, "Давай настроим параметры на печати, или сразу отправляй документ на печать", reply_markup=printparam_select_keyboard())
    # elif callback_query.data == "choose_create_type":
    #     #вопросики касательно того, как реализовать эту штуку, ибо по идее, если вставлять текст в телегу, кроме переноса строки и пробелов все остальное
    #     #форматирование проебется
    #     await bot.send_message(callback_query.from_user.id, "Напиши текст, который хочешь отправить\n"
    #                            "*Из этого текста будет создан текстовый файл для распечатки")
    #     await text_from_user.user_text.set()
    elif callback_query.data == "printparam_select_type":
        await bot.send_message(callback_query.from_user.id, "Ваш заказ:\n\n"
                                                            "Количество страниц: x\n"
                                                            "Двусторонняя печать: x\n"
                                                            "Количество копий\n"
                                                            "Интервал страницы\n\n"
                                                            "Цена - x рублей", reply_markup=pay_keyboard())
    elif callback_query.data == "printparam_set_type":
        await bot.send_message(callback_query.from_user.id, "Выберете параметры, которые вы хотите изменить\n"
                                                            "Стандартные параметры:\n"
                                                            "Количество копий: 1\n"
                                                            "Двухсторонняя печать: Нет\n"
                                                            "Отдельные страницы: Весь файл", reply_markup=print_set_keyboard())
    elif callback_query.data == "printsettings_count_type":
        await bot.send_message(callback_query.from_user.id, "Введите количеество копий")
        await print_settings.copycount.set()
    elif callback_query.data == "printsetting_doubleside_type":
        await bot.send_message(callback_query.from_user.id, "Введите 'Да' для включения двустронней печати")
        await print_settings.doubleside.set()
    elif callback_query.data == "printsetting_needpages_type":
        await bot.send_message(callback_query.from_user.id, "Введите страницы, которые вы хотете распечатать")
        await print_settings.needpages.set()
    elif callback_query.data == "printparam_select_type":
        # из бдшки подтянуть параметры все
        await bot.send_message(callback_query.from_user.id, "Ваш заказ:\n\n"
                                                            "Количество страниц: x\n"
                                                            "Двусторонняя печать: x\n"
                                                            "Количество копий\n"
                                                            "Интервал страницы\n\n"
                                                            "Цена - x рублей", reply_markup=pay_keyboard())
    elif callback_query.data == "printsetting_ready_type":
        #из бдшки подтянуть параметры все
        await bot.send_message(callback_query.from_user.id, "Ваш заказ:\n\n"
                                                            "Количество страниц: x\n"
                                                            "Двусторонняя печать: x\n"
                                                            "Количество копий\n"
                                                            "Интервал страницы\n\n"
                                                            "Цена - x рублей", reply_markup=pay_keyboard())
    elif callback_query.data == "pay_type":
        await bot.send_message(callback_query.from_user.id, "Спасибо, что воспользовались нашим сервисом!\n\n"
                                                            "Оставьте обратную связь для улучшения продукта\n"
                                                            "Какую функцию хотели бы видеть?"
                                                             "Что не понравилось", reply_markup=fdbck_menu_keyboard())
    elif callback_query.data == 'feedback_btn':
        await bot.send_message(callback_query.from_user.id, "Пожалуйста, напишите свой отзыв")
        await feedback.userfeedback.set()
    elif callback_query.data == 'menu_btn':
        await bot.send_message(callback_query.from_user.id, "Переход в основное меню", reply_markup=menu_keyboard())



@dp.message_handler(state=reques_city.city)
async def city_handler(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await state.finish()
    await bot.send_message(message.from_user.id, "Выберите принтер для печати удобным вам способом",
                           reply_markup=point_select_keyboard())


# Обработка города через геолокацию
@dp.message_handler(content_types=["location"], state=locat.reqlocation)
async def city_handler(message: types.Message, state: FSMContext):
    # далее по координатам определить город
    location = [message.location.longitude, message.location.latitude]
    await state.update_data(reqlocation=location)
    await message.answer(f"Ваши координаты {message.location.longitude, message.location.latitude}")
    await bot.send_message(message.from_user.id, "Выберите принтер для печати удобным вам способом",
                           reply_markup=point_select_keyboard())
    await state.finish()


# Выбор точки по адресу
@dp.message_handler(state=locat.street)
async def street_handler(message: types.Message, state: FSMContext):
    street = message.text
    snd_list = [street + ',' + str(randint(1, 100)), street + ',' + str(randint(1, 100))]
    await message.answer(f"Локации находяшиеся по этой улице:", reply_markup=list_buttoncreate_keyboard(snd_list))
    await state.finish()


# Выбор точки по геолокации
@dp.message_handler(content_types=["location"], state=locat.tmp_location)
async def street_handler(message: types.Message, state: FSMContext):
    tmp_locat = [message.location.longitude, message.location.latitude]
    await state.update_data(tmp_location=tmp_locat)
    await message.answer(
        f"Ваши координаты {message.location.longitude, message.location.latitude}, рядом с вами имеются следующие точки\n"
        f"Карла Маркса 68 – Казанский национальный универ\n"
        f"Толстого 5 - Кафе к чаю\n"
        f"Вахитова 6 – Отделение МТС")
    await state.finish()


@dp.message_handler(state=text_from_user.user_text)
async def user_test_handler(message: types.Message, state: FSMContext):
    print(bot.forward_message(message.chat.id, from_chat_id=message.forward_from_chat.id, message_id=message.migrate_from_chat_id))
    usr_text = message.text
    await state.update_data(user_text=usr_text)
    await state.finish()
    await bot.send_message(message.from_user.id, "Давай настроим параметры на печати, или сразу отправляй документ на печать", reply_markup=printparam_select_keyboard())


@dp.message_handler(state=print_settings.copycount)
async def user_test_handler(message: types.Message, state: FSMContext):
    copycount = message.text
    await state.update_data(copycount=copycount)
    await state.finish()
    await bot.send_message(message.from_user.id, "Выбери другие параметры для изменения или 'Готово', если установил все необходимые параметры", reply_markup=print_set_keyboard())


@dp.message_handler(state=print_settings.doubleside)
async def user_test_handler(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(doubleside=answer)
    data = await state.get_data()
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "Выбери другие параметры для изменения или 'Готово', если установил все необходимые параметры",
                           reply_markup=print_set_keyboard())


@dp.message_handler(state=print_settings.needpages)
async def user_test_handler(message: types.Message, state: FSMContext):
    needpages = [message.text]
    await state.update_data(needpages=needpages)
    await state.finish()
    await bot.send_message(message.from_user.id,
                           "Выбери другие параметры для изменения или 'Готово', если установил все необходимые параметры",
                           reply_markup=print_set_keyboard())


@dp.message_handler(state=feedback.userfeedback)
async def user_test_handler(message: types.Message, state: FSMContext):
    fdbck = message.text
    await state.update_data(feedback=fdbck)
    await state.finish()
    await bot.send_message(message.from_user.id, "Большое спасибо за отзыв!")
    await bot.send_message(message.from_user.id, "меню", reply_markup=menu_keyboard())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
