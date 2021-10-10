from . colorsphere import ColorPicker
from . ledcolor import hsl_color
from xled.control import HighControlInterface
from xled.discover import discover
import matplotlib.pyplot as plt


# Below is an example application of the color picker.
# Call launch_colorpicker with the HighControlInterface as argument.
# Hover over the sphere to watch colors. Click on a color to upload
# it as a movie.
# You can provide your own click and move callbacks for other effects.


global_cp = False
rtmode = False
outermode = False
printcol = False


def make_click_func(ctr):

    def on_click(hsl, event):
        global outermode
        global printcol
        if hsl:
            pat = ctr.make_solid_pattern(hsl_color(*hsl))
            id = ctr.upload_movie(ctr.to_movie(pat), 1, force=True)
            ctr.set_movies_current(id)
            if printcol:
                print(hsl_color(*hsl))
            outermode = 'movie'

    return on_click


def make_move_func(ctr):

    def on_move(hsl, event):
        global rtmode
        global outermode
        if hsl:
            if not rtmode:
                outermode = ctr.get_mode()['mode']
            pat = ctr.make_solid_pattern(hsl_color(*hsl))
            ctr.show_rt_frame(ctr.to_movie(pat))
            rtmode = True
        else:
            if rtmode:
                if outermode:
                    ctr.set_mode(outermode)
                rtmode = False

    return on_move


def launch_colorpicker(ctr, printcolor=False, fromshell=False):
    global global_cp
    global printcol
    printcol = printcolor
    global_cp = ColorPicker(make_click_func(ctr), make_move_func(ctr))
    if fromshell:
        plt.ioff()
        plt.show()
        if outermode:
            ctr.set_mode(outermode)


if __name__ == '__main__':
    dev = discover()
    ctr = HighControlInterface(dev.ip_address)

    launch_colorpicker(ctr, True, True)
