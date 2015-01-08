from libshorttext.classifier import *

from converter import *
from classifier import *


# TODO how to handle exception
class GroceryException(Exception):
    pass


class Grocery(object):
    def __init__(self, name, tokenizer=None):
        self.name = name
        if tokenizer is not None:
            if not hasattr(tokenizer, '__call__'):
                raise GroceryException()
            self.tokenizer = tokenizer
        self.model = None

    def check_load_status(self, func):
        def wrapper(*args):
            if self.model is not None:
                raise GroceryException()
            func(args)

        return wrapper

    def train(self, train_file):
        text_converter = GroceryTextConverter()
        # TODO custom tokenizer
        # if self.tokenizer is not None:
        #     text_converter.text_prep.tokenizer = self.tokenizer
        svm_file = '%s.svm' % self.name
        text_converter.convert_text(train_file, output=svm_file)
        self.model = GroceryClassifier(text_converter).train_converted_text(svm_file)
        return self

    @check_load_status
    def predict(self, single_text):
        return predict_single_text(single_text, self.model).predicted_y

    @check_load_status
    def test(self, test_file):
        predict_result = predict_text(test_file, self.model, svm_file='%s_test.svm' % self.name)
        self.show_accuracy(predict_result)

    @staticmethod
    def show_accuracy(predict_result):
        print("Accuracy = {0:.4f}% ({1}/{2})".format(
            predict_result.get_accuracy() * 100,
            sum(ty == py for ty, py in zip(predict_result.true_y, predict_result.predicted_y)),
            len(predict_result.true_y)))

    @check_load_status
    def save(self):
        self.model.save(self.name, force=True)

    def load(self):
        # TODO how to load new model?
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