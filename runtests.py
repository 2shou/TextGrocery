# coding: utf-8

import jieba
import unittest

from tgrocery import Grocery


class GroceryTestCase(unittest.TestCase):
    def setUp(self):
        self.grocery = Grocery('test', tokenizer=jieba.cut)  # To support Chinese short-text classification

    def test_train(self):
        self.grocery.train('sample/train_ch.txt')
        assert self.grocery.get_load_status()

    def test_predict(self):
        assert self.grocery.predict('考生必读：新托福写作考试评分标准') == 'education'

    def test_test(self):
        self.grocery.test('sample/test_ch.txt')

if __name__ == 'main':
    unittest.main()