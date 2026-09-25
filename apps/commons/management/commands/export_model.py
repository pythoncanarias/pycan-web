#!/usr/bin/env python3

from pathlib import Path

from django.apps import apps
from django.core import serializers
from django.core.management.base import BaseCommand

from adapters.console import print, cyan, green

EXPORT_DIRECTORT = Path('exported')


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
        all_rows = Model.objects.all().order_by('pk')
        num_rows = all_rows.count()
        print(f'[{num_rows} registros]', end=' ')
        filename = EXPORT_DIRECTORT / f'{app_name}_{model_name}.json'
        print(f'a {cyan(filename)}', end=' ')
        with open(filename, 'w', encoding='utf-8') as f_out:
            serializers.serialize('json', all_rows,
                stream=f_out,
                use_natural_foreign_keys=True,
                use_natural_primary_keys=True,
                indent=4,
                )
        print(green('[OK]'))
