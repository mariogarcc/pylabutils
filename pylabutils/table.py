from IPython.display import display, Latex

def table(data, data_titles, precision, shape = 'ver', box = 'ver'):
    '''Generates a simple Latex table.

    'data', 'data_titles' and 'precision' should all be tuples and have the same item order.
    'shape' values: 'hor' or 'ver'; 'box' values: 'hor', 'ver', 'full' or 'none'.
    'precision' values must be strings: '3.5f'; '.3i'; '.2f'; '.f' '''

    shape_values = ('ver', 'hor')
    box_values = ('full', 'none', 'ver', 'hor')
    if shape not in shape_values:
        raise(ValueError('shape value is incorrect'))
        return
    if box not in box_values:
        raise(ValueError('box value is incorrect'))
        return
    else:
        if len(data) != len(precision) or len(data) != len(data_titles):
            raise(ValueError('data\'s, data titles\' and precision\'s sizes don\'t match'))
            return
        else:
            for i in range(len(data)):
                if len(data[i]) != len(data[i-1]):
                    raise(ValueError('data\'s sizes don\'t match'))
                    return
                else:
                    pass

    cadena  = '\\begin{table}[H]\n\\begin{tabular}'

    disp = ''
    tt = ''

    if shape == 'ver':
        if box == 'none' or box == 'hor':
            disp += '{' + 'c' * len(data) + '}'
        else:
            disp += '{' + '|c' * len(data) + '|}'
        cadena += disp
        tt += '\n\\hline\n'
        for i in range(len(data_titles)):
            tt += data_titles[i]
            if i != len(data_titles) - 1:
                tt += ' & '
            else:
                tt +=  '\\\\\n\\hline\n'
        cadena += tt
        for i in range(len(data[0])):
            dt = '('
            pt = ''
            for j in range(len(data)):
                dt += 'data[' + str(j) + '][' + str(i) + ']'
                pt += '%' + precision[j]
                if j != len(data) - 1:
                    dt += ', '
                    pt += ' & '
                else:
                    dt += ')'
                    if box == 'none' or box == 'ver':
                        pt += ' \\\\\n'
                    else:
                        pt += ' \\\\\n\\hline\n'
            cadena += pt % eval(dt)

    elif shape == 'hor':
        if box == 'none' or box == 'hor':
            disp += '{|c|' + 'c' * len(data) + '|}'
        else:
            disp += '{|c' + '|c' * len(data) + '|}'
        cadena += disp + '\n\\hline\n'
        for i in range(len(data)):
            dt = '('
            pt = data_titles[i] + ' & '
            for j in range(len(data[0])):
                dt += 'data[' + str(i) + '][' + str(j) + ']'
                pt += '%' + precision[i]
                if j != len(data[0]) - 1:
                    dt += ', '
                    pt += ' & '
                else:
                    dt += ')'
                    if box == 'none' or box == 'ver':
                        pt += ' \\\\\n'
                    else:
                        pt += ' \\\\\n\\hline\n'
            cadena += pt % eval(dt)

    if box == 'hor' or box == 'full':
        cadena += '\\end{tabular}\n\\end{table}\n'
    else:
        cadena += '\\hline\n\\end{tabular}\n\\end{table}\n'

    display(Latex(cadena))

    return
