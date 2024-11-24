"""
colorsphere.colorwidgets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author: Anders Holst (anders.holst@ri.se), 2024

Useful widgets, such as various types of buttons, for use with the color sphere when creating interactve user interfaces with it.

"""

import matplotlib.pyplot as plt
import matplotlib as mpl


def gray(gr):
    x = max(0.0, min(1.0, gr))
    p = (pow(x, 1.0 / 2.4) * 1.055 - 0.055) if x > 0.0031308 else x * 12.92
    return (p, p, p)


class CCWidget(object):
    def __init__(self, fig, rect):
        self.fig = fig
        self.ax = fig.add_axes(rect, frame_on=False, xticks=[], yticks=[])
        self.rect = rect

    def get_width(self):
        return self.fig.canvas.get_width_height()[0] * self.rect[2]

    def get_height(self):
        return self.fig.canvas.get_width_height()[1] * self.rect[3]

    def get_pixpt(self):
        return 72.0 / self.fig.dpi

    def show(self):
        self.ax.set_visible(True)
        self.fig.canvas.draw()

    def hide(self):
        self.ax.set_visible(False)
        self.fig.canvas.draw()

    def refresh(self):
        self.fig.canvas.flush_events()


class CCText(CCWidget):
    def __init__(self, fig, pos, txt, relfonthgt):
        super(CCText, self).__init__(fig, (0, 0, 1, 1))
        self.relfontheight = relfonthgt
        self.text = plt.Text(pos[0], pos[1], txt, ha='center', va='center')
        self.resize()
        self.ax.add_artist(self.text)

    def resize(self):
        fontsz = min(self.get_width(), self.get_height()) * self.relfontheight * self.get_pixpt()
        self.text.set_fontsize(fontsz)


class CCSample(CCWidget):
    def __init__(self, fig, rect, bg, sfunc, colfunc, btup=False, kdict=False):
        super(CCSample, self).__init__(fig, rect)
        self.bg = bg
        self.select_func = sfunc
        self.color_func = colfunc
        self.button_tuple = btup
        self.key_dict = kdict
        self.hsl = None
        self.oldhsl = None
        self.dragpos = False
        self.sqr = plt.Rectangle(
            (0, 0), 1.0, 1.0, linewidth=8*self.get_pixpt(), edgecolor=(0, 0, 0), facecolor=bg
        )
        self.sqr2 = plt.Rectangle(
            (0, 0), 1.0, 1.0, linewidth=0, edgecolor=(0, 0, 0), fill=False
        )
        self.ax.add_artist(self.sqr2)
        self.ax.add_artist(self.sqr)

    def remove(self):
        self.sqr2.remove()
        self.sqr.remove()
        self.ax.remove()
        
    def set_color(self, hsl, ev=None):
        if hsl:
            self.hsl = hsl
        else:
            self.hsl = self.oldhsl
        self.sqr.set_facecolor(self.color_func(*self.hsl) if self.hsl else self.bg)

    def select(self):
        self.oldhsl = self.hsl
        if self.oldhsl:
            self.sqr2.set_linewidth(8*self.get_pixpt())
            self.sqr2.set_facecolor(self.color_func(*self.oldhsl))
            self.sqr2.set_fill(True)
            self.sqr.set_linewidth(0)
            self.sqr.set_bounds((0.2,0.2,0.6,0.6))
            self.sqr.set_fill(True)
        else:
            self.sqr.set_linewidth(8*self.get_pixpt())
        self.select_func(self)

    def unselect(self):
        if self.oldhsl:
            self.sqr2.set_linewidth(2*self.get_pixpt())
            self.sqr2.set_facecolor(self.color_func(*self.hsl))
            self.sqr.set_fill(False)
        else:
            self.sqr.set_linewidth(2*self.get_pixpt())

    def button_press_event(self, event):
        if self.button_tuple and self.button_tuple[0]:
            self.button_tuple[0](event, self)

    def motion_notify_event(self, event):
        if self.button_tuple and self.button_tuple[1]:
            self.button_tuple[1](event, self)

    def button_release_event(self, event):
        if self.button_tuple and self.button_tuple[2]:
            self.button_tuple[2](event, self)

    def key_press_event(self, event):
        if self.key_dict and event.key in self.key_dict:
            self.key_dict[event.key](event, self)


