import os
import unittest
from tempfile import mkdtemp

import pypdftk

TEST_PDF_PATH = 'test_files/python-guide.pdf'
TEST_XFDF_PATH = 'test_files/simple.xfdf'

class TestPyPDFTK(unittest.TestCase):
    def test_get_num_pages(self):
        num = pypdftk.get_num_pages(TEST_PDF_PATH)
        self.assertEqual(num, 129)

    @unittest.skip('Not implemented yet')
    def test_fill_form(self):
        pass

    @unittest.skip('Not implemented yet')
    def dump_data_fields(self):
        pass

    @unittest.skip('Not implemented yet')
    def text_fill_form(self):
        # (pdf_path, datas={}, out_file=None, flatten=True):
        pass

    def test_concat(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        output_file = pypdftk.concat([TEST_PDF_PATH, TEST_PDF_PATH, TEST_PDF_PATH])
        concat_total_pages = pypdftk.get_num_pages(output_file)
        self.assertEqual(total_pages * 3, concat_total_pages)

    def test_split(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        paths = pypdftk.split(TEST_PDF_PATH)
        self.assertEqual(len(paths) - 1, total_pages)
        self.assertTrue('doc_data.txt' in paths[0])
        for p in paths:
            self.assertTrue(os.path.exists(p))

    def test_split_output_dir(self):
        output_dir = mkdtemp()
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        paths = pypdftk.split(TEST_PDF_PATH, out_dir=output_dir)
        self.assertEqual(len(paths) - 1, total_pages)
        for p in paths:
            out_path = os.path.join(output_dir, os.path.basename(p))
            self.assertTrue(out_path)

    def test_gen_xfdf(self):
        sample_data = {
            "name": "juju",
            "city": "Paris"
        }
        xfdf_path = pypdftk.gen_xfdf(sample_data)
        xfdf = "".join(open(xfdf_path, 'r').readlines())
        expected = "".join(open(TEST_XFDF_PATH, 'r').readlines())
        self.assertEqual(xfdf, expected)

    def test_replace_page_at_begin(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(TEST_PDF_PATH, 1, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_PATH))

    def test_replace_page_at_middle(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(TEST_PDF_PATH, 3, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_PATH))

    def test_replace_page_at_end(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        last_page = pypdftk.get_num_pages(TEST_PDF_PATH)
        pdf_to_insert = 'test_files/page_01.pdf'
        pypdftk.replace_page(TEST_PDF_PATH, last_page, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_PATH))

    @unittest.skip('Not implemented yet')
    def test_stamp(self):
        pass


if __name__ == '__main__':
    unittest.main()