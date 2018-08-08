from django.conf import settings
from django.http import HttpResponse
from jinja2 import Environment, FileSystemLoader
import os
import datetime
import pdfkit
import tempfile


TEMPLATES_DIRS = [os.path.join(settings.BASE_DIR, *app.split('.'), 'reports')
                  for app in settings.INSTALLED_APPS if app.startswith('apps')]

RENDERED_TEMPLATES_DIR = "/tmp/"

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
    def __init__(self, template_path, mapping, pdfkit_options={}):
        """
        Constructor of the class.

        Args:
            template_path: path to the template.
            mapping: dictionary with keys-values to render with.
            pdfkit_options: dictionary with pdfkit options (optional).
        """
        self.template = ENV.get_template(template_path)
        self.template_html = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.html'
        )
        self.template_pdf = tempfile.NamedTemporaryFile(delete=False)

        # override pdfkit options with arguments (in case)
        self.options = {
            k: v for k, v in
            list(PDFKIT_OPTIONS.items()) + list(pdfkit_options.items())
        }
        header_html = self.options.get('header-html')
        if header_html:
            self.header = ENV.get_template(header_html)
            self.header_html = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.html'
            )
            self.options['header-html'] = self.header_html.name
        else:
            self.header = None
        footer_html = self.options.get('footer-html')
        if footer_html:
            self.footer = ENV.get_template(footer_html)
            self.footer_html = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.html'
            )
            self.options['footer-html'] = self.footer_html.name
        else:
            self.footer = None

        self.mapping = mapping

        # add custom mappings to the template
        self.mapping['timestamp'] = datetime.datetime.now()
        self.mapping['commons_dir'] = os.path.join(
            settings.BASE_DIR, 'apps/commons/reports/commons'
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
        rendered_template = self.template.render(self.mapping)
        with self.template_html as f:
            f.write(rendered_template.encode('utf-8'))
        if self.header:
            rendered_template = self.header.render(self.mapping)
            with self.header_html as f:
                f.write(rendered_template.encode('utf-8'))
        if self.footer:
            rendered_template = self.footer.render(self.mapping)
            with self.footer_html as f:
                f.write(rendered_template.encode('utf-8'))

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