class CCEffect(CCWidget):
    def __init__(self, fig, rect, bg, label, func1, func2, data):
        super(CCEffect, self).__init__(fig, rect)
        self.func1 = func1
        self.func2 = func2
        self.data = data
        self.label = label
        self.gr0 = bg
        self.gr1 = gray(0.25)
        self.gr2 = gray(0.4)
        self.gr3 = gray(0.65)
        self.gr4 = gray(0.75)
        self.circ1 = mpl.patches.Ellipse(
            (0.5, 0.5), 0.8, 0.8, linewidth=0, edgecolor=self.gr2, facecolor=self.gr0
        )
        self.circ2 = mpl.patches.Ellipse(
            (0.5, 0.5), 0.8, 0.8, linewidth=0, edgecolor=self.gr1, fill=False
        )
        self.circ3 = mpl.patches.Ellipse(
            (0.5, 0.5), 0.8, 0.8, linewidth=0, edgecolor=self.gr3, fill=False
        )
        self.circ4 = mpl.patches.Ellipse(
            (0.5, 0.5), 0.8, 0.8, linewidth=0, edgecolor=self.gr2, fill=False)
        self.txt = plt.Text(0.5, 0.5, label, ha='center', va='center')
        self.ax.add_artist(self.circ1)
        self.ax.add_artist(self.circ2)
        self.ax.add_artist(self.circ3)
        self.ax.add_artist(self.circ4)
        self.ax.add_artist(self.txt)
        self.pressed = False
        self.resize()
        self.redraw()

    def resize(self):
        self.size = min(self.get_width(), self.get_height())
        xoff = (1.0 - self.size/self.get_width()) / 2
        yoff = (1.0 - self.size/self.get_height()) / 2
        dpix = self.size/15
        dx = dpix/self.get_width()
        dy = dpix/self.get_height()
        self.toff = -0.3*dy
        for circ in [self.circ1, self.circ2, self.circ3, self.circ4]:
            circ.width = 1.0 - 4*dx - 2*xoff
            circ.height = 1.0 - 4*dy - 2*yoff
        self.circ2.set_center((0.5+dx/3, 0.5-dy/3))
        self.circ3.set_center((0.5-dx/3, 0.5+dy/3))
        self.circ1.set_linewidth(2*dpix*self.get_pixpt())
        for circ in [self.circ2, self.circ3]:
            circ.set_linewidth(dpix*self.get_pixpt())
        self.circ4.set_linewidth(dpix*self.get_pixpt() / 1.5)
        self.txt.set_fontsize(self.size/7*self.get_pixpt())

    def redraw(self):
        if self.pressed:
            self.circ1.set_facecolor(self.gr4)
            self.txt.set_position((0.5, 0.5 + self.toff))
        else:
            self.circ1.set_facecolor(self.gr0)
            self.txt.set_position((0.5, 0.5))

    def button_press_event(self, event):
        if self.pressed:
            self.pressed = False
        else:
            self.pressed = True
            self.redraw()
            self.refresh()
            self.func1(self, self.data)

    def button_release_event(self, event):
        if not self.pressed:
            self.func2(self, self.data)
            self.redraw()


class CCButton(CCWidget):
    def __init__(self, fig, rect, bg, label, func):
        super(CCButton, self).__init__(fig, rect)
        self.label = label
        self.func = func
        self.gr0 = bg
        self.gr1 = gray(0.25)
        self.gr2 = gray(0.4)
        self.gr3 = gray(0.65)
        self.gr4 = gray(0.75)
        pth = mpl.path.Path(((0.5, 0.5),(0.5, 0.5)), (mpl.path.Path.MOVETO, mpl.path.Path.LINETO))
        self.pa1 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr2, facecolor=self.gr0
        )
        self.pa2 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr1, fill=False
        )
        self.pa3 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr3, fill=False
        )
        self.pa4 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr2, fill=False)
        self.txt = plt.Text(0.5, 0.5, label, ha='center', va='center')
        self.ax.add_artist(self.pa1)
        self.ax.add_artist(self.pa2)
        self.ax.add_artist(self.pa3)
        self.ax.add_artist(self.pa4)
        self.ax.add_artist(self.txt)
        self.resize()

    def make_path(self, marg, rnd, off, ar):
        x1, x2 = (marg+off)/ar, (marg+rnd+off)/ar
        x3, x4 = 1.0-(marg+rnd-off)/ar, 1.0-(marg-off)/ar
        y1, y2 = marg-off, marg+rnd-off
        y3, y4 = 1.0-marg-rnd-off, 1.0-marg-off
        c = [mpl.path.Path.MOVETO, mpl.path.Path.CURVE3, mpl.path.Path.CURVE3,
             mpl.path.Path.LINETO, mpl.path.Path.CURVE3, mpl.path.Path.CURVE3,
             mpl.path.Path.LINETO, mpl.path.Path.CURVE3, mpl.path.Path.CURVE3,
             mpl.path.Path.LINETO, mpl.path.Path.CURVE3, mpl.path.Path.CURVE3,
             mpl.path.Path.LINETO]
        v = ((x3, y4), (x4, y4), (x4, y3), (x4, y2), (x4, y1), (x3, y1),
             (x2, y1), (x1, y1), (x1, y2), (x1, y3), (x1, y4), (x2, y4), (x3, y4))
        return mpl.path.Path(v, c)

    def resize(self):
        self.size = self.get_height()
        self.ar = self.get_width() / self.get_height()
        dpix = self.size/15
        dx = dpix/self.get_width()
        dy = dpix/self.get_height()
        self.toff = -0.3*dy
        self.pa1.set_path(self.make_path(0.1, 0.25, 0.0, self.ar))
        self.pa2.set_path(self.make_path(0.1, 0.25, dy/3, self.ar))
        self.pa3.set_path(self.make_path(0.1, 0.25, -dy/3, self.ar))
        self.pa4.set_path(self.make_path(0.1, 0.25, 0.0, self.ar))
        self.pa1.set_linewidth(2*dpix*self.get_pixpt())
        for pa in [self.pa2, self.pa3]:
            pa.set_linewidth(dpix*self.get_pixpt())
        self.pa4.set_linewidth(dpix*self.get_pixpt() / 1.5)
        self.txt.set_fontsize(self.size/4*self.get_pixpt())
    
    def redraw(self, pressed):
        if pressed:
            self.pa1.set_facecolor(self.gr4)
            self.txt.set_position((0.5, 0.5 + self.toff))
        else:
            self.pa1.set_facecolor(self.gr0)
            self.txt.set_position((0.5, 0.5))
    
    def button_press_event(self, event):
        self.redraw(True)
        self.refresh()
        self.func()

    def button_release_event(self, event):
        self.redraw(False)


