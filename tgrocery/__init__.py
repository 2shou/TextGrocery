from converter import *
from classifier import *
from utils import read_text_src


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

    def train(self, train_src):
        text_converter = GroceryTextConverter()
        # TODO custom tokenizer
        # if self.tokenizer is not None:
        # text_converter.text_prep.tokenizer = self.tokenizer
        svm_file = '%s.svm' % self.name
        # TODO how to realize more elegantly?
        text_converter.convert_text(train_src, output=svm_file)
        model = train(svm_file, '', '-s 4')
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
            print self.predict(text), text
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
        self.model = GroceryTextModel()
        self.model.load(self.name)
        # if self.tokenizer is not None:
        # self.model.text_converter.text_prep.tokenizer = self.tokenizer

        # def __del__(self):
        # train_svm = '%s.svm' % self.name
        #     if os.path.exists(train_svm):
        #         os.remove(train_svm)
        #     test_svm = '%s_test.svm' % self.name
        #     if os.path.exists(test_svm):
        #         os.remove(test_svm)