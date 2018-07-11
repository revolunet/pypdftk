# -*- encoding: UTF-8 -*-
import os
import unittest
import json
from tempfile import mkdtemp
# Needed for comparison of XFDF XML
import xml.etree.ElementTree as ET

import pypdftk

TEST_PDF_PATH = 'test_files/python-guide.pdf'
TEST_XPDF_PATH = 'test_files/form.pdf'
TEST_XPDF_DATA_DUMP = 'test_files/form.json'
TEST_XPDF_FILLED_PATH = 'test_files/form-filled.pdf'
TEST_XPDF_FILLED_DATA_DUMP = 'test_files/form-filled.json'
TEST_XFDF_PATH = 'test_files/simple.xfdf'
SAMPLE_DATA = {
    "city": "Paris",
    "name": "juju"
}
SAMPLE_DATA2 = {
    "Given Name Text Box": "name test",
    "Language 3 Check Box": "Yes"
}

def read(path):
    fd = open(path, 'r')
    content = fd.read()
    fd.close()
    return content

# json comparison... https://stackoverflow.com/a/25851972/174027
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

class TestPyPDFTK(unittest.TestCase):
    def test_get_num_pages(self):
        num = pypdftk.get_num_pages(TEST_PDF_PATH)
        self.assertEqual(num, 129)

    def test_fill_form(self):
        result = pypdftk.fill_form(TEST_XPDF_PATH, datas=SAMPLE_DATA2, flatten=False)
        result_data = ordered(pypdftk.dump_data_fields(result))
        expected_data = ordered(json.loads(read(TEST_XPDF_FILLED_DATA_DUMP)))
        self.assertEqual(result_data, expected_data)

    def test_dump_data_fields(self):
        result_data = ordered(pypdftk.dump_data_fields(TEST_XPDF_PATH))
        expected_data = ordered(json.loads(read(TEST_XPDF_DATA_DUMP)))
        self.assertEqual(result_data, expected_data)

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
        xfdf_path = pypdftk.gen_xfdf(SAMPLE_DATA)
        xfdf = read(xfdf_path)
        expected = read(TEST_XFDF_PATH)
        # XML can have sibling elements in different order. So: 
        # * Parse the XML, get list of the root's children, convert to string, sort
        xfdf_standard_order     = [ET.tostring(i) for i in list(ET.fromstring(xfdf).iter())]
        expected_standard_order = [ET.tostring(i) for i in list(ET.fromstring(expected).iter())]
        xfdf_standard_order.sort()
        expected_standard_order.sort()
        self.assertEqual(xfdf_standard_order, expected_standard_order)

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