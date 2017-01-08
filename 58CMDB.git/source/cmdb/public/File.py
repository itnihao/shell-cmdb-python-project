# -*- coding: utf-8 -*-
import random
import os
import xlrd


def handle_uploaded_file(f):
    UPLOAD_ROOT = '/tmp/'
    filename = 'cmdb-%d.xlsx' % (random.randint(1, 1000))
    file_full_path = os.path.join(UPLOAD_ROOT, filename)
    with open(file_full_path, 'wb+') as destinaltion:
        for chunk in f.chunks():
            destinaltion.write(chunk)
    return xlrd.open_workbook(file_full_path)
