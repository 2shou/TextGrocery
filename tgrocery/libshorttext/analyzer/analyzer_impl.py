#!/usr/bin/env python
import sys, os
from collections import defaultdict 
from ..classifier import *
__all__ = ['TextInstance', 'InstanceSet', 'Analyzer']

if sys.version_info[0] >= 3:
	xrange = range
	izip = zip
else:
	from itertools import izip

class TextInstance:
	'''
	:class:`TextInstance` represents a text instance. It includes the index, 
	the true label, the predicted label, the text, and the decision values 
	of the text instance. Normally you do not directly create an instance. 
	Instead, it is usually manipulated by :class:`InstanceSet`. For 
	more information, please see the usage in :class:`InstanceSet`.
	'''

	def __init__(self, idx, true_y = '', predicted_y = '', text = '', extra_svm_feats = [], decvals = None):
		self.idx = idx #: Instance index in the text source.
		
		#: The true label (if provided in the text source in the prediction phase).
		self.true_y = true_y 
		
		#: The predicted label.
		self.predicted_y = predicted_y

		#: The original text. The value is an empty :class:`str` 
		#: (``''``) at the beginning. The value is filled after
		#: :func:`PredInst.load_text` is called.
		self.text = text
		#: The extra svm features. The value is an empty :class:`str`
		#: at the beginning. The value is filled after 
		#: :func:`PredInst.load_text` is called.
		self.extra_svm_feats = extra_svm_feats

		#: A :class:`list` of decision values. The length should be the
		#: number of classes.
		self.decvals = decvals

	def __str__(self):
		string = '''text = {text}
true label = {true_y}
predicted label = {predicted_y}
'''.format(text = self.text, true_y = self.true_y, predicted_y = self.predicted_y)
		if self.extra_svm_feats:
			string += 'extra svm features = {extra}\n'.format(extra = self.extra_svm_feats)
		return string
	
class InstanceSet:
	'''
	:class:`InstanceSet` is a group of :class:`TextInstance` instances. It is used to
	get a subset of interested data. It should be initialized with a prediction
	result file (and a testing data). By default, the path to the testing data
	is stored in the prediction result file so you can only give the path to
	prediction result file.

		>>> from libshorttext.analyzer import *
		>>> insts = InstanceSet('prediction_result_path')

	If you have moved testing data, then you must re-assign the path to testing
	data.

		>>> from libshorttext.analyzer import *
		>>> insts = InstanceSet('prediction_result_path', 'testing_data_path')
	'''

	def __init__(self, rst_src = None, text_src = None):
		self.insts = None
		self.correct = None
		self.filepath = None
		self.extra_svm_files = []
		self.true_labels = None
		self.predict_labels = None
		self.quantity = None
		self.selectors = []
		if rst_src is not None:
			self._load(rst_src, text_src)

	def __iter__(self):
		return iter(self.insts)

	def __getitem__(self, idx):
		return self.insts[idx]
	
	def select(self, *sel_funcs):
		'''
		This function helps users find interested data. The arguments 
		are `selector functions`, where both the argument and returned
		values are lists. There are several build-in selector functions.
		Refer to :ref:`selectorfunctions`.
		
		>>> from libshorttext.analyzer import *
		>>> insts = InstanceSet('prediction_result_path')
		>>> insts1 = insts.select(wrong, with_labels(['Books', 'Music'])) 
		'''
		### How to link to the section??
		insts = self.insts
		selectors = self.selectors[:]
		for sel_func in sel_funcs:
			insts = sel_func(insts)
			selectors.append(sel_func._libshorttext_msg or '')
		#if not insts:
		#	raise Exception("No instance selected.")
		sel_insts = InstanceSet()
		sel_insts.filepath = self.filepath
		sel_insts.extra_svm_files = self.extra_svm_files
		sel_insts.selectors = selectors
		sel_insts.insts = insts
		return sel_insts

	def load_text(self):
		'''
		The text of instances are not stored in the prediction result file,
		so you need to call this function to load texts from testing data.

		>>> from libshorttext.analyzer import *
		>>> insts = InstanceSet('prediction_result_path')
		>>> insts.load_text()

		This method also load the extra svm features if extra svm files
		are used when training.
		'''
		EMPTY_MESSAGE = '**None**'
		sorted_insts = sorted(self.insts, key = lambda inst: inst.idx)
		i = 0
		for idx, lines in enumerate(izip(*([open(self.filepath, 'r')] + [open(f, 'r') for f in self.extra_svm_files]))):
			line = lines[0]
			extra_svm_feats = lines[1:]
			nr_extra_svm_feats = len(extra_svm_feats)
			if idx > sorted_insts[-1].idx:
				break
			if idx == sorted_insts[i].idx:
				try:
					sorted_insts[i].text = line.split('\t',1)[1].strip()
				except:
					sorted_insts[i].text = EMPTY_MESSAGE

				sorted_insts[i].extra_svm_feats = [None] * nr_extra_svm_feats
				for j, extra_svm_feat in enumerate(extra_svm_feats):
					try:
						sorted_insts[i].extra_svm_feats[j] = dict(map(lambda t: (int(t[0]), float(t[1])), [feat.split(':') for feat in extra_svm_feat.split(None, 1)[1].split()]))
					except:
						sorted_insts[i].extra_svm_feats[j] = EMPTY_MESSAGE
				i += 1
			
	def _load(self, src, text_src):
		if isinstance(src, PredictionResult):
			pass
		elif isinstance(src, str):
			result = PredictionResult()
			result.load(src)
		else:
			raise Exception('"result" should be PredictionResult or string.')
	
		if not result.analyzable():
			raise ValueError('The given result is not analyzable.')
	
		# +++ Need to move to another place.			   
		#if self.model._hashcode != result.model_id:
		#	sys.stderr.write('Warning: model ID is different from that in the predicted result. Do you use a different model to analyze?\n')
	
		if text_src is None:
			self.filepath = result.text_src
		else:
			self.filepath = text_src
		self.extra_svm_files = result.extra_svm_files
		predicted_y = result.predicted_y
		self.acc = result.get_accuracy()
		decvals = result.decvals
		true_y = result.true_y
				   
		self.insts, self.true_labels, self.predict_labels = [], set(), set()
		for idx in range(len(true_y)):
			self.insts += [TextInstance(idx, true_y = true_y[idx], predicted_y = predicted_y[idx], decvals = list(decvals[idx]))]
			self.true_labels.add(true_y[idx])
			self.predict_labels.add(predicted_y[idx])
	
