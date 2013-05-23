#!/usr/bin/env python
from distutils.core import setup

setup(
    name='PyPdfTk',
    description='''Python wrapper for PDFTK''',
    long_description=open('README.md').read(),
    version='0.1dev',
    author='Julien Bouquillon',
    author_email='julien@revolunet.com',
    url='http://github.com/revolunet/pypdftk',
    packages=['pypdftk'],
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
)
