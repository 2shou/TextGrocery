# coding: utf-8

from tgrocery import Grocery


# save
grocery = Grocery('test')
grocery.train('train_ch.txt')
grocery.save()

# load
new_grocery = Grocery('test')
new_grocery.load()
print new_grocery.predict('考生必读：新托福写作考试评分标准')
