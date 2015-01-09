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
        self.classifier = None

    def get_load_status(self):
        return self.model is not None

    def train(self, train_file):
        text_converter = GroceryTextConverter()
        # TODO custom tokenizer
        # if self.tokenizer is not None:
        # text_converter.text_prep.tokenizer = self.tokenizer
        svm_file = '%s.svm' % self.name
        # TODO how to realize more elegantly?
        text_converter.convert_text(train_file, output=svm_file)
        self.classifier = GroceryClassifier(text_converter)
        self.model = self.classifier.train_converted_text(svm_file)
        return self

    def predict(self, single_text):
        if not self.get_load_status():
            raise GroceryException()
        return self.classifier.predict_text(single_text, self.model).predicted_y

    # def test(self, test_file):
    # if not self.get_load_status():
    # raise GroceryException()
    # predict_result = GroceryClassifier.predict_text(test_file, self.model, svm_file='%s_test.svm' % self.name)
    # self.show_accuracy(predict_result)

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
        # TODO how to load new model?
        self.model = GroceryTextModel(self.name)
        if self.tokenizer is not None:
            self.model.text_converter.text_prep.tokenizer = self.tokenizer

    def __del__(self):
        train_svm = '%s.svm' % self.name
        if os.path.exists(train_svm):
            os.remove(train_svm)
        test_svm = '%s_test.svm' % self.name
        if os.path.exists(test_svm):
            os.remove(test_svm)