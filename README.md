pdftk.py
========

Python module to drive the awesome [pdftk][0] binary.

Proudly brought to you by the [revolunet][1] team

## Features

 - `fill_form` : fill a PDF with given data
 - `merge` : merge multiple PDFs into one
 - `split` : split a single PDF in many pages
 - `gen_xfdf` : generate a XFDF file suited for filling PDF forms
 - `get_num_pages` : return number of pages for a given PDF

By default, all the output use temporary files, and you can override this.


## Example

Fill a PDF model and add a cover page :

```python

import pdftk

datas = {
    'firstname': 'Julien',
    'company': 'revolunet',
    'price': 42
}
generated_pdf = pdftk.fill_form('/path/to/model.pdf', datas)
out_pdf = pdftk.merge(['/path/to/cover.pdf', generated_pdf])
```




 [0]: http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/
 [1]: http://revolunet.com
