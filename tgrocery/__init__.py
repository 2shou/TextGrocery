from converter import *
from classifier import *
from utils import read_text_src


# TODO how to handle exception
class GroceryException(Exception):
    pass


class Grocery(object):
    def __init__(self, name, custom_tokenize=None):
        self.name = name
        if custom_tokenize is not None:
            if not hasattr(custom_tokenize, '__call__'):
                raise GroceryException()
        self.custom_tokenize = custom_tokenize
        self.model = None
        self.classifier = None
        self.train_svm_file = None

    def get_load_status(self):
        return self.model is not None

    def train(self, train_src):
        text_converter = GroceryTextConverter(custom_tokenize=self.custom_tokenize)
        # TODO custom tokenizer
        self.train_svm_file = '%s_train.svm' % self.name
        # TODO how to realize more elegantly?
        text_converter.convert_text(train_src, output=self.train_svm_file)
        model = train(self.train_svm_file, '', '-s 4')
        self.model = GroceryTextModel(text_converter, model)
        return self

    def predict(self, single_text):
        if not self.get_load_status():
            raise GroceryException()
        return self.model.predict_text(single_text).predicted_y

    def test(self, text_src):
        text_src = read_text_src(text_src)
        true_y = []
        predicted_y = []
        for line in text_src:
            try:
                label, text = line
            except ValueError:
                continue
            predicted_y.append(self.predict(text))
            true_y.append(label)
        l = len(true_y)
        return sum([true_y[i] == predicted_y[i] for i in range(l)]) / float(l)

    def save(self):
        if not self.get_load_status():
            raise GroceryException()
        self.model.save(self.name, force=True)

    def load(self):
        # TODO how to load new model?
        self.model = GroceryTextModel(self.custom_tokenize)
        self.model.load(self.name)

    def __del__(self):
        if self.train_svm_file and os.path.exists(self.train_svm_file):
            os.remove(self.train_svm_file)
