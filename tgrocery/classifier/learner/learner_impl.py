#!/usr/bin/env python

from ctypes import *
from ctypes.util import find_library
import sys
import os
from os import path
import shutil

if sys.version_info[0] >= 3:
	xrange = range
	import pickle as cPickle
	izip = zip
	def unicode(string, setting):
		return string
else :
	import cPickle
	from itertools import izip

util = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'util.so.1'))

LIBLINEAR_HOME = os.environ.get('LIBLINEAR_HOME') or os.path.dirname(os.path.abspath(__file__)) + '/liblinear'
sys.path = [LIBLINEAR_HOME, LIBLINEAR_HOME + '/python'] + sys.path

import liblinear
from liblinearutil import train as liblinear_train, predict as liblinear_predict, save_model as liblinear_save_model, load_model as liblinear_load_model

__all__ = ['LearnerParameter', 'LearnerModel', 
		'train', 'predict_one', 'predict', 'LIBLINEAR_HOME']

def print_debug(src):
	if os.environ.get('SHORTTEXTDEBUG'):
		print('[DEBUG]: ' + src)

def fillprototype(f, restype, argtypes): 
	f.restype = restype
	f.argtypes = argtypes

def genFields(names, types): 
	return list(zip(names, types))

#--------------Interface to util---------------
class SVMProblem(Structure):
	_names = ["prob", "x_space", "n_x_space"]
	_types = [liblinear.problem, POINTER(liblinear.feature_node), c_int64]
	_fields_ = genFields(_names, _types)

	def __del__ (self):
		print_debug('SVMProblem delete:%s'% id(self))
		util.freeSVMProblem(self)

def read_SVMProblem(src):
	status = c_int64()
	svmprob = util.read_problem(src.encode(), 0, pointer(status))  # bias = 0 is required

	status = status.value

	if status == 0:	
		print_debug('SVMProblem construct:%s'% id(svmprob))
		return svmprob

	if status == -1:
		raise IOError("Can not open file " + src + ".")

	if status == -2:
		raise MemoryError("Memory Exhausted. Try to restart python.")

	raise ValueError("Wrong file format in line " + str(status) + ".")


fillprototype(util.read_problem, SVMProblem, [c_char_p, c_double, POINTER(c_int64)])
fillprototype(util.freeSVMProblem, None, [SVMProblem])
fillprototype(util.compute_idf, c_double, [POINTER(liblinear.problem), POINTER(c_double)])
fillprototype(util.normalize, None, [POINTER(liblinear.problem), c_int, c_int, c_int, c_int, POINTER(c_double)])

class LearnerProblem(liblinear.problem):
	def __init__(self, src):
		#svmprob = util.read_problem(src.encode(), 0)  # bias = 0 is required
		svmprob = read_SVMProblem(src)  # bias = 0 is required
		self.x = svmprob.prob.x
		self.y = svmprob.prob.y
		self.l = svmprob.prob.l
		self.n = svmprob.prob.n
		self.bias = svmprob.prob.bias
		self.x_space = svmprob.x_space
		self.n_x_space = svmprob.n_x_space
		print_debug('LearnerProblem construct:%s'% id(svmprob))

	def set_bias(self, bias):
		if self.bias == bias:
			return
		node = liblinear.feature_node(self.n, bias) 
		if bias >= 0 and self.bias < 0: 
			self.n += 1
			node = liblinear.feature_node(self.n, bias)
		if bias < 0 and self.bias >= 0: 
			self.n -= 1
			node = liblinear.feature_node(-1, bias)

		for i in range(1,self.l):
			self.x[i][-2] = node
		self.x_space[self.n_x_space-2] = node
		self.bias = bias

	def normalize(self, learner_param, idf):
		print_debug ("normal parameters: bin_feat {0}, inst_norm {1}, tf {2}, idf {3}\n".format(learner_param.binary_feature,
			learner_param.inst_normalization,
			learner_param.term_frequency,
			learner_param.inverse_document_frequency,
		))
		util.normalize(pointer(self),
			learner_param.binary_feature,
			learner_param.inst_normalization,
			learner_param.term_frequency,
			learner_param.inverse_document_frequency,
			idf)

	@staticmethod
	def normalize_one(xi, learner_param, idf):
		"""
		The maximum index of xi should be less
		or equal to the weight vector size.
		"""
		norm = 0
		word_count = 0
		i = 0
		while xi[i].index != -1:
			idx = xi[i].index-1
			if learner_param.binary_feature:
				xi[i].value = xi[i].value != 0

			word_count += abs(xi[i].value)

			if learner_param.inverse_document_frequency and idx < len(idf):
				xi[i].value *= idf[idx]

			norm += xi[i].value * xi[i].value
			i += 1

		norm **= .5


		if learner_param.term_frequency:
			i = 0
			while xi[i].index != -1:
				xi[i].value /= word_count
				i += 1

		if learner_param.inst_normalization:
			i = 0
			while xi[i].index != -1:
				xi[i].value /= norm 
				i += 1

	def compute_idf(self):
		idf = (c_double * self.n)()
		util.compute_idf(self, idf)
		return idf

