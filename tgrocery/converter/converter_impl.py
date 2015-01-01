#!/usr/bin/env python

__all__ = ["TextPreprocessor", "FeatureGenerator", "ClassMapping", "Text2svmConverter", "convert_text"]

import sys, os
import unicodedata, re
from collections import defaultdict

if sys.version_info[0] >= 3:
	xrange = range
	import pickle as cPickle
	izip = zip
	def unicode(string, setting):
		return string
else :
	import cPickle
	from itertools import izip


# import porter stemmer
from .stemmer import porter


from ctypes import *
# XXX This function must support outputing to one of the input file!!
def _merge_files(svm_files, offsets, is_training, output):	
	if not isinstance(offsets, list) or len(svm_files) != len(offsets):
		raise ValueError('offsets should be a list where the length is the number of merged files')
	
	util = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'classifier', 'learner', 'util.so.1'))
	util.merge_problems.restype = None
	util.merge_problems.argtypes = [POINTER(c_char_p), c_int, POINTER(c_int64), c_char_p, c_char, POINTER(c_int64)]

	size = len(svm_files)

	c_svm_files = (c_char_p * size)()
	for i, f in enumerate(svm_files):
		c_svm_files[i] = c_char_p(f.encode())
	c_offsets = (c_int64 * size)()
	if not is_training:
		for i, v in enumerate(offsets):
			c_offsets[i] = c_int64(v)
	c_is_training = c_char(chr(is_training).encode('ascii'))
	c_error_code = c_int64()

	output = c_char_p(bytes(output,'utf-8')) if sys.version_info[0] >= 3 else c_char_p(output)
	util.merge_problems(c_svm_files, c_int(size), c_offsets, output, c_is_training, c_error_code)

	error_code = c_error_code.value

	if error_code > 0:
		raise ValueError('wrong file format in line ' + str(error_code))
	elif error_code == -1:
		raise IOError('cannot open file')
	elif error_code == -2:
		raise MemoryError("Memory Exhausted. Try to restart python.")
	elif error_code == -3:
		raise ValueError('merging svm files of different sizes')
	elif error_code == -4:
		raise ValueError('at least one file should be given to merge')

	if is_training:
		for i in range(size):
			offsets[i] = c_offsets[i]

def _iterdict(d):
	if sys.version_info[0] >= 3: 
		return d.items()
	else :
		return d.iteritems()

def _dict2list(d):
	if len(d) == 0: return []
	
	#XXX check if we can replace the following line to "m = len(d)"
	m = max(v for k,v in _iterdict(d))
	ret = [''] * (m+1)
	for k,v in _iterdict(d): 
		ret[v] = k
	return ret

def _list2dict(l):
	return dict((v,k) for k,v in enumerate(l))

