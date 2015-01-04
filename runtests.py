import jieba

from tgrocery import Grocery


grocery = Grocery('test', tokenizer=jieba.cut)
grocery.train('sample/train_ch.txt')
grocery.predict('考生必读：新托福写作考试评分标准')