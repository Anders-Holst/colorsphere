from . colorsphere import ColorPicker
from . ledcolor import hsl_color
#from dataclasses import dataclass
from xled.control import HighControlInterface
from xled.discover import discover
import matplotlib.pyplot as pyplot
import sys


# Below is an example application of the color picker.
# Call launch_colorpicker with the HighControlInterface as argument.
# Hover over the sphere to watch colors. Click on a color to upload
# it as a movie.
# You can provide your own click and move callbacks for other effects.


#@dataclass
class XledCallbacks:
    ip_address = None
    rtmode = False
    outermode = False
    printcol = False
    printcolhsl = True

    def __init__(self):
        self.ip_address = self.ip_address or discover().ip_address
        self.ctr = HighControlInterface(self.ip_address)

    def on_click(self, hsl, event):
        if hsl:
            pat = self.ctr.make_solid_pattern(hsl_color(*hsl))
            id = self.ctr.upload_movie(self.ctr.to_movie(pat), 1, force=True)
            self.ctr.set_movies_current(id)
            if self.printcol:
                print(hsl_color(*hsl))
            elif self.printcolhsl:
                print(hsl)
            self.outermode = 'movie'

    def on_move(self, hsl, event):
        if hsl:
            if not self.rtmode:
                self.outermode = self.ctr.get_mode()['mode']
            pat = self.ctr.make_solid_pattern(hsl_color(*hsl))
            self.ctr.show_rt_frame(self.ctr.to_movie(pat))
            self.rtmode = True
        else:
            if self.rtmode:
                if self.outermode:
                    self.ctr.set_mode(self.outermode)
                self.rtmode = False

    def launch(self):
        self.colorpicker = ColorPicker(self.on_click, self.on_move)


if __name__ == '__main__':

    variant = sys.argv[1] if len(sys.argv)>1 else None

    if variant == 'foreground':
        XledCallbacks().launch()
        pyplot.ioff()
        pyplot.show()

    elif variant == 'subprocess':
        import time
        from threading import Timer

        def func1():
            xlc = XledCallbacks()
            xlc.launch()
            xlc.colorpicker.win.add_close_callback(lambda *args: xlc.colorpicker.win.fig.canvas.stop_event_loop())
            xlc.colorpicker.win.fig.canvas.start_event_loop(0)
        
        tmr = Timer(0.0, func1)
        tmr.start()

        for i in range(30):
            time.sleep(1.0)
            print(i)

    else:
        XledCallbacks().launch()
        for i in range(30):
            pyplot.pause(1.0)
            print(i)
