from django.conf import settings
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader
import os
import datetime
import pdfkit
import tempfile


TEMPLATES_DIRS = [os.path.join(settings.BASE_DIR, app, 'reports')
                  for app in settings.INSTALLED_APPS]

ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIRS))

PDFKIT_OPTIONS = {
    'encoding': 'UTF-8',
    'disable-smart-shrinking': None,
    'margin-top': '4cm',
    'margin-bottom': '3cm',
    'margin-left': '2cm',
    'margin-right': '2cm',
    'header-spacing': '10',
    'footer-spacing': '10',
    'header-html': 'commons/header.j2',
    'footer-html': 'commons/footer.j2'
}


class Report():
    def __init__(self, template_path, mapping, pdfkit_options=None):
        """
        Constructor of the class.

        Args:
            template_path: path to the template.
            mapping: dictionary with keys-values to render with.
            pdfkit_options: dictionary with pdfkit options (optional).
        """
        # override pdfkit options with arguments (in case)
        self.options = PDFKIT_OPTIONS.copy()
        if pdfkit_options:
            self.options.update(pdfkit_options)
        self.template, self.template_html = \
            Report._create_template_handlers(template_path)
        self.template_pdf = tempfile.NamedTemporaryFile(delete=False)

        header_html = self.options.get('header-html')
        if header_html:
            self.header, self.header_html = \
                Report._create_template_handlers(header_html)
            self.options['header-html'] = self.header_html.name
        else:
            self.header = None

        footer_html = self.options.get('footer-html')
        if footer_html:
            self.footer, self.footer_html = \
                Report._create_template_handlers(footer_html)
            self.options['footer-html'] = self.footer_html.name
        else:
            self.footer = None

        self.mapping = mapping

        # add custom mappings to the template
        self.mapping['timestamp'] = datetime.datetime.now()
        self.mapping['commons_dir'] = os.path.join(
            settings.BASE_DIR, 'commons/reports/commons'
        )
        self.mapping['mybase_dir'] = os.path.dirname(
            os.path.abspath(self.template.filename)
        )
        self.mapping['load_fonts'] = settings.LOAD_FONTS_IN_REPORTS

    def render(self, http_response=True):
        """
        Render the template.

        Args:
            http_response: True if you want to return an instance of
                django.http.HttpResponse (optional).
                If set to True the temporary files will be deleted. Otherwise,
                If set to False, the rendered template will remain accessible
                using the attribute self.template.name (path to the file).

        Returns:
            If http_response is True, returns a Django like HttpResponse.
        """
        Report._render_template(self.template,
                                self.template_html,
                                self.mapping)
        if self.header:
            Report._render_template(self.header,
                                    self.header_html,
                                    self.mapping)
        if self.footer:
            Report._render_template(self.footer,
                                    self.footer_html,
                                    self.mapping)

        pdfkit.from_file(
            self.template_html.name,
            self.template_pdf.name,
            options=self.options
        )

        if http_response:
            response = HttpResponse(open(self.template_pdf.name, 'rb'))
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = \
                'attachment; filename="ticket.pdf"'
            self._delete_tempfiles()
            return response

    def _delete_tempfiles(self):
        os.remove(self.template_html.name)
        os.remove(self.template_pdf.name)
        if self.header:
            os.remove(self.header_html.name)
        if self.footer:
            os.remove(self.footer_html.name)

    @staticmethod
    def _create_template_handlers(template_path):
        template = ENV.get_template(template_path)
        template_html = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.html'
        )
        return template, template_html

    @staticmethod
    def _render_template(template, output_file_handler, mapping):
        rendered_template = template.render(mapping)
        with output_file_handler as f:
            f.write(rendered_template.encode('utf-8'))
