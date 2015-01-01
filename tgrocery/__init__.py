"""
LibShort is a package for short text classification. It supports training, test,
and analysis tools.
"""

import os

from tgrocery.analyzer import *
from tgrocery.classifier import *
from tgrocery.converter import *


class GroceryException(Exception):
    pass


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
        return predict_result.get_accuracy()

    def save(self):
        if not self.get_load_status():
            raise GroceryException()
        self.model.save(self.name, force=True)

    def load(self):
        # Overwrite the previous model?
        if self.get_load_status():
            raise GroceryException()
        self.model = TextModel()
        self.model.load(self.name)

    def __del__(self):
        train_svm = '%s.svm' % self.name
        if os.path.exists(train_svm):
            os.remove(train_svm)
        test_svm = '%s_test.svm' % self.name
        if os.path.exists(test_svm):
            os.remove(test_svm)