from . colorsphere import ColorPicker
from matplotlib import pyplot
from blessed import Terminal
from functools import wraps



def print_at(name, term, items, x=0, y=0):
    if items:
        with term.location(x, y):
            print(name, ', '.join(f'{i:+.3f}' for i in items))


def main(term):
    def click(rgb, event):
        print_at('Click', term, rgb, 0, 1)


    def move(rgb, event):
        print_at('Move ', term, rgb)


    print(term.home + term.clear)
    cp = ColorPicker(click, move)
    pyplot.ioff()
    pyplot.show()


if __name__ == '__main__':
    main(Terminal())
