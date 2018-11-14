#!/usr/bin/env python

from django.core.management.base import BaseCommand
from events.models import Trade


class Command(BaseCommand):
    help = 'Middleman'

    def handle(self, *args, **options):
        print("Buscando trade activo")
        trade = Trade.load_active_trade()
        if not trade:
            print("No hay trade activo")
            print("Buscando candidatos")
            waiting_list, refund = Trade.find_candidates()
            if waiting_list and refund:
                print("Tenemos candidatos")
                trade = Trade.create(waiting_list, refund)
            else:
                print("No hay candidatos")
                return
        if trade.is_due():
            print(f'Trade finished (sucessful: {self.sucessful})')
