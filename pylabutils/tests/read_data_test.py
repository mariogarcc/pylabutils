import os
import pylabutils.utils.io as uio

print("Creating new file...")
with open('test_table.txt', 'w+') as file:
    file.write("A, B, C, D, E\n"
               "1, 2., 30.03, 4, 5e-5\n"
               "5, 6., 70.07, 8, 10e10")
    file.close()

print("What is in the file:")
with open('test_table.txt', 'r') as file:
    print(file.read())
    file.close()

print("What we read:")
uio.read_data('test_table.txt')
print(uio._data)
print(uio._data.info())


os.remove('test_table.txt')
