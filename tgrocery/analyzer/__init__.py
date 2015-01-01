"""
:mod:`analyzer` is used for micro (for a single text instance) or macro (e.g., 
accuracy) analysis. Users can use :class:`InstanceSet` to specify the scope
to analyze by :class:`Analyzer`.

::
	
	>>> from libshorttext.analyzer import *
	>>> 
	>>> # load instances from an analyzable predict result file
	>>> insts = InstanceSet('prediction_result_path')
	>>> # find instances labels whose true and predicted labels are as specified
	>>> insts = insts.select(with_labels(['Books', 'Music', 'Art']))
	>>> 
	>>> # create an analyzer
	>>> analyzer = Analyzer('model_path')
	>>> analyzer.gen_confusion_table(insts)
	         Books  Music  Art
	Books      169      1    0
	Music        2    214    0
	Art          6      0  162

To use the analysis tools, an analyzable result and a model are required. Refer to
:class:`libshorttext.classifier.PredictionResult` and 
:class:`libshorttext.classifier.TextModel`.

"""

from .analyzer_impl import *
del analyzer_impl

from .selector import *
del selector
