from django.conf import settings
from jinja2 import Environment, FileSystemLoader
from subprocess import Popen, PIPE
import uuid
import os
import datetime


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
        self.output_filename = output_filename or \
            RENDERED_TEMPLATES_DIR + str(uuid.uuid4()) + '.pdf'

        self.mapping['generation_time'] = datetime.datetime.now()
        self.mapping['base_dir'] = RENDERED_TEMPLATES_DIR
        self.rendered_template = self.template.render(self.mapping)

        p = Popen(['prince', '-', self.output_filename], stdin=PIPE)
        p.stdin.write(self.rendered_template.encode('utf-8'))
        p.stdin.close()
        p.communicate()

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
