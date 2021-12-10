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

# Converts a page range list into the number of pages
def rangeCount(ranges):
    count = 0
    for range in ranges:
        if len(range)==1:
            count += 1
        elif len(range)==2:
            count += abs(range[0]-range[1]) + 1
        else:
            raise ValueError(str(range)+" contains more than 2 values")
    return count

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


    def test_get_pages_clone(self):
        total_pages = pypdftk.get_num_pages(TEST_PDF_PATH)
        output_file = pypdftk.get_pages(TEST_PDF_PATH,[])
        concat_total_pages = pypdftk.get_num_pages(output_file)
        self.assertEqual(total_pages, concat_total_pages)

    def test_get_pages_single(self):
        pageRanges = [[1]]
        output_file = pypdftk.get_pages(TEST_PDF_PATH,pageRanges)
        concat_total_pages = pypdftk.get_num_pages(output_file)
        self.assertEqual(rangeCount(pageRanges), concat_total_pages)

    def test_get_pages_range(self):
        pageRanges = [[2,5]]
        output_file = pypdftk.get_pages(TEST_PDF_PATH,pageRanges)
        concat_total_pages = pypdftk.get_num_pages(output_file)
        self.assertEqual(rangeCount(pageRanges), concat_total_pages)

    def test_get_pages_single_range(self):
        pageRanges = [[1],[2,5]]
        output_file = pypdftk.get_pages(TEST_PDF_PATH,pageRanges)
        concat_total_pages = pypdftk.get_num_pages(output_file)
        self.assertEqual(rangeCount(pageRanges), concat_total_pages)

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

    def test_dump_data(self):
        form_info_data = """InfoBegin
InfoKey: Keywords
InfoValue: PDF Form
InfoBegin
InfoKey: Creator
InfoValue: Writer
InfoBegin
InfoKey: CreationDate
InfoValue: D:20130629204853+02&apos;00&apos;
InfoBegin
InfoKey: Producer
InfoValue: OpenOffice.org 3.4
InfoBegin
InfoKey: Title
InfoValue: PDF Form Example
PdfID0: 5e0a553555622a0516e9877ca55217a6
PdfID1: 5e0a553555622a0516e9877ca55217a6
NumberOfPages: 1
PageMediaBegin
PageMediaNumber: 1
PageMediaRotation: 0
PageMediaRect: 0 0 595 842
PageMediaDimensions: 595 842"""
        dumped_data = pypdftk.dump_data('test_files/form.pdf')
        self.assertEqual(dumped_data, form_info_data)

    def test_update_info(self):
        form_info_data = """InfoBegin
InfoKey: Keywords
InfoValue: My fancy form
InfoBegin
InfoKey: Creator
InfoValue: Ghostwriter
InfoBegin
InfoKey: CreationDate
InfoValue: D:20210101204853+02&apos;00&apos;
InfoBegin
InfoKey: Producer
InfoValue: PDFTK
InfoBegin
InfoKey: Title
InfoValue: Form with updated metadata
PdfID0: 5e0a553555622a0516e9877ca55217a6
PdfID1: 5e0a553555622a0516e9877ca55217a6
NumberOfPages: 1
PageMediaBegin
PageMediaNumber: 1
PageMediaRotation: 0
PageMediaRect: 0 0 595 842
PageMediaDimensions: 595 842"""

        with open("test_files/form_info_data.txt", 'w') as f:
            f.write(form_info_data)
        pypdftk.update_info('test_files/form.pdf', 'test_files/form_info_data.txt', 'test_files/form_updated.pdf')
        dumped_data = pypdftk.dump_data('test_files/form_updated.pdf')
        self.assertEqual(dumped_data, form_info_data)

    @unittest.skip('Not implemented yet')
    def test_stamp(self):
        pass


if __name__ == '__main__':
    unittest.main()