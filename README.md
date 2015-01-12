TextGrocery
===========

[![Build Status](https://travis-ci.org/2shou/TextGrocery.svg?branch=master)](https://travis-ci.org/2shou/TextGrocery)

A simple, efficient short-text classification tool based on LibLinear

Embed with [jieba](https://github.com/fxsjy/jieba) as default tokenizer to support Chinese Tokenize

Other languages: [中文文档](README_CN.md)

Performance
-----------

- Train set: 48k news titles with 32 labels
- Test set: 16k news titles with 32 labels
- Compare with svm and naive-bayes of [scikit-learn](https://github.com/scikit-learn/scikit-learn)

|         Classifier       | Accuracy  |  Time cost(s)  |
|:------------------------:|:---------:|:--------------:|
|     scikit-learn(nb)     |   76.8%   |     134        |
|     scikit-learn(svm)    |   76.9%   |     121        |
|     **TextGrocery**      | **79.6%** |    **49**      |

Sample Code
-----------

```python
>>> from tgrocery import Grocery
# Create a grocery(don't forget to set a name)
>>> grocery = Grocery('sample')
# Train from list
>>> train_src = [
    ('education', '名师指导托福语法技巧：名词的复数形式'),
    ('education', '中国高考成绩海外认可 是“狼来了”吗？'),
    ('sports', '图文：法网孟菲尔斯苦战进16强 孟菲尔斯怒吼'),
    ('sports', '四川丹棱举行全国长距登山挑战赛 近万人参与')
]
>>> grocery.train(train_src)
# Or train from file
>>> grocery.train('train_ch.txt')
# Save model
>>> grocery.save()
# Load model(the same name as previous)
>>> new_grocery = Grocery('sample')
>>> new_grocery.load()
# Predict
>>> new_grocery.predict('考生必读：新托福写作考试评分标准')
education
# Test from list
>>> test_src = [
    ('education', '福建春季公务员考试报名18日截止 2月6日考试'),
    ('sports', '意甲首轮补赛交战记录:米兰客场8战不败国米10年连胜'),
]
>>> new_grocery.test(test_src)
# Return Accuracy
0.5
# Or test from file
>>> new_grocery.test('test_ch.txt')
# Custom tokenize
>>> custom_grocery = Grocery('custom', custom_tokenize=list)
```

More examples: [sample/](sample/)

Install
-------

    $ pip install tgrocery

> Only test under Unix-based System
