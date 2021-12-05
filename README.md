# Colorsphere - An RGB color picker with colors arranged in a 3D sphere.

This module implements an interactive 3-dimensional color picker -
to the author's knowledge the first ever 3-dimensional color picker.

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

In the default usage, clicking a color in the sphere will print out
its RGB and HSL (hue, saturation, lightness) color coordinates.

Installs with 'pip install colorsphere'
Or, to install from this directory:

1. Create a new virtualenv
2. `python setup.py install`

To run standalone from a terminal:

`python -m colorsphere`

You can also use the ColorSphere or ColorPicker class in your own
programs, but that require some more programming of course.
