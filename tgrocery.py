"""
TextGrocery is a simple short-text classification tool based on LibShortText.
"""

import os
from collections import defaultdict

from libshorttext.classifier import *
from libshorttext.converter import *
import jieba


class GroceryException(Exception):
    pass


class GroceryTextPreProcessor(object):
    def __init__(self):
        self.tok2idx = {}

    @staticmethod
    def _default_tokenize(text):
        return jieba.cut(text, cut_all=True)

    def preprocess(self, text):
        tokens = self._default_tokenize(text)
        ret = []
        for idx, tok in enumerate(tokens):
            if tok not in self.tok2idx:
                self.tok2idx[tok] = len(self.tok2idx)
            ret.append(self.tok2idx[tok])
        return ret


class GroceryFeatureGenerator(object):
    def __init__(self):
        pass

    def unigram(self, text):
        feat = defaultdict(int)
        NG = self.ngram2fidx
        for x in text:
            if (x,) not in NG:
                if self._readonly: continue
                NG[x,] = len(NG)
                self.fidx2ngram = None
            feat[NG[x,]] += 1
        return feat

    def bigram(self, text):
        feat = self.unigram(text)
        NG = self.ngram2fidx
        for x, y in zip(text[:-1], text[1:]):
            if (x, y) not in NG:
                if self._readonly: continue
                NG[x, y] = len(NG)
                self.fidx2ngram = None
            feat[NG[x, y]] += 1
        return feat


class ClassMapping(object):
    def __init__(self):
        pass


class GroceryTextConverter(object):
    def __init__(self):
        self.text_prep = GroceryTextPreProcessor()
        self.feat_gen = GroceryFeatureGenerator()
        self.class_map = ClassMapping()

    def transfer_svm(self, text):
        feat = self.feat_gen.bigram(self.text_prep.preprocess(text))


class Grocery(object):
    def __init__(self, name, tokenizer=None):
        self.name = name
        if tokenizer is not None:
            if hasattr(tokenizer, '__call__'):
                self.tokenizer = tokenizer
            else:
                raise GroceryException()
        self.model = None

    def get_load_status(self):
        return self.model is not None

    def train(self, train_file):
        text_converter = Text2svmConverter()
        if self.tokenizer is not None:
            text_converter.text_prep.tokenizer = self.tokenizer
        svm_file = '%s.svm' % self.name
        convert_text(train_file, text_converter, svm_file)
        self.model = train_converted_text(svm_file, text_converter)
        return self

    def predict(self, single_text):
        if not self.get_load_status():
            raise GroceryException()
        return predict_single_text(single_text, self.model).predicted_y

    def test(self, test_file):
        if not self.get_load_status():
            raise GroceryException()
        predict_result = predict_text(test_file, self.model, svm_file='%s_test.svm' % self.name)
        self.show_accuracy(predict_result)

    @staticmethod
    def show_accuracy(predict_result):
        print("Accuracy = {0:.4f}% ({1}/{2})".format(
            predict_result.get_accuracy() * 100,
            sum(ty == py for ty, py in zip(predict_result.true_y, predict_result.predicted_y)),
            len(predict_result.true_y)))

    def save(self):
        if not self.get_load_status():
            raise GroceryException()
        self.model.save(self.name, force=True)

    def load(self):
        # Overwrite the previous model?
        if self.get_load_status():
            raise GroceryException()
        self.model = TextModel(self.name)
        if self.tokenizer is not None:
            self.model.text_converter.text_prep.tokenizer = self.tokenizer

    def __del__(self):
        train_svm = '%s.svm' % self.name
        if os.path.exists(train_svm):
            os.remove(train_svm)
        test_svm = '%s_test.svm' % self.name
        if os.path.exists(test_svm):
            os.remove(test_svm)