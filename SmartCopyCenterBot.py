import os.path
from editor import Editor, IMAGE_DIR, DOCUMENT_DIR

import telebot

smartCopyCenterBot = telebot.TeleBot(token=os.environ.get('TOKEN'))


def get_file_info(settings):
    def get_request(get_prop):
        def wrapper(message):
            message, file_contact, root_dir, file_name = get_prop(message)
            chat_id = message.chat.id
            file_info = smartCopyCenterBot.get_file(file_contact)
            downloaded_file = smartCopyCenterBot.download_file(file_info.file_path)
            src = os.path.join(os.path.abspath(root_dir),
                               ''.join([str(message.from_user.username), '_', file_name]))
            return downloaded_file, src

        return wrapper

    return get_request


@get_file_info(settings='document')
def get_document(message):
    file_contact = message.document.file_id
    file_name = message.document.file_name
    root_dir = './input_documents'
    return message, file_contact, root_dir, file_name


@get_file_info(settings='photo')
def get_image(message):
    file_contact = message.photo[len(message.photo) - 2].file_id
    file_name = smartCopyCenterBot.get_file(file_contact).file_path.split('/')[-1]
    root_dir = './input_images'
    return message, file_contact, root_dir, file_name


class BotHandler:
    __commands_list = {
        '/start': f'Добро пожаловать в сервис удаленной печати.'
                  f'Здесь вы можете отправить файл нашему умному '
                  f'боту, который конвертирует ваш файл в PDF и '
                  f'отправит этот документ на печать удаленной '
                  f'машине. Инструкции и условия использования вы '
                  f'можете получить с помощью команды /help.',
        '/help': 'hello ruslan'
    }

    def __init__(self, message):
        self.__message = self.__commands_list[message.text]
        self.__user_name = message.from_user.username

    def get_message(self):
        return self.__message


@smartCopyCenterBot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    smartCopyCenterBot.send_message(message.from_user.id, BotHandler(message).get_message())


@smartCopyCenterBot.message_handler(content_types=['document', 'photo'])
def save_document(message):
    try:
        if message.document is None:
            downloaded_file, src = get_image(message)
            mode = IMAGE_DIR
        else:
            downloaded_file, src = get_document(message)
            mode = DOCUMENT_DIR
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            converting_files_in_dirs(mode)
        smartCopyCenterBot.reply_to(message, 'success')
    except Exception as e:
        smartCopyCenterBot.reply_to(message, e)


def converting_files_in_dirs(mode):
    files = os.listdir(mode)
    files = [os.path.join(mode, f) for f in files]
    files2pdf = Editor(page_format='A4', files_path_list=files)
    files2pdf.converting()


smartCopyCenterBot.polling(none_stop=True, interval=0)