class TextPreprocessor(object):
	"""
	:class:`TextPreprocessor` is used to pre-process the raw texts to a
	:class:`list` of feature indices. First, each text is tokenized by the 
	:attr:`tokenizer` into a :class:`list` of tokens. Tokens are then passed to 
	the :attr:`stemmer` and the :attr:`stopword_remover`. Finally, each 
	stemmed token is converted to a token index. 

	Refer to :meth:`parse_option` for the *option* parameter. 
	
	If *readonly* is set to ``True``, the feature index mapping will not
	be updated even if new tokens are explored. These new tokens will be
	ignored. *readonly* should be set as ``True`` for test, and ``False``
	for training.

	"""
	def __init__(self, option='-stemming 0 -stopword 0', readonly=False):
		self._option  = option
		self._readonly=readonly
		self.tok2idx = {'>>dummy<<':0}
		self.idx2tok = None
		opts = self.parse_option(option)
		#: The function used to stem tokens. 
		#:
		#: Refer to :ref:`CustomizedPreprocessing`.
		self.stemmer = opts[0]
		#: The function used to remove stop words.
		#:
		#: Refer to :ref:`CustomizedPreprocessing`.
		self.stopword_remover = opts[1]
		#: The function used to tokenize texts into a :class:`list` of tokens. 
		#:
		#: Refer to :ref:`CustomizedPreprocessing`.
		self.tokenizer = self.default_tokenizer

	def parse_option(self, option):
		"""
		Parse the given :class:`str` parameter *option* and set 
		:attr:`stemmer` and :attr:`stopword_remover` to the desired functions.

		*option* is a :class:`str` instance:

		================== ==========================================
		Options            Description
		================== ==========================================
		-stopword *method* If *method* is `1`, then 
				   :meth:`default_stoplist` is used. If 
				   *method* is `0`, then no word will be 
				   removed. Default is `0` (no stopword removal).
		-stemming *method* If *method* is `1`, then Porter stemmer is 
		                   used. If *method* is `0`, tokens are not 
				   stemmed. Default is `0` (no stemming).
		================== ==========================================

		The following example creates a :class:`TextPreprocessor` that 
		applies Porter stemmer and removes stop words.

		>>> preprocessor = TextPreprocessor()
		>>> preprocessor.parse_option('-stopword 1 -stemming 1')

		.. note::
			
			Redundant options are ignored quietly. Users should pay attention
			to the spelling of the options.
		"""
		option = option.strip().split()
		stoplist, tokstemmer = set(), lambda x: x
		i = 0
		while i < len(option):
			if option[i][0] != '-': break
			if option[i] == '-stopword': 
				if int(option[i+1]) != 0: 
					stoplist = self.default_stoplist()
			elif option[i] == '-stemming': 
				if int(option[i+1]) != 0:
					tokstemmer = porter.stem
			i+=2
		stoplist = set(tokstemmer(x) for x in stoplist)
		stemmer = lambda text: map(tokstemmer, text)
		stopword_remover = lambda text: filter(lambda tok: tok not in stoplist, text)
		return stemmer, stopword_remover

	def get_idx2tok(self, idx):
		""" 
		Access the index-token mapping. Given a numerical *idx*, this 
		function returns the corresponding token.

		.. note::

			Because the index-to-token mapping is not maintained internally, the first
			time to call this function takes longer time to build the reverse 
			mapping. This function should be always called with a readonly 
			:class:`TextPreprocessor` instance to avoid inconsistence between 
			the token-to-index mapping and its reverse.
		"""
		if not self.idx2tok: 
			self.idx2tok = _dict2list(self.tok2idx)
		return self.idx2tok[idx]

	def save(self, dest_file):
		"""
		Save the :class:`TextPreprocessor` to a file.
		
		.. note::

			Function variables are not saved by this method.
			Even if :attr:`stopword_remover`, :attr:`stemmer`, or
			:attr:`tokenizer` are modified, they will **not** be 
			saved accordingly. Therefore, they must be set again 
			after being loaded. Refer to :ref:`CustomizedPreprocessing`.
		"""
		self.idx2tok = _dict2list(self.tok2idx)
		config = {'option':self._option,'idx2tok':self.idx2tok}
		cPickle.dump(config, open(dest_file,'wb'), -1)

	# by default, mapping file will be not updated when we load the file 
	def load(self, src_file, readonly=True):
		"""
		Load the :class:`TextPreprocessor` instance from the *src_file* file,
		which is a pickle file generated by :class:`cPickle`. 

		If *readonly* is `True`, the :class:`TextPreprocessor` instance will
		not be modifiable.
		"""
		config = cPickle.load(open(src_file,'rb'))
		self._readonly = readonly
		self._option = config['option']
		self.idx2tok = config['idx2tok']
		self.tok2idx = _list2dict(config['idx2tok'])
		self.stemmer, self.stopword_remover = self.parse_option(config['option'])
		self.tokenizer = self.default_tokenizer
		return self

	@staticmethod
	def default_stoplist():
		"""
		Return a default stopword list provided by LibShortText.

		Note that LibShortText stems words first (if stemmer is 
		provided). Therefore, all words on the stopword list should
		be stemmed first. The following example creates a stoplist_remover 
		from a list.

		>>> from libshorttext.converter import *
		>>> 
		>>> preprocessor = TextPreprocessor('-stemming 1')
		>>> stoplist = preprocessor.stemmer(list(TextPreprocessor.default_stoplist()))
		>>> preprocessor.stopword_remover = lambda text: filter(
		... 	lambda token: token not in stoplist, text)

		"""

		# This function only parses the default stop word list file.
		# *src* should not be an argument.
		src = "" 
		if not src:
			src = '{0}/stop-words/stoplist-nsp.regex'.format(os.path.dirname(os.path.abspath(__file__)))
		srcfile = open(src)
		stoplist = set(map(chr, range(ord('a'),ord('z')+1)))
		srcfile.readline()
		srcfile.readline()
		for line in srcfile:
			stoplist.add(line[5:-4].lower().replace(']',''))
		return stoplist

	# check if a better and more efficient way to tokenize text
	# http://stackoverflow.com/questions/9455510/remove-all-non-ascii-from-string
	@staticmethod
	def default_tokenizer(text):
		"""
		The default tokenizer provided by LibShortText.

		The default tokenizer is used to tokenize English documents.
		It splits a text to tokens by whitespace characters, and 
		normalizes tokens using `NFD (normalization form D) <http://docs.python.org/2/library/unicodedata.html#unicodedata.normalize>`_.
		"""
		def foo(c):
			if ord(c)>127: return ''
			if c.isdigit() or c.isalpha(): return c
			else : return ' '

		text = unicodedata.normalize('NFD', unicode(text, 'utf-8')).lower()
		text = ''.join(map(foo,text))
		text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)
		text = re.sub(r'([0-9])([a-z])', r'\1 \2', text)
		text = re.sub(r'\s+', r' ', text)
		return text.strip().split()

	def preprocess(self, text):
		"""
		Preprocess the given *text* into a :class:`list` of token indices, where
		*text* is a :class:`str` instance.

		If the preprocessor is not in the read-only mode, :meth:`preprocess` expands the internal
		token-index mapping for unseen tokens; otherwise, this function 
		ignores unseen tokens. 
		"""
		text = self.tokenizer(text)
		text = self.stemmer(text)
		text = self.stopword_remover(text)
		ret = []
		for i,tok in enumerate(text):
			if tok not in self.tok2idx:
				if self._readonly: continue
				self.tok2idx[tok] = len(self.tok2idx)
				self.idx2tok = None
			ret += [self.tok2idx[tok]]
		return ret


