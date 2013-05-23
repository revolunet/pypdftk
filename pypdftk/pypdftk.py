# -*- encoding: UTF-8 -*-

''' PyPdfTk

Python module to drive the awesome pdftk binary.
See http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/

'''

import os
import subprocess
import tempfile
import shutil

PDFTK_PATH = '/usr/bin/pdftk'


def run_command(command):
    ''' run a system command and yield output '''
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


def get_num_pages(pdf_path):
    ''' return number of pages in a given PDF file '''
    for line in run_command([PDFTK_PATH, pdf_path, 'dump_data']):
        if line.lower().startswith('numberofpages'):
            return int(line.split(':')[1])
    return 0


def fill_form(pdf_path, datas={}, out_file=None, flatten=True):
    '''
        Fills a PDF form with given dict input data.
        Return temp file if no out_file provided.
    '''
    error = False
    tmp_fdf = gen_xfdf(datas)
    if not out_file:
        handle, out_file = tempfile.mkstemp()

    cmd = "%s %s fill_form %s output %s" % (PDFTK_PATH, pdf_path, tmp_fdf, out_file)
    if flatten:
        cmd += ' flatten'
    try:
        p = subprocess.Popen(cmd, shell=True)
    except:
        error = True
    p.wait()
    os.remove(tmp_fdf)
    if error or not os.path.isfile(out_file):
        print 'Error filling PDF page %s' % pdf_path
        # if merge failed, return the original PDF
        shutil.copyfile(pdf_path, out_file)
    return out_file


def concat(files, out_file=None):
    '''
        Merge multiples PDF files.
        Return temp file if no out_file provided.
    '''
    if not out_file:
        handle, out_file = tempfile.mkstemp()
    if len(files) == 1:
        shutil.copyfile(files[0], out_file)
    args = [PDFTK_PATH]
    args += files
    args += ['cat', 'output', out_file]
    run_command(args)
    return out_file


def split(pdf_path, out_dir=None):
    '''
        Split a single PDF file into pages.
        Use a temp directory if no out_dir provided.
    '''
    if not out_dir:
        out_dir = tempfile.mkdtemp()
    out_pattern = '%s/page_%%02d.pdf' % out_dir
    run_command((PDFTK_PATH, pdf_path, 'burst', 'output', out_pattern))
    out_files = os.listdir(out_dir)
    out_files.sort()
    return [os.path.join(out_dir, filename) for filename in out_files]


def gen_xfdf(datas={}):
    ''' Generates a temp XFDF file suited for fill_form function, based on dict input data '''
    fields = []
    for key, value in datas.items():
        fields.append(u"""<field name="%s"><value>%s</value></field>""" % (key, value))
    tpl = u"""<?xml version="1.0" encoding="UTF-8"?>
    <xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">
        <fields>
            %s
        </fields>
    </xfdf>""" % "\n".join(fields)
    handle, out_file = tempfile.mkstemp()
    f = open(out_file, 'w')
    f.write(tpl.encode('UTF-8'))
    f.close()
    return out_file
