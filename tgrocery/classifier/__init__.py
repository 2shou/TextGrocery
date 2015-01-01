"""
The :mod:`classifier` is a high-level interface to train a short-text data. 
Members of :mod:`classifier` include :class:`TextModel` and its utility 
functions. :class:`TextModel` is obtained in training and then used in prediction.

The standard method to get a :class:`TextModel` instance is via function 
:func:`train_text` or :func:`train_converted_text`, which trains
text data (refer to :ref:`dataset`) or LIBSVM-format data, respectively. 

	>>> from libshorttext.classifier import *
	>>> # train a model and save it to a file
	>>> m, svm_file = train_text('train_file')
	>>> # save the model to a file
	>>> m.save('model_path')

After obtaining a :class:`TextModel`, users can use :func:`predict_text` or 
:func:`predict_single_text` to predict the label of a new short text.
	
	>>> from libshorttext.classifier import *
	>>> # load a model from a file
	>>> m = TextModel('model_path')
	>>> # predict a sentence
	>>> result = predict_single_text('This is a sentence.', m) 

Another class in module :mod:`classifier` is :class:`PredictionResult`, which is a
wrapper of prediction results. Both :func:`predict_text` and 
:func:`predict_single_text` return a :class:`PredictionResult` object.

:mod:`classifier` does not access the low-level LIBLINEAR's train and predict 
utilities directly. All jobs are passed to a submodule called :mod:`learner`, 
which is a middle-level classifier and communicates between :mod:`classifier`
and LIBLINEAR. Users can also use the :mod:`learner` module directly without
:mod:`classifier` to achieve more complicated usages.
"""


from .classifier_impl import * 
del classifier_impl
