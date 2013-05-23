pypdftk
========

Python module to drive the awesome [pdftk][0] binary.

Proudly brought to you by the [revolunet][1] team

## Features

### `fill_form`
Fill a PDF with given data and returns the output PDF path
 - `pdf_path` : input PDF
 - `datas` : dictionnary of fielf names / values
 - `out_file` (default=auto) : output PDF path. will use tempfile if not provided
 - `flatten` (default=True) : flatten the final PDF
 
### `concat`
Merge multiple PDFs into one single file and returns the output PDF path
 - `files` : list of PDF files to concatenate
 - `out_file` (default=auto) : output PDF path. will use tempfile if not provided

### `split`
Split a single PDF in many pages and return a list of pages paths
 - `pdf_path` : input PDF
 - `out_dir` (default=auto) : output PDFs dir. will use tempfile if not provided

**warning** if you give a out_dir parameter, ensure its empty, or the split function may destroy your files and return incorrect results.

### `gen_xfdf`
Generate a XFDF file suited for filling PDF forms and return the generated XFDF file path
 - `datas` : dictionnary of datas
 
### `get_num_pages`
Return the number of pages for a given PDF
 - `pdf_path` : input PDF file




## Example

Fill a PDF model and add a cover page :

```python

import pypdftk

datas = {
    'firstname': 'Julien',
    'company': 'revolunet',
    'price': 42
}
generated_pdf = pypdftk.fill_form('/path/to/model.pdf', datas)
out_pdf = pypdftk.merge(['/path/to/cover.pdf', generated_pdf])
```



## Licence
This module is released under the permissive [MIT license](http://revolunet.mit-license.org). Your contributions are always welcome.


 [0]: http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/
 [1]: http://revolunet.com
