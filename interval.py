import re

class Interval:
    '''
    Defines intervals in the real numbers line, such as:
    (n, m); [a, b]; (x, y]; [t0, t1);

    Usage examples:
    >>> 3 in Interval('(0, 3]')
    True
    >>> 1 in Interval('[0, 1)')
    False
    '''

    def __init__(self, interval):

        if isinstance(interval, Interval):
            self.begin, self.end = interval.begin, interval.end
            self.begin_included = interval.begin_included
            self.end_included = interval.end_included
            return

        number_re = '-?[0-9]+(?:.[0-9]+)?'
        interval_re = ('^\s*'
                    + '(\[|\()'  #  opening bracket
                    + '\s*'
                    + '(' + number_re + ')'  #  beginning of the interval
                    + '\s*,\s*'
                    + '(' + number_re + ')'  #  end of the interval
                    + '\s*'
                    + '(\]|\))'  #  closing bracket
                    + '\s*$')

        match = re.search(interval_re, interval)
        if match is None:
            raise ValueError(
            'Got an incorrect string representation of an interval: {!r}'
            .format(interval)
            )

        opening_bracket, begin, end, closing_bracket = match.groups()
        self.begin, self.end = float(begin), float(end)

        if self.begin >= self.end:
            raise ValueError('Interval\'s begin shoud be'
                ' smaller than it\'s end')

        self.begin_included = opening_bracket == '['
        self.end_included = closing_bracket == ']'

        # It might have been better to use number_re = '.*' and
        # catch exceptions, float() raises instead --> author's note (means ?)

    def __repr__(self):
        return 'Interval({!r})'.format(str(self))

    def __str__(self):
        opening_bracket = '[' if self.begin_included else '('
        closing_bracket = ']' if self.end_included else ')'
        return '{}{}, {}{}'.format(opening_bracket, self.begin, self.end, closing_bracket)

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
# comment code
