# coding: utf-8

from tgrocery import Grocery


# save
grocery = Grocery('test')
train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
grocery.train(train_src)
grocery.save()

# load
# grocery name must be the same as the previous one
new_grocery = Grocery('test')
new_grocery.load()
print new_grocery.predict('考生必读：新托福写作考试评分标准')
