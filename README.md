# pylabutils

`pylabutils` is a small, experimental python package that aims to provide some
aid in the making of simple data analysis reports in a lighter, more ergonomic
and more streamlined manner.

It currently offers 5 main methods (and an additional utility):

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

There is at least one important issue to be noted, that is to be fixed,
regarding the `fit` method. As [described](https://github.com/mariogarcc/pylabutils/blob/64f9595c3c4a77a511cf00339541776c8e435a8d/pylabutils/numfit/fit.py#L52)
in the function's `__doc__`:

> \[...\] you cannot use arbitrary constants or modules by reference in the
function string, because of the way `eval()` works (it calls the scope
inside a custom, private function, and the modules or constants declared
by the user are non-existent in that scope).
What this essentially means is that you are, until this issue is fixed,
restricted to the use of `math`, `numpy` as 'np' and `scipy.constants`
as 'scs' attributes, e.g. `'y = scs.R + {A} * np.exp(math.e + {B}*x)'`