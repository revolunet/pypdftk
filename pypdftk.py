# -*- encoding: UTF-8 -*-

''' pypdftk

Python module to drive the awesome pdftk binary.
See http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/

'''

import os
import subprocess
import tempfile
import shutil

if os.getenv('PDFTK_PATH'):
    PDFTK_PATH = os.getenv('PDFTK_PATH')
else:
    PDFTK_PATH = '/usr/bin/pdftk'


def check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return output


def run_command(command, shell=False):
    ''' run a system command and yield output '''
    p = check_output(command, shell=shell)
    return p.split('\n')


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
    cleanOnFail = False
    tmp_fdf = gen_xfdf(datas)
    if not out_file:
        cleanOnFail = True
        handle, out_file = tempfile.mkstemp()

    cmd = "%s %s fill_form %s output %s" % (PDFTK_PATH, pdf_path, tmp_fdf, out_file)
    if flatten:
        cmd += ' flatten'
    try:
        run_command(cmd, True)
    except:
        if cleanOnFail:
            os.remove(tmp_fdf)
        raise
    return out_file


def concat(files, out_file=None):
    '''
        Merge multiples PDF files.
        Return temp file if no out_file provided.
    '''
    cleanOnFail = False
    if not out_file:
        cleanOnFail = True
        handle, out_file = tempfile.mkstemp()
    if len(files) == 1:
        shutil.copyfile(files[0], out_file)
    args = [PDFTK_PATH]
    args += files
    args += ['cat', 'output', out_file]
    try:
        run_command(args)
    except:
        if cleanOnFail:
            os.remove(out_file)
        raise
    return out_file


def split(pdf_path, out_dir=None):
    '''
        Split a single PDF file into pages.
        Use a temp directory if no out_dir provided.
    '''
    cleanOnFail = False
    if not out_dir:
        cleanOnFail = True
        out_dir = tempfile.mkdtemp()
    out_pattern = '%s/page_%%02d.pdf' % out_dir
    try:
        run_command((PDFTK_PATH, pdf_path, 'burst', 'output', out_pattern))
    except:
        if cleanOnFail:
            shutil.rmtree(out_dir)
        raise
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

