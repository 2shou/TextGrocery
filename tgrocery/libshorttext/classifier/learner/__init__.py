"""
The middle-level classifier :mod:`learner` is used to train or predict a 
LIBSVM-format data. This module extends LIBLINEAR python interface to provide
more utilities such as various feature representations and instance-wise normalization. 
The only difference between this module and standard LIBLINEAR python interface is
that :mod:`learner` provides more utilities, e.g., instance normalization, 
tf-idf, and binary feature representation. We call it as a middle-level classifier 
because it provides an interface between :mod:`libshorttext.classifier` and LIBLINEAR.
Note that some of the utilities of :mod:`learner` is implemented in C language
for efficiency.

.. note::

	If the data set is in text format, use :mod:`libshorttext.classfier`
	rather than :mod:`learner`.

:mod:`learner` has three utility functions and one model class. If users 
want to replace :mod:`learner` module by their own implementation, they need to
implement the three utility functions and :class:`LearnerModel`, which will be
used by :mod:`libshorttext.classifier` and :mod:`libshorttext.analyzer`.
"""


from .learner_impl import *
del learner_impl
