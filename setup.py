#!/usr/bin/env python
from distutils.core import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pypdftk',
    description='''Python wrapper for PDFTK''',
    long_description=long_description,
    version='0.5',
    author='Julien Bouquillon',
    author_email='julien@revolunet.com',
    url='http://github.com/revolunet/pypdftk',
    py_modules=['pypdftk'],
    scripts=['pypdftk.py'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
