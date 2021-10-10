from . colorsphere import ColorPicker
from matplotlib import pyplot


def make_callback(name):
    return lambda *a, **ka: print(name, a, ka)


def main():
    cp = ColorPicker(make_callback('click'), make_callback('move'))
    pyplot.ioff()
    pyplot.show()


if __name__ == '__main__':
    main()
