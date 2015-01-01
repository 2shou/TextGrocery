# coding: utf-8

import jieba

from tgrocery import Grocery


grocery = Grocery('test', tokenizer=jieba.cut)
grocery.train('train_file.txt')
print grocery.predict('考生必读：新托福写作考试评分标准')
grocery.test('test_file.txt')
print grocery.get_load_status()