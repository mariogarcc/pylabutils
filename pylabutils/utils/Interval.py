import re

__all__ = ['Interval']

class Interval:
    """
    Defines intervals in the real numbers line, such as:
    (n, m); [a, b]; (x, y]; [t0, t1);

    Usage examples:

    `>>> 3 in Interval('(0, 3]')`\n
    `True`

    `>>> 1 in Interval('[0, 1)')`\n
    `False`

    """

    def __init__(self, interval_str):

        if isinstance(interval_str, Interval):
            self.begin, self.end = interval_str.begin, interval_str.end
            self.begin_included = interval_str.begin_included
            self.end_included = interval_str.end_included
            return
        # redundant case for when input is already an interval

        number_re = r'[\d\.\w\(\)]+?'
        interval_re = r'^\s*' \
                    + r'(\[|\()' \
                    + r'\s*' \
                    + r'(' + number_re + r')' \
                    + r'\s*,\s*' \
                    + r'(' + number_re + ')' \
                    + r'\s*' \
                    + r'(\]|\))' \
                    + r'\s*$'

        match = re.search(interval_re, interval_str)
        if match is None:
            raise ValueError(
            'got an incorrect string representation of an interval: {!r}'
            .format(interval_str)
            )

        opening_bracket, begin, end, closing_bracket = match.groups()
        try:
            self.begin, self.end = float(eval(begin)), float(eval(end))
        except TypeError:
            raise TypeError("one of the interval arguments is not a number")


        if self.begin >= self.end:
            self.begin, self.end = self.end, self.begin

        self.begin_included = opening_bracket == '['
        self.end_included = closing_bracket == ']'


    def __repr__(self):
        return 'Interval({!r})'.format(str(self))

    def __str__(self):
        opening_bracket = '[' if self.begin_included else '('
        closing_bracket = ']' if self.end_included else ')'
        return '{}{}, {}{}'.format(opening_bracket, self.begin, \
            self.end, closing_bracket)

    def __contains__(self, number):
        if self.begin < number < self.end:
            return True
        if number == self.begin:
            return self.begin_included
        if number == self.end:
            return self.end_included


# To do:
# operations/concatenation
# n-dimensional extensibility
# some sort of linspace using a .split method
