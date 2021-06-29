#!/usr/bin/env python

from functools import partial

import colorama
import tabulate

WHITE = colorama.Fore.WHITE
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
CYAN = colorama.Fore.CYAN

RESET = colorama.Style.RESET_ALL

colorama.init()


def colored(text, color=WHITE):
    return f"{color}{text}{RESET}"


red = partial(colored, color=RED)

cyan = partial(colored, color=CYAN)

green = partial(colored, color=GREEN)


def as_table(headers, body):
    return tabulate.tabulate(body, headers=headers)


def yes_no(flag, yes='Si', no='no'):
    return green(yes) if flag else red(no)