class LearnerParameter(liblinear.parameter):
	"""
	:class:`LearnerParameter` is the parameter structure used by 
	:class:`LearnerModel`. It consists of normalization parameters and 
	LIBLINEAR parameters.

	Both *liblinear_opts* and *learner_opts* are :class:`str` or a 
	:class:`list` of :class:`str`. For example, you can write either
	
	>>> param = LearnerParameter('-N 1 -T 1', '-c 2 -e 1e-2')

	or

	>>> param = LearnerParameter(['-N', '1', '-T', '1'], ['-c', '2', '-e', '1e-2'])

	*liblinear_opts* is LIBLINEAR's parameters. Refer to LIBLINEAR's 
	document for more details. *learner_opts* includes options for feature
	representation and instance-wise normalization. The preprocessor of
	LibShortText converts text files to LIBSVM-format data, where the 
	features are word counts. All *value* in the options should be either 
	``1`` or ``0``, where ``1`` enables the option.

		========== ====================================================
		options    explanation when *value* is ``1``
		========== ====================================================
		-D *value* Binary representation. All non-zero values are 
		           treated as 1. Default is enabled.
		-T *value* Term frequency. The data are divided by the feature
		           sum. That is, 
		           :math:`x_i \leftarrow (x_i)/\sum_j |x_j|`,
		           where :math:`x` is the training instance and 
		           :math:`x_i` is the :math:`i`-th feature of :math:`x`.
		           Default is disabled.
		-I *value* Inverse document frequency (idf). Default is 
		           disabled.
		-N *value* Instance normalization. The training instances are 
		           normalized to unit vectors before training. Default
		           is enabled.
		========== ====================================================
			   
	Note that if more than one option is enabled, then they are done in the
	order: binary representation, term frequency, IDF, and instance 
	normalization. The following example is tf-idf representation without
	instance normalization.

	>>> param = LearnerParameter('-D 0 -T 1 -I 1 -N 0', liblinear_opts)

	"""
	def __init__(self, learner_opts = '', liblinear_opts = ''):
		self.parse_options(learner_opts, liblinear_opts)
		
	def set_to_default_values(self):
		"""
		Set the options to some values 
		(``'-D 1 -T 0 -I 0 -N 1'``).
		"""
		liblinear.parameter.set_to_default_values(self) 
		self.binary_feature = 1
		self.inst_normalization = 1
		self.term_frequency = 0
		self.inverse_document_frequency = 0
	
	def parse_options(self, learner_opts, liblinear_opts):
		"""
		Set the options to the specific values.
		"""
		
		self.raw_options = (learner_opts, liblinear_opts)
		if isinstance(learner_opts, list):
			argv = learner_opts
		elif isinstance(learner_opts, str):
			argv = learner_opts.split()
		else:
			raise TypeError("Wrong types")
		self.set_to_default_values()
		liblinear.parameter.parse_options(self, liblinear_opts)
		
		i = 0
		while i < len(argv):
			if argv[i] == "-D":
				i = i + 1
				self.binary_feature = int(argv[i])
			elif argv[i] == "-N":
				i = i + 1
				self.inst_normalization = int(argv[i])
			elif argv[i] == "-I":
				i = i + 1
				self.inverse_document_frequency = int(argv[i])
			elif argv[i] == "-T":
				i = i + 1
				self.term_frequency = int(argv[i])
			else :
				raise ValueError('No option ' + argv[i]) 
			i = i + 1


