__version__ = '0.9.0'

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


def _run_setup():
    from setuptools import setup

    with open('requirements.txt') as f:
        REQUIRED = f.read().splitlines()

    setup(
        name='colorsphere',
        version=__version__,
        author='Anders Holst',
        author_email='anders.holst@ri.se',
        url='https://github.com/rec/colorsphere',
        py_modules=['colorsphere'],
        description='Select colors on a 3D sphere',
        long_description=open('README.md').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['graphics'],
        install_requires=REQUIRED,
    )


if __name__ == '__main__':
    _run_setup()
