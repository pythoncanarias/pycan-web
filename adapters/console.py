from functools import partial

import rich
import rich.table


def _colored(text, color='white'):
    return f'[{color}]{text}[/{color}]'


red = partial(_colored, color='red')


cyan = partial(_colored, color='cyan')


green = partial(_colored, color='green')


print = rich.print


def as_table(headers, body, title=''):
    table = rich.table.Table(title=title)
    for column_name in headers:
        table.add_column(column_name)
    for row in body:
        table.add_row(*[str(r) for r in row])
    return table


def yes_no(flag, yes='Si', no='no'):
    return green(yes) if flag else red(no)
