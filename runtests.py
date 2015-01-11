# coding: utf-8

import unittest
import os
import shutil

from tgrocery import Grocery


class GroceryTestCase(unittest.TestCase):
    def setUp(self):
        self.train_src = [
            ('education', '名师指导托福语法技巧：名词的复数形式'),
            ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
            ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
            ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
        ]
        self.grocery_name = 'test'

    def test_main(self):
        grocery = Grocery(self.grocery_name)
        grocery.train(self.train_src)
        grocery.save()
        new_grocery = Grocery('test')
        new_grocery.load()
        assert grocery.get_load_status()
        assert grocery.predict('考生必读：新托福写作考试评分标准') == 'education'
        # cleanup
        if self.grocery_name and os.path.exists(self.grocery_name):
            shutil.rmtree(self.grocery_name)


if __name__ == 'main':
    unittest.main()