class LearnerModel(liblinear.model):
	"""
	:class:`LearnerModel` is a middle-level classification model. It 
	inherits from :class:`liblinear.model` by having two more members:
	a :class:`LearnerParameter` instance and an inverse document frequency list.

	We do not recommend users to create a :class:`LearnerModel` by themselves. 
	Instead, users should create and manipulate a :class:`LearnerModel`
	via :func:`train`, :func:`predict`, and :func:`predict_one`.
	
	If users want to redefine :class:`LearnerModel`, they must 
	implement the following four methods used by 
	:mod:`libshorttext.classifier` and :mod:`libshorttext.analyzer`.
	"""

	def _reconstruct_label_idx(self):
		def _get_label_idx(nr_class, labels):
			return dict(zip(labels[:nr_class], range(nr_class)))
		
		if self.c_model is not None:
			self.labelidx = _get_label_idx(self.c_model.nr_class, self.c_model.label)


	def __init__(self, c_model, param = None, idf = None):
		"""
		constructor of :class:`LearnerModel`.
		"""
		
		print_debug('c_model(%s), self(%s)' % (id(c_model), id(self)))

		if isinstance(c_model, str):
			self.load(c_model)			
			return
		elif isinstance(c_model, liblinear.model):
			if param is None:
				raise ValueError("param can not be None if model is given.")
		else:
			raise TypeError("c_model should be model file name or a model.")

		self.c_model = c_model # prevent GC
		
		if isinstance(param, LearnerParameter):
			self.param_options = param.raw_options
		elif isinstance(param, tuple):
			self.param_options = param
		else:
			raise TypeError("param should be a LearnerParameter or a tuple.")
		
		if idf is not None:
			self.idf = idf[:self.c_model.nr_feature + (self.c_model.bias >= 0)] 
		else:
			self.idf = None

		for attr in c_model._names:
			setattr(self, attr, getattr(c_model, attr))

		self._reconstruct_label_idx()

	def get_weight(self, j, k):
		"""
		Return the weight of feature *j* and label *k*.
		"""
		return self.c_model.w[(j-1)*self.c_model.nr_class + self.labelidx[k]]

	def get_labels(self):
		"""
		Return the labels of this model.
		"""
		return self.label[:self.nr_class]

	def load(self, model_dir):
		"""
		Load the contents from a :class:`TextModel` directory. 
		"""
		
		self.c_model = liblinear_load_model(path.join(model_dir,'liblinear_model'))
		
		options_file = path.join(model_dir,'options.pickle')
		self.param_options = cPickle.load(open(options_file,'rb'))
		
		idf_file = path.join(model_dir,'idf.pickle')
		self.idf = cPickle.load(open(idf_file,'rb'))
		
		self.__init__(self.c_model, LearnerParameter(self.param_options[0], self.param_options[1]), self.idf)

	def save(self, model_dir, force=False):
		"""
		Save the model to a directory. If *force* is set to ``True``, 
		the existing directory will be overwritten; otherwise, 
		:class:`IOError` will be raised.
		"""

		if path.exists(model_dir): 
			if force: 
				shutil.rmtree(model_dir)
			else : 
				raise OSError('Please use force option to overwrite the existing files.')
		os.mkdir(model_dir)

		liblinear_save_model(path.join(model_dir,'liblinear_model'), self.c_model) 
		options_file = path.join(model_dir,'options.pickle')
		cPickle.dump(self.param_options, open(options_file,'wb'),-1) 
		
		idf_file = path.join(model_dir,'idf.pickle')
		cPickle.dump(self.idf, open(idf_file,'wb'),-1) 

	def __str__(self):
		if type(self.param_options) is tuple and len(self.param_options) > 0:
			return 'LearnerModel: ' + (self.param_options[0] or 'default')
		else:
			return 'empty LearnerModel'

def train(data_file_name, learner_opts="", liblinear_opts=""):
	"""
	Return a :class:`LearnerModel`.

	*data_file_name* is the file path of the LIBSVM-format data. *learner_opts* is a 
	:class:`str`. Refer to :ref:`learner_param`. *liblinear_opts* is a :class:`str` of 
	LIBLINEAR's parameters. Refer to LIBLINEAR's document.
	"""
	
	learner_prob = LearnerProblem(data_file_name)
	learner_param = LearnerParameter(learner_opts, liblinear_opts)
	
	idf = None
	if learner_param.inverse_document_frequency:
		idf = learner_prob.compute_idf()
	
	learner_prob.normalize(learner_param, idf)

	m = liblinear_train(learner_prob, learner_param)
	if not learner_param.cross_validation:
		m.x_space = None  # This is required to reduce the memory usage...
		m = LearnerModel(m, learner_param, idf)
	return m

