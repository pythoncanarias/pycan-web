#! / usr / bin / env python
# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from decimal import Decimal as dec

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.platypus import Table, TableStyle

from invoices.constants import (
    IGIC_7,
    NO_IGIC,
    ORG_ADDRESS,
    ORG_CIF,
    ORG_CITY,
    ORG_EMAIL,
    ORG_MOTTO,
    ORG_NAME,
    ORG_WEB,
    RETENTION_21,
    RETENTION_6,
)


class InvoiceMaker(object):
    PAGE_HEIGHT = A4[1]
    PAGE_WIDTH = A4[0]

    ORG_DATA = {
        'name': ORG_NAME,
        'motto': ORG_MOTTO,
        'cif': ORG_CIF,
        'address': ORG_ADDRESS,
        'city': ORG_CITY,
        'email': ORG_EMAIL,
        'web': ORG_WEB,
    }

    def __init__(self, invoice):
        self.invoice = invoice

        self.font = 'DejaVu'

        self._configure_fonts(self.font)
        self._set_style()

    def _set_style(self):
        self.frame = Frame(
            1.2 * cm,
            6.2 * cm,
            self.PAGE_WIDTH - 2.4 * cm,
            self.PAGE_HEIGHT - 11.5 * cm,
            leftPadding=0, rightPadding=0
        )
        self.paragraph_estile_1 = ParagraphStyle('', fontName='DejaVu', fontSize=12, alignment=0)

        self.table_style = TableStyle([
            ('BOTTOMPADDING', (0, 0), (- 1, - 1), 0),
            ('TOPPADDING', (0, 0), (- 1, - 1), 0),
            ('LEFTPADDING', (1, 0), (- 3, - 1), 0),
            ('FONT', (0, 0), (- 1, - 1), self.font, 12),
            ('FONT', (2, 0), (3, - 1), self.font, 9),
            ('ALIGN', (0, 0), (- 1, - 1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, - 1), 'LEFT'),
            ('VALIGN', (0, 0), (- 1, - 1), 'MIDDLE'),
        ])
        self.first_page = PageTemplate(id='1st_page', frames=self.frame, onPage=self._render_page)

        abs_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        directory = os.path.join(abs_path, 'media', 'invoices')
        abs_filename = os.path.join(directory, self.invoice.filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.sheet_style = BaseDocTemplate(
            abs_filename,
            pagesize=A4,
            pageTemplates=[self.first_page],
            showBoundary=0,
            leftMargin=0,
            rightMargin=0,
            topMargin=0,
            bottomMargin=0,
            allowSplitting=1,
            tittle=None,
            author=None,
            _pageBreakQuick=1,
            encrypt=None,
        )

        self.body = []

        concepts = self.invoice.concept_set.all().order_by('-amount')
        if concepts:
            table_cont = []
            pos = 1
            for cncpt in concepts:
                description = Paragraph(cncpt.description, self.paragraph_estile_1)
                table_cont.append([pos, description, cncpt.quantity, cncpt.amount, cncpt.amount * cncpt.quantity])
                pos += 1
            self.body.append(
                Table(
                    table_cont,
                    style=self.table_style,
                    colWidths=(1.2 * cm, 13 * cm, 0.8 * cm, 1.6 * cm, 2 * cm)
                )
            )

        self.sheet_style.build(self.body)

    @staticmethod
    def _configure_fonts(font):
        normal = font
        italic = '{}It'.format(font)
        bold = '{}Bd'.format(font)
        bold_italic = '{}BdIt'.format(font)

        fonts_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'fonts')

        pdfmetrics.registerFont(TTFont(normal, os.path.join(fonts_path, 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont(italic, os.path.join(fonts_path, 'DejaVuCondensedSansOblique.ttf')))
        pdfmetrics.registerFont(TTFont(bold, os.path.join(fonts_path, 'DejaVuSansBold.ttf')))
        pdfmetrics.registerFont(TTFont(bold_italic, os.path.join(fonts_path, 'DejaVuSansBoldOblique.ttf')))

        registerFontFamily('Dejavu', normal=normal, bold=bold, italic=italic, boldItalic=bold_italic)

    @staticmethod
    def _open_file(filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

    def _render_page(self, canvas, sheet_style):
        canvas.saveState()

        # header
        canvas.setLineWidth(0)
        canvas.line(
            self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 1.95 * cm,
            self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 4.35 * cm
        )
        canvas.rect(1.2 * cm, self.PAGE_HEIGHT - 1.65 * cm, self.PAGE_WIDTH - 2.4 * cm, - 3 * cm)
        # logo_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'images')
        # logo_python_path = os.path.join(logo_directory, 'logo_python.png')
        # image_size = 18 * cm
        # canvas.drawImage(
        #     logo_python_path, 1.3 * cm, (self.PAGE_HEIGHT - image_size) / 2,
        #     width=image_size, height=image_size, mask='auto')

        # left box
        canvas.drawString(1.4 * cm, self.PAGE_HEIGHT - 2.3 * cm, self.ORG_DATA['name'])
        canvas.drawRightString(self.PAGE_WIDTH / 2 - 0.3 * cm, self.PAGE_HEIGHT - 2.3 * cm, self.ORG_DATA['motto'])

        canvas.drawString(1.4 * cm, self.PAGE_HEIGHT - 2.8 * cm, self.ORG_DATA['cif'])

        canvas.setFont(self.font, 8)
        canvas.drawString(6.2 * cm, self.PAGE_HEIGHT - 3.8 * cm, 'número')
        canvas.drawString(6.2 * cm, self.PAGE_HEIGHT - 3.3 * cm, 'fecha')
        canvas.drawRightString(self.PAGE_WIDTH / 2 - 0.3 * cm, self.PAGE_HEIGHT - 4.3 * cm, 'número cuenta')

        canvas.setFont(self.font, 12)

        canvas.drawRightString(
            self.PAGE_WIDTH / 2 - 0.3 * cm, self.PAGE_HEIGHT - 3.8 * cm, self.invoice.verbose_invoice_number)
        canvas.drawString(1.4 * cm, self.PAGE_HEIGHT - 3.3 * cm, 'ciudad')
        canvas.drawRightString(self.PAGE_WIDTH / 2 - 0.3 * cm, self.PAGE_HEIGHT - 3.3 * cm, '%s' % self.invoice.date)

        # right box
        canvas.drawString(
            self.PAGE_WIDTH / 2 + 0.3 * cm, self.PAGE_HEIGHT - 2.3 * cm, 'cliente'
        )
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 2.8 * cm, self.invoice.client.name)
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 3.3 * cm, self.invoice.client.address)
        if self.invoice.client.rest_address:
            canvas.drawString(
                self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 3.8 * cm, self.invoice.client.rest_address)
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 4.3 * cm, self.invoice.client.city)
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, self.PAGE_HEIGHT - 4.3 * cm, self.invoice.client.nif)

        canvas.setFont(self.font, 8)
        canvas.drawRightString(1.9 * cm, self.PAGE_HEIGHT - 5.35 * cm, 'ord')
        canvas.drawString(2.5 * cm, self.PAGE_HEIGHT - 5.35 * cm, 'concepto')
        canvas.drawString(self.PAGE_WIDTH - 5.5 * cm, self.PAGE_HEIGHT - 5.35 * cm, 'uds')
        canvas.drawString(self.PAGE_WIDTH - 4.3 * cm, self.PAGE_HEIGHT - 5.35 * cm, 'precio')
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, self.PAGE_HEIGHT - 5.35 * cm, 'total')

        canvas.setLineWidth(0)
        canvas.line(1.2 * cm, self.PAGE_HEIGHT - 5.5 * cm, self.PAGE_WIDTH - 1.2 * cm, self.PAGE_HEIGHT - 5.5 * cm)

        canvas.setStrokeColor('grey')
        canvas.setDash(0, 2)
        canvas.line(
            3.2 * cm, self.PAGE_HEIGHT - 5 * cm,
            3.2 * cm, 6.2 * cm)
        canvas.line(
            self.PAGE_WIDTH - 4 * cm, self.PAGE_HEIGHT - 5 * cm,
            self.PAGE_WIDTH - 4 * cm, 6.2 * cm
        )
        canvas.setStrokeColor('Black')

        canvas.setDash(1)
        canvas.setLineWidth(1)
        canvas.rect(1.2 * cm, self.PAGE_HEIGHT - 5 * cm, self.PAGE_WIDTH - 2.4 * cm, - 18.5 * cm)

        # totals
        canvas.setLineWidth(0)
        canvas.setFont(self.font, 12)
        canvas.rect(1.2 * cm, 2.8 * cm, self.PAGE_WIDTH - 2.4 * cm, 3 * cm)
        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 5.3 * cm, 'suma')
        subtotal = dec('0.00')

        for concept in self.invoice.concept_set.all():
            subtotal += concept.amount * concept.quantity

        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 5.3 * cm, '%.2f €' % subtotal)

        if self.invoice.taxes == IGIC_7:
            imp = subtotal * 7 / 100
            canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.8 * cm, 'IGIC 7%')
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.8 * cm, '%.2f €' % imp)
        elif self.invoice.taxes == NO_IGIC:
            imp = dec('0.00')
            canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.8 * cm, 'NO IGIC')
        else:
            imp = subtotal * 21 / 100
            canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.8 * cm, 'IVA 21%')
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.8 * cm, '%.2f €' % imp)

        if self.invoice.retention == RETENTION_21:
            irpf = subtotal * 21 / 100
            canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.3 * cm, 'ret. 12%')
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.3 * cm, '%.2f €' % irpf)
        elif self.invoice.retention == RETENTION_6:
            irpf = subtotal * 6 / 100
            canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.3 * cm, 'ret 6%')
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.3 * cm, '%.2f €' % irpf)
        else:
            irpf = 0

        grantotal = subtotal + imp - irpf

        canvas.setFont(self.font, 14)
        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 3.5 * cm, self.invoice.get_taxes_display())
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 3.5 * cm, '%.2f €' % grantotal)
        canvas.setFont(self.font, 9)
        canvas.drawString(self.PAGE_WIDTH - 8.5 * cm, 3.1 * cm, self.invoice.get_taxes_display())

        canvas.setLineWidth(1)
        canvas.rect(self.PAGE_WIDTH - 9.8 * cm, 2.9 * cm, 8.5 * cm, 1.2 * cm)

        canvas.setFont(self.font, 9)

        canvas.drawCentredString(self.PAGE_WIDTH / 2, 2 * cm, self.ORG_DATA['address'])
        canvas.drawCentredString(self.PAGE_WIDTH / 2, 1.7 * cm, self.ORG_DATA['email'])
        canvas.drawCentredString(self.PAGE_WIDTH / 2, 1.4 * cm, self.ORG_DATA['web'])

        canvas.setLineWidth(1)

        canvas.line(5.2 * cm, 2.4 * cm, self.PAGE_WIDTH - 5.2 * cm, 2.4 * cm)

        # logo_python_letras_path = os.path.join(logo_directory, 'logo_python_letras.png')
        # canvas.drawImage(logo_python_letras_path, 1.3 * cm, 2.9 * cm, width=7.8 * cm, height=2.8 * cm)

        # watermark proforma
        if self.invoice.proforma:
            canvas.setFont(self.font, 80)
            canvas.rotate(45)
            canvas.setFillGray(0.75)
            canvas.drawCentredString(19 * cm, 3 * cm, 'PROFORMA')

        # watermark null
        if not self.invoice.active:
            canvas.setFont(self.font, 80)
            canvas.rotate(-45)
            canvas.setFillGray(0.75)
            canvas.drawCentredString(-5 * cm, 19 * cm, 'NULA')

        canvas.restoreState()