class Analyzer:
	'''
	:class:`Analyzer` is a tool for analyzing a group of instances, which is
	controlled by :class:`InstanceSet`. Typically :class:`Analyzer` is initialized
	with a path to a model.

		>>> from libshorttext.analyzer import *
		>>> analyzer = Analyzer('model_path')

	It can also be initialized with a :class:`libshorttext.classifier.TextModel`
	instance.
	
		>>> from libshorttext.analyzer import *
		>>> from libshorttext.classifier import *
		>>> text_model = TextModel('model_path')
		>>> analyzer = Analyzer(text_model)
		
	You can also construct an analyzer without a model. However,
	model-dependent functions cannot be used.

		>>> from libshorttext.analyzer import *
		>>> analyzer = Analyzer()
	'''
	
	def __init__(self, model = None):
		self.labels = None
		self.model = None
		if model is not None:
			self.load_model(model)
		
	def load_model(self, model):
		'''
		:func:`load_model` is used to load a model into
		:class:`Analyzer`. If you did not load a model in the constructor or if you
		would like to use another model, you can use this function.

		There are two ways to load a model: from an instance of
		:class:`libshorttext.classifier.TextModel` or a path to a model.

		>>> from libshorttext.analyzer import *
		>>> analyzer = Analyzer('original_model_path')
		>>> analyzer.load_model('new_model_path')
		'''
		
		if isinstance(model, TextModel):
			self.model = model
		elif isinstance(model, str):
			self.model = TextModel()
			self.model.load(model)
		else:
			raise Exception('"model" should be TextModel or string.')
		self.labels = self.model.get_labels()
		
	def analyze_single(self, target, amount = 5, output = None, extra_svm_feats = []):
		'''
		:func:`analyze_single` is used to analyze a single instance. It prints
		weights of all features in some classes (default 5). The output is
		sorted according to decision values in descending order. *target* can be an
		instance or a string that you want to analyze. *amount* is how many instances
		you want to print. If *output* is specified by a path to a file, the
		result will be outputted to the file instead of on the screen.

			>>> from libshorttext.analyzer import *
			>>> analyzer = Analyzer('model_path')
			>>> insts = InstanceSet('prediction_result_path')
			>>> insts.load_text()
			>>> analyzer.analyze_single(insts[61], 3)
			                    Jewelry & Watches  Cameras & Photo  Coins & Paper Money
			pb                          7.589e-19        2.041e-01            0.000e+00
			green                      -8.897e-02        1.227e-02           -1.507e-01
			mm                          5.922e-01        6.731e-01            1.256e-03
			onyx silver                 1.382e-01       -6.198e-02           -4.743e-19
			48                         -1.792e-02        2.188e-02           -1.346e-04
			pendant                     1.107e+00       -1.039e-01           -1.409e-01
			silver pendant              2.455e-01       -7.826e-02           -8.379e-02
			silver                      8.533e-01       -2.205e-02            8.076e-01
			onyx                        1.520e-01       -6.198e-02           -4.743e-19
			**decval**                  9.937e-01        1.944e-01            1.444e-01
			>>> analyzer.analyze_single('MICKEY MOUSE POT STAKE', 3)
			                Home & Garden  Video Games & Consoles  Computers/Tablets & Networking
			mickey              9.477e-02              -3.168e-02                       6.722e-02
			mouse               2.119e-01               2.039e-01                      -2.212e-02
			pot                 8.897e-01              -5.167e-02                      -2.466e-02
			stake               4.057e-01              -2.147e-02                      -3.699e-02
			mickey mouse        1.146e-01              -3.168e-02                       6.784e-02
			mouse pot           4.041e-01              -2.147e-02                      -1.588e-02
			pot stake           5.363e-01              -2.147e-02                      -1.588e-02
			**decval**          1.004e+00               9.255e-03                       7.385e-03


		If *target* is a :class:`str` and extra svm files are used in 
		training, the same number of extra svm features can be 
		specified in *extra_svm_feats*. Extra svm features should be 
		a list of dictionaries. If *target* is a :class:`TextInstance`,
		the extra features in the :class:`TextInstance` will be used.
		'''
		if self.model is None:
			raise Exception('Model not loaded.')
		if isinstance(target,str):
			text = target
			true_y = None
			result = predict_single_text(text, self.model, extra_svm_feats = extra_svm_feats)
			decvals = result.decvals
		elif isinstance(target,TextInstance):
			if target.text is None:
				raise Exception('Please load texts first.')
			text, extra_svm_feats, true_y = target.text, target.extra_svm_feats, target.true_y
			decvals = target.decvals
		if isinstance(output, str):
			output = open(output, 'w')

		features, weights, labels = self.model.get_weight(text, extra_svm_feats = extra_svm_feats)
		nr_labels = len(labels)
		nr_feats = len(features)
		if not features or not weights:
			raise Exception('Invalid instance.')
		features = [' '.join(feature) for feature in features]
		features += ['**decval**']
		weights_table = [[0]*nr_labels]*(nr_feats+1)
		sorted_idx = sorted(xrange(nr_labels), key=lambda i:decvals[i], reverse=True)
		labels = [labels[idx] for idx in sorted_idx]

		for feat in xrange(nr_feats):
			formatter = lambda idx: '{0:.3e}'.format(weights[feat][idx])
			weights_table[feat] = [formatter(idx) for idx in sorted_idx]
		weights_table[-1] = ['{0:.3e}'.format(decvals[idx]) for idx in sorted_idx]

		if amount != 0:
			labels = labels[:amount]
		draw_table(features, labels, weights_table, output)
		if true_y is not None:
			print('True label: {0}'.format(true_y))

	def _calculate_info(self, pred_insts):
		pred_insts.quantity = len(pred_insts.insts)
		pred_insts.true_labels, pred_insts.predict_labels, pred_insts.correct = \
			set(), set(), 0
		for inst in pred_insts.insts:
			pred_insts.true_labels.add(inst.true_y)
			pred_insts.predict_labels.add(inst.predicted_y)
			if inst.true_y == inst.predicted_y:
				pred_insts.correct += 1
		
	def info(self, pred_insts, output = None):
		'''
		:func:`info` gets information about a group of instances (an object
		of :class:`InstanceSet`). *pred_insts* is the target instances. If *output*
		is specified by a path to a file, the result will be outputted to the file
		instead of on the screen.

			>>> from libshorttext.analyzer import *
			>>> analyzer = Analyzer('model_path')
			>>> insts = InstanceSet('prediction_result_path')
			>>> insts = insts.select(with_labels(['Books', 'Music', 'Art']))
			>>> analyzer.info(insts)
			Number of instances: 554
			Accuracy: 0.983754512635 (545/554)
			True labels: "Art"  "Books"  "Music"
			Predict labels: "Art"  "Books"  "Music"
			Text source:
			/home/guestwalk/working/short_text/svn/software-dev/test_file
			Selectors:
			-> labels: "Books", "Music", "Art"
		'''
		if isinstance(output, str):
			output = open(output, 'w')
		if pred_insts.quantity is None:
			self._calculate_info(pred_insts)
		acc = float(pred_insts.correct)/pred_insts.quantity

		string = '''Number of instances: {quantity}
Accuracy: {acc} ({correct}/{quantity}) 
True labels: {true_y}
Predicted labels: {predicted_y}
Text source: {text_src}
Selectors: \n-> {selectors}'''\
			  .format(quantity = pred_insts.quantity, correct = pred_insts.correct,\
					  acc = acc, true_y = '"'+'"  "'.join(pred_insts.true_labels)+'"',\
					  predicted_y = '"'+'"  "'.join(pred_insts.predict_labels)+'"',\
					  text_src = os.path.abspath(pred_insts.filepath),\
					  selectors = '\n-> '.join(pred_insts.selectors))

		write(string, output)

	def gen_confusion_table(self, pred_insts, output = None):
		'''
		:func:`gen_confusion_table` generates a confusion table of a group of
		predicted instances *pred_insts*. If *output* is specified by a path 
		to a file, the result will be outputted to the file instead of  
		on the screen.

			>>> from libshorttext.analyzer import *
			>>> analyzer = Analyzer('model_path')
			>>> insts = InstanceSet('prediction_result_path')
			>>> insts = insts.select(with_labels(['Books', 'Music', 'Art']))
			>>> analyzer.gen_confusion_table(insts)
			         Books  Music  Art
			Books      169      1    0
			Music        2    214    0
			Art          6      0  162
		'''
		if isinstance(output, str):
			output = open(output, 'w')
		if pred_insts.quantity is None:
			self._calculate_info(pred_insts)
		labels = pred_insts.true_labels.union(pred_insts.predict_labels)
		#columns = rows
			
		invalid_labels = []
		for label in labels:
			if label not in pred_insts.true_labels and label not in pred_insts.predict_labels:
				invalid_labels.append(label)
		if invalid_labels:
			invalid_labels = ' '.join(invalid_labels)
			raise Exception('Labels {0} are invalid.'.format(invalid_labels))

		labels_dic = dict(zip(labels, xrange(len(labels))))
		confusion_table = [[0 for i in range(len(labels_dic))] for j in range(len(labels_dic))]
		for inst in pred_insts.insts:
			if inst.true_y in labels_dic and inst.predicted_y in labels_dic:
				confusion_table[labels_dic[inst.true_y]][labels_dic[inst.predicted_y]] += 1
		for idx_row, row in enumerate(confusion_table):
			for idx_col, col in enumerate(row):
				confusion_table[idx_row][idx_col] = str(confusion_table[idx_row][idx_col])

		draw_table(labels, labels, confusion_table, output)
		
		if output:
			output.close()
	
def write(string, output = None):
	if output is None:
		print(string)
	else:
		output.write(string + '\n')

		
def draw_table(rows, columns, table, output = None):
	offset = 2
	column_widths = []
	title_width = max([len(row) for row in rows]) + offset
		
	for col_idx, column in enumerate(columns):
		column_widths.append(max([len(table[row_idx][col_idx]) \
				for row_idx, row in enumerate(rows)] + [len(column)]) + offset)
		
	string = ''.ljust(title_width)
	for idx, column in enumerate(columns):
		string += column.rjust(column_widths[idx])
	write(string, output)

	for row_idx, row in enumerate(rows):
		string = row.ljust(title_width)
		for col_idx, column in enumerate(columns):
			string += table[row_idx][col_idx].rjust(column_widths[col_idx])
		write(string, output)
