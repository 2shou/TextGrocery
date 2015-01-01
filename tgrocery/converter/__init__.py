"""
:mod:`converter` module is used convert a text data set to a numerical data set.
More specifically, it converts a text file to a LIBSVM-format data. Refer to 
:ref:`dataset` for the format of texts.

The utilities of :mod:`converter` is wrapped in :class:`Text2svmConverter`.
:class:`Text2svmConverter` consists of three components: 
:class:`TextPreprocessor`, :class:`FeatureGenerator`, and :class:`ClassMapping`.
For users who only need the most basic usage, they can use the utility function
:func:`convert_text` without understanding :mod:`converter`.

"""


from .converter_impl import *
del converter_impl
