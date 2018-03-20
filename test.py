import os
import unittest
import tempfile

import pypdftk

TEST_PDF_01_PATH = 'test_files/test_pdf_01.pdf'
TEST_PDF_02_PATH = 'test_files/test_pdf_02.pdf'


class TestPyPDFTK(unittest.TestCase):
    def test_get_num_pages(self):
        num = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        self.assertEqual(num, 129)

    @unittest.skip('Not implemented yet')
    def test_fill_form(self):
        pass

    def test_concat(self):
        files = [TEST_PDF_01_PATH, TEST_PDF_02_PATH]
        expected_total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH) + \
                               pypdftk.get_num_pages(TEST_PDF_02_PATH)
        temp_pdf = tempfile.mktemp(suffix='.pdf')
        pypdftk.concat(files, out_file=temp_pdf)
        self.assertEqual(expected_total_pages, pypdftk.get_num_pages(temp_pdf))

    def test_split(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        paths = pypdftk.split(TEST_PDF_01_PATH)
        self.assertEqual(len(paths) - 1, total_pages)
        self.assertTrue('doc_data.txt' in paths[0])
        for p in paths:
            self.assertTrue(os.path.exists(p))

    def test_split_output_dir(self):
        output_dir = tempfile.mkdtemp()
        total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        paths = pypdftk.split(TEST_PDF_01_PATH, out_dir=output_dir)
        self.assertEqual(len(paths) - 1, total_pages)
        for p in paths:
            out_path = os.path.join(output_dir, os.path.basename(p))
            self.assertTrue(out_path)

    def test_gen_xfdf(self):
        output_baseline = """
        <?xml version="1.0" encoding="UTF-8"?>
        <xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">
            <fields>
                <field name="field_02"><value>value_02</value></field>
                <field name="field_01"><value>value_01</value></field>
            </fields>
        </xfdf>
        """

        out_file = pypdftk.gen_xfdf({
            'field_01': 'value_01',
            'field_02': 'value_02'
        })
        with open(out_file) as fd:
            self.assertEqual(''.join(fd.read().split()),
                             ''.join(output_baseline.split()))

    def test_replace_page_at_begin(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        pdf_to_insert = TEST_PDF_02_PATH
        pypdftk.replace_page(TEST_PDF_01_PATH, 1, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_01_PATH))

    def test_replace_page_at_middle(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        pdf_to_insert = TEST_PDF_02_PATH
        pypdftk.replace_page(TEST_PDF_01_PATH, 3, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_01_PATH))

    def test_replace_page_at_end(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        last_page = pypdftk.get_num_pages(TEST_PDF_01_PATH)
        pdf_to_insert = TEST_PDF_02_PATH
        pypdftk.replace_page(TEST_PDF_01_PATH, last_page, pdf_to_insert)
        self.assertEqual(total_pages, pypdftk.get_num_pages(TEST_PDF_01_PATH))

    def test_stamp(self):
        temp_pdf = tempfile.mktemp(suffix='.pdf')
        stamp_path = TEST_PDF_02_PATH
        pypdftk.stamp(TEST_PDF_01_PATH, stamp_path, output_pdf_path=temp_pdf)
        self.assertEqual(pypdftk.get_num_pages(TEST_PDF_01_PATH),
                         pypdftk.get_num_pages(temp_pdf))


if __name__ == '__main__':
    unittest.main()