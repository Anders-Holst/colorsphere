"""
colorsphere.colorsphere
~~~~~~~~~~~~~~~~~~~~~~~

Author: Anders Holst (anders.holst@ri.se), 2021

This module implements an interactive 3-dimensional color picker -
to the author's knowledge the first ever 3-dimensional color picker.

The main entrypoint is the class ColorPicker, which takes one callback
function to call whenever a color is clicked, and another callback
function to call when the mouse moves. Both callback functions
takes the hsl-coordinates under the mouse (or False if outside the
sphere) and the click event as arguments.

The color sphere represents the whole color body, where one pole
is black, the other pole is white, and the color circle is around the
equator. If you follow a meridian from the black pole, the color will
gradually increase in strength to its maximum brilliance and then
seamlessly continue to become brighter all the way to white. Less
saturated colors are inside the sphere. The axis through the middle of
the sphere between the poles contains all grays from black to
white. Thus, the hue is represented by the longitude, the lightness by
the latitude, and the saturation by the proportion from the surface to
the center black-white axis of the sphere. You can rotate the sphere
either by dragging the surface, or using the scroll wheel. Shift-
scrolling goes sideways. Control scrolling goes inside the spere.

The module requires matplotlib and numpy, and a fairly fast computer to
run.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from math import floor, sqrt, sin, cos, atan2, acos, pi

from .windowmgr import WindowMgr


class ColorSphere:
    def __init__(self, fig, rect, wdt, hgt, pixpt, callback, useevent=False):
        self.setup_color_body()
        self.callback = callback
        self.useevent = useevent
        self.mouse_color_callbacks = []
        self.color_style_callbacks = []
        self.block_draw = False
        self.lastbpos = False
        self.p1 = False
        self.fig = fig
        self.rect = rect
        self.resize(wdt, hgt)
        self.pixpt = pixpt
        self.diam = 1.0
        cent = (0, 0)
        self.ax = fig.add_axes(rect, frame_on=False, xticks=[], yticks=[])
        self.gray1 = self.hsl_color(0.0, 0.0, 0.0)
        self.gray2 = self.hsl_color(0.0, 0.0, 0.5)
        self.im = self.ax.imshow([[self.gray1]], origin="lower")
        diameps = 0.5 * 10 / self.size
        self.circ2 = mpl.patches.Ellipse(
            cent, self.diam, self.diam, linewidth=0, edgecolor=self.gray2, fill=False
        )
        self.circ1 = mpl.patches.Ellipse(
            cent, self.diam + diameps, self.diam + diameps, linewidth=10 * self.pixpt, edgecolor=self.gray1, fill=False
        )
        self.ax.add_artist(self.circ2)
        self.ax.add_artist(self.circ1)
        self.rad = 1.0
        self.eye = self.origmatrix()
        self.draw()

    def resize(self, newwdt, newhgt):
        self.size = min(newwdt * self.rect[2], newhgt * self.rect[3])
        self.xoff = newwdt * (self.rect[0] + self.rect[2] / 2) - self.size / 2
        self.yoff = newhgt * (self.rect[1] + self.rect[3] / 2) - self.size / 2
        self.dotsz = self.size / 100.0
        xx = np.array([i for j in range(101) for i in range(101)])
        yy = np.array([j for j in range(101) for i in range(101)])
        self.xxarr = xx * self.dotsz / (self.size * 0.5) - 1.0
        self.yyarr = yy * self.dotsz / (self.size * 0.5) - 1.0

    def setup_color_body(self):
        self.ramp_n = {}
        self.ramp_v = {}
        self.ramp_d = {}
        ramp = {}
        ramp["3col"] = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.5], [0.0, 1.0, 0.0], [0.5, 0.5, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.0, 0.0, 1.0]]
        ramp["4col"] = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.5], [0.0, 1.0, 0.0], [0.25, 0.75, 0.0], [0.5, 0.5, 0.0], [0.75, 0.25, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.0, 0.0, 1.0]]
        ramp["6col"] = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.5], [0.0, 1.0, 0.0], [0.25, 0.75, 0.0], [0.5, 0.5, 0.0], [0.625, 0.375, 0.0], [0.75, 0.25, 0.0], [0.875, 0.125, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [1.0 / 3, 0.0, 2.0 / 3], [1.0 / 6, 0.0, 5.0 / 6], [0.0, 0.0, 1.0]]
        ramp["8col"] = [[0.0, 0.0, 1.0], [0.0, 0.5, 0.5], [0.0, 1.0, 0.0], [0.5, 0.5, 0.0], [0.75, 0.25, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.25, 0.0, 0.75], [0.0, 0.0, 1.0]]
        ramp["10col"] = [[0.0, 0.0, 1.0], [0.0, 0.25, 0.75], [0.0, 0.5, 0.5], [0.0, 1.0, 0.0], [0.5, 0.5, 0.0], [4.0 / 6, 2.0 / 6, 0.0], [5.0 / 6, 1.0 / 6, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.5], [0.25, 0.0, 0.75], [0.0, 0.0, 1.0]]
        for key in ramp:
            self.ramp_n[key] = len(ramp[key]) - 1
            self.ramp_v[key] = np.array(
                list(map(lambda x: x + [max(x)], ramp[key]))
            ).transpose()
            self.ramp_d[key] = np.array(
                list(map(lambda v: np.append(v[1:], v[-1]) - v, self.ramp_v[key]))
            )
        self.brightness = [0.25, 0.54, 0.21]
        self.color_style = ["8col", "equilight"]

    def set_color_style(self, style):
        if type(style) in [list, tuple] and len(style) == 2:
            self.color_style[0] = style[0]
            self.color_style[1] = style[1]
        elif style in ["linear", "equilight"]:
            self.color_style[1] = style
        elif style in self.ramp_n:
            self.color_style[0] = style
        for func in self.color_style_callbacks:
            func(self.color_style)
        self.draw()

    def colorgamma(self, x):
        return (pow(x, 1.0 / 2.4) * 1.055 - 0.055) if x > 0.0031308 else x * 12.92

    def invcolorgamma(self, x):
        return pow((x + 0.055) / 1.055, 2.4) if x > 0.04045 else x / 12.92

    def hsl_color(self, hue, sat, light):
        tmp = hue * self.ramp_n[self.color_style[0]]
        hind = int(floor(tmp))
        hprop = tmp % 1.0
        rgbm = tuple(
            map(
                lambda v, d: v[hind] + d[hind] * hprop,
                self.ramp_v[self.color_style[0]],
                self.ramp_d[self.color_style[0]],
            )
        )
        rgb = tuple(map(lambda x: x / rgbm[3], rgbm[0:3]))
        ll = (light + 1.0) * 0.5
        if self.color_style[1] == "linear":
            if ll < 0.5:
                t1 = light + 1.0
                t2 = 0.0
            else:
                t1 = 1.0 - light
                t2 = light
        else:
            br = sum(map(lambda c, b: c * b, rgb, self.brightness))
            p = min(1.0, (1.0 - ll) / (1.0 - br), (1.0 - ll) / (1.0 - self.brightness[1]))
            t1 = ll * p / ((br - 1.0) * p + 1.0)
            t2 = max(0.0, ll - t1 * br)
        t1 = sat * t1
        t2 = sat * t2 + ll * (1.0 - sat)
        return tuple(map(lambda c: self.colorgamma(max(0.0, min(1.0, c * t1 + t2))), rgb))

    def rotxmatrix(self, ang):
        sa = sin(ang)
        ca = cos(ang)
        return np.matrix([[ca, 0, sa], [0, 1, 0], [-sa, 0, ca]])

    def rotymatrix(self, ang):
        sa = sin(ang)
        ca = cos(ang)
        return np.matrix([[1, 0, 0], [0, ca, sa], [0, -sa, ca]])

    def origmatrix(self):
        return np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])

    def coordinates(self, xx, yy):
        x = xx / (self.size * 0.5) - 1.0
        y = yy / (self.size * 0.5) - 1.0
        p2 = x * x + y * y
        r2 = self.rad * self.rad
        if p2 > r2 + 2.0 * self.rad * self.dotsz / (self.size * 0.5):
            return False
        z = sqrt(max(0.0, r2 - p2))
        pe = list(map(lambda v: v[0], self.eye * [[x], [y], [z]]))
        hue = (atan2(pe[0], pe[1]) / (2 * pi)) % 1.0
        if self.rad < 1.0:
            q1 = pe[0] * pe[0] + pe[1] * pe[1]
            q2 = max(0.0, 1.0 - pe[2] * pe[2])
            sat = sqrt(q1 / q2) if q2 > q1 else 1.0
        else:
            sat = 1.0
        light = 1.0 - 2.0 * acos(max(-1.0, min(1.0, pe[2]))) / pi
        return (hue, sat, light)

    def draw(self, event=None):
        if not self.block_draw:
            ndiam = self.diam * (0.5 + self.rad / 2.0)
            self.circ2.width = ndiam
            self.circ2.height = ndiam
            self.circ2.set_linewidth((1.0 - ndiam / self.diam) * self.size * self.pixpt)
            arr = self.calc_coordinates_color_array()
            self.im.set_array(arr)
            if event and self.mouse_color_callbacks:
                self.block_draw = True
                self.color_change_event(event)
                self.block_draw = False
            if not plt.isinteractive():
                self.fig.canvas.draw()

    def scroll_event(self, event):
        changed = False
        if event.key == "control":
            if event.button == "up":
                self.eye = self.eye * self.rotxmatrix(-5.0 * pi / 180.0)
                changed = True
            elif event.button == "down":
                self.eye = self.eye * self.rotxmatrix(5.0 * pi / 180.0)
                changed = True
        elif event.key == "shift":
            if event.button == "up":
                self.eye = self.eye * self.rotymatrix(-5.0 * pi / 180.0)
                changed = True
            elif event.button == "down":
                self.eye = self.eye * self.rotymatrix(5.0 * pi / 180.0)
                changed = True
        else:
            if event.button == "up":
                if self.rad < 1.0:
                    self.rad = min(1.0, self.rad + 0.01)
                    changed = True
            elif event.button == "down":
                if self.rad > 0.01:
                    self.rad = max(0.01, self.rad - 0.01)
                    changed = True
        if changed:
            self.draw(event)

    def button_press_event(self, event):
        self.lastbpos = (event.x, event.y)
        self.starteye = self.eye
        x = (event.x - self.xoff) / (self.size * 0.5) - 1.0
        y = (event.y - self.yoff) / (self.size * 0.5) - 1.0
        rr2 = x * x + y * y
        r2 = self.rad * self.rad
        if rr2 <= r2 + 2.0 * self.rad * self.dotsz / (self.size * 0.5):
            self.p1 = np.array([x, y, sqrt(max(0.0, r2 - rr2))])
        else:
            self.p1 = False

    def button_release_event(self, event):
        if self.lastbpos == (event.x, event.y):
            if event.button == 1 and self.callback:
                coord = self.coordinates(event.x - self.xoff, event.y - self.yoff)
                if coord:
                    if self.useevent:
                        self.callback(coord, event)
                    else:
                        self.callback(coord)

    def motion_notify_event(self, event):
        if self.p1 is not False:
            x = (event.x - self.xoff) / (self.size * 0.5) - 1.0
            y = (event.y - self.yoff) / (self.size * 0.5) - 1.0
            p2 = np.array([x, y, sqrt(max(0.0, self.rad * self.rad - x * x - y * y))])
            p1 = self.p1
            q = np.cross(p1, p2)
            norm = np.vdot(q, q)
            if norm == 0.0:
                self.eye = self.starteye
            else:
                q = q / sqrt(norm)
                a = atan2(-q[1], q[2])
                b = atan2(sqrt(q[1] * q[1] + q[2] * q[2]), q[0])
                v = atan2(np.vdot(np.cross(q, p1), p2), np.vdot(p1, p2))
                tt = self.rotxmatrix(b) * self.rotymatrix(a)
                self.eye = self.starteye * tt.transpose() * self.rotymatrix(v) * tt
            self.draw()

    def color_change_event(self, event):
        hsl = self.coordinates(event.x - self.xoff, event.y - self.yoff)
        for func in self.mouse_color_callbacks:
            func(hsl, event)
        if not self.block_draw:
            if not plt.isinteractive():
                self.fig.canvas.draw()

    def key_press_event(self, event):
        changed = False
        if event.key == "right":
            self.eye = self.eye * self.rotxmatrix(-5.0 * pi / 180.0)
            changed = True
        elif event.key == "left":
            self.eye = self.eye * self.rotxmatrix(5.0 * pi / 180.0)
            changed = True
        elif event.key == "up":
            self.eye = self.eye * self.rotymatrix(-5.0 * pi / 180.0)
            changed = True
        elif event.key == "down":
            self.eye = self.eye * self.rotymatrix(5.0 * pi / 180.0)
            changed = True
        if changed:
            self.draw(event)

    def calc_coordinates_color_array(self):
        x = self.xxarr
        y = self.yyarr
        p2 = x * x + y * y
        r2 = self.rad * self.rad
        z = np.sqrt((r2 - p2 + np.abs(r2 - p2)) / 2.0)
        mask = (p2 < r2 + 2.0 * self.rad * self.dotsz / (self.size * 0.5)).astype(int)
        x = np.multiply(x, mask)
        y = np.multiply(y, mask)
        z = np.multiply(z, mask)
        pe = self.eye * [x, y, z]
        pe = (pe + 1.0 - np.abs(pe - 1.0)) / 2.0
        pe = (pe - 1.0 + np.abs(pe + 1.0)) / 2.0
        hue = (np.arctan2(pe[0], pe[1]) / (2 * pi)) % 1.0
        if self.rad < 1.0:
            qe = np.multiply(pe, pe)
            q1 = qe[0] + qe[1]
            q2 = 1.0001 - qe[2]
            sat = np.sqrt(q1 / q2)
            sat = (sat + 1.0 - np.abs(sat - 1.0)) / 2.0
        else:
            sat = np.multiply(np.ones(pe[2].shape), mask)
        light = 1.0 - 2.0 * np.arccos(pe[2]) / pi
        tmp = hue * self.ramp_n[self.color_style[0]]
        hind = np.floor(np.array(tmp)[0]).astype(int)
        hprop = tmp % 1.0
        v = np.take_along_axis(
            self.ramp_v[self.color_style[0]], np.array([hind] * 4), 1
        )
        d = np.take_along_axis(
            self.ramp_d[self.color_style[0]], np.array([hind] * 4), 1
        )
        rgbm = np.array(v + np.multiply(d, hprop))
        rgb = np.divide(np.matrix(rgbm[0:3]), rgbm[3])
        ll = (light + 1.0) * 0.5
        if self.color_style[1] == "linear":
            t1 = 1.0 - np.abs(light)
            t2 = (light + 1.0 - t1) * 0.5
        else:
            br = self.brightness * rgb
            lmin = (ll + br - np.abs(ll - br)) / 2.0
            lmin = (lmin + self.brightness[1] - np.abs(lmin - self.brightness[1])) / 2.0
            p = (1.0 - ll) / (1.0 - lmin)
            t1 = np.multiply(ll, p) / (np.multiply(br - 1.0, p) + 1.0)
            t2 = ll - np.multiply(t1, br)
        t1 = np.multiply(sat, t1)
        t2 = np.multiply(sat, t2) + np.multiply(ll, 1.0 - sat)
        rgb = np.add(np.multiply(rgb, t1), t2)
        rgb = (rgb + 1.0 - np.abs(rgb - 1.0)) / 2.0
        rgb = (rgb + np.abs(rgb)) / 2.0
        #rgb = np.power(rgb, 0.417)
        rgb = np.where(rgb>0.0031308, np.power(rgb, 1.0/2.4)*1.055 - 0.055, rgb*12.92)
        return np.array(rgb.transpose()).reshape((101, 101, 3))


class ColorSample:
    def __init__(self, fig, sphere, rect, bw, initcol):
        self.fig = fig
        self.sphere = sphere
        self.ax = fig.add_axes(rect, frame_on=False, xticks=[], yticks=[])
        self.rect = rect
        self.sqr = plt.Rectangle(
            (0, 0), 1.0, 1.0, linewidth=bw, edgecolor=(0, 0, 0), facecolor=initcol
        )
        self.ax.add_artist(self.sqr)

    def set_color(self, hsl, ev=None):
        if hsl:
            self.sqr.set_facecolor(self.sphere.hsl_color(*hsl))
            # if not plt.isinteractive():
            #     self.fig.canvas.draw()


class ColorPicker:
    def __init__(self, callback_click, callback_move, name="Color Sphere"):
        width = 500
        height = 500
        rect = (0.1, 0.1, 0.8, 0.8)
        self.win = WindowMgr(name, width, height, 1, 1)
        self.sphere = ColorSphere(
            self.win.fig, rect, width, height, self.win.pixpt, callback_click, True
        )
        self.sample = ColorSample(
            self.win.fig, self.sphere, (0.04, 0.04, 0.16, 0.16), 2 * self.win.pixpt, self.sphere.hsl_color(0.0, 0.0, 1.0)
        )
        self.win.set_background(self.sphere.hsl_color(0.0, 0.0, 0.0))
        self.win.register_target(rect, self.sphere)
        self.win.add_motion_callback(self.sphere.color_change_event)
        self.win.add_resize_callback(lambda ev: self.sphere.resize(ev.width, ev.height))
        self.sphere.mouse_color_callbacks.append(self.sample.set_color)
        if callback_move:
            self.sphere.mouse_color_callbacks.append(callback_move)
            self.win.add_close_callback(lambda ev: callback_move(None, ev))
