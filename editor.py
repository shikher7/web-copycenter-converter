import os.path
from dotenv import load_dotenv

from converter import ImageConverter, OfficeConverter, html2pdf, txt2pdf

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
        'html': False
    }

    def __init__(self, page_format, files_path_list):
        self.__files_path_list = files_path_list
        self.__page_format = page_format

    def __distributing(self, file_path, extension):
        if extension not in ['html', 'txt']:
            self.__distributor[extension](self.__page_format, file_path).convert_to_pdf()
        elif extension == 'txt':
            txt2pdf(file_path, self.__page_format)
        elif extension == 'html':
            html2pdf(file_path, self.__page_format)
        try:
            os.remove(file_path)
        except OSError as e:
            print("ERROR: %s - %s." % (e.filename, e.strerror))

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
        obj = Editor('A3',
                     files_path_list=[
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/file_example_XLS_1000.xls',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/file_example_XLSX_10.xlsx',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/file-sample_100kB.doc',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/file-sample_100kB.docx',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/pngtree-pink-watercolor-brushes-png-image_5054156.jpg',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/lol.txt',
                         '/home/woodver/pycharmProj/web-copycenter-converter-main/input_images/index.html'])
        obj.converting()
