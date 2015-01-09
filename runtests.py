# coding: utf-8

import unittest

from tgrocery import Grocery


class GroceryTestCase(unittest.TestCase):
    def setUp(self):
        self.grocery = Grocery('test')

    def test_main(self):
        self.grocery.train('sample/train_ch.txt')
        assert self.grocery.get_load_status()
        assert self.grocery.predict('考生必读：新托福写作考试评分标准') == 'education'


if __name__ == 'main':
    unittest.main()