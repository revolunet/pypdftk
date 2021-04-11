#!/usr/bin/env python
from distutils.core import setup

setup(
    name='pypdftk',
    description='''Python wrapper for PDFTK''',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    version='0.4',
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
