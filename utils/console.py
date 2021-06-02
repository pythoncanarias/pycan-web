#!/usr/bin/env python

import decimal


def red(s):
    return f"\u001b[31m{s}\u001b[0m"


def cyan(s):
    return f"\u001b[36m{s}\u001b[0m"


def green(s):
    return f"\u001b[32m{s}\u001b[0m"


def yes_no(b, yes='Si', no='no'):
    return green(yes) if b else red(no)


def as_cell(val, width):
    if isinstance(val, (int, float, decimal.Decimal, bool)):
        return f"{{:>{width}}}".format(str(val))
    elif isinstance(val, bool):
        return f"{{:>{width}}}".format(str(yes_no(val)))
    else:
        return f"{{:<{width}}}".format(str(val))


def as_table(headers, rows):
    assert all([
        len(headers) == len(row)
        for row in rows
        ])
    result = []
    widths = [len(str(head)) for head in headers]
    for row in rows:
        widths = [
            max(a, len(str(b)))
            for a, b in zip(widths, row)
        ]
    result.append(' '.join([as_cell(h, w) for h, w in zip(headers, widths)]))
    result.append(' '.join(['-' * w for w in widths]))
    for row in rows:
        result.append(' '.join([as_cell(v, w) for v, w in zip(row, widths)]))
    result.append(' '.join(['-' * w for w in widths]))
    return '\n'.join(result)
