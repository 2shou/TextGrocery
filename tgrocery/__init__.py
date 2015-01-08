from libshorttext.classifier import *

from converter import *
from classifier import *


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
        text_converter = GroceryTextConverter()
        if self.tokenizer is not None:
            text_converter.text_prep.tokenizer = self.tokenizer
        svm_file = '%s.svm' % self.name
        text_converter.convert_text(train_file, output=svm_file)
        self.model = GroceryClassifier(text_converter).train_converted_text(svm_file)
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