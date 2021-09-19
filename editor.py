import os
import time

from converter import ImageConverter, OfficeConverter, html2pdf, txt2pdf

import fleep


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

    def converting(self):
        for file_path in self.__files_path_list:
            if file_path.split('/')[-1].split('.')[-1] in self.__distributor:
                self.__distributing(file_path, extension=file_path.split('/')[-1].split('.')[-1])


if __name__ == '__main__':
    obj = Editor('A3',
                 files_path_list=[
                     '/home/shikher/Documents/GitHub/web-copycenter-converter/Untitled.docx',
                     'home/shikher/Documents/GitHub/web-copycenter-converter/sample1.txt'])
    obj.converting()
