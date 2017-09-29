#!/usr/bin/python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    # Application name
    name = "pyKmlChart",
    #platform = "linux"

    # Version number
    version = "0.1.0",

    # Application author details
    author = "Hendrik Millner",
    author_email = "hendrik.millner@symeo.com",

    # Packages
    #packages = find_packages(),
    packages = [
        "kmlChart"
    ],
    #include_package_data = True,

    # Single Modules
    #py_modules = [ "" ],

    # Details
    description = "Symeo parameter and state handling",
    long_description = open( "README.md" ).read(),
    url="https://github.com/denebolar/pyKmlChart",

    # License
    license = "LICENSE",
    #license = "MIT",

    # Unit tests
    test_suite = 'tests',

    # Dependent packages (distributions)
    install_requires = [
    ],

    # Entry points
    #entry_points = {
    #    'console_scripts': [
    #        'state = state:main',
    #    ],
    #},

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: GIS',
    ],

    # Egg-safe
    #zip_safe = False    # we don't like eggs
)
