#! / usr / bin / env python
# -*- coding: utf-8 -*-
from decimal import Decimal

from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph
from reportlab.platypus import Table, TableStyle
import os
import subprocess
import sys

from organizations.models import Organization


class InvoiceMaker(object):
    PAGE_HEIGHT = A4[1]
    PAGE_WIDTH = A4[0]

    def __init__(self, invoice):
        self.python_canarias = Organization.objects.get(name__istartswith=settings.ORGANIZATION_NAME)

        self.invoice = invoice

        self._configure_fonts('DejaVu')
        self._set_style()

    def _set_style(self):
        self.frame = Frame(
            1.1 * cm,
            6.2 * cm,
            self.PAGE_WIDTH - 2.4 * cm,
            self.PAGE_HEIGHT - 12 * cm,
            leftPadding=0, rightPadding=0
        )
        self.paragraph_estile_1 = ParagraphStyle('', fontName='DejaVu', fontSize=12, alignment=0)

        self.table_style = TableStyle([
            ('BOTTOMPADDING', (0, 0), (- 1, - 1), 0),
            ('TOPPADDING', (0, 0), (- 1, - 1), 0),
            ('LEFTPADDING', (1, 0), (- 3, - 1), 0),
            ('FONT', (0, 0), (- 1, - 1), self.normal, 12),
            ('FONT', (2, 0), (3, - 1), self.normal, 9),
            ('ALIGN', (0, 0), (- 1, - 1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, - 1), 'LEFT'),
            ('VALIGN', (0, 0), (- 1, - 1), 'MIDDLE'),
        ])
        self.first_page = PageTemplate(id='1st_page', frames=self.frame, onPage=self._render_page)

        # check if target directory exists
        dirname = os.path.dirname(self.invoice.path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        self.sheet_style = BaseDocTemplate(
            self.invoice.path,
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
                    colWidths=(1.2 * cm, 13.1 * cm, 0.8 * cm, 1.6 * cm, 2 * cm)
                )
            )

        self.sheet_style.build(self.body)

    def _configure_fonts(self, font):
        self.normal = font
        self.italic = '{}It'.format(self.normal)
        self.bold = '{}Bd'.format(self.normal)
        self.bold_italic = '{}BdIt'.format(self.normal)

        fonts_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'fonts')

        pdfmetrics.registerFont(TTFont(self.normal, os.path.join(fonts_path, 'DejaVuSans.ttf')))
        pdfmetrics.registerFont(TTFont(self.italic, os.path.join(fonts_path, 'DejaVuCondensedSansOblique.ttf')))
        pdfmetrics.registerFont(TTFont(self.bold, os.path.join(fonts_path, 'DejaVuSansBold.ttf')))
        pdfmetrics.registerFont(TTFont(self.bold_italic, os.path.join(fonts_path, 'DejaVuSansBoldOblique.ttf')))

        registerFontFamily(
            self.normal, normal=self.normal, bold=self.bold, italic=self.italic, boldItalic=self.bold_italic)

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
        canvas.rect(1.2 * cm, self.PAGE_HEIGHT - 1 * cm, self.PAGE_WIDTH - 2.4 * cm, - 0.8 * cm)
        canvas.setFont(self.bold, 12)
        canvas.drawString(1.4 * cm, self.PAGE_HEIGHT - 1.58 * cm, 'FACTURA')

        canvas.setFont(self.normal, 9)
        canvas.drawRightString(
            self.PAGE_WIDTH - 1.3 * cm, self.PAGE_HEIGHT - 1.30 * cm, self.invoice.date.strftime('%d-%m-%Y'))
        canvas.drawRightString(
            self.PAGE_WIDTH - 1.3 * cm, self.PAGE_HEIGHT - 1.70 * cm, self.invoice.verbose_invoice_number)
        canvas.setFont(self.bold, 9)
        canvas.drawString(self.PAGE_WIDTH - 6 * cm, self.PAGE_HEIGHT - 1.30 * cm, 'FECHA')
        canvas.drawString(self.PAGE_WIDTH - 6 * cm, self.PAGE_HEIGHT - 1.70 * cm, 'NUMERO')

        # top box
        canvas.setLineWidth(0)
        canvas.line(
            self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 2.35 * cm,
            self.PAGE_WIDTH / 2, self.PAGE_HEIGHT - 4.75 * cm
        )
        canvas.rect(1.2 * cm, self.PAGE_HEIGHT - 2.1 * cm, self.PAGE_WIDTH - 2.4 * cm, - 3 * cm)
        logo_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources', 'images')
        logo_python_path = os.path.join(logo_directory, 'logo_python.png')
        image_size = 17 * cm
        canvas.drawImage(
            logo_python_path,
            2 * cm,
            ((self.PAGE_HEIGHT - image_size) / 2),
            width=image_size,
            height=image_size,
            mask='auto'
        )

        # LEFT HALF
        canvas.setFont(self.bold, 12)
        canvas.drawString(1.4 * cm, self.PAGE_HEIGHT - 2.7 * cm, self.python_canarias.name)
        canvas.setFont(self.normal, 9)
        canvas.drawString(1.7 * cm, self.PAGE_HEIGHT - 3.2 * cm, self.python_canarias.address)
        vertical_1 = self.PAGE_HEIGHT - 3.55 * cm
        if self.python_canarias.rest_address:
            canvas.drawString(1.7 * cm, self.PAGE_HEIGHT - 3.55 * cm, self.python_canarias.rest_address)
            vertical_1 = self.PAGE_HEIGHT - 3.9 * cm
        canvas.drawString(1.7 * cm, vertical_1, '{} {}'.format(self.python_canarias.po_box, self.python_canarias.city))

        canvas.setFont(self.bold, 9)
        canvas.drawRightString(self.PAGE_WIDTH / 2 - 0.3 * cm, self.PAGE_HEIGHT - 4.8 * cm, self.python_canarias.cif)

        # RIGHT HALF
        canvas.setFont(self.bold, 12)
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.3 * cm, self.PAGE_HEIGHT - 2.7 * cm, 'CLIENTE')
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 3.2 * cm, self.invoice.client.name)
        canvas.setFont(self.normal, 9)
        canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, self.PAGE_HEIGHT - 3.55 * cm, self.invoice.client.address)

        vertical_2 = self.PAGE_HEIGHT - 3.9 * cm
        if self.invoice.client.rest_address:
            vertical_1 = self.PAGE_HEIGHT - 3.9 * cm
            vertical_2 = self.PAGE_HEIGHT - 4.25 * cm
            canvas.drawString(self.PAGE_WIDTH / 2 + 0.6 * cm, vertical_1, self.invoice.client.rest_address)
        canvas.drawString(
            self.PAGE_WIDTH / 2 + 0.6 * cm,
            vertical_2,
            '{} {}'.format(self.invoice.client.po_box, self.invoice.client.city)
        )
        canvas.setFont(self.bold, 9)
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, self.PAGE_HEIGHT - 4.8 * cm, self.invoice.client.nif)

        # CONCEPTS
        canvas.setFont(self.normal, 8)
        canvas.drawRightString(1.9 * cm, self.PAGE_HEIGHT - 5.85 * cm, 'ord')
        canvas.drawString(2.5 * cm, self.PAGE_HEIGHT - 5.85 * cm, 'concepto')
        canvas.drawString(self.PAGE_WIDTH - 5.5 * cm, self.PAGE_HEIGHT - 5.85 * cm, 'uds')
        canvas.drawString(self.PAGE_WIDTH - 4.3 * cm, self.PAGE_HEIGHT - 5.85 * cm, 'precio')
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, self.PAGE_HEIGHT - 5.85 * cm, 'total')
        canvas.setLineWidth(0)
        canvas.line(1.2 * cm, self.PAGE_HEIGHT - 6 * cm, self.PAGE_WIDTH - 1.2 * cm, self.PAGE_HEIGHT - 6 * cm)

        canvas.setStrokeColor('Black')

        canvas.setDash(1)
        canvas.setLineWidth(1)
        canvas.rect(1.2 * cm, self.PAGE_HEIGHT - 5.5 * cm, self.PAGE_WIDTH - 2.4 * cm, - 18 * cm)

        # TOTALS BOX
        canvas.setLineWidth(0)
        canvas.rect(1.2 * cm, 2.8 * cm, self.PAGE_WIDTH - 2.4 * cm, 3 * cm)
        canvas.setFont(self.bold, 12)
        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 5.3 * cm, 'SUBTOTAL')
        subtotal = Decimal('0.00')
        canvas.setFont(self.normal, 12)

        for concept in self.invoice.concept_set.all():
            subtotal += concept.amount * concept.quantity

        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 5.3 * cm, '{} €'.format(subtotal))

        retention = 0
        taxes = 0

        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.8 * cm, self.invoice.get_taxes_display())
        if self.invoice.taxes:
            taxes_percentage = Decimal(self.invoice.get_taxes_display().split('(')[1].split('%')[0])
            taxes = subtotal * taxes_percentage / 100
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.8 * cm, '{} €'.format(taxes))

        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 4.3 * cm, self.invoice.get_retention_display())
        if self.invoice.retention:
            retention_percentage = Decimal(self.invoice.get_retention_display().replace('IRPF ', '').replace('%', ''))
            retention = subtotal * retention_percentage / 100
            canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 4.3 * cm, '-{} €'.format(retention))

        grantotal = subtotal + taxes - retention

        canvas.setLineWidth(1)
        canvas.rect(self.PAGE_WIDTH - 9.8 * cm, 2.9 * cm, 8.5 * cm, 1.2 * cm)

        canvas.setFont(self.bold, 12)
        canvas.drawString(self.PAGE_WIDTH - 9.5 * cm, 3.5 * cm, 'TOTAL:')
        canvas.drawRightString(self.PAGE_WIDTH - 1.5 * cm, 3.5 * cm, '{} €'.format(grantotal))

        canvas.setFont(self.normal, 14)
        canvas.drawString(1.5 * cm, 5.2 * cm, 'Pago por transferencia bancaria:')
        canvas.setFont(self.normal, 12)
        canvas.drawString(2 * cm, 4.7 * cm, 'OpenBank')
        canvas.setFont(self.bold, 12)
        canvas.drawString(2 * cm, 4.2 * cm, self.python_canarias.iban)

        # FOOTER
        canvas.setFont(self.normal, 9)
        canvas.drawCentredString(self.PAGE_WIDTH / 2, 2 * cm, self.python_canarias.email)
        canvas.drawCentredString(self.PAGE_WIDTH / 2, 1.5 * cm, self.python_canarias.url)

        # watermark proforma
        if self.invoice.proforma:
            canvas.setFont(self.normal, 80)
            canvas.rotate(45)
            canvas.setFillGray(0.75)
            canvas.drawCentredString(19 * cm, 3 * cm, 'PROFORMA')

        # watermark null
        if not self.invoice.active:
            canvas.setFont(self.normal, 80)
            canvas.rotate(-45)
            canvas.setFillGray(0.75)
            canvas.drawCentredString(-5 * cm, 19 * cm, 'NULA')

        canvas.restoreState()
