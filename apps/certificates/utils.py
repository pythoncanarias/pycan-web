#!/usr/bin/env python

# import os
# import re
# import subprocess
# import sys
# import logging


# current_module = sys.modules[__name__]
# base_dir = os.path.dirname(current_module.__file__)


# FORMAT = '%(asctime)-15s %(levelname)s %(message)s'

# logging.basicConfig(format=FORMAT)
# logger = logging.getLogger(__name__)


# def get_template_full_name(filename, base=base_dir):
    # return os.path.join(base, 'templates', filename)


# def get_output_full_name(filename, base=base_dir):
    # output_dir = os.path.join(base, 'media')
    # if not os.path.exists(output_dir):
        # os.makedirs(output_dir)
    # return os.path.join(output_dir, filename)


# def inkscape_export(source_filename, target_filename, tron=False):
    # commands = [
        # "inkscape",
        # "--export-pdf={}".format(target_filename),
        # source_filename,
        # ]
    # if tron:
        # logger.info(" ".join(commands))
    # subprocess.call(commands)


# def create_certificate(template, output_name, **kwargs):

    # def extract_value(match):
        # name = match.group(1)[2:-2].strip()
        # return kwargs.get(name, 'Value {} not found'.format(name))

    # pat = re.compile(r'(\{\{.+\}\})')
    # full_input_name = get_template_full_name('{}.svg'.format(template))
    # full_output_name = get_output_full_name('{}.svg'.format(output_name))
    # with open(full_input_name, 'r') as fin:
        # with open(full_output_name, 'w') as fout:
            # template = fin.read()
            # output = pat.sub(extract_value, template)
            # fout.write(output)
    # pdf_filename = get_output_full_name('{}.pdf'.format(output_name))
    # inkscape_export(full_output_name, pdf_filename)
    # return pdf_filename
