from typing import Tuple

BLACK = '000000'
WHITE = 'FFFFFF'


def get_rgb_from_hex(value: str) -> Tuple[int, int, int, int]:
    red = int(value[:2], base=16)
    green = int(value[2:4], base=16)
    blue = int(value[4:6], base=16)
    alpha = int(value[6:8], base=16) if len(value) > 6 else 255
    return red, green, blue, alpha


def get_luminance(red, green, blue, alpha) -> int:
    luminance = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    luminance *= alpha / 255
    return round(luminance)
