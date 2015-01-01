#!/usr/bin/env python

from random import sample

__all__ = ['wrong', 'with_labels', 'sort_by_dec', 'subset', 'selectorize', 'reverse']

def selectorize(option = 'general', comment = None):
	"""
	A function decorator which returns a function wrapper to generate a 
	selector function.
	
	*option* can be ``'select'``, ``'sort'``, or ``'general'``. See the 
	following table.
	
	+---------------+-----------------------------------------------------+
	|   *option*    |      What should the defined function do?           |
	+===============+=====================================================+
	| ``'select'``  | The defined function should decide whether an       |
	|               | instance should be selected or not. Therefore, the  |
	|               | input is a :class:`TextInstance`, and the output    | 
	|               | should be ``True`` or ``False``. ``True`` means that|
	|               | this instance should be selected.                   |
	+---------------+-----------------------------------------------------+
	| ``'sort'``    | The defined function should return the key of an    |
	|               | :class:`TextInstance` for sorting. The input is a   |
	|               | :class:`TextInstance`, and the output should be a   |
	|               | value or an object that is comparable.              |
	+---------------+-----------------------------------------------------+
	| ``'general'`` | Equivalent to the original function without applying| 
	|               | the function wrapper. Therefore, the defined        |
	|               | function's input and output are a list of           |
	|               | :class:`TextInstance`.                              |
	+---------------+-----------------------------------------------------+

	For example, :func:`wrong` is equivalent to the following function::

		@selectorize('select', 'Select wrongly predicted instances')
		def wrong(inst):
			return inst.true_y !=  inst.predicted_y
	
	And, :func:`sort_by_dec` is equivalent to the following function::
		
		@selectorize('sort', 'Sort by maximum decision values.')
		def sort_by_dec(inst):
			return max(inst.decvals)
	
	*comment* is the argument of the comment on the function, which will
	be shown by the :meth:`libshorttext.analyzer.Analyzer.info`. See the
	following example.

	::

		>>> from libshorttext.analyzer import *
		>>> 
		>>> @selectorize(comment = 'foo function')
		>>> def foo(x):
		>>> 	return x
		>>> 
		>>> insts = InstanceSet('predict_result_path').select(foo)
		>>> Analyzer('model_path').info(insts)
		[output skipped]
		Selectors :
		-> foo function
	"""

	def inner_func(input_func):
		if option == "select":
			def inner_func2(insts):
				return list(filter(input_func, insts))
		elif option == "sort":
			def inner_func2(insts):
				return sorted(insts, key = input_func)
		elif option == "general":
			inner_func2 = input_func
		else:
			raise Exception("No such setting.")
		
		if input_func is None or comment is None:
			inner_func2._libshorttext_msg = "user-defined selector function"
		else:
			inner_func2._libshorttext_msg = comment
		
		inner_func2.__doc__ = input_func.__doc__
		
		return inner_func2
	return inner_func

@selectorize('select', 'Select wrongly predicted instances')
def wrong(inst):
	'''
	Select wrongly predicted instances. It assumes that the labels in the
	test data are true labels. 
	
	This function should be passed to :meth:`InstanceSet.select` without any 
	argument.

	>>> insts = InstanceSet('prediction_result_path').select(wrong)
	'''
	return inst.true_y !=  inst.predicted_y

def with_labels(labels, target = 'both'):
	'''
	Select instances with specified labels. *labels* is an iterable object
	of :class:`str` instances, which represent the label names. 
	
	*target* can be ``'true'``, ``'predict'``, ``'both'``, ``'or'``. If 
	*target* is ``'true'``, then this function finds instances based on the 
	true label specified in the test data. If *target* is 
	``'predict'``, it finds instances based on the predicted labels. 
	``'both'`` and ``'or'`` find the intersection and the union of 
	``'true'`` and ``'predict'``, respectively. The default value of 
	``'target'`` is ``'both'``.

	The following example selects instances where the true labels are
	``'Music'`` or ``'Books'``.

	>>> insts = InstanceSet('prediction_result_path').select(with_labels(['Books', 'Music']))
	'''
	@selectorize('select', 'labels: "{0}"'.format('", "'.join(labels)))
	def inner_func(inst):
		if target == 'both':
			return inst.true_y in labels and inst.predicted_y in labels
		elif target == 'or':
			return inst.true_y in labels or inst.predicted_y in labels
		elif target == 'true':
			return inst.true_y in labels
		elif target == 'predict':
			return inst.predicted_y in labels
		else:
			raise Exception("No such setting.")
	return inner_func

@selectorize('sort', 'Sort by maximum decision values.')
def sort_by_dec(inst):
	'''
	Sort instances by the decision values of the predicted labels in ascending
	order. You can combine this function with :func:`reverse` to sort decision 
	values from large to small.
	
	>>> insts = InstanceSet('prediction_result_path').select(sort_by_dec, reverse)
	
	This function should be passed to :meth:`InstanceSet.select` without any argument. 
	'''
	return max(inst.decvals)

def subset(amount, method = 'top'):
	'''
	Find a subset of the :class:`InstanceSet`. *amount* is the number of 
	selected instances. *method* can be ``'top'`` or ``'random'``. If 
	*method* is ``'top'``, the first *amount* instances are selected.
	Otherwise, :meth:`InstanceSet` selects instances randomly. If *amount* is 
	larger than the number of instances, :meth:`InstanceSet` will return all
	instances.

	The ``'top'`` method is useful when used after :func:`sort_by_dec`. The
	following example selects ten instances with the smallest decision values of
	the predicted label.
	
	>>> insts = InstanceSet('prediction_result_path').select(sort_by_dec, subset(10))
	'''
	@selectorize(comment = 'Select {0} instances in {1}.'.format(amount, method))
	def inner_func(insts):
		if amount > len(insts):
			return insts
		elif method == 'random':
			return sample(insts, amount)
		elif method == 'top':
			return insts[0:amount]
		else:
			raise Exception("No such setting.")
	return inner_func


@selectorize(comment = 'Reverse the order of instances')
def reverse(insts):
	"""
	Reverse the order of instances.
	
	This function should be passed to :meth:`InstanceSet.select` without any 
	argument.

	>>> insts = InstanceSet('prediction_result_path').select(reverse)
	"""
	return list(reversed(insts))
