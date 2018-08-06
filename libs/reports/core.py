from django.conf import settings
from jinja2 import Environment, FileSystemLoader
import uuid
import os
import datetime
import pdfkit


TEMPLATES_DIRS = [os.path.join(settings.BASE_DIR, *app.split('.'), 'reports')
                  for app in settings.INSTALLED_APPS if app.startswith('apps')]

RENDERED_TEMPLATES_DIR = "/tmp/"

ENV = Environment(loader=FileSystemLoader(TEMPLATES_DIRS))


class Report():
    def __init__(self, template_filepath, mapping):
        """
        Constructor of the class.

        Args:
            template_filepath: path to the template.
            mapping: dictionary with keys-values to render with.
        """
        self.template = ENV.get_template(template_filepath)
        self.mapping = mapping

    def render(self, output_filename=None, delete=True, http_response=True):
        """
        Render the template.

        Args:
            output_filename: in case you want to save the output (optional).
            delete: True if you want to delete the rendered file (optional).
            http_response: True if you want to return an instance of
                django.http.HttpResponse (optional).

        Returns:
            If http_response is True, returns a Django like HttpResponse.
        """
        self.output_filename = output_filename or os.path.join(
            RENDERED_TEMPLATES_DIR, str(uuid.uuid4()) + '.pdf'
        )
        rendered_tmpl_filename = os.path.join(
            RENDERED_TEMPLATES_DIR, str(uuid.uuid4()) + '.html'
        )

        # add custom mappings to the template
        self.mapping['timestamp'] = datetime.datetime.now()
        self.mapping['commons_dir'] = os.path.join(
            settings.BASE_DIR, 'apps/commons/reports/commons'
        )
        self.mapping['my_base_dir'] = os.path.dirname(
            os.path.abspath(self.template.filename)
        )

        rendered_template = self.template.render(self.mapping)
        with open(rendered_tmpl_filename, 'wb') as f:
            f.write(rendered_template.encode('utf-8'))

        options = {
            'encoding': 'UTF-8',
            'disable-smart-shrinking': None
        }
        pdfkit.from_file(
            rendered_tmpl_filename,
            self.output_filename,
            options=options
        )
        os.remove(rendered_tmpl_filename)

        if http_response:
            from django.http import HttpResponse
            response = HttpResponse(open(self.output_filename, 'rb'))
            if delete:
                os.remove(self.output_filename)
            response['Content-Type'] = 'application/pdf'
            user_filename = self.output_filename or os.path.splitext(
                    os.path.basename(self.template.filename))[0]
            response['Content-Disposition'] = \
                'attachment; filename="{}.pdf"'.format(user_filename)
            return response
        if delete:
            os.remove(self.output_filename)
