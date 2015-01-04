# coding: utf-8

import jieba

from tgrocery import Grocery


# save
grocery = Grocery('test', tokenizer=jieba.cut)  # To support Chinese short-text classification
grocery.train('train_ch.txt')
grocery.save()

# load
new_grocery = Grocery('test', tokenizer=jieba.cut)
new_grocery.load()
print new_grocery.predict('考生必读：新托福写作考试评分标准')
