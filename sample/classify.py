# coding: utf-8

import jieba

from tgrocery import Grocery


grocery = Grocery('test', tokenizer=jieba.cut)  # To support Chinese short-text classification
grocery.train('train_ch.txt')
print grocery.get_load_status()
print grocery.predict('考生必读：新托福写作考试评分标准')
