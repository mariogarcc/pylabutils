# pylabutils

`pylabutils` is a small, experimental python package that aims to provide some
aid in the making of simple data analysis reports in a lighter, more ergonomic
and more streamlined manner.

It currently offers 5 main methods:

+ `fit` : the process of defining a function and setting up the optimization
  method all in one line, with added functionalities for immediate graphical
  representation.
+ `read_data` : an easy way to read your data from most table-like files
  and have it stored in a convenient `pandas.DataFrame`.
+ `tex_table` : prints your data into a fancy, common LaTeX table, with an
  added bit of customization included.
+ `multisort` : allows you to sort all of your data based on any of the
  variables stored, in case they don't all follow a monotonic progression.
+ `wdir` : a manager that yields a path, useful for when your data is stored
  externally.
+ `Interval` : a small class that lets you create *Real* number intervals,
  letting you check belongings using the `in` operator.

They all do have detailed `__doc__` attributes that explain all of their
arguments and keyword arguments, which you can view, and I encourage so,
by using either `help(<method>)` or `<method>.__doc__`.

There are, in addition, some "private" methods that can give some
functionalities that are included in some of the "main" methods, but these
are not really intended for active use and do not have a detailed description
accompanying them.