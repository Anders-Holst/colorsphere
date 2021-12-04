from .colorsphere import ColorPicker

# Below is a simple example application of the color picker.
# It prints the RGB and HSL coordinates for a color you click on.


class ColorPickerLauncher:
    printrgb = False
    printhsl = False

    def __init__(self):
        pass

    def on_click(self, hsl, event):
        if hsl:
            if self.printrgb:
                print("RGB: ", self.hsl_to_rgb(hsl))
            if self.printhsl:
                print("HSL:", hsl)
            print()

    def on_move(self, hsl, event):
        pass

    def hsl_to_rgb(self, hsl):
        return tuple(map(lambda c: int(round(c * 255)), self.cp.sphere.hsl_color(*hsl)))

    def launch(self, from_shell=False, printrgb=False, printhsl=False):
        self.printrgb = printrgb
        self.printhsl = printhsl
        self.cp = ColorPicker(self.on_click, self.on_move, name="Color Picker")
        if from_shell:
            self.cp.win.add_close_callback(lambda *args: self.cp.win.fig.canvas.stop_event_loop())
            self.cp.win.fig.canvas.start_event_loop(0)


if __name__ == "__main__":

    ColorPickerLauncher().launch(from_shell=True, printrgb=True, printhsl=True)
