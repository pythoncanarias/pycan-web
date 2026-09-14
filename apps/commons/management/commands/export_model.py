#!/usr/bin/env python3

import json
from pathlib import Path

from django.core.serializers.json import DjangoJSONEncoder
from django.core.management.base import BaseCommand
from utils.console import cyan, green 
from django.apps import apps
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile

EXPORT_DIRECTORT = Path('exported')


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)



class Command(BaseCommand):

    help = 'Exportación de modelos'

    def add_arguments(self, parser):
        self.parser = parser
        parser.add_argument('app_name', help='Nombre de la app')
        parser.add_argument('model_name', help='Nombre del modelo')

    def handle(self, *args, **options):
        app_name = options.get('app_name')
        model_name = options.get('model_name')
        print( f'{green(app_name)}.{green(model_name)}', end=' ')
        Model = apps.get_model(app_name, model_name)
        num_rows = Model.objects.all().count()
        print(f'[{num_rows} registros]', end=' ')
        rows = [
            model_to_dict(row)
            for row in Model.objects.all().order_by('pk')
            ]
        filename = EXPORT_DIRECTORT / f'{app_name}_{model_name}.json'
        print(f'a {cyan(filename)}', end=' ')
        with open(filename, 'w', encoding='utf-8') as f_out:
            json.dump(rows, f_out, indent=4, cls=ExtendedEncoder)
        print(green('[OK]'))
