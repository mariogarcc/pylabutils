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
            self.begin = interval_str.begin
            self.end = interval_str.end
            self.begin_sign = interval_str.begin_sign
            self.end_sign = interval_str.end_sign
            self.begin_included = interval_str.begin_included
            self.end_included = interval_str.end_included
            return

        number_re = r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
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
            f'got an incorrect string representation of an interval: {interval_str!r}'
            )

        opening_bracket, begin, end, closing_bracket = match.groups()
        self.begin, self.end = float(begin), float(end)

        self.begin_included = opening_bracket == '['
        self.end_included = closing_bracket == ']'

        if self.begin > self.end:
            self.begin, self.end = self.end, self.begin
            self.begin_included, self.end_included = self.end_included, self.begin_included

        self.begin_sign = '[' if self.begin_included else '('
        self.end_sign = ']' if self.end_included else ')'


    def __str__(self):
        return f'{self.begin_sign}{self.begin}, {self.end}{self.end_sign}'


    def __repr__(self):
        return f'Interval({str(self)!r})'


    def __contains__(self, number):
        if self.begin < number < self.end:
            return True
        elif number == self.begin:
            return self.begin_included
        elif number == self.end:
            return self.end_included
        else:
            return False


    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False

        return (
            self.begin == other.begin and
            self.end == other.end and
            self.begin_sign == other.begin_sign and
            self.end_sign == other.end_sign
        )


    def __len__(self):
        return self.end - self.begin


    def __add__(self, other): #union
        if not isinstance(other, Interval):
            raise NotImplementedError

        if self.end < other.begin or other.end < self.begin:
            raise NotImplementedError

        selfmin = self.begin < other.begin
        selfmax = self.end > other.end

        begin_num = self.begin if selfmin else other.begin
        begin_sign = self.begin_sign if selfmin else other.begin_sign

        end_num = self.end if selfmax else other.end
        end_sign = self.end_sign if selfmax else other.end_sign

        return Interval(f'{begin_sign}{begin_num}, {end_num}{end_sign}')


    def __radd__(self, other):
        return self.__add__(other)


    def __iadd__(self, other):
        return self.__add__(other)


    def __sub__(self, other): #substraction
        raise NotImplementedError


    def __and__(self, other): #intersection
        raise NotImplementedError


    def __or__(self, other): #union
        raise NotImplementedError


    def __getitem__(self, key):
        raise NotImplementedError


    def __setitem__(self, key, value):
        raise NotImplementedError


    def __iter__(self, *args):
        raise NotImplementedError


    def split(self, *args):
        raise NotImplementedError
