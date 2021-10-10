from . colorsphere import ColorPicker
from . ledcolor import hsl_color
from matplotlib import pyplot
from blessed import Terminal
from functools import wraps


def print_at(name, term, hsl, x=0, y=0):
    rgb = hsl_color(*hsl)
    with term.location(x, y):
        color = term.color_rgb(*rgb)
        print(color(name), ' '.join(f'{i:02X}' for i in rgb))


def main(term):
    def click(hsl, event):
        if hsl:
            print_at('Click', term, hsl, 0, 1)


    def move(hsl, event):
        if hsl:
            print_at('Move ', term, hsl)


    print(term.home + term.clear)
    cp = ColorPicker(click, move)
    pyplot.ioff()
    pyplot.show()


if __name__ == '__main__':
    main(Terminal())