class FeatureGenerator(object):
	"""
	:class:`FeatureGenerator` is used to generate uni-gram or bi-gram features.
	"""

	def __init__(self, option='-feature 1', readonly=False):
		#: :attr:`option` is a :class:`str` instance, which could be
		#: ``-feature 0``: uni-gram features
		#: ``-feature 1``: bi-gram features (default)
		self._option = option
		#: :attr:`readonly` is a :class:`bool` variable used to indicate whether
		#: the future operations of this instance can update the internal 
		#: ngram-index mapping. (the default value is ``False``).
		self._readonly = readonly
		self.ngram2fidx = {'>>dummy<<':0}
		self.fidx2ngram=None
		#: :attr:`feat_gen` is variable pointing to the function that conducts 
		#: feature generation. It can be either :func:`unigram` or 
		#: :func:`bigram`, determined by :attr:`option`.
		self.feat_gen = self.parse_option(option)

	def parse_option(self, option):
		"""
		Parse the given :class:`str` parameter *option* and set 
		:attr:`feat_gen` to the desired function.

		There is only one option in this version.

		================= ========================================
		Option            Description
		================= ========================================
		-feature *method* If *method* is `1`, then bigram is used.
		                  If *method* is `0`, unigram is used.
				  Default is `1` (bigram).
		================= ========================================

		For example, the following example creates a unigram feature
		generator.

		>>> feature_generator = FeatureGenerator()
		>>> feature_generator.parse_option('-feature 0')

		.. note::
		
			Redundant options are ignored quietly. Users should pay attention
			to the spelling of the options.
		"""
		option = option.strip().split()
		feat_gen = self.bigram
		i = 0
		while i < len(option):
			if option[i][0] != '-': break
			if option[i] == '-feature': 
				if int(option[i+1]) == 0: 
					feat_gen = self.unigram
			i+=2
		return feat_gen 

	def get_fidx2ngram(self, fidx):
		""" 
		Access the index-to-ngram mapping. Given a numerical
		*fidx*, this function returns the corresponding ngram.

		.. note::

			Because the index-to-ngram mapping is not maintained internally, the first
			time to call this function takes longer time to build the 
			mapping. This function should be always called with a readonly 
			:class:`FeatureGenerator` instance to avoid inconsistence between 
			the ngram-to-index mapping and its reverse.
		"""
		if not self.fidx2ngram: 
			self.fidx2ngram = _dict2list(self.ngram2fidx)
		return self.fidx2ngram[fidx]

	def save(self, dest_file):
		"""
		Save the :class:`FeatureGenerator` instance into the *dest_file* file,
		which will be a pickle file generated by :class:`cPickle`. We suggest 
		using Python 2.7 or newer versions for faster implementation of 
		:class:`cPickle`.
		"""
		self.fidx2ngram = _dict2list(self.ngram2fidx)
		config = {'option':self._option,'fidx2ngram':self.fidx2ngram}
		cPickle.dump(config, open(dest_file,'wb'), -1)

	# by default, mapping file will be not updated when we load the file 
	def load(self, src_file, readonly=True):
		"""
		Load the :class:`FeatureGenerator` instance from the *src_file* file,
		which is a pickle file generated by :class:`cPickle`. We suggest using 
		Python 2.7 or newer versions for faster implementation of 
		:class:`cPickle`.

		If *readonly* is `True`, the :class:`FeatureGenerator` instance will
		be readonly. 
		"""
		config = cPickle.load(open(src_file,'rb'))
		self._option = config['option']
		self.fidx2ngram = config['fidx2ngram']
		self.ngram2fidx = _list2dict(config['fidx2ngram'])
		self._readonly=readonly
		self.feat_gen = self.parse_option(config['option'])
		return self
		
	def toSVM(self, text):
		"""
		Generate a :class:`dict` instance for the given *text*, which is a 
		:class:`list` of tokens. Each `key` of the returning dictionary
		is an index corresponding to an ngram feature, while the
		corresponding `value` is the count of the occurrence of that feature.

		If not in read only mode, this function expands the internal
		ngram-index mapping for unseen ngrams; otherwise, this function 
		ignores unseen ngrams. 
		
		"""
		return self.feat_gen(text)
		#return ''.join(' %d:%d' %(f, feat[f]) for f in sorted(feat))

	def unigram(self, text):
		"""
		Generate a :class:`dict` corresponding to the sparse vector of the 
		uni-gram representation of the given *text*, which is a 
		:class:`list` of tokens.
		"""
		feat = defaultdict(int)
		NG = self.ngram2fidx
		for x in text:
			if (x,) not in NG:
				if self._readonly: continue
				NG[x,] = len(NG)
				self.fidx2ngram = None
			feat[NG[x,]]+=1
		return feat

	def bigram(self, text):
		"""
		Generate a :class:`dict` corresponding to the sparse vector of the bi-gram
		representation of the given *text*, which is a :class:`list` of tokens.
		"""
		feat = self.unigram(text) 
		NG = self.ngram2fidx
		for x,y in zip(text[:-1], text[1:]):
			if (x,y) not in NG: 
				if self._readonly: continue
				NG[x,y] = len(NG)
				self.fidx2ngram = None
			feat[NG[x,y]]+=1
		return feat


