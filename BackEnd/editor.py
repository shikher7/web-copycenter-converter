import os.path
from dotenv import load_dotenv

from converter import ImageConverter, OfficeConverter, html2pdf, txt2pdf, save_pdf, PageSize

ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'input_images')
DOCUMENT_DIR = os.path.join(ROOT_DIR, 'input_documents')


class Editor:
    __distributor = {
        'png': ImageConverter,
        'jpg': ImageConverter,
        'jpeg': ImageConverter,
        'doc': OfficeConverter,
        'docx': OfficeConverter,
        'xls': OfficeConverter,
        'xlsx': OfficeConverter,
        'ppt': OfficeConverter,
        'pptx': OfficeConverter,
        'bmp': ImageConverter,
        'eps': ImageConverter,
        'gif': ImageConverter,
        'txt': False,
        'rtf': OfficeConverter,
        'html': False,
        'pdf': False
    }

    def __init__(self, page_format, files_path_list):
        self.__files_path_list = files_path_list
        self.__page_format = page_format

    def __distributing(self, file_path, extension):
        if extension not in ['html', 'txt', 'pdf']:
            self.__distributor[extension](extension, self.__page_format, file_path).convert_to_pdf()
        elif extension == 'txt':
            txt2pdf(file_path, self.__page_format, exception=extension)
        elif extension == 'html':
            html2pdf(file_path, self.__page_format, exception=extension)
        elif extension == 'pdf':
            save_pdf(file_path)

    def converting(self):
        for file_path in self.__files_path_list:
            if file_path.split('/')[-1].split('.')[-1] in self.__distributor:
                self.__distributing(file_path, extension=file_path.split('/')[-1].split('.')[-1])


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
DEBUG = bool(int(os.environ.get('DEBUG')))
if DEBUG:
    if __name__ == '__main__':
        obj = Editor('A4',
                     files_path_list=[
                         '/home/slijirqqq/PycharmProjects/web-copy-center-converter/trash/background.jpg',
                         '/home/slijirqqq/PycharmProjects/web-copy-center-converter/trash/file-sample_1MB.docx',
                         '/home/slijirqqq/PycharmProjects/web-copy-center-converter/trash/file-sample_1MB.doc',
                         '/home/slijirqqq/PycharmProjects/web-copy-center-converter/trash/lol.html',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/pngtree-pink-watercolor-brushes-png-image_5054156.jpg',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/lol.txt.txt',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/index.html'])
        obj.converting()
