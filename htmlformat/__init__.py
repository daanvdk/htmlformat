from .parser import parse
from .renderer import render


def format(content):
    return render(parse(content))
