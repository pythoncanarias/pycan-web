import os

from django.utils import timezone
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table


class BaseReport:
    FONTS = {
        'light': 'Existence-Light.ttf',
        'bold': 'Amaranth-Bold.ttf',
        'title': 'AirAmerica-Regular.ttf',
        'far': 'Font Awesome-5-Free-Regular-400.ttf',
        'fab': 'Font-Awesome-5-Brands-Regular-400.ttf',
        'fas': 'Font-Awesome-5-Free-Solid-900.ttf',
        'fira': 'FiraCode-Light.ttf'
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.configure_paths()
        self.configure_fonts()

    def configure_paths(self):
        self.resources_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.fonts_path = os.path.join(self.resources_path, 'fonts')
        self.images_path = os.path.join(self.resources_path, 'images')

    def configure_fonts(self):
        self.fonts = {}
        for font_alias, font_filename in BaseReport.FONTS.items():
            font_path = os.path.join(self.fonts_path, font_filename)
            pdfmetrics.registerFont(TTFont(font_alias, font_path))

    def coord(self, x, y, unit=mm):
        x, y = x * unit, self.height - y * unit
        return x, y

    def insert_image(self, image_path, x, y, width, anchor='sw'):
        self.canvas.drawImage(
            image_path,
            x,
            y,
            width=width,
            preserveAspectRatio=True,
            anchorAtXY=True,
            mask='auto',
            anchor=anchor)

    def paragraph(self, text):
        return Paragraph(text, self.styles['Normal'])


class Header(BaseReport):

    def __init__(self, canvas, x, y, width=17 * cm, height=3 * cm):
        BaseReport.__init__(self, width, height)
        self.canvas = canvas
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.saveState()

        logo_path = os.path.join(self.images_path, 'logo-python-canarias.png')
        self.insert_image(
            logo_path,
            self.x,
            self.y,
            45 * mm,
            anchor='nw')

        self.canvas.setLineWidth(0.2 * mm)
        y = self.y - 18 * mm
        self.canvas.line(self.x, y, self.x + self.width, y)

        self.canvas.restoreState()


class Footer(BaseReport):

    def __init__(self, canvas, x, y, width=17 * cm, height=3 * cm):
        BaseReport.__init__(self, width, height)
        self.canvas = canvas
        self.x = x
        self.y = y

    def draw(self):
        self.canvas.saveState()

        self.canvas.setLineWidth(0.2 * mm)
        self.canvas.line(self.x, self.y, self.x + self.width, self.y)
        # icon
        self.canvas.setFont('fas', 10)
        self.canvas.drawString(self.x, self.y - 5 * mm, '\uf0c1')
        # url
        self.canvas.setFont('bold', 10)
        self.canvas.drawString(self.x + 4 * mm, self.y - 5 * mm,
                               'pythoncanarias.es')

        self.canvas.restoreState()


class QRCode(BaseReport):

    def __init__(self, canvas, x, y, barcode, width=5 * cm, height=5 * cm):
        BaseReport.__init__(self, width, height)
        self.canvas = canvas
        self.x = x
        self.y = y
        self.barcode = barcode

    def draw(self):
        self.canvas.saveState()

        # qrcode image
        qr_code = qr.QrCodeWidget(self.barcode)
        qr_code.barWidth = self.width
        qr_code.barHeight = self.height
        qr_code.qrVersion = 1
        d = Drawing()
        d.add(qr_code)
        renderPDF.draw(d, self.canvas, self.x, self.y)

        # qrcode text
        self.canvas.setFont('fira', 8)
        self.canvas.rotate(90)
        self.canvas.drawString(52 * mm, -18 * cm, self.barcode)

        self.canvas.restoreState()


class TicketMaker(BaseReport):

    def __init__(self, pdf_file, ticket, width=A4[0], height=A4[1]):
        super().__init__(width, height)
        self.ticket = ticket
        self.doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4,
            rightMargin=3 * cm,
            leftMargin=2 * cm,
            topMargin=4 * cm,
            bottomMargin=3 * cm)
        self.elements = []

    def create_title(self):
        p = self.paragraph(f'''
            <para leading=27><font size=25 name=title>{ self.ticket.event }
            </font></para>''')
        self.elements.append(p)
        s = Spacer(1, 1 * cm)
        self.elements.append(s)

    def create_features(self):
        start = timezone.localtime(self.ticket.event.start_datetime())
        event_date = start.strftime('%d/%m/%Y')
        if start.hour == 0:
            event_hour = 'Aún sin definir'
        else:
            event_hour = start.strftime('%H:%Mh')
        data = (
            ('\uf554', 'asistente', self.ticket.customer_full_name),
            ('\uf0e0', 'email', self.ticket.customer_email),
            ('\uf784', 'fecha del evento', event_date),
            ('\uf017', 'hora de comienzo', event_hour),
            ('\uf810', 'tipo de entrada', self.ticket.article.category.name),
            ('\uf4c0', 'precio de la entrada',
                f'{self.ticket.article.price}€'),
            ('\uf07a', 'fecha de compra',
                self.ticket.sold_at.strftime('%d/%m/%y @ %H:%Mh')),
            ('\uf3c5', 'ubicación',
             self.paragraph(f'''
                <font name=bold>{ self.ticket.event.venue.name }</font>''')),
            ('\uf14e', 'dirección',
             self.paragraph(f'''
                <font name=bold>{ self.ticket.event.venue.address }</font>
            '''))
        )

        tblstyle = ([('FONT', (0, 0), (0, -1), 'fas'),
                     ('FONT', (1, 0), (1, -1), 'light'),
                     ('FONT', (2, 0), (2, -1), 'bold'),
                     ('TEXTCOLOR', (0, 0), (0, -1), '#595959'),
                     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                     ('ALIGN', (0, 0), (0, -1), 'CENTER')])
        tbl = Table(
            data, colWidths=(6 * mm, 4 * cm, 10 * cm), rowHeights=(8 * mm))
        tbl.setStyle(tblstyle)
        self.elements.append(tbl)

    def create_header(self):
        header = Header(self.canvas, *self.coord(2, 1, cm))
        header.draw()

    def create_footer(self):
        footer = Footer(self.canvas, *self.coord(2, 27, cm))
        footer.draw()

    def create_qr(self):
        qrcode = QRCode(self.canvas, *self.coord(13, 25, cm),
                        str(self.ticket.keycode))
        qrcode.draw()

    def draw_flowables(self):
        self.create_title()
        self.create_features()

    def draw_fixed(self, canvas, doc):
        self.canvas = canvas
        self.create_header()
        self.create_qr()
        self.create_footer()

    def save(self):
        self.doc.build(self.elements, onFirstPage=self.draw_fixed)

    def create(self):
        self.draw_flowables()
        self.save()