class ClassMapping(object):
	"""
	:class:`ClassMapping` is used to handle the mapping between the class label
	and the internal class index.

	*option* is ignored in this version.
	"""
	def __init__(self, option='', readonly=False):
		# No option in this version
		self._option = option
		#::attr:`readonly` is a :class:`bool` variable used to indicate whether
		#:the future operations of this instance can update the internal 
		#:label-index mapping. (the defaut value is ``False``).
		self._readonly = readonly
		self.class2idx = {}
		self.idx2class = None

	def save(self, dest_file):
		"""
		Save the :class:`ClassMapping` instance into the *dest_file* file,
		which will be a pickle file generated by :class:`cPickle`.
		"""
		self.idx2class = _dict2list(self.class2idx)
		config = {'option':self._option,'idx2class':self.idx2class}
		cPickle.dump(config, open(dest_file,'wb'), -1)

	# by default, mapping file will be not updated when we load the file 
	def load(self, src_file, readonly=True):
		"""
		Load the :class:`ClassMapping` instance from the *src_file* file,
		which is a pickle file generated by :class:`cPickle`. 

		If *readonly* is `True`, the :class:`ClassMapping` instance will
		be readonly. 
		"""
		config = cPickle.load(open(src_file,'rb'))
		self._readonly = readonly
		self._option = config['option']
		self.idx2class = config['idx2class']
		self.class2idx = _list2dict(config['idx2class'])
		return self


	def toIdx(self, class_name):
		"""
		Return the internal class index for the given *class_name*.

		If :attr:`readonly` is `False`, :func:`toIdx` generates a new index
		for a unseen *class_name*; otherwise, :func:`toIdx` returns `None`.
		"""
		if class_name in self.class2idx:
			return self.class2idx[class_name]
		elif self._readonly:
			return None

		m = len(self.class2idx)
		self.class2idx[class_name] = m
		self.idx2class = None
		return m

	def toClassName(self, idx):
		"""
		Return the class label corresponding to the given class *idx*. 
		
		.. note::

			This method will reconstruct the mapping if :meth:`toIdx`
			has been called after the previous :meth:`toClassName`.
			Users should not call :meth:`toClassName` and :meth:`toIdx`
			rotatively.
			
		"""
		if self.idx2class is None:
			self.idx2class = _dict2list(self.class2idx)
		if idx == -1:
			return "**not in training**"
		if idx >= len(self.idx2class): 
			raise KeyError('class idx ({0}) should be less than the number of classes ({0}).'.format(idx, len(self.idx2class)))
		return self.idx2class[idx]

	def rename(self, old_label, new_label):
		"""
		Rename the *old_label* to the *new_label*. 
		*old_label* can be either a :class:`str` to denote the class label or an
		:class:`int` class to denote the class index.  
		*new_label* should be a :class:`str` different from existing labels.
		"""
		if not isinstance(new_label, str):
			raise TypeError("new_label should be a str")

		if isinstance(old_label, int):
			old_label = toClassName(old_label)
		if isinstance(old_label, str):
			if old_label not in self.class2idx:
				raise ValueError('class {0} does not exist'.format(old_label))
		else:
			raise TypeError("old label should be int (index) or str (name)")

		if new_label in self.class2idx:
			raise ValueError('class {0} already exists'.format(new_label))

		self.class2idx[new_label] = self.class2idx.pop(old_label)	
		self.idx2class = None


