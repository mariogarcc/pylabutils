from pylabutils.wdir import wdir
import os
import re

current_dir = os.getcwd()
parent_folder = current_dir[:-re.search(r'\\', current_dir[::-1]).start()]

with wdir(parent_folder):
    file = open('test.txt', 'w')
    file.write('This is a test.')
    file.close()
