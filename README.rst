pypdftk |pypi| |travis| |githubactions|
===========================================

Python module to drive the awesome `pdftk`_ binary.

Proudly brought to you by many `awesome contributors`_

Features
--------

``fill_form``
~~~~~~~~~~~~~

Fill a PDF with given data and returns the output PDF path

-  ``pdf_path`` : input PDF
-  ``datas`` : dictionnary of fielf names / values
-  ``out_file`` (default=auto) : output PDF path. will use tempfile if
   not provided
-  ``flatten`` (default=True) : flatten the final PDF
-  ``drop_xfa`` (default=False) : omit XFA data from the output PDF

``concat``
~~~~~~~~~~

Merge multiple PDFs into one single file and returns the output PDF path

-  ``files`` : list of PDF files to concatenate
-  ``out_file`` (default=auto) : output PDF path. will use tempfile if
   not provided

``get_pages``
~~~~~~~~~~~~~

Concatenate a list of page ranges into one single file and returns the
output PDF path

-  ``pdf_path`` : input PDF
-  ``ranges`` (default=\ ``[]``) : ``[]`` for clone, ``[[2]]`` for
   extracting 2nd page, ``[[1],[2,5],[3]]`` for concatenating pages 1,
   2-5, 3
-  ``out_file`` (default=auto) : output PDF path. will use tempfile if
   not provided

``split``
~~~~~~~~~

Split a single PDF in many pages and return a list of pages paths

-  ``pdf_path`` : input PDF
-  ``out_dir`` (default=auto) : output PDFs dir. will use tempfile if
   not provided

**warning** if you give a out_dir parameter, ensure its empty, or the
split function may destroy your files and return incorrect results.

``gen_xfdf``
~~~~~~~~~~~~

Generate a XFDF file suited for filling PDF forms and return the
generated XFDF file path

-  ``datas`` : dictionnary of datas

``get_num_pages``
~~~~~~~~~~~~~~~~~

Return the number of pages for a given PDF

-  ``pdf_path`` : input PDF file

``replace_page``
~~~~~~~~~~~~~~~~

Replace a page in a PDF (pdf_path) by the PDF pointed by
pdf_to_insert_path.

-  ``pdf_path`` is the PDF that will have its page replaced.
-  ``page_number`` is the number of the page in pdf_path to be replaced.
   It is 1-based.
-  ``pdf_to_insert_path`` is the PDF that will be inserted at the old
   page.

``stamp``
~~~~~~~~~

Applies a stamp (from ``stamp_pdf_path``) to the PDF file in
``pdf_path``. If no ``output_pdf_path`` is provided, it returns a
temporary file with the result PDF.

``[compress | uncompress]``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   These are only useful when you want to edit PDF code in a text
   editor like vim or emacs.  Remove PDF page stream compression by
   applying the uncompress filter. Use the compress filter to
   restore compression.

-  ``pdf_path`` : input PDF file
-  ``out_file`` (default=auto) : output PDF path. will use tempfile if
   not provided
-  ``flatten`` (default=True) : flatten the final PDF

``dump_data_fields``
~~~~~~~~~~~~~~~~~~~~

Read PDF and output form field statistics.

-  ``pdf_path`` : input PDF file

``dump_data``
~~~~~~~~~~~~~~~~~~~~

Read PDF and output metadata, bookmarks, page metrics.

-  ``pdf_path`` : input PDF file
-  ``out_file`` (default=None) : text file containing dumped data


``update_info``
~~~~~~~~~~~~~~~~~~~~

Read PDF ``pdf_path``, update metadata according to ``info_data`` and
write the finale PDF to ``out_file``.

-  ``pdf_path`` : input PDF file
-  ``info_data`` : text file containing new info data
-  ``out_file`` : output PDF file


Example
-------

Fill a PDF model and add a cover page :

.. code:: python

   import pypdftk

   datas = {
       'firstname': 'Julien',
       'company': 'revolunet',
       'price': 42
   }
   generated_pdf = pypdftk.fill_form('/path/to/model.pdf', datas)
   out_pdf = pypdftk.concat(['/path/to/cover.pdf', generated_pdf])

pdftk path
----------

By default, path is ``/usr/bin/pdftk``, but you can override it with the
``PDFTK_PATH`` environment variable

Licence
-------

This module is released under the permissive `MIT license`_. Your
contributions are always welcome.

.. _pdftk: http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/
.. _revolunet: http://revolunet.com
.. _awesome contributors: https://github.com/revolunet/pypdftk/graphs/contributors
.. _MIT license: http://revolunet.mit-license.org

.. |pypi| image:: https://img.shields.io/pypi/v/pypdftk
   :target: https://pypi.org/project/pypdftk/
.. |travis| image:: https://travis-ci.org/yguarata/pypdftk.svg?branch=master
   :target: https://travis-ci.org/yguarata/pypdftk
.. |githubactions| image:: https://github.com/revolunet/pypdftk/actions/workflows/quality.yml/badge.svg