class CCGlyph(CCWidget):
    def __init__(self, fig, rect, pathdescr, func1, func2, toggle=False):
        super(CCGlyph, self).__init__(fig, rect)
        self.descr = pathdescr
        self.func1 = func1
        self.func2 = func2
        self.toggle = toggle
        self.pressed = False
        self.gr1 = gray(0.25)
        self.gr2 = gray(0.4)
        self.gr3 = gray(0.65)
        self.gr4 = gray(0.75)
        pth = mpl.path.Path(((0.5, 0.5),(0.5, 0.5)), (mpl.path.Path.MOVETO, mpl.path.Path.LINETO))
        self.pa1 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr2, fill=False
        )
        self.pa2 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr1, fill=False
        )
        self.pa3 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr3, fill=False
        )
        self.pa4 = mpl.patches.PathPatch(
            pth, linewidth=0, edgecolor=self.gr2, fill=False)
        self.ax.add_artist(self.pa1)
        self.ax.add_artist(self.pa2)
        self.ax.add_artist(self.pa3)
        self.ax.add_artist(self.pa4)
        self.resize()

    def make_path(self, marg, off, ar):
        if ar >= 1.0:
            scx = (1.0 - 2*marg)/ar
            offx = (1.0 - 1.0/ar)/2 + (marg + off)/ar
            scy = (1.0 - 2*marg)
            offy = marg - off
        else:
            scx = (1.0 - 2*marg)
            offx = marg + off
            scy = ar*(1.0 - 2*marg)
            offy = (1.0 - ar)/2 + (marg - off)*ar
        c = [ [mpl.path.Path.MOVETO, mpl.path.Path.LINETO, mpl.path.Path.CURVE3][t[0]] for t in self.descr ]
        v = [ (offx + scx*t[1], offy + scy*t[2]) for t in self.descr ]
        return mpl.path.Path(v, c)

    def resize(self):
        self.size = min(self.get_width(), self.get_height())
        self.ar = self.get_width() / self.get_height()
        dpix = self.size/15
        dx = dpix/self.get_width()
        dy = dpix/self.get_height()
        self.pa1.set_path(self.make_path(0.1, 0.0, self.ar))
        self.pa2.set_path(self.make_path(0.1, dy/3, self.ar))
        self.pa3.set_path(self.make_path(0.1, -dy/3, self.ar))
        self.pa4.set_path(self.make_path(0.1, 0.0, self.ar))
        self.pa1.set_linewidth(2*dpix*self.get_pixpt())
        for pa in [self.pa2, self.pa3]:
            pa.set_linewidth(dpix*self.get_pixpt())
        self.pa4.set_linewidth(dpix*self.get_pixpt()) #  / 1.5
    
    def redraw(self, pressed):
        if pressed:
            self.pa2.set_edgecolor(self.gr3)
            self.pa3.set_edgecolor(self.gr1)
        else:
            self.pa2.set_edgecolor(self.gr1)
            self.pa3.set_edgecolor(self.gr3)

    def button_press_event(self, event):
        if self.toggle and self.pressed:
            self.pressed = False
        else:
            self.pressed = True
            self.redraw(True)
            if self.func1:
                self.refresh()
                self.func1()

    def button_release_event(self, event):
        if not self.toggle or not self.pressed:
            self.pressed = False
            self.redraw(False)
            if self.func2:
                self.refresh()
                self.func2()


