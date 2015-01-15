from converter import *
from classifier import *


__all__ = ['Grocery']


class GroceryException(Exception):
    pass


class GroceryNotTrainException(GroceryException):
    def __init__(self):
        self.message = 'Text model has not been trained.'


class Grocery(object):
    def __init__(self, name, custom_tokenize=None):
        self.name = name
        if custom_tokenize is not None:
            if not hasattr(custom_tokenize, '__call__'):
                raise GroceryException('Tokenize func must be callable.')
        self.custom_tokenize = custom_tokenize
        self.model = None
        self.classifier = None
        self.train_svm_file = None

    def get_load_status(self):
        return self.model is not None and isinstance(self.model, GroceryTextModel)

    def train(self, train_src, delimiter='\t'):
        text_converter = GroceryTextConverter(custom_tokenize=self.custom_tokenize)
        self.train_svm_file = '%s_train.svm' % self.name
        text_converter.convert_text(train_src, output=self.train_svm_file, delimiter=delimiter)
        # default parameter
        model = train(self.train_svm_file, '', '-s 4')
        self.model = GroceryTextModel(text_converter, model)
        return self

    def predict(self, single_text):
        if not self.get_load_status():
            raise GroceryNotTrainException()
        return self.model.predict_text(single_text)

    def test(self, text_src, delimiter='\t'):
        if not self.get_load_status():
            raise GroceryNotTrainException()
        return GroceryTest(self.model).test(text_src, delimiter)

    def save(self):
        if not self.get_load_status():
            raise GroceryNotTrainException()
        self.model.save(self.name, force=True)

    def load(self):
        self.model = GroceryTextModel(self.custom_tokenize)
        self.model.load(self.name)

    def __del__(self):
        if self.train_svm_file and os.path.exists(self.train_svm_file):
            os.remove(self.train_svm_file)