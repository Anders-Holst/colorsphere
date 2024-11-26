__version__ = '0.1.1'

_classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]

readme =  """
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
either by dragging the surface, or using the arrow keys. The scroll
wheel takes you inside the sphere.

In the default usage, clicking a color in the sphere will print out
its RGB and HSL (hue, saturation, lightness) color coordinates.
However, the main purpose is to use it as a color picker from within
other python programs.
"""

def _run_setup():
    from setuptools import setup

    setup(
        name='colorsphere',
        version=__version__,
        author='Anders Holst',
        author_email='anders.holst@ri.se',
        url='https://github.com/Anders-Holst/colorsphere',
        packages=['colorsphere'],
        description='Select colors on a 3D sphere',
        long_description=readme,
        license='MIT',
        classifiers=_classifiers,
        keywords=['graphics'],
        install_requires=['matplotlib','numpy'],
    )


if __name__ == '__main__':
    _run_setup()