def predict_one(xi, m):
	"""
	Return the label and a :class:`c_double` array of decision values of
	the test instance *xi* using :class:`LearnerModel` *m*.

	*xi* can be a :class:`list` or a :class:`dict` as in LIBLINEAR python 
	interface. It can also be a LIBLINEAR feature_node array.

	.. note::

		This function is designed to analyze the result of one instance.
		It has a severe efficiency issue and should be used only by
		:func:`libshorttext.classifier.predict_single_text`. If many 
		instances need to be predicted, they should be stored in a file
		and predicted by :func:`predict`.

	.. warning::

		The content of *xi* may be **changed** after the function call.
	"""
	
	if isinstance(xi, (list, dict)):
		xi = liblinear.gen_feature_nodearray(xi)[0]
	elif not isinstance(xi, POINTER(liblinear.feature_node)):
		raise TypeError("xi should be a test instance")
	
	learner_param = LearnerParameter(m.param_options[0], m.param_options[1])

	if m.bias >= 0:
		i = 0
		while xi[i].index != -1: i += 1

		# Already has bias, or bias reserved.
		# Actually this statement should be true if
		# the data is read by read_SVMProblem.
		if i > 0 and xi[i-1].index == m.nr_feature + 1:
			i -= 1 
		
		xi[i] = liblinear.feature_node(m.nr_feature + 1, m.bias)
		xi[i+1] = liblinear.feature_node(-1, 0)
	
	LearnerProblem.normalize_one(xi, learner_param, m.idf)

	dec_values = (c_double * m.nr_class)()
	label = liblinear.liblinear.predict_values(m, xi, dec_values)

	return label, dec_values

def predict(data_file_name, m, liblinear_opts=""):
	"""
	Return a quadruple: the predicted labels, the accuracy, the decision values, and the
	true labels in the test data file (obtained through the :class:`LearnerModel` *m*).

	The predicted labels and true labels in the file are :class:`list`. The accuracy is 
	evaluated by assuming that the labels in the file are the true label.

	The decision values are in a :class:`list`, where the length is the same as the number
	of test instances. Each element in the list is a :class:`c_double` array, and the 
	values in the array are an instance's decision values in different classes.
	For example, the decision value of instance i and class k can be obtained by

	>>> predicted_label, accuracy, all_dec_values, label = predict('svm_file', model)
	>>> print all_dec_values[i][k]
	"""
	
	learner_prob = LearnerProblem(data_file_name)
	learner_param = LearnerParameter(m.param_options[0], m.param_options[1])

	idf = None
	if m.idf:
		idf = (c_double * len(m.idf))()
		for i in range(len(m.idf)): idf[i] = m.idf[i]
	learner_prob.normalize(learner_param, idf)

	all_dec_values = []
	acc = 0
	py = []  # predicted y
	ty = []  # true y
	
	dec_values = (c_double * m.nr_class)()
	
	for i in range(learner_prob.l):
		label = liblinear.liblinear.predict_values(m, learner_prob.x[i], dec_values)
		all_dec_values += [dec_values[:m.nr_class]]
		py += [label]
		ty += [learner_prob.y[i]]

		if label == learner_prob.y[i]:
			acc += 1

	acc /= float(learner_prob.l)


	return py, acc, all_dec_values, ty



if __name__ == '__main__':
	argv = sys.argv
	if len(argv) < 2: #4 or '-v' not in argv:
		print("{0} -v fold [other liblinear_options] [learner_opts] training-data".format(argv[0]))
		sys.exit(-1)
	data_file_name = argv[-1]
	learner_opts, liblinear_opts = [], []
	i = 1 
	while i < len(argv)-1:
		if argv[i] in ["-D", "-N", "-I", "-T"]:
			learner_opts += [argv[i], argv[i+1]]
			i += 2
		else :
			liblinear_opts += [argv[i]]
			i += 1
	m = train(data_file_name, learner_opts, liblinear_opts)
