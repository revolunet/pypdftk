import os
import unittest
from tempfile import mkdtemp

import pypdftk

class TestPyPDFTK(unittest.TestCase):
    test_file_01 = 'test_files/python-guide.pdf'

    def test_get_num_pages(self):
        num = pypdftk.get_num_pages(self.test_file_01)
        self.assertEqual(num, 129)

    @unittest.skip('Not implemented yet')
    def test_fill_form(self):
        pass

    def test_concat(self):
        pass

    def test_split(self):
        paths = pypdftk.split(self.test_file_01)
        self.assertEqual(len(paths), 130)
        self.assertTrue('doc_data.txt' in paths[0])
        for p in paths:
            self.assertTrue(os.path.exists(p))

    def test_split_output_dir(self):
        output_dir = mkdtemp()
        paths = pypdftk.split(self.test_file_01, out_dir=output_dir)
        for p in paths:
            out_path = os.path.join(output_dir, os.path.basename(p))
            self.assertTrue(out_path)

    @unittest.skip('Not implemented yet')
    def test_gen_xfdf(self):
        pass

    def test_replace_page_at_begin(self):
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(self.test_file_01, 1, pdf_to_insert)

    def test_replace_page_at_middle(self):
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(self.test_file_01, 3, pdf_to_insert)

    def test_replace_page_at_end(self):
        last_page = pypdftk.get_num_pages(self.test_file_01)
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(self.test_file_01, last_page, pdf_to_insert)

    @unittest.skip('Not implemented yet')
    def test_stamp(self):
        pass


if __name__ == '__main__':
    unittest.main()