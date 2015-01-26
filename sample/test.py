# coding: utf-8

from tgrocery import Grocery


grocery = Grocery('test')
train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
grocery.train(train_src)
print grocery.get_load_status()

test_src = [
    ('education', '福建春季公务员考试报名18日截止 2月6日考试'),
    ('sports', '意甲首轮补赛交战记录:米兰客场8战不败国米10年连胜'),
]
test_result = grocery.test(test_src)
print test_result.accuracy_labels
print test_result.recall_labels

grocery = Grocery('text_src')
train_src = '../text_src/train_ch.txt'
grocery.train(train_src)
print grocery.get_load_status()

test_src = '../text_src/test_ch.txt'
test_result = grocery.test(test_src)
print test_result.accuracy_labels
print test_result.recall_labels
test_result.show_result()