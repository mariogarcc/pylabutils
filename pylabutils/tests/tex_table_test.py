from pylabutils.utils.io import tex_table

col1 = [1.00923, 222.123, 311111.1, 3241]
col2 = [4.3232, 5.9, 6.3, 40004]
col3 = [0.001, 0.002, 0.003, 0.006]
titles = ['col1', r'$\mathrm{col2}$', r'$col\gamma$']

print("Data to be utilized:\n")
print("Printed titles: {}".format(titles))
print("{} = {}".format('col1', col1))
print("{} = {}".format('col2', col2))
print("{} = {}".format('col3', col3))

tex_table([col1, col2, col3], titles, shape = 'v', sep = 'v',
    exp = [True, True, False],
    exp_prec = [0, 2, 3],
)
