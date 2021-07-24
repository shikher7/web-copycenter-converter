import datetime
from PIL import Image

import img2pdf
import sys
import subprocess
import re
import os
import pdfkit
from fpdf import FPDF


# sudo apt-get install wkhtmltopdf !!!!!

class PageSize:
    __formats_list_size = {
        'A4': ('8.3', '11.7'), 'A3': ('11.7', '16.8'), 'A2': ('16.8', '23.7')
    }

    def __init__(self, format_file='A4', input_path='./'):
        self.page_format = format_file
        self.page_size = self.__formats_list_size[format_file]
        self.input_path = os.path.abspath(input_path)
        self.out_put_path = os.path.join(os.path.curdir, f'{format_file}')


class ImageConverter(PageSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.float_page_size = [
            img2pdf.in_to_pt(float(self.page_size[0])),
            img2pdf.in_to_pt(float(self.page_size[1]))
        ]
        self.__layout_function = img2pdf.get_layout_fun(self.float_page_size)
        self.image_file = Image.open(self.input_path)

    def convert_to_pdf(self):
        basename = (self.input_path.split('/')[-1]).split('.')[:]
        suffix = datetime.datetime.now().strftime('%d.%m.%y')
        basename += '_' + suffix
        convert_time = datetime.datetime.now().strftime('%H:%M:00')
        self.page_size = tuple(map(float, self.page_size))
        self.page_size = (int(self.page_size[0] * 200), int(self.page_size[1] * 200))
        target_width, target_height = self.page_size
        current_width, current_height = self.image_file.size
        scale = max((current_width / float(target_width)), (current_height / float(target_height)))
        final_image_size = [round(current_width / scale), round(current_height / scale)]
        resized_image = self.image_file.resize(size=final_image_size, resample=Image.LANCZOS)
        canvas_image = Image.new(mode='RGB', size=self.page_size, color='white')
        canvas_image.paste(resized_image)
        try:
            from pathlib import Path
            Path(os.path.join(self.page_format, suffix, convert_time, basename[1])).mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            print('Directory already exists')
        canvas_image.save(os.path.join(self.out_put_path, suffix, convert_time, basename[1], basename[
            0] + '.pdf'), format='PDF', quality=200)


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


class OfficeConverter(PageSize):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def __libreoffice_exec(cls):
        if sys.platform == 'darwin':
            return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
        return 'libreoffice'

    def convert_to_pdf(self, timeout=None):
        basename = (self.input_path.split('/')[-1]).split('.')[-1]
        print(basename)
        suffix = datetime.datetime.now().strftime('%d.%m.%y')
        convert_time = datetime.datetime.now().strftime('%H:%M:00')
        args = [self.__libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir',
                os.path.join(self.out_put_path, suffix, convert_time, basename), self.input_path]
        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())

        if filename is None:
            raise LibreOfficeError(process.stdout.decode())
        else:
            return filename.group(1)


def exception_files2pdf(file_path, format):
    file = PageSize(format_file=format, input_path=file_path)
    datetime_dir = datetime.datetime.now().strftime('%d.%m.%y')
    convert_time = datetime.datetime.now().strftime('%H:%M:00')
    try:
        from pathlib import Path
        Path(
            os.path.join(file.out_put_path, datetime_dir, convert_time, file_path.split('/')[-1].split('.')[-1])).mkdir(
            parents=True, exist_ok=True)
    except FileExistsError:
        print('Directory already exists')
    output_path = os.path.join(file.out_put_path,
                               datetime_dir, convert_time, file_path.split('/')[-1].split('.')[
                                   -1] + f'/{file_path.split("/")[-1].split(".")[:-1][0]}.pdf')
    return file_path, output_path


def txt2pdf(input_path, format, arg='-o'):
    file_path, output_path = exception_files2pdf(input_path, format)
    pdf_file = FPDF(format=format)
    pdf_file.add_page()
    pdf_file.set_font('Arial')
    txt_file = open(file_path, 'r')
    for line in txt_file:
        pdf_file.cell(200, 10, txt=line, ln=1, align='C')
    pdf_file.output(output_path)
    txt_file.close()


def html2pdf(input_path, format):
    file_path, output_path = exception_files2pdf(input_path, format)
    return pdfkit.from_file(file_path, output_path)