class Text2svmConverter(object):
	"""
	:class:`Text2svmConverter` converts a text data to a LIBSVM-format data.
	(Refer to :ref:`dataset` for text data format.) It consists of three
	components: :class:`TextPreprocessor`, :class:`FeatureGenerator`, and 
	:class:`ClassMapping`.

	The *option* can be any option of :class:`TextPreprocessor`, 
	:class:`FeatureGenerator` and :class:`ClassMapping`.
	
	.. note::
		
		Redundant options are ignored quietly. Users should pay attention
		to the spelling of the options.

	:class:`Text2svmConverter` can be read only if the flag is set. If it is
	not read only, the converter will be updated if new tokens or new class
	names are found.
	"""

	def __init__(self, option="", readonly=False):
		self._option = option
		self._readonly = readonly
		self._extra_nr_feats = []
		self._extra_file_ids = []
		text_prep_opt, feat_gen_opt, class_map_opt = self._parse_option(option)
		#: The :class:`TextPreprocessor` instance.
		self.text_prep = TextPreprocessor(text_prep_opt, readonly)
		#: The :class:`FeatureGenerator` instance.
		self.feat_gen = FeatureGenerator(feat_gen_opt, readonly)
		#: The :class:`ClassMapping` instance.
		self.class_map = ClassMapping(class_map_opt, readonly)

	def _parse_option(self, option):
		text_prep_opt, feat_gen_opt, class_map_opt = '', '', ''
		option = option.strip().split()
		i = 0
		while i < len(option):
			if i+1 >= len(option):
				raise ValueError("{0} cannot be the last option.".format(option[i]))

			if type(option[i+1]) is not int and not option[i+1].isdigit():
				raise ValueError("Invalid option {0} {1}.".format(option[i], option[i+1]))
			if option[i] in ['-stopword', '-stemming']: 
				text_prep_opt = ' '.join([text_prep_opt, option[i], option[i+1]])
			elif option[i] in ['-feature']: 
				feat_gen_opt = ' '.join([feat_gen_opt, option[i], option[i+1]])
			else:
				raise ValueError("Invalid option {0}.".format(option[i]))
			i+=2
		return text_prep_opt, feat_gen_opt, class_map_opt

	def merge_svm_files(self, svm_file, extra_svm_files):
		"""
		Append extra feature files to *svm_file*.

		*extra_svm_files* is a class:`list` of extra feature files in
		LIBSVM-format. These features will be appended to *svm_file*.
		All files in *extra_svm_files* and *svm_file* should have the
		same number of instances.

		.. note::
			The output file is *svm_file*. Therefore, the original
			*svm_file* will be overwritten without backup.
		"""
		if not isinstance(extra_svm_files, (tuple, list)):
			raise TypeError('extra_svm_files should be a tuple or a list')

		nr_files = len(extra_svm_files)

		if self._readonly: # test
			if len(self._extra_file_ids) != nr_files:
				raise ValueError('wrong number of extra svm files ({0} expected)'.format(len(self._extra_file_ids)))
			if nr_files == 0: return
			
			_merge_files([svm_file] + extra_svm_files, self._extra_nr_feats, False, svm_file)

		else: # train
			if nr_files == 0: return
			
			self._extra_file_ids = [os.path.basename(f) for f in extra_svm_files]
			self._extra_nr_feats = [0] * (nr_files + 1)
			_merge_files([svm_file] + extra_svm_files, self._extra_nr_feats, True, svm_file)


	def save(self, dest_dir):
		"""
		Save the model to a directory.
		"""
		
		config = {'text_prep':'text_prep.config.pickle',
				'feat_gen':'feat_gen.config.pickle',
				'class_map':'class_map.config.pickle',
				'extra_nr_feats': 'extra_nr_feats.pickle',
				'extra_file_ids': 'extra_file_ids.pickle'}
		if not os.path.exists(dest_dir): os.mkdir(dest_dir)
		self.text_prep.save(os.path.join(dest_dir,config['text_prep']))
		self.feat_gen.save(os.path.join(dest_dir,config['feat_gen']))
		self.class_map.save(os.path.join(dest_dir,config['class_map']))
		
		cPickle.dump(self._extra_nr_feats, open(os.path.join(dest_dir, config['extra_nr_feats']), 'wb'), -1)
		cPickle.dump(self._extra_file_ids, open(os.path.join(dest_dir, config['extra_file_ids']), 'wb'), -1)

	def load(self, src_dir, readonly=True):
		"""
		Load the model from a directory.
		"""
		
		self._readonly = readonly

		config = {'text_prep':'text_prep.config.pickle',
				'feat_gen':'feat_gen.config.pickle',
				'class_map':'class_map.config.pickle',
				'extra_nr_feats': 'extra_nr_feats.pickle',
				'extra_file_ids': 'extra_file_ids.pickle'}
		self.text_prep.load(os.path.join(src_dir,config['text_prep']),readonly)
		self.feat_gen.load(os.path.join(src_dir,config['feat_gen']),readonly)
		self.class_map.load(os.path.join(src_dir,config['class_map']),readonly)
		
		self._extra_nr_feats = cPickle.load(open(os.path.join(src_dir, config['extra_nr_feats']), 'rb'))
		self._extra_file_ids = cPickle.load(open(os.path.join(src_dir, config['extra_file_ids']), 'rb'))
		return self

	def get_fidx2tok(self, fidx):
		"""
		Return the token by the corresponding feature index.
		"""
		
		bases = self._extra_nr_feats
		if len(bases) <= 0 or fidx <= bases[0]:
			idx2tok = self.text_prep.get_idx2tok
			fidx2ngram = self.feat_gen.get_fidx2ngram
			return [idx2tok(idx) for idx in fidx2ngram(fidx)]
		else : 
			for i in range(len(self._extra_file_ids)):
				if fidx <= bases[i+1]:
					return ['{0}:{1}'.format(self._extra_file_ids[i], fidx - bases[i])]

	def toSVM(self, text, class_name = None, extra_svm_feats = []):
		"""
		Return an LIBSVM python interface instance by the *text*. Note
		that :attr:`feat_gen` will be updated if the converter is not
		read only and there are new tokens in the given text.

		*extra_svm_feats* is a list of feature sets, each of which is a 'class':`dict`. 
		The length should be zero or the same as the extra svm files used. If
		the length is zero (i.e., an empty list), then the features returned 
		as if there is no extra svm files.
		
		"""

		if len(extra_svm_feats) > 0 and self._readonly and len(self._extra_file_ids) != 0 and len(self._extra_file_ids) != len(extra_svm_feats):
			raise ValueError("wrong size of extra_svm_feats")


		text = self.text_prep.preprocess(text)
		feat = self.feat_gen.toSVM(text)
		bases = self._extra_nr_feats
		for i, extra_feat in enumerate(extra_svm_feats):
			for fid in extra_feat:
				if bases[i] + fid > bases[i+1]:
					continue
				feat[bases[i]+fid] = extra_feat[fid]

		if class_name is None:
			return feat

		return feat, self.getClassIdx(class_name)

	def getClassIdx(self, class_name):
		"""
		Return the class index by the class name.
		"""
		return self.class_map.toIdx(class_name)

	def getClassName(self, class_idx):
		"""
		Return the class name by the class index.
		"""
		return self.class_map.toClassName(class_idx)

	def __str__(self):
		return 'Text2svmConverter: ' + (self._option or 'default')


