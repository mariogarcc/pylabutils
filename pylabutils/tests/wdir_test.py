import os
import re
from pylabutils.utils.io import wdir

print("Obtaining parent folder...\n")
current_dir = os.getcwd()
print("...")
parent_folder = current_dir[:-re.search(r'\\', current_dir[::-1]).start()]
if len(parent_folder) < 4:
    print("Parent folder obtained:\n")
else:
    raise NameError(
        "Parent folder could not be obtained"
        " (disk names are not accepted)")
print(parent_folder)

print("Attempting to create test file 'test.txt'...\n")
with wdir(parent_folder):
    file = open('test.txt', 'w')
    file.write('This is a test.')
    file.close()
    print("Achieved!")
