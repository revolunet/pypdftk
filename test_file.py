import pypdftk


def test_split():
    input_file = "./Out/some_file.pdf"
    pypdftk.split(input_file, "./Out")

def test_num_pages():
    input_file = "./Out/some_file.pdf"
    num_pgs = pypdftk.get_num_pages(input_file)
    print num_pgs

def test_concat():
    files = ["./Out/page_01.pdf", "./Out/page_02.pdf", "./Out/page_03.pdf"]
    pypdftk.concat(files, "./Out/sample_output.pdf")

def test_compress():
    input_file = "/Out/test1.unc.pdf"
    pypdftk.compress(input_file, "./Out/test1.c.pdf")

def test_uncompress():
    input_file = "./Out/test1.pdf"
    pypdftk.uncompress(input_file, "./Out/test1.unc.pdf")

def main():
    #test_split()
    test_num_pages()
    #test_concat()
    test_uncompress()
    test_compress()

if __name__ == '__main__':
    main()