def convert_text(text_src, converter, output=''):
	"""
	Convert a text data to a LIBSVM-format data.

	*text_src* is the path of the text data or a :class:`file`. (Refer to 
	:ref:`dataset`). *output* is the output of the converted LIBSVM-format
	data. *output* can also be a file path or a :class:`file`. Note that 
	if *text_src* or *output* is a :class:`file`, it will be closed.
	*converter* is a :class:`Text2svmConverter` instance.
	"""
	
	if output == "": output = text_src+'.svm'
	if isinstance(output, str):
		output = open(output,'w')
	elif not isinstance(output, file):
		raise TypeError('output is a str or a file.')

	if isinstance(text_src, str):
		text_src = open(text_src)
	elif not isinstance(text_src, file):
		raise TypeError('text_src is a str or a file.')
	

	# add some error handling here!!
	for line in text_src:
		try:
			label, text = line.split('\t', 1)
		except Exception as e:
			label, text = '**ILL INST**', '**ILL INST**'
			#raise ValueError('cannot tokenize: ' + line)
		feat, label = converter.toSVM(text, label)
		feat = ''.join(' {0}:{1}'.format(f,feat[f]) for f in sorted(feat))
		if label == None: label = -1
		output.write(str(label) + ' ' +feat+'\n')
	output.close()
	text_src.close